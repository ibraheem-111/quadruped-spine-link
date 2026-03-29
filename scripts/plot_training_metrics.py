from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from tensorboard.backend.event_processing import event_accumulator


DEFAULT_FILTERS = ["loss", "reward", "entropy", "kl", "learning_rate", "episode"]


def moving_average(values: list[float], window: int) -> list[float]:
    if window <= 1 or len(values) < window:
        return values
    out = []
    csum = 0.0
    for i, value in enumerate(values):
        csum += value
        if i >= window:
            csum -= values[i - window]
        denom = window if i >= window - 1 else i + 1
        out.append(csum / denom)
    return out


def pick_event_file(run_dir: Path, event_file: str | None) -> Path:
    if event_file:
        chosen = Path(event_file).expanduser().resolve()
        if not chosen.exists():
            raise FileNotFoundError(f"Event file not found: {chosen}")
        return chosen

    candidates = sorted(run_dir.glob("events.out.tfevents.*"), key=lambda p: p.stat().st_mtime)
    if not candidates:
        raise FileNotFoundError(f"No TensorBoard event files found in {run_dir}")
    return candidates[-1]


def select_tags(all_tags: list[str], tags_arg: str | None) -> list[str]:
    if tags_arg:
        wanted = [tag.strip() for tag in tags_arg.split(",") if tag.strip()]
    else:
        wanted = DEFAULT_FILTERS

    selected = []
    for tag in all_tags:
        low = tag.lower()
        if any(key.lower() in low for key in wanted):
            selected.append(tag)

    if not selected:
        selected = all_tags[:]
    return selected


def load_scalars(ea: event_accumulator.EventAccumulator, tags: list[str]) -> dict[str, list[tuple[int, float, float]]]:
    data: dict[str, list[tuple[int, float, float]]] = {}
    for tag in tags:
        try:
            events = ea.Scalars(tag)
        except KeyError:
            continue
        data[tag] = [(event.step, event.value, event.wall_time) for event in events]
    return data


def write_long_csv(data: dict[str, list[tuple[int, float, float]]], output_csv: Path) -> None:
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["tag", "step", "value", "wall_time"])
        for tag, rows in data.items():
            for step, value, wall_time in rows:
                writer.writerow([tag, step, value, wall_time])


def plot_individual(data: dict[str, list[tuple[int, float, float]]], output_dir: Path, smooth_window: int) -> list[Path]:
    output_files: list[Path] = []
    for tag, rows in data.items():
        if not rows:
            continue

        steps = [row[0] for row in rows]
        values = [row[1] for row in rows]
        values = moving_average(values, smooth_window)

        fig, axis = plt.subplots(figsize=(9, 4.5))
        axis.plot(steps, values, linewidth=1.5)
        axis.set_title(tag)
        axis.set_xlabel("iteration/step")
        axis.set_ylabel("value")
        axis.grid(True, alpha=0.3)

        safe_name = tag.replace("/", "_").replace("\\", "_").replace(" ", "_")
        out_path = output_dir / f"{safe_name}.png"
        fig.tight_layout()
        fig.savefig(out_path, dpi=130)
        plt.close(fig)
        output_files.append(out_path)

    return output_files


def plot_grid(data: dict[str, list[tuple[int, float, float]]], output_dir: Path, smooth_window: int) -> Path | None:
    tags = [tag for tag, rows in data.items() if rows]
    if not tags:
        return None

    count = len(tags)
    cols = 2 if count > 1 else 1
    rows = (count + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(12, 3.8 * rows))
    if hasattr(axes, "flatten"):
        axes_list = list(axes.flatten())
    elif isinstance(axes, list):
        axes_list = axes
    else:
        axes_list = [axes]

    for i, tag in enumerate(tags):
        axis = axes_list[i]
        series = data[tag]
        x_vals = [row[0] for row in series]
        y_vals = moving_average([row[1] for row in series], smooth_window)
        axis.plot(x_vals, y_vals, linewidth=1.4)
        axis.set_title(tag, fontsize=10)
        axis.set_xlabel("iteration/step")
        axis.grid(True, alpha=0.3)

    for j in range(len(tags), len(axes_list)):
        axes_list[j].axis("off")

    out_path = output_dir / "metrics_grid.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot RSL-RL TensorBoard scalar metrics.")
    parser.add_argument("--run-dir", required=True, help="Run directory containing events.out.tfevents.*")
    parser.add_argument("--event-file", default=None, help="Specific TensorBoard event file path")
    parser.add_argument("--output-dir", default=None, help="Output folder for plots and CSV (default: run dir/plots)")
    parser.add_argument("--tags", default=None, help="Comma-separated filter words, e.g. loss,reward,entropy")
    parser.add_argument("--smooth-window", type=int, default=1, help="Moving average window for plotting")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    if not run_dir.exists():
        raise FileNotFoundError(f"Run dir not found: {run_dir}")

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else (run_dir / "plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    event_path = pick_event_file(run_dir, args.event_file)
    accumulator = event_accumulator.EventAccumulator(
        str(event_path),
        size_guidance={event_accumulator.SCALARS: 0},
    )
    accumulator.Reload()

    all_tags = accumulator.Tags().get("scalars", [])
    if not all_tags:
        raise RuntimeError(f"No scalar tags found in: {event_path}")

    selected_tags = select_tags(all_tags, args.tags)
    data = load_scalars(accumulator, selected_tags)

    csv_path = output_dir / "metrics_long.csv"
    write_long_csv(data, csv_path)

    individual_plots = plot_individual(data, output_dir, max(1, args.smooth_window))
    grid_plot = plot_grid(data, output_dir, max(1, args.smooth_window))

    print(f"Event file: {event_path}")
    print("Selected tags:")
    for tag in data.keys():
        print(f"  - {tag}")
    print(f"CSV: {csv_path}")
    print("Individual plots:")
    for path in individual_plots:
        print(f"  - {path}")
    if grid_plot:
        print(f"Grid plot: {grid_plot}")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path

from isaaclab_assets.robots.unitree import UNITREE_GO2_CFG


# Resolve the USD path relative to this file so it works on any machine.
_ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets" / "robots"
USD_PATH = _ASSETS_DIR / "go2_spine_a0_locked.usd"


# Copy the stock Go2 config and only swap the spawn USD.
UNITREE_GO2_SPINE_A0_LOCKED_CFG = UNITREE_GO2_CFG.copy()
UNITREE_GO2_SPINE_A0_LOCKED_CFG.spawn.usd_path = str(USD_PATH)
UNITREE_GO2_SPINE_A0_LOCKED_CFG.init_state.rot = (-0.70710678, 0.70710678, 0.0, 0.0)
UNITREE_GO2_SPINE_A0_LOCKED_CFG.init_state.pos = (0.0, 0.0, 0.36)

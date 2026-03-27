from pathlib import Path

from pxr import Usd, UsdGeom

usd_path = Path("source/radl/radl/assets/robots/go2_spine_a0_locked.usd").resolve()
stage = Usd.Stage.Open(str(usd_path))
print("Opened:", bool(stage), usd_path)

if not stage:
    raise SystemExit(1)

root_layer = stage.GetRootLayer()
root_dir = Path(root_layer.realPath).parent

targets = [
    "/go2_description/trunk_front",
    "/go2_description/trunk_rear",
    "/go2_description/spine_link",
    "/go2_description/trunk_front/spine_cylinder_front",
    "/go2_description/trunk_rear/spine_cylinder_rear",
]

print("\n=== Prim validity / xformability ===")
for path in targets:
    prim = stage.GetPrimAtPath(path)
    valid = prim.IsValid()
    xformable = UsdGeom.Xformable(prim).GetPrim().IsValid() if valid else False
    prim_type = prim.GetTypeName() if valid else "N/A"
    print(f"{path}: valid={valid}, xformable={xformable}, type={prim_type}")

print("\n=== Payload/Reference asset paths ===")
for prim in stage.Traverse():
    payloads = prim.GetMetadata("payload")
    refs = prim.GetMetadata("references")

    if payloads:
        for item in payloads.GetAddedOrExplicitItems():
            asset_path = item.assetPath
            resolved = (root_dir / asset_path).resolve() if asset_path else None
            exists = resolved.exists() if resolved else False
            print(f"PAYLOAD {prim.GetPath()} -> {asset_path} | exists={exists} | resolved={resolved}")

    if refs:
        for item in refs.GetAddedOrExplicitItems():
            asset_path = item.assetPath
            resolved = (root_dir / asset_path).resolve() if asset_path else None
            exists = resolved.exists() if resolved else False
            print(f"REF     {prim.GetPath()} -> {asset_path} | exists={exists} | resolved={resolved}")

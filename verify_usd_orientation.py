from pathlib import Path

from pxr import Usd, UsdGeom

usd_path = Path("source/radl/radl/assets/robots/go2_spine_articulated.usd").resolve()
stage = Usd.Stage.Open(str(usd_path))
print(f"USD: {usd_path}")
print(f"Opened: {bool(stage)}")
if not stage:
    raise SystemExit(1)

print(f"StageUpAxis: {UsdGeom.GetStageUpAxis(stage)}")

check_prims = [
    "/go2_description",
    "/go2_description/base",
    "/go2_description/trunk_front",
    "/go2_description/spine_link",
    "/go2_description/trunk_rear",
]

print("\n=== Key Prim Xform Ops ===")
for prim_path in check_prims:
    prim = stage.GetPrimAtPath(prim_path)
    prim_type = prim.GetTypeName() if prim.IsValid() else "N/A"
    print(f"[{prim_path}] valid={prim.IsValid()} type={prim_type}")
    if prim.IsValid():
        xformable = UsdGeom.Xformable(prim)
        ops = xformable.GetOrderedXformOps()
        print("  ops=", [op.GetOpName() for op in ops])
        for op in ops:
            print(f"   - {op.GetOpName()} = {op.Get()}")

print("\n=== Any rotateX:unitsResolve under /go2_description ===")
found = []
root = stage.GetPrimAtPath("/go2_description")
for prim in Usd.PrimRange(root):
    if not prim.IsValid():
        continue
    xformable = UsdGeom.Xformable(prim)
    for op in xformable.GetOrderedXformOps():
        if "rotateX:unitsResolve" in op.GetOpName():
            found.append((str(prim.GetPath()), op.Get()))

if not found:
    print("None found")
else:
    for path, value in found:
        print(f"{path}: rotateX:unitsResolve={value}")

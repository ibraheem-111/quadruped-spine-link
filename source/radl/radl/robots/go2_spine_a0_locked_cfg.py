from __future__ import annotations

from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.actuators import ActuatorNetMLPCfg, DCMotorCfg, ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR, ISAACLAB_NUCLEUS_DIR

UNITREE_GO2_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_NUCLEUS_DIR}/Robots/Unitree/Go2/go2.usd",
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False, solver_position_iteration_count=4, solver_velocity_iteration_count=0
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.4),
        joint_pos={
            ".*L_hip_joint": 0.1,
            ".*R_hip_joint": -0.1,
            "F[L,R]_thigh_joint": 0.8,
            "R[L,R]_thigh_joint": 1.0,
            ".*_calf_joint": -1.5,
            "spine_joint_.*": 0.0,
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        "base_legs": DCMotorCfg(
            joint_names_expr=[".*_hip_joint", ".*_thigh_joint", ".*_calf_joint", "spine_joint_.*"],
            effort_limit=23.5,
            saturation_effort=23.5,
            velocity_limit=30.0,
            stiffness=25.0,
            damping=0.5,
            friction=0.0,
        ),
    },
)


# Resolve the USD path relative to this file so it works on any machine.
_ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets" / "robots"
# USD_PATH = _ASSETS_DIR / "go2_spine_a0_locked.usd"
USD_PATH = _ASSETS_DIR / "go2_spine_articulated.usd"


# Copy the stock Go2 config and only swap the spawn USD.
UNITREE_GO2_SPINE_A0_LOCKED_CFG = UNITREE_GO2_CFG.copy()
UNITREE_GO2_SPINE_A0_LOCKED_CFG.spawn.usd_path = str(USD_PATH)
# UNITREE_GO2_SPINE_A0_LOCKED_CFG.init_state.rot = (0.70710678, -0.70710678, 0.0, 0.0)
# UNITREE_GO2_SPINE_A0_LOCKED_CFG.init_state.rot = (0.0, 0.0, 0.0, 0.0)
# UNITREE_GO2_SPINE_A0_LOCKED_CFG.init_state.pos = (0.0, 0.0, 0.36)

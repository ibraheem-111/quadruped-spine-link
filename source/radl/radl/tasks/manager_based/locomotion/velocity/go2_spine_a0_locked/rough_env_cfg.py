from isaaclab.utils import configclass
from isaaclab_tasks.manager_based.locomotion.velocity.config.go2.rough_env_cfg import (
    UnitreeGo2RoughEnvCfg,
)

from radl.robots.go2_spine_a0_locked_cfg import UNITREE_GO2_SPINE_A0_LOCKED_CFG


@configclass
class UnitreeGo2SpineA0LockedRoughEnvCfg(UnitreeGo2RoughEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        canonical_base_body = "trunk_front"
        torso_bodies_regex = "(base|trunk_.*|spine_.*)"

        self.scene.robot = UNITREE_GO2_SPINE_A0_LOCKED_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        if hasattr(self.scene, "height_scanner") and self.scene.height_scanner is not None:
            self.scene.height_scanner.prim_path = f"{{ENV_REGEX_NS}}/Robot/{canonical_base_body}"

        if hasattr(self.events, "add_base_mass") and self.events.add_base_mass is not None:
            self.events.add_base_mass.params["asset_cfg"].body_names = canonical_base_body

        if hasattr(self.events, "base_external_force_torque") and self.events.base_external_force_torque is not None:
            self.events.base_external_force_torque.params["asset_cfg"].body_names = canonical_base_body

        if hasattr(self.terminations, "base_contact") and self.terminations.base_contact is not None:
            self.terminations.base_contact.params["sensor_cfg"].body_names = torso_bodies_regex
            if "asset_cfg" in self.terminations.base_contact.params:
                self.terminations.base_contact.params["asset_cfg"].body_names = canonical_base_body


@configclass
class UnitreeGo2SpineA0LockedRoughEnvCfg_PLAY(UnitreeGo2SpineA0LockedRoughEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5

        self.observations.policy.enable_corruption = False
        self.events.base_external_force_torque = None
        self.events.push_robot = None


@configclass
class UnitreeGo2SpineA0LockedRoughEnvCfg_DEBUG(UnitreeGo2SpineA0LockedRoughEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        if hasattr(self.events, "add_base_mass"):
            self.events.add_base_mass = None
        if hasattr(self.events, "base_external_force_torque"):
            self.events.base_external_force_torque = None
        if hasattr(self.events, "base_com"):
            self.events.base_com = None
        if hasattr(self.events, "push_robot"):
            self.events.push_robot = None

        if hasattr(self.events, "reset_base") and self.events.reset_base is not None:
            self.events.reset_base.params = {
                "pose_range": {
                    "x": (0.0, 0.0),
                    "y": (0.0, 0.0),
                    "yaw": (0.0, 0.0),
                },
                "velocity_range": {
                    "x": (0.0, 0.0),
                    "y": (0.0, 0.0),
                    "z": (0.0, 0.0),
                    "roll": (0.0, 0.0),
                    "pitch": (0.0, 0.0),
                    "yaw": (0.0, 0.0),
                },
            }


@configclass
class UnitreeGo2SpineA0LockedRoughEnvCfg_DEBUG_PLAY(UnitreeGo2SpineA0LockedRoughEnvCfg_DEBUG):
    def __post_init__(self):
        super().__post_init__()

        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5

        self.observations.policy.enable_corruption = False

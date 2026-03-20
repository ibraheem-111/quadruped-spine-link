# from isaaclab.utils import configclass
# from isaaclab_tasks.manager_based.locomotion.velocity.go2.flat_env_cfg import UnitreeGo2FlatEnvCfg
# from radl.robots.go2_spine_a0_locked_cfg import UNITREE_GO2_SPINE_A0_LOCKED_CFG


# @configclass
# class UnitreeGo2SpineA0LockedFlatEnvCfg(UnitreeGo2FlatEnvCfg):
#     """Configuration for Go2 with spine locked to 0 in flat environment."""

#     def __post_init__(self):
#         """Post initialization to set the robot config."""
#         super().__post_init__()
        
#         self.scene.robot = UNITREE_GO2_SPINE_A0_LOCKED_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

#         self.actions.joint_pos.join_names = [".*_hip_joint", ".*_thigh_joint", ".*_calf_joint"]

#         base_body = "trunk_front"  # base body to check contact for termination

#         self.terminations.base_contact.params["sensor_cfg"].body_names = base_body
#         self.terminations.base_contact.params["asset_cfg"].body_names = base_body
from isaaclab.utils import configclass

# We reuse the entire Go2 Flat velocity task definition (rewards, obs, resets, terrain plane, etc.)
from isaaclab_tasks.manager_based.locomotion.velocity.config.go2.flat_env_cfg import (
    UnitreeGo2FlatEnvCfg,
)

# Your custom robot spawn config (points to your modified USD)
from radl.robots.go2_spine_a0_locked_cfg import UNITREE_GO2_SPINE_A0_LOCKED_CFG


@configclass
class UnitreeGo2SpineA0LockedFlatEnvCfg(UnitreeGo2FlatEnvCfg):
    """Flat velocity-tracking locomotion task using the custom Go2 USD with A0 locked spine.

    Notes on what this class is doing:
    - Isaac Lab env configs are "recipes" for building an RL environment.
      They define: robot spawn, terrain, sensors, observations, actions, rewards, resets, terminations.
    - We inherit the proven Go2 Flat task and only swap the robot asset + adapt torso assumptions.
    """

    def __post_init__(self):
        super().__post_init__()

        # Canonical base-like body for any inherited single-body assumptions.
        CANONICAL_BASE_BODY = "trunk_front"
        # Torso group used for contact semantics in this multi-link torso setup.
        TORSO_BODIES_REGEX = "(base|trunk_.*|spine_.*)"

        # --------------------------------------------------------------------------------------
        # A) Spawn our robot USD under the per-environment namespace
        #    {ENV_REGEX_NS}/Robot becomes /World/envs/env_0/Robot, /World/envs/env_1/Robot, ...
        # --------------------------------------------------------------------------------------
        self.scene.robot = UNITREE_GO2_SPINE_A0_LOCKED_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # --------------------------------------------------------------------------------------
        # B) Actions: control ONLY the 12 leg joints (exclude spine joints completely)
        #    Default velocity env often uses ".*" (all joints), which would incorrectly include spine joints.
        # --------------------------------------------------------------------------------------
        self.actions.joint_pos.joint_names = [
            ".*_hip_joint",
            ".*_thigh_joint",
            ".*_calf_joint",
        ]

        # --------------------------------------------------------------------------------------
        # C) Replace inherited "base" assumptions.
        #
        # - For contact semantics, use the full torso-group regex.
        # - For any single-body reference, use trunk_front as canonical base-like link.
        # --------------------------------------------------------------------------------------

        if hasattr(self.scene, "height_scanner") and self.scene.height_scanner is not None:
            self.scene.height_scanner.prim_path = f"{{ENV_REGEX_NS}}/Robot/{CANONICAL_BASE_BODY}"

        if hasattr(self.terminations, "base_contact") and self.terminations.base_contact is not None:
            # base_contact uses illegal_contact() on the ContactSensor "contact_forces"
            # and filters by body_names; we replace "base" with the torso-group regex.
            self.terminations.base_contact.params["sensor_cfg"].body_names = TORSO_BODIES_REGEX
            if "asset_cfg" in self.terminations.base_contact.params:
                self.terminations.base_contact.params["asset_cfg"].body_names = CANONICAL_BASE_BODY

        # --------------------------------------------------------------------------------------
        # D) Bring-up stability: disable "base" disturbance/randomization events initially.
        #
        # These events target body_names="base" in the stock config. With multi-link torso,
        # applying them incorrectly causes early training instability and/or config errors.
        #
        # Once training runs, you can re-enable and target a single reference torso link
        # (e.g., trunk_front or spine_link) if you want pushes or mass randomization.
        # --------------------------------------------------------------------------------------
        if hasattr(self.events, "add_base_mass"):
            self.events.add_base_mass = None
        if hasattr(self.events, "base_external_force_torque"):
            self.events.base_external_force_torque = None
        if hasattr(self.events, "base_com"):
            self.events.base_com = None

        # --------------------------------------------------------------------------------------
        # E) Flat env already disables height scanner and terrain curriculum in the parent class.
        #    (Nothing to do here.)
        # --------------------------------------------------------------------------------------


@configclass
class UnitreeGo2SpineA0LockedFlatEnvCfg_PLAY(UnitreeGo2SpineA0LockedFlatEnvCfg):
    """Smaller, less randomized version for visualization/playback."""

    def __post_init__(self):
        super().__post_init__()

        # Fewer envs so it runs fast with rendering
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5

        # Disable observation corruption for play
        self.observations.policy.enable_corruption = False

        # Make sure pushes are off in play
        if hasattr(self.events, "base_external_force_torque"):
            self.events.base_external_force_torque = None
        if hasattr(self.events, "push_robot"):
            self.events.push_robot = None

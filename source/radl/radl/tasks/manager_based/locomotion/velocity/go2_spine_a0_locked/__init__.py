import gymnasium as gym

# Reuse the stock Go2 agent configs (PPO runner configs)
from isaaclab_tasks.manager_based.locomotion.velocity.config.go2 import agents

_ENV_CFG = (
    "radl.tasks.manager_based.locomotion.velocity.go2_spine_a0_locked.flat_env_cfg:"
    "UnitreeGo2SpineA0LockedFlatEnvCfg"
)

_ENV_CFG_DEBUG = (
    "radl.tasks.manager_based.locomotion.velocity.go2_spine_a0_locked.flat_env_cfg:"
    "UnitreeGo2SpineA0LockedFlatEnvCfg_DEBUG"
)

# ROUGH_ENV_CFG = (
#     "radl.tasks.manager_based.locomotion.velocity.go2_spine_a0_locked.rough_env_cfg:"
#     "UnitreeGo2SpineA0LockedRoughEnvCfg"

# Register a task ID you will use for training
gym.register(
    id="Template-Velocity-Flat-Unitree-Go2-SpineA0Locked-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": _ENV_CFG,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:UnitreeGo2FlatPPORunnerCfg",
        "skrl_cfg_entry_point": f"{agents.__name__}:skrl_flat_ppo_cfg.yaml",
    },
)

gym.register(
    id="Template-Velocity-Flat-Unitree-Go2-SpineA0Locked-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{_ENV_CFG}_PLAY",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:UnitreeGo2FlatPPORunnerCfg",
        "skrl_cfg_entry_point": f"{agents.__name__}:skrl_flat_ppo_cfg.yaml",
    },
)

gym.register(
    id="Template-Velocity-Flat-Unitree-Go2-SpineA0Locked-Debug-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": _ENV_CFG_DEBUG,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:UnitreeGo2FlatPPORunnerCfg",
        "skrl_cfg_entry_point": f"{agents.__name__}:skrl_flat_ppo_cfg.yaml",
    },
)

gym.register(
    id="Template-Velocity-Flat-Unitree-Go2-SpineA0Locked-Debug-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{_ENV_CFG_DEBUG}_PLAY",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:UnitreeGo2FlatPPORunnerCfg",
        "skrl_cfg_entry_point": f"{agents.__name__}:skrl_flat_ppo_cfg.yaml",
    },
)
from gym.envs.registration import register

register(
    id='tansaku-v0',
    entry_point='tansaku_env.envs:TansakuEnv',
)

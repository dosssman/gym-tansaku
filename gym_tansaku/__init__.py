from gym.envs.registration import register

#Both vertical and horizontal cost applied
register(
    id='tansaku-v0',
    entry_point='tansaku_env.envs:TansakuEnv',
)

# Only vertical cost applied
register(
    id='tansaku-v1',
    entry_point='tansaku_env.envs:TansakuVOnlyEnv',
)

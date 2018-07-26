import gym
from gym import error, space, utils
from gym.utils import seeding

class TansakuEnv( gym.Env):
    # Not used
    metadata = { "render.modes": [ "graphic", "console"]}

    def __init__( self):
        pass

    def step( self, action):
        pass

    def reset( self):
        pass

    def render( self, mode="console", close=False):
        pass

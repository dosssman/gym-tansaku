import gym
from gym import error, spaces, utils
from gym.utils import seeding

class TansakuVOnlyEnv( gym.Env):
    # Not used
    metadata = { "render.modes": [ "graphic", "console"]}

    def __init__( self):
        #Num to letters mapping arrays
        self.chitens =  ["A", "B", "C", "D", "E", "F"] #地点
        self.heights = [0, 8, 16, 24, 32, 40]


        #Map Integer states to letter and number states, more intuitives
        self.states_map = []
        self.states_map.append( "A0")
        for letter in self.chitens[1:5]:
            for height in self.heights:
                self.states_map.append( letter + str( height))
        self.states_map.append( "F0")

        #Env params
        self.observation_space = spaces.Discrete( 37)
        self.action_space = spaces.Discrete( 7)
        self.current_state = 0
        self.done = False


        #State internal decomposition for convenience
        self.current_height = 0
        self.current_chiten = 0


        #Cost mapping function
        self.cost_map = [
            [ 0, 4000, 4800, 5520, 6160, 6720],
            [ 800, 1600, 2680, 4000, 4720, 6080],
            [ 320, 480, 800, 2240, 3120, 4640],
            [ 0, 160, 320, 560, 1600, 3040],
            [ 0, 0, 80, 240, 480, 1600],
            [ 0, 0, 0, 0, 160, 240]
        ]

    def step( self, a):
        #Clipping
        if a > 6: a = 6
        if a < 0: a = 0

        if self.done:
            return self.current_state, 0, self.done, {}

        #Allows height change only on chiten B, C, D, E
        if a < 6 and ( self.current_chiten == 0 or self.current_chiten == 5):
            return self.current_state, 0, self.done, {}

        rwrd = 0
        next_chiten = self.current_chiten
        next_height = self.current_height

        next_state_lis = ""

        if a == 6:
            #Move to the next　地点
            next_chiten += 1
            if next_chiten > 4 and next_height != 0: next_chiten = 4
            next_state_lis = self.chitens[ next_chiten] + \
                str( self.heights[ self.current_height])

        else:
            next_height = a
            next_state_lis = self.chitens[ next_chiten] + \
                str( self.heights[ next_height])

        #Check if reached final state s == 36, namely F0
        next_state = self.states_map.index( next_state_lis)

        if next_chiten == 5:
            self.done = True

        reward = 0
        if a < 6 :
            reward = - self.cost_map[ self.current_height][ a]
        if ( self.current_state_lis() in [ "B0", "C0", "D0"]
            and a == 6):
            reward = -9999

        #Update current envs
        self.current_chiten = next_chiten
        if a < 6: self.current_height = a #Only change height if action != 6
        self.current_state = next_state

        return next_state, reward, self.done, {}

    def reset( self):
        self.current_state = 0
        self.current_height = 0
        self.current_chiten = 0
        self.done = False

        return self.current_state, 0, self.done, {}

    def _render( self, mode="console", close=False):
        pass

    def current_state_lis( self):
        return self.states_map[ self.current_state]

#DEBUG
if __name__ == "__main__":
    test = TansakuEnv()

    print( "Current State Lis:", test.current_state_lis())

    test.step( 6)
    test.step( 5)
    test.step( 6)
    test.step( 4)
    print( "Current State Lis:", test.current_state_lis())
    print( "Are you done ? ", test.done)

    #
    # print( "Current State Lis:", test.current_state_lis())
    # print( "Are you done ? ", test.done)
    #
    # test.step( 6)
    #
    # print( "Current State Lis:", test.current_state_lis())
    # print( "Are you done ? ", test.done)
    #
    # test.step( 6)
    #
    # print( "Current State Lis:", test.current_state_lis())
    # print( "Are you done ? ", test.done)
    #
    # test.step( 6)
    #
    # print( "Current State Lis:", test.current_state_lis())
    # print( "Are you done ? ", test.done)
    #
    # test.step( 6)
    #
    # print( "Current State Lis:", test.current_state_lis())
    # print( "Are you done ? ", test.done)
    #
    # test.step( 6)
    #
    # print( "Current State Lis:", test.current_state_lis())
    # print( "Are you done ? ", test.done)

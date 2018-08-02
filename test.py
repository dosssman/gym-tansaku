import gym
import gym_tansaku
import numpy as np
from gym_tansaku.envs.tansaku_env_vertonly import TansakuVOnlyEnv
from q_agent import QAgent

env = TansakuVOnlyEnv()

# done = False
# while not done:
#     print( "Current State:", env.current_state_lis())
#     print( "Enter action between 0 and 6:")
#     action = int( input())
#
#     next_state, reward, done, _ = env.step( action)
#     print( "Reward: ", reward)

# Run over 100 episodes ?
agent = agent = QAgent( env.observation_space.n, env.action_space.n,
    step_size=.1)

for ep in range( 1, 500):

    current_state, _, _ ,_ = env.reset()
    done = False
    score = 0
    step = 1

    while not done:
        action = agent.predict( current_state)
        next_state, reward, done, _ = env.step( action)
        score += reward
        # agent.improve_policy( current_state, action, next_state, reward, step)
        agent.improve_policy( current_state, action, next_state, reward, ep)
        step += 1
        current_state = next_state

        print( "\tEpisode: {}; Score: {}".format( ep, score))

print( "\t\tTesting agent on 5 episodes")
for ep in range( 1, 6):
    current_state, _, _, _ = env.reset()
    done = False
    score = 0

    while not done:
        action = agent.predict( current_state)
        next_state, reward, done, _ = env.step( action)
        score += reward
        current_state = next_state

    print("\t\tEpisode %d; Scored: %d" % (ep, score))

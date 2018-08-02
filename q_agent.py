import numpy as np
import random

#Table Lookup
class QAgent( object):

    def __init__( self, state_count, action_count, discount_factor = 1,
        step_size=.1):

        self.step_size = step_size
        self.state_count = state_count
        self.action_count = action_count
        self.discount_factor = discount_factor

        # self.state_action_value = [[ random.random() for _ in range( self.action_count)]
        #     for _ in range( self.state_count)]

        self.state_action_value = [[ 0.0 for _ in range( self.action_count)]
            for _ in range( self.state_count)]

        self.state_action_value[-1] = [ 0.0
            for _ in range( self.action_count)]

        self.policy = [[ (1.0 / self.action_count)
            for action in range(self.action_count)]
            for state in range(self.state_count)]

    def improve_policy( self, state, action, next_state, rwrd, step_count):
        ### Target Policy Greedy on State Action Value
        q_target = ( rwrd + self.discount_factor *
            self.state_action_value[next_state][np.argmax(
                self.state_action_value[next_state])]
        )

        q_error = q_target -self.state_action_value[state][action]

        self.state_action_value[state][action] += self.step_size * q_error;

        ###Policy Improvement ( Behaviour)
        epsilon = 1.0 / step_count
        base_prob = epsilon / self.action_count

        self.policy[state] = [( (base_prob +1-epsilon)
            if i == np.argmax( self.state_action_value[state]) else base_prob)
            for i in range( self.action_count)]

    #### TODO: Off line Q learning
    def improve_policy_offline( self, state, action, next_state, rwrd, step_count):
        ### Target Policy Greedy on State Action Value
        # q_target = ( rwrd + self.discount_factor *
        #     self.state_action_value[next_state][np.argmax(
        #         self.state_action_value[state])]
        # )
        #
        # q_error = q_target -self.state_action_value[state][action]
        #
        # self.state_action_value[state][action] += self.step_size * q_error;
        #
        # ###Policy Improvement ( Behaviour)
        # epsilon = 1.0 / step_count
        # base_prob = epsilon / self.action_count
        #
        # self.policy[state] = [( (base_prob +1-epsilon)
        #     if i == np.argmax( self.state_action_value[state]) else base_prob)
        #     for i in range( self.action_count)]
        pass

    def predict( self, state):
        return int( np.random.choice( self.action_count, size=1,
            p=self.policy[state]))

#Lin Fun Appro over finite Action Space
class QAgentAcLin( object):

    def __init__( self, features_count, action_count, discount_factor = .95,
        learning_rate=.1, epsilon_decay=1):

        self.action_count = action_count
        self.learning_rate = learning_rate
        self.epsilon_decay = epsilon_decay
        self.features_count = features_count
        self.discount_factor = discount_factor

        self.w = [ [random.random() for _ in range( self.features_count)]
            for _ in range( self.action_count)]

    def update_w( self, state_vec, action, rwrd, next_state_vec):

        q_target = ( rwrd + self.discount_factor *
            self.action_value_fn( next_state_vec, np.argmax(
                [ self.action_value_fn( next_state_vec, a) for a in range( self.action_count)]))
        )

        q_error = q_target - self.action_value_fn( state_vec, action)

        delta_w = [[( self.learning_rate * q_error
            * state_vec[iw]) if action == iiw else 0 for iw,weight in enumerate( weight_set)]
            for iiw,weight_set in enumerate( self.w)]

        self.w = [[ ( self.w[iw][i] + delta_w[iw][i])
            for i in range( len( weight_set)) ]
            for iw, weight_set in enumerate( self.w)]

    #### TODO: Off line Q learning
    def improve_policy_offline( self, state, action, next_state, rwrd, step_count):
        ### Target Policy Greedy on State Action Value
        pass

    def action_value_fn( self, features_vec, action):
        return np.sum( [ features_vec[i] * self.w[action][i]
            for i in range( self.features_count)])

    def predict_dec_e_greedy( self, features_vec):
        epsilon = 1.0 / self.epsilon_decay
        base_prob = epsilon / self.action_count

        action_values = [ self.action_value_fn( features_vec, action)
            for action in range( self.action_count)]

        action_picked = np.random.choice(
            [ a for a in range( self.action_count)],
            p=[( (base_prob +1-epsilon)
                if i == np.argmax( action_values) else base_prob)
                for i in range( self.action_count)])

        return action_picked

    def decay_epsilon( self):
        self.epsilon_decay +=1

        return self.epsilon_decay

    def vectorize( self, current_state):
        return [ 1 if current_state == i else 0 for i in range( self.features_count)]

#LSPIQ

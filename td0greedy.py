import numpy as np

#States definition
heights = [0, 8, 16, 24, 32, 40]
chitens = ["B", "C", "D", "E"]

#Define state map
states_map = { 0: [ 0, 0, "B0"] }
for k, chiten in enumerate( chitens[1:]):
    for kh, height in enumerate( heights[1:]):
        states_map[len( states_map)] = [ k+1, height, chiten + str( height)]
states_map[ len(states_map)] = [ 3, 0, "E0"]
# End State map

# print( states_map)
# input()

costs_map = [
    [ 0, 4000, 4800, 5520, 6160, 6720],
    [ 800, 1600, 2680, 4000, 4720, 6080],
    [ 320, 480, 800, 2240, 3120, 4640],
    [ 0, 160, 320, 560, 1600, 3040],
    [ 0, 0, 80, 240, 480, 1600],
    [ 0, 0, 0, 0, 160, 240]
]

#Define possible actions for each state
action_range = []
for state in range( 11):
    action_range.append( heights[1:])

for i in range( 6):
    action_range.append( [0])
# End action range

#Check action range mapping
# for state_k, state_data in states_map.items():
#     print( "Action range for ", state_data[2])
#     print( action_range[state_k])
# input()

#TODO: TD Values
# 授業の資料によってF()です
state_value = [ 0.0 for _ in range( len( states_map)) ]
# print( state_value)
# End Q Action values

#Learning params
lr = .5
discount = 1.

#Get next state
def get_state_ch( chiten, height):
    state = 0
    for state_k, state_data in states_map.items():
        if state_data[0] == chiten and state_data[1] == height:
            state = state_k
            break

    return state

def get_lis_state_ch( chiten, height):
    lis_state = ""
    for state_k, state_data in states_map.items():
        if state_data[0] == chiten and state_data[1] == height:
            lis_state = state_data[2]
            break
    return lis_state

def get_next_state( current_state, a):
    next_chiten = states_map[current_state][0]
    if next_chiten < 3:
        next_chiten += 1

    return get_state_ch( next_chiten, a)

#Get state and related verification
# c,h = 3, 40
# print( "start state:", get_lis_state_ch( c,h))
# test_next_state = get_next_state( get_state_ch( c,h), 0)
# print( "destination state:", states_map[test_next_state])
# input()

# TODO: Edit
def display_state_value( state_value):
    print("Displaying State Value")
    for state_k, state_data in states_map.items():
        print( "F(%s) = %0.2f" %
            ( state_data[2], state_value[state_k]))

if __name__ == "__main__":
    for ep in range( 1, 100):

        #DEBUG
        print( "Episode ", ep)

        done = False
        total_cost = 0
        current_state = 0

        while not done:
            # Compute the best action to take based on F value
            action_costs = [ (costs_map[heights.index( states_map[current_state][1])][heights.index( action)]
                + discount * state_value[get_next_state(current_state, action)])
                for action in action_range[ current_state] ]

            action_index = np.argmin( action_costs)
            action = action_range[ current_state][action_index]

            disp_action_cost = 0
            # Cost: current height to action's height
            if states_map[current_state][0] == action: #Same height
                action_cost = 0
            else:
                action_cost = action_costs[ action_index]
                disp_action_cost = costs_map[ heights.index( states_map[current_state][1])][ heights.index( action)]

            next_state = get_next_state( current_state, action)
            # Magic ?
            # next_action_index = np.argmin( q_values[next_state])
            td_target = action_cost
            td_error = td_target - state_value[current_state]

            # Update state values F
            state_value_before = state_value[ current_state]
            state_value[ current_state] += lr * td_error
            state_value_after = state_value[ current_state]

            # DEBUG: Trace transistions
            print( "\t From: %s, Action: %d, Cost: %d, To: %s;   F(%s):前=%0.2f -> 後%0.2f"
                % ( states_map[current_state][2], action, disp_action_cost, states_map[next_state][2],
                states_map[current_state][2], state_value_before, state_value_after ))

            #States updates
            current_state = next_state
            total_cost += disp_action_cost

            #Mark the episode as ended because we reached E0
            if current_state == 16: done = True

        print( "End Episode %d , Total cost: %d\n" % ( ep, total_cost))
        # display_state_value( state_value)
    display_state_value( state_value)

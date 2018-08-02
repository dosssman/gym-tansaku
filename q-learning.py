import numpy as np

#States definition
heights = [0, 8, 16, 24, 32, 40]
chitens = ["B", "C", "D", "E"]

#Define state map
states_map = { 0: [ 0, 0, "B0"] }
for k, chiten in enumerate( chitens):
    for kh, height in enumerate( heights[1:]):
        states_map[len( states_map)] = [ k, height, chiten + str( height)]
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
for state in range( 16):
    action_range.append( heights[1:])

for i in range( 6):
    action_range.append( [0])
# End action range

#Check action range mapping
# for state_k, state_data in states_map.items():
#     print( "Action range for ", state_data[2])
#     print( action_range[state_k])
# input()

#Q Action Values
q_values = [ [0.0 for _ in range( len( action_range[ k]))] for k,_ in states_map.items()]
# print( q_values)
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
    # for state_k, state_data in states_map.items():
    #     if (state_data[0] == states_map[current_state][0] + 1 and
    #         state_data[1] == a):
    #         next_state = state_k
    #         break

    return get_state_ch( next_chiten, a)

#Get state and related verification
# c,h = 3, 40
# print( "start state:", get_lis_state_ch( c,h))
# test_next_state = get_next_state( get_state_ch( c,h), 0)
# print( "destination state:", states_map[test_next_state])
# input()

def display_q_values( q_values):
    print("Displaying Q Values")
    for state_k, state_data in states_map.items():
        for k, action in enumerate( action_range[state_k]):
            print( "Q(%s,%d) = %0.2f" %
                ( state_data[2], action, q_values[state_k][k]))
        print("")

if __name__ == "__main__":
    for ep in range( 1, 100):

        #DEBUG
        print( "Episode ", ep)

        done = False
        total_cost = 0
        current_state = 0

        while not done:
            # Probably gets the first one in case of Q VAlues collision ?
            action_index = np.argmin( q_values[current_state])
            action = action_range[ current_state][action_index]
            # Cost: current height to action's height
            if states_map[current_state][0] == action: #Same height
                action_cost = 0
            else:
                action_cost = costs_map[ heights.index( states_map[current_state][1])][ heights.index( action)]

            next_state = get_next_state( current_state, action)
            # Magic ?
            next_action_index = np.argmin( q_values[next_state])
            q_target = action_cost + discount * q_values[next_state][next_action_index]
            q_error = q_target - q_values[current_state][action_index]

            #Update Q Values
            q_value_before = q_values[ current_state][action_index]
            q_values[ current_state][action_index] += lr * q_error
            q_value_after = q_values[ current_state][action_index]

            # DEBUG: Trace transistions
            print( "\t From: %s, Action: %d, Cost: %d, To: %s; \t Q(%s,%d):前=%0.2f -> 後%0.2f"
                % ( states_map[current_state][2], action, action_cost, states_map[next_state][2],
                states_map[current_state][2], action, q_value_before, q_value_after
            ))

            #States updates
            current_state = next_state
            total_cost += action_cost

            #Mark the episode as ended because we reached E0
            if current_state == 21: done = True

        print( "End Episode %d , Total cost: %d\n" % ( ep, total_cost))
        # display_q_values( q_values)
    display_q_values( q_values)

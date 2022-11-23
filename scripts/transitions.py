import map

def transitions():
    transitions={
            "RIGHT" : transition_states("RIGHT", 1, 0),
            "LEFT" : transition_states("LEFT", -1, 0),
            "UP" : transition_states("UP", 0, 1),
            "DOWN" : transition_states("DOWN", 0, -1),
            "TERMINAL": transition_states("TERMINAL", 0, 0)
        }
    return transitions

def transition_states(direction, x, y):
    """
    calculates transition matrix given probabilities

    :param direction: direction of movement
    :param x: what to add to the x axis to go in that direction
    :param y: what to add to the y axis to go in that direction
    :return: transition probabilities dictionary
    """
    states = map.states()
    possible_transitions = map.possible_transitions()

    transition_dict = {}
    for state in states:
        transition_dict[state] = {}
        for next_state in states:
            #if self.possible_transitions[state] == ["TERMINAL"]:
            #    transition_dict[state][next_state] = 1
            if next_state == state: # if the next state and the start state are the same
                if not direction in possible_transitions[state]:# if you cant move in that direction from state
                    transition_dict[state][next_state] = 1   # stay where you are
                else:
                    transition_dict[state][next_state] = 0.2    # otherwise you have a probability of not moving 0.2
            elif direction in possible_transitions[state]\
                and states[state][0] + x == states[next_state][0]\
                and states[state][1] + y == states[next_state][1]: #if you can go in the direction
                        transition_dict[state][next_state] = 0.8                #and if the state in the direction
            else:                                                                #is the next state then prob is 0.8
                transition_dict[state][next_state] = 0 # if you can t go there then probability 0

    return transition_dict


def calc_state_string(sx, sy):
    return "s" + str(sx + sy * 11)

def state_int(x, y):
    return x + y * 11

def generate_states():

    grid_map = map.grid_map()
    possible_states = {}
    state_no = "s"
    i = 0
    for row in range(11):
        for col in range(9):
            if grid_map[row][col] == 0:
                possible_states[str(state_no) + str(i)] = (col, row)
                i += 1
    # print(possible_states)
    return possible_states
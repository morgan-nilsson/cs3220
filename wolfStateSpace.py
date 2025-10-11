from wolfProblem import WolfProblem, Locations
import random

def is_valid_state(wolf_car, sheep_car, cabbage_car):
    """
    Check if a state is valid by enforcing the boat capacity constraint.
    The boat can hold at most one character at a time.
    """
    # Count how many characters are in the boat
    characters_in_boat = 0
    if wolf_car == Locations.BOAT:
        characters_in_boat += 1
    if sheep_car == Locations.BOAT:
        characters_in_boat += 1
    if cabbage_car == Locations.BOAT:
        characters_in_boat += 1
    
    # Boat can hold at most 1 character
    return characters_in_boat <= 1

def get_valid_states():
    list = []
    for wolf_car in [Locations.LEFT, Locations.RIGHT, Locations.BOAT]:
        for sheep_car in [Locations.LEFT, Locations.RIGHT, Locations.BOAT]:
                for cabbage_car in [Locations.LEFT, Locations.RIGHT, Locations.BOAT]:
                    for boat_car in [Locations.LEFT, Locations.RIGHT]:
                            # Only add valid states (boat capacity constraint)
                            if is_valid_state(wolf_car, sheep_car, cabbage_car):
                                list.append([wolf_car, sheep_car, cabbage_car, boat_car])
    return list

def encode_state(state):
    string = str(state[0])[0] + str(state[1])[0] + str(state[2])[0] + str(state[3])[0]
    return string

def make_wolf_world(valid_list):
    states = valid_list
    wolf_problem = WolfProblem()

    wolf_world = dict()
    for state in states:
        string = encode_state(state)
        wolf_world[string] = dict()
        for action in wolf_problem.actions(state):
            wolf_world[string][action] = encode_state(wolf_problem.result(state, action))
    return wolf_world

def print_wolf_world(wolf_world):
    list_valid = []
    list_invalids = []
    for key, value in wolf_world.items():
        if value == {}:
            list_invalids.append([key, value])
        else:
            list_valid.append([key, value])
    
    print("Valid states: ")
    for i in range(len(list_valid)):
        print(list_valid[i][0], list_valid[i][1])
    print("\n")

    print("Invalid states: ")
    for i in range(len(list_invalids)):
        print(list_invalids[i][0], list_invalids[i][1])

def wolfStatesLocations(valid_list):
    keyList = []
    for i in range(len(valid_list)):
        keyList.append(encode_state(valid_list[i]))
    x = []
    y = []
    n=len(keyList)
    for _ in range(n):
        x.append(random.randint(0, n+1)+100)
        y.append(random.randint(0, n+1)+100)
    zipped = zip(x, y)
    return dict(zip(keyList, zipped))

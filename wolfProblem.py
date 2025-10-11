from src.problemClass import Problem
from enum import Enum

class Actions(Enum):
    BOAT_LEFT = "BOAT_LEFT"
    BOAT_RIGHT = "BOAT_RIGHT"
    LOAD_WOLF = "LOAD_WOLF"
    UNLOAD_WOLF = "UNLOAD_WOLF"
    LOAD_SHEEP = "LOAD_SHEEP"
    UNLOAD_SHEEP = "UNLOAD_SHEEP"
    LOAD_CABBAGE = "LOAD_CABBAGE"
    UNLOAD_CABBAGE = "UNLOAD_CABBAGE"

class Locations:
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    BOAT = "BOAT"

class Character(Enum):
    WOLF = 0
    SHEEP = 1
    CABBAGE = 2
    BOAT = 3

class WolfProblem(Problem):

    def __init__(self):
        self.initial = [Locations.LEFT, Locations.LEFT, Locations.LEFT, Locations.LEFT] # boat last
        self.goal = [Locations.RIGHT, Locations.RIGHT, Locations.RIGHT, Locations.RIGHT]

    def is_same_side(self, state, thing: Character, thing2: Character) -> bool:
        '''
        Check if thing and thing2 are on the same side of the river
        '''
        if state[thing.value] == state[thing2.value]:
            return True
        return False

    def what_in_boat(self, state):
        '''
        Returns the character in the boat, or None if boat is empty
        '''
        for char in [Character.WOLF, Character.SHEEP, Character.CABBAGE]:
            if state[char.value] == Locations.BOAT:
                return char
        return None


    def actions(self, state): 
        # Check if current state is invalid
        if self.check_invalid_state(state):
            return []
        
        actions_list = []
        
        # Add boat movements based on current boat location
        if state[Character.BOAT.value] == Locations.LEFT:
            actions_list.append(Actions.BOAT_RIGHT)
        elif state[Character.BOAT.value] == Locations.RIGHT:
            actions_list.append(Actions.BOAT_LEFT)

        whats_in_boat = self.what_in_boat(state)
        if whats_in_boat == Character.CABBAGE:
            actions_list.append(Actions.UNLOAD_CABBAGE)
        elif whats_in_boat == Character.SHEEP:
            actions_list.append(Actions.UNLOAD_SHEEP)
        elif whats_in_boat == Character.WOLF:
            actions_list.append(Actions.UNLOAD_WOLF)
        elif whats_in_boat == None:
            if self.is_same_side(state, Character.BOAT, Character.CABBAGE):
                actions_list.append(Actions.LOAD_CABBAGE)
            if self.is_same_side(state, Character.BOAT, Character.SHEEP):
                actions_list.append(Actions.LOAD_SHEEP)
            if self.is_same_side(state, Character.BOAT, Character.WOLF):
                actions_list.append(Actions.LOAD_WOLF)
        
        return actions_list
    
    def result(self, state, action):
        # Note: We assume the action is valid (called by search algorithms)
        # The search algorithm should only call result with actions from actions(state)

        def move_thing(state, thing: Character, location: str):
            state[thing.value] = location

        new_state = state[:]

        if action == Actions.BOAT_LEFT:
            move_thing(new_state, Character.BOAT, Locations.LEFT)
        elif action == Actions.BOAT_RIGHT:
            move_thing(new_state, Character.BOAT, Locations.RIGHT)
        elif action == Actions.LOAD_CABBAGE:
            move_thing(new_state, Character.CABBAGE, Locations.BOAT)
        elif action == Actions.UNLOAD_CABBAGE:
            move_thing(new_state, Character.CABBAGE, new_state[Character.BOAT.value])
        elif action == Actions.LOAD_SHEEP:
            move_thing(new_state, Character.SHEEP, Locations.BOAT)
        elif action == Actions.UNLOAD_SHEEP:
            move_thing(new_state, Character.SHEEP, new_state[Character.BOAT.value])
        elif action == Actions.LOAD_WOLF:
            move_thing(new_state, Character.WOLF, Locations.BOAT)
        elif action == Actions.UNLOAD_WOLF:
            move_thing(new_state, Character.WOLF, new_state[Character.BOAT.value])
        
        return new_state

    def check_invalid_state(self, state):
        """Check if the state is invalid (wolf eats sheep, or sheep eats cabbage)"""
        # Get all characters on each side (excluding boat)
        left_side = []
        right_side = []
        
        for char in [Character.WOLF, Character.SHEEP, Character.CABBAGE]:
            if state[char.value] == Locations.LEFT:
                left_side.append(char)
            elif state[char.value] == Locations.RIGHT:
                right_side.append(char)
        
        # Check if farmer (boat) is present on each side
        farmer_on_left = state[Character.BOAT.value] == Locations.LEFT
        farmer_on_right = state[Character.BOAT.value] == Locations.RIGHT
        
        # Check for invalid combinations
        if not farmer_on_left:
            if Character.WOLF in left_side and Character.SHEEP in left_side:
                return True
            if Character.SHEEP in left_side and Character.CABBAGE in left_side:
                return True
                
        if not farmer_on_right:
            if Character.WOLF in right_side and Character.SHEEP in right_side:
                return True
            if Character.SHEEP in right_side and Character.CABBAGE in right_side:
                return True
                
        return False
            
    def goal_test(self, state):
        return state == self.goal
    
    def path_cost(self, c, state1, action, state2):
        # Cost: 1 for action (1), 2 for action (4), 3 for actions (2,3)
        action_costs = {
            Actions.BOAT_LEFT: 1,      # Action 1 - cost 1
            Actions.BOAT_RIGHT: 1,     # Action 1 - cost 1
            Actions.LOAD_WOLF: 3,      # Action 2 - cost 3
            Actions.UNLOAD_WOLF: 3,    # Action 2 - cost 3
            Actions.LOAD_SHEEP: 3,     # Action 3 - cost 3
            Actions.UNLOAD_SHEEP: 3,   # Action 3 - cost 3
            Actions.LOAD_CABBAGE: 2,   # Action 4 - cost 2
            Actions.UNLOAD_CABBAGE: 2  # Action 4 - cost 2
        }
        
        # Get the cost for this specific action
        action_cost = action_costs.get(action) 
        if c == None:
            return 1
        else:
            return c + action_cost
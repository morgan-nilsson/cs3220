from src.problemClass import Problem
from wolfProblem import Actions, Character, Locations

from enum import Enum
    

class WolfProblem(Problem):

    def __init__(self):
        self.initial = [Locations.LEFT, Locations.LEFT, Locations.LEFT, Locations.LEFT] # boat last
        self.goal = [Locations.RIGHT, Locations.RIGHT, Locations.RIGHT, Locations.RIGHT]
        self.is_dead = False

    def is_same_side(self, state, thing: Character, thing2: Character) -> bool:
        '''
        Check if thing and thing2 are on the same side of the river
        '''
        if state[thing] == state[thing2]:
            return True
        return False

    def what_in_boat(self, state):
        '''
        Returns an element of the Character enum if something is in the boat, else None
        '''
        for c in state:
            if c == Locations.BOAT:
                return c
        return None


    def actions(self, state): 
        if self.is_dead:
            return []
        yield Actions.BOAT_LEFT
        yield Actions.BOAT_RIGHT


        whats_in_boat = self.what_in_boat(state)
        if whats_in_boat == Character.CABBAGE:
            yield Actions.UNLOAD_CABBAGE

        elif whats_in_boat == Character.SHEEP:
            yield Actions.UNLOAD_SHEEP

        elif whats_in_boat == Character.WOLF:
            yield Actions.UNLOAD_WOLF

        elif whats_in_boat == None:
            if self.is_same_side(state, Character.BOAT, Character.CABBAGE):
                yield Actions.LOAD_CABBAGE

            if self.is_same_side(state, Character.BOAT, Character.SHEEP):
                yield Actions.LOAD_SHEEP

            if self.is_same_side(state, Character.BOAT, Character.WOLF):
                yield Actions.LOAD_WOLF
    
    def result(self, state, action):

        if action not in self.actions(state):
            print("Invalid action attempted:", action)
            return state #Invalid action, return the same state
        
        if self.is_dead:
            print("Attempted action on failed state:", action)
            return state

        def move_thing(state, thing: Character, location: str):
            state[thing] = location

        new_state = state[:]

        if action == Actions.BOAT_LEFT:
            move_thing(new_state, Character.BOAT, Locations.LEFT)
        elif action == Actions.BOAT_RIGHT:
            move_thing(new_state, Character.BOAT, Locations.RIGHT)
        elif action == Actions.LOAD_CABBAGE:
            move_thing(new_state, Character.CABBAGE, Locations.BOAT)
        elif action == Actions.UNLOAD_CABBAGE:
            move_thing(new_state, Character.CABBAGE, new_state[Character.BOAT])
        elif action == Actions.LOAD_SHEEP:
            move_thing(new_state, Character.SHEEP, Locations.BOAT)
        elif action == Actions.UNLOAD_SHEEP:
            move_thing(new_state, Character.SHEEP, new_state[Character.BOAT])
        elif action == Actions.LOAD_WOLF:
            move_thing(new_state, Character.WOLF, Locations.BOAT)
        elif action == Actions.UNLOAD_WOLF:
            move_thing(new_state, Character.WOLF, new_state[Character.BOAT])
        
        def is_bad_state(side):
            if Character.WOLF in new_state[side] and Character.SHEEP in new_state[side] and Character.BOAT not in new_state[side]:
                return True
            if Character.SHEEP in new_state[side] and Character.CABBAGE in new_state[side] and Character.BOAT not in new_state[side]:
                return True
            return False
        
        self.is_dead = is_bad_state('left') or is_bad_state('right')

            
    def goal_test(self, state):
        return super().goal_test(state)
    
    def path_cost(self, c, state1, action, state2):
        if c == None:
            return 1
        else:
            return c + 1
    
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
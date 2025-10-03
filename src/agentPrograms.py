import random

'''An idea of Random Agent Program is to choose an action at random, ignoring all percepts'''
def RandomAgentProgram(actions):
   return lambda percept: random.choice(actions)

def TableDrivenAgentProgram(table):
    """
    This agent selects an action based on the percept sequence.
    To customize it, provide as table a dictionary of all 
    {percept_sequence:action} pairs.
    """
    percepts = []

    def program(percept):
        percepts.append(percept)
        #print(tuple(percepts))
        action = table.get(tuple(percepts))
        
        if action is None:
          print("Not such percept sequence in my table")

        return action

    return program
  
  
def ReflexAgentProgram(rules,interpret_input,rule_match):
  #This AP takes action based solely on the percept.
    
    def program(percept):
        state = interpret_input(percept)
        action = rule_match(state, rules)
        return action

    return program


def interpret_input(percept):
  loc, status = percept
  return status


def rule_match(state, rules):
  for key in rules:
    if state in key:
      return rules[key]


from src.locations import loc_D

# return the program function for the ReflexAgentA2pro
def ReflexAgentA2proProgram(rules: dict):

    def program(percepts: tuple[tuple[int, int], list[object]]) -> str:

        coords, perceptions = percepts

        # There is nothing in the room
        if len(perceptions) == 0:

            # If we are in the last room, stop
            if coords == loc_D:
                return "Stop"

            return "Go ahead"

        # there can be multiple things in the room but we only address one
        what_was_seen = identify_perception(perceptions[0])
        # I don't know what I saw so stop
        if what_was_seen == "Unknown":
            print("I don't know what I saw")
            return "Stop"
            
        return rules[what_was_seen]

    return program

from src.Task3YourClasses import OfficeManager, ITStaff, Student

def identify_perception(perception: object): 
    if isinstance(perception, OfficeManager):
        return "Office manager"
    elif isinstance(perception, ITStaff):
       return "IT"
    elif isinstance(perception, Student):
        return "Student"
    else:
      return "Unknown"

def rule_match_A2pro(state: str, rules: dict[str, str]) -> str:
    return rules[state]
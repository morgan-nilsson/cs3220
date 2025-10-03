#lab2 part1 - cat in the house

import random
import collections

#these are the two locations for the two-state environment
from src.locations import *

#this is a base class representing ANY physical object that can appear
#in ANY evnironment
from src.thingClass import Thing

#in order to get anywhere, we'll need an Agent - a subclass of Thing.
#it has one required attribute - .program, which represents the Agent
#Program (i.e. the base of its logic). This program should hold a function
#that takes 1 argument (percept) and returns an action.
from src.agentClass import Agent

#we'll also need the environment class - a base class representing an
#abstract environment. The environment keeps a list of .agents, and each
#agent has a .performance slot initialized to 0. All 'real' environemnt
#classes must inherit from this one.
from src.trivialVacuumEnvironmentClass import TrivialVacuumEnvironment

print(loc_A, loc_B)

table =     {((loc_A, 'Clean'),): 'Right',
             ((loc_A, 'Dirty'),): 'Suck',
             ((loc_B, 'Clean'),): 'Left',
             ((loc_B, 'Dirty'),): 'Suck',
             ((loc_A, 'Dirty'), (loc_A, 'Clean')): 'Right',
             ((loc_A, 'Clean'), (loc_B, 'Dirty')): 'Suck',
             ((loc_B, 'Clean'), (loc_A, 'Dirty')): 'Suck',
             ((loc_B, 'Dirty'), (loc_B, 'Clean')): 'Left',
             ((loc_A, 'Dirty'), (loc_A, 'Clean'), (loc_B, 'Dirty')): 'Suck',
             ((loc_B, 'Dirty'), (loc_B, 'Clean'), (loc_A, 'Dirty')): 'Suck'
            }

a = [] #assume that this is a percept sequence
a.append(((1, 0), 'Clean')) # add a new percept
print(tuple(a))

#testing out the Thing class:
thing0 = Thing()
print(thing0)
print(thing0.is_alive())
print(thing0.show_state())

#by default, thing is NOT alive and does NOT know how to show state.
#(it won't even have any..)

def RandomAgentProgram(actions):
    return lambda percept: random.choice(actions)
#lambda functions take any number of arguments but only have 1 expression.

actionList = ['Right', 'Left', 'Suck', 'NoOp']
f = RandomAgentProgram(actionList)

for i in range(5):
    print(f('111'))

#implementing the Random Agent - the agent instance that randomly chooses
#one of the actions from the vacuum environment (our actionList)

def RandomVacuumAgent():
    return Agent(RandomAgentProgram(actionList))

a1 = RandomVacuumAgent()
print(f"{a1} has the performance: {a1.performance}")
for i in range(5):
    print(a1.program('111'))

e1 = TrivialVacuumEnvironment()
#Checking the initial state of the environment
print("State of the Environment: {}.".format(e1.status))

#it is now time to create our random agent. this agent will randomly choose
#either 'right,' 'left,' 'suck,' or 'noOp.'
a1 = RandomVacuumAgent()

#the agent needs to be added to our environemnt instance e1
e1.add_thing(a1)
print("RandomVacuumAgent is located at {}.".format(a1.location))

#let's try running our environment for 1 step, and then check its current
#state.
#e1.step()
#print("State of the Environment: {}.".format(e1.status))
#print("RandomVacuumAgent is located at {}.".format(a1.location))

#you can also run the environment for its entire lifecycle
e1.run()

e1.status == {(1, 0): 'Clean', (0, 0): 'Clean'}

print("------time for the new environment!!------")

e2 = TrivialVacuumEnvironment()
a2 = RandomVacuumAgent()
e2.add_thing(a2)

print("State of the Environment: {}".format(e2.status))
print("RandomVacuumAgent is located at {}.".format(a2.location))
e2.run()

#now you're ready to begin task 1! random agents :)
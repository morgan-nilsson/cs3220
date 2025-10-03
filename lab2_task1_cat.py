import random
import collections

from src.thingClass import Thing
from inheritedThingClass import Milk, Mouse, Dog
from src.agentClass import Agent
from src.agents import RandomCatAgent
from crazyHouseEnvironmentClass import crazyHouseEnvironment

actionList = ['MoveRight', 'MoveLeft', 'Eat', 'Drink', 'Fight']

mouse = Mouse()
milk = Milk()
dog = Dog()
cat = RandomCatAgent()
e1 = crazyHouseEnvironment()

cat.__name__ = "Cat"

e1.add_thing(mouse)
e1.add_thing(milk)
e1.add_thing(dog)
e1.add_thing(cat)
e1.correct_placments()

print("Initial State of the Environment: {}.".format(e1.status))
while not e1.is_done():
    print()
    e1.step()
    print("State of the Environment: {}.".format(e1.status))
    print("Cat Performance: {}.".format(cat.performance))
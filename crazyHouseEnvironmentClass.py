from src.environmentClass import Environment
from src.thingClass import Thing
from src.locations import *
from inheritedThingClass import Milk, Mouse, Dog

import random

class crazyHouseEnvironment(Environment):
  def __init__(self):
    super().__init__()
    self.status = {hLoc_A: [],
                   hLoc_B: [], 
                   hLoc_C: [], 
                   hLoc_D: [], 
                   hLoc_E: []}
    self.things = []
    self.locations = [hLoc_A, hLoc_B, hLoc_C, hLoc_D, hLoc_E]

  def add_thing(self, thing):
    super().add_thing(thing)
    thing.location = self.default_location(thing)
    self.status[thing.location].append(thing)

  def find_thing(self, thing_type):
    for l in self.status:
      for t in self.status[l]:
        if isinstance(t, thing_type):
          return t

  def correct_placments(self):
    dog = self.find_thing(Dog)
    mouse = self.find_thing(Mouse)
    milk = self.find_thing(Milk)

    # follow dog mouse rules
    if ((mouse != None and dog != None) and (dog.location == mouse.location)):
      if dog.location == hLoc_A: # if they're both at the leftmost spot, mouse goes right one.
        self.status[mouse.location].remove(mouse)
        mouse.location = hLoc_B
        self.status[mouse.location].append(mouse)
      elif dog.location == hLoc_E: # if they're both at the rightmost spot, mouse goes left one.
        self.status[mouse.location].remove(mouse)
        mouse.location = hLoc_D
        self.status[mouse.location].append(mouse)
      else:
        self.status[mouse.location].remove(mouse)
        mouse.location = mouse.location + random.choice([-1, 1])
        self.status[mouse.location].append(mouse)

    # follow milk mouse rules
    if ((milk != None and mouse != None) and (milk.location == mouse.location)):
      self.status[milk.location].remove(milk)
      self.delete_thing(milk)
    


  def percept(self, agent):
    #Returns the agent's location, and the location status (which Things are there).
    return agent.location, self.status[agent.location]

  def is_agent_alive(self, agent):
    return agent.alive

  def update_agent_alive(self, agent):
    if agent.performance < 0:
      agent.alive = False
      print("Agent {} has lost.".format(agent))

  def execute_action(self, agent, action):
    '''Check if agent alive, if so, execute action'''
    if self.is_agent_alive(agent):

        if action == 'MoveRight':
            if(agent.location == hLoc_E):
               print("{} can not move any further to the right!".format(agent))
            else:
              self.status[agent.location].remove(agent)
              agent.location += 1
              self.status[agent.location].append(agent)
              agent.performance -= 1
            self.update_agent_alive(agent)

        elif action == 'MoveLeft':
            if(agent.location == hLoc_A):
               print("{} can not move any further to the left!".format(agent))
            else:
              self.status[agent.location].remove(agent)
              agent.location -= 1
              self.status[agent.location].append(agent)
              agent.performance -= 1
            self.update_agent_alive(agent)

        elif action == 'Eat':
            mouse = self.find_thing(Mouse)
            if mouse != None and self.status.get(agent.location).count(mouse) > 0:
                print("The cat is trying to eat the mouse!")
                if agent.performance >= 3:
                   self.delete_thing(mouse)
                   print("The cat ate the mouse!")
                   agent.performance += 10
            else:
               print("There is nothing to eat.")
            self.update_agent_alive(agent)

        elif action == 'Drink':
            milk = self.find_thing(Milk)
            if milk != None and self.status.get(agent.location).count(milk) > 0:
               self.delete_thing(self.find_thing(Milk))
               print("The cat drank the milk!")
               agent.performance += 5
            else:
               print("There is nothing to drink.")
            self.update_agent_alive(agent)

        elif action == 'Fight':
            dog = self.find_thing(Dog)
            if dog != None and self.status.get(agent.location).count(dog) > 0:
               print("The cat is trying to fight the dog!")
               if agent.performance >= 10:
                  agent.performance += 20
                  print("The cat beat the dog!")
               else:
                  agent.performance -= 10
                  print("The cat lost to the dog.")
            else:
              print("There is nothing to fight.")
            self.update_agent_alive(agent)

  def default_location(self, thing):
        """Agents start in a location at random."""
        print("Agent is starting in random location...")
        return random.choice([hLoc_A, hLoc_B, hLoc_C, hLoc_D, hLoc_E])
        
  def delete_thing(self, thing):
    self.status[thing.location].remove(thing)
    return super().delete_thing(thing)
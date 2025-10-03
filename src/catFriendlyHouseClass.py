from src.environmentClass import Environment
from src.agentCatClass import *
from src.foodClass import Milk, Sausage
from src.locations import *
import random

class CatFriendlyHouse(Environment):
    def __init__(self):
        super().__init__()  
        self.locations = [loc_A, loc_B] #the locations of the house
        self.status = {} #Track whats is in each room

        #Initialize the status of each room to empty
        for location in self.locations:
            self.status[location] = 'Empty'
        
        #place food in the house
        self.place_food()

    def place_food(self):
        #create food with random weight
        milk = Milk(random.randint(101, 200))
        sausage = Sausage(random.randint(101, 200))

        #place food in the house
        milk_room = random.choice(self.locations)
        if milk_room == loc_A:
            sausage_room = loc_B
        else:
            sausage_room = loc_A
        
        # Set food locations
        milk.location = milk_room
        sausage.location = sausage_room

        # Update room status for perception
        self.status[milk_room] = milk
        self.status[sausage_room] = sausage
        
        print(f"🥛 Milk placed in room {milk_room}")
        print(f"🌭 Sausage placed in room {sausage_room}")
 

    def percept(self, agent):
    #Returns the agent's location, and the location status (Empty/MilkHere/SausageHere).
        return agent.location, self.status[agent.location]

    def is_agent_alive(self, AgentCat):
        return AgentCat.alive
    
    def update_agent_alive(self, AgentCat):
        if AgentCat.performance <= 0:
            AgentCat.alive = False
            print("Agent {} is dead.".format(AgentCat))
    
    def execute_action(self, agentCat: AgentCat, action):
        '''Check if agent alive, if so, execute action'''
        if self.is_agent_alive(agentCat):
            if action == 'MoveRight':
                agentCat.location = loc_B
                agentCat.performance -= 1
                self.update_agent_alive(agentCat)
            elif action == 'MoveLeft':
                agentCat.location = loc_A
                agentCat.performance -= 1
                self.update_agent_alive(agentCat)
            elif action == 'Drink':
                agentCat.drink(self.status.get(agentCat.location))
                self.status[agentCat.location] = 'Empty'
            elif action == 'Eat':
                agentCat.eat(self.status.get(agentCat.location))
                self.status[agentCat.location] = 'Empty'
            else:
                print("No action to execute")



    def default_location(self, thing):
        """Agents start in either location at random."""
        print("Agent is starting in random location...")
        return random.choice([loc_A, loc_B])
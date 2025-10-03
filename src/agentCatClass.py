from src.agentClass import Agent
from src.foodClass import Milk, Sausage, Food
from src.rules import feedingRules

class AgentCat(Agent):

    """AgentCat is a subclass of Agent that can eat and drink."""
    def __init__(self):
        super().__init__(None)
        self.name = "Cat"
        self.program = AgentCat.program
    
    def eat(self, food):
        """Can eats food (only sausage allowed)"""

        if isinstance(food, Sausage):
            # preformance gain is equal to calories / 100
            performance_gain = food.calories / 100
            self.performance += performance_gain
            print(f"Cat ate sausage! Performance +{performance_gain} (now {self.performance})")
            return True
        else:
            print("Can't eat this item (only sausage).")
            return False
    
    def drink(self, food):
        """Can drink food (only milk allowed)"""

        if isinstance(food, Milk):
            # preformance gain is equal to calories / 100
            performance_gain = food.calories / 100
            self.performance += performance_gain
            print(f"Cat drank milk! Performance +{performance_gain} (now {self.performance})")
            
            return True
        else:
            print("Cant cant drink sausage")
            return False

    def program(percepts: tuple[tuple[int, int], Food]) -> str:
        print(percepts)
        loc, food = percepts
        food = str(food)
        return feedingRules.get((loc, food))
        
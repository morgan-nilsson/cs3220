from src.thingClass import Thing

class Food(Thing):
    """Base class for all food items."""
    def __init__(self, weight):
        self.weight = weight
        self.calories = self.get_calories()
    
    def get_calories(self):
        """Get the calories of the food item."""
        return 0

class Milk(Food):
    """Class for milk food item."""

    #initialize the weight of the milk food item
    def __init__(self, weight):
        super().__init__(weight)

    def get_calories(self):
        """Get the calories of the milk food item."""
        # Whole milk: ~ 61 kcal / 100 g
        return (self.weight) * (61 / 100)
    
    def __repr__(self):
        return 'MilkHere'


class Sausage(Food):
    """Class for sausage food item."""

    #initialize the weight of the sausage food item
    def __init__(self, weight):
        super().__init__(weight)

    def get_calories(self):
        """Get the calories of the sausage food item."""
        # Chicken/turkey sausage: ~ 150–200 kcal / 100 g
        return (self.weight) * (175 / 100)
    
    def __repr__(self):
        return 'SausageHere'

from src.thingClass import Thing

class Milk(Thing):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "Milk"


class Dog(Thing):
    def __init__(self):
        super().__init__()
    def __repr__(self):
        return "Dog"
    
class Mouse(Thing):
    def __init__(self):
        super().__init__()
    def __repr__(self):
        return "Mouse"


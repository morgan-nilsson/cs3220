

from src.agentCatClass import AgentCat
from src.catFriendlyHouseClass import CatFriendlyHouse

def main():
    house = CatFriendlyHouse()

    house.add_thing(AgentCat())

    house.run()



    
if __name__ == '__main__':
    main()
    
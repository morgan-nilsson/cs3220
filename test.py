from asteroidEnvironment import AsteroidEnvironment
maze = AsteroidEnvironment(4)
print("This is my maze \n", maze.maze)

mazeALLActs = maze.defineMazeActions()
print("\n This is my mazeAvailableActions")
for key, value in mazeALLActs.items():
    print(key, value)

print("\n This is my possible_actions_from_state")
mazePossibleActs = {}
for state, value in mazeALLActs.items():
    key = maze.possible_actions_from_state(state)
    for i, j in key.items(): 
        print(i, j) 
        mazePossibleActs[i] = j


print("\n This is my makeMazeTransformationModel")
maze1TM = {}
maze1TM = maze.makeMazeTransformationModel(mazePossibleActs)
for i, j in maze1TM.items():
    print(i, j)
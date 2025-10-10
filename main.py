from MazeEnviroment import MazeEnviroment
from MazeSolvingAgent import MazeSolvingAgent

agent = MazeSolvingAgent()
maze = MazeEnviroment(agent)

str = ""
while str != "exit":
    maze.step()
    str = input("Press Enter to continue, type 'exit' to quit: ")
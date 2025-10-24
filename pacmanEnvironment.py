from __future__ import annotations
from src.environmentClass import Environment
from enum import Enum
import numpy as np
from numpy import matrix
import random
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from pacmanAgent import PacManAgent

class PacManComponents(Enum):
    PATH = 0
    WALL = 1
    FOOD = 2
    GHOST = 3

class PacManAction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class MatrixPacMan:
    def __init__(self, maze: list[list], n: int) -> None:
        self.maze: list[list] = maze
        self.n: int = n
    
    def get(self, x: int, y: int):
        return self.maze[y][x]
    
    def set(self, x: int, y: int, value: int):
        self.maze[y][x] = value

    def N(self) -> int:
        return self.n * self.n

    def __repr__(self):
        return str(matrix(self.maze))
    
    def __len__(self):
        return len(self.maze)
    

class PacManEnvironment(Environment):
    def __init__(self, n):
        self.maze: MatrixPacMan | None = None
        super().__init__()
        self.agents: list[PacManAgent] = []
        self.ghost_locations: list[tuple[int, int]] = []
        self.food_dot_locations: list[tuple[int, int]] = []
        self.createPacmanEnvironment(n)
        self.initial_location = self.get_random_empty_location()
        if self.initial_location is None:
            raise ValueError("No empty location found for initial agent placement.")
        self.goal_location = self.get_random_empty_location()
        while self.goal_location == self.initial_location:
            self.goal_location = self.get_random_empty_location()
        if self.goal_location is None:
            raise ValueError("No empty location found for goal placement.")

        

    def createPacmanEnvironment(self, n) -> None:
        size = (n, n)
        prob_wall = .40
        prob_path = .60
        
        matFlat = np.random.choice([PacManComponents.WALL.value, PacManComponents.PATH.value], size=size, p=[prob_wall, prob_path])
        mat: list[list[int]] = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(matFlat[i][j])
            mat.append(row)
        self.maze = MatrixPacMan(mat, n)
        self.placeGhosts()
        self.placeFood()


    def placeGhosts(self):
        i = 1
        if self.maze == None:
            raise ValueError("Maze is not initialized.")
        
        while (i <= 5):
            empty_location = self.get_random_location_without_ghosts()
            if empty_location != None:
                self.ghost_locations.append(empty_location)
                self.maze.set(empty_location[0], empty_location[1], PacManComponents.GHOST.value)
                i += 1
            else:
                continue

    def placeFood(self):
        i = 1
        if self.maze == None:
            raise ValueError("Maze is not initialized.")
        n = self.maze.N() * 0.1
        
        while (i <= n):
            empty_location = self.get_random_location_without_ghosts()
            if empty_location != None:
                self.food_dot_locations.append(empty_location)
                x = empty_location[0]
                y = empty_location[1]
                self.maze.set(x, y, PacManComponents.FOOD.value)
                i += 1
            else:
                continue

    def get_random_location_without_ghosts(self):
        while True:
            loc = self.get_random_empty_location()
            if loc == None:
                continue
            if loc not in self.ghost_locations:
                return loc

    
    def definePacManActions(self) -> dict[tuple[int, int], list[PacManAction]]:
        maze = self.maze
        if maze is None:
            return {}
        n = len(maze)
        mazeAvailableActions = {}
        for x in range(n):
            for y in range(n):
                if x == 0 and y == 0:
                    mazeAvailableActions[(x,y)] = [PacManAction.DOWN.value, PacManAction.RIGHT.value]
                elif x == 0 and y == n-1:
                    mazeAvailableActions[(x,y)] = [PacManAction.UP.value, PacManAction.RIGHT.value]
                elif x == n-1 and y == 0:
                    mazeAvailableActions[(x,y)] = [PacManAction.DOWN.value, PacManAction.LEFT.value]
                elif x == n-1 and y == n-1:
                    mazeAvailableActions[(x,y)] = [PacManAction.UP.value, PacManAction.LEFT.value]
                elif x == 0:
                    mazeAvailableActions[(x,y)] = [PacManAction.UP.value, PacManAction.DOWN.value, PacManAction.RIGHT.value]
                elif x == n-1:
                    mazeAvailableActions[(x,y)] = [PacManAction.UP.value, PacManAction.DOWN.value, PacManAction.LEFT.value]
                elif y == 0:
                    mazeAvailableActions[(x,y)] = [PacManAction.DOWN.value, PacManAction.LEFT.value, PacManAction.RIGHT.value]
                elif y == n-1:
                    mazeAvailableActions[(x,y)] = [PacManAction.UP.value, PacManAction.LEFT.value, PacManAction.RIGHT.value]
                else:
                    mazeAvailableActions[(x,y)] = [PacManAction.UP.value, PacManAction.DOWN.value, PacManAction.LEFT.value, PacManAction.RIGHT.value]
        return mazeAvailableActions

    def possible_actions_from_state(self, state: tuple[int, int]) -> dict[tuple[int, int], list[PacManAction]]:
        all_actions = self.definePacManActions()
        all_from_state = all_actions.get(state)
        if all_from_state is None:
            return {}
        if self.maze is None:
            return {}
        x, y  = state
        n = len(self.maze)
        good: list[PacManAction] = []
        for action in all_from_state:
            if action == PacManAction.UP.value:
                if y - 1 >= 0 and self.maze.get(x, y-1) != PacManComponents.WALL.value:
                    good.append(action)
            elif action == PacManAction.DOWN.value:
                if y + 1 < n and self.maze.get(x, y + 1) != PacManComponents.WALL.value:
                    good.append(action)
            elif action == PacManAction.LEFT.value:
                if x - 1 >= 0 and self.maze.get(x - 1, y) != PacManComponents.WALL.value:
                    good.append(action)
            elif action == PacManAction.RIGHT.value:
                if x + 1 < n and self.maze.get(x + 1, y) != PacManComponents.WALL.value:
                    good.append(action)
        return {state: good}
    
    def makePacManTransformationModel(self, mazeActs: dict[tuple[int, int], list[PacManAction]]):
        moves = {}  # reset for each state
        for key in mazeActs:
            for action in mazeActs[key]:
                if action == PacManAction.UP.value:
                    x=key[0]
                    y=key[1]-1
                    moves.setdefault(key, {})["up"] = (x, y)
                elif action == PacManAction.DOWN.value:
                    x=key[0]
                    y=key[1]+1
                    moves.setdefault(key, {})["down"] = (x, y)          
                elif action == PacManAction.RIGHT.value:
                    x=key[0]+1
                    y=key[1]
                    moves.setdefault(key, {})["right"] = (x, y)
                elif  action == PacManAction.LEFT.value:
                    x=key[0]-1
                    y=key[1]
                    moves.setdefault(key, {})["left"] = (x, y)
            if len(mazeActs[key])==0:
                moves.setdefault(key,{})
        return moves

        
    def move(self, agent: PacManAgent, action: PacManAction) -> tuple[int, int]:
        x, y = agent.state
        if action == PacManAction.UP.value:
            y -= 1            
        elif action == PacManAction.DOWN.value:
            y += 1
        elif action == PacManAction.LEFT.value:
            x -= 1
        elif action == PacManAction.RIGHT.value:
            x += 1

        return (x, y)

    def manhattan_distance(self, state1: tuple[int, int], state2: tuple[int, int]) -> int:
        return abs(state1[0] - state2[0]) + abs(state1[1] - state2[1])

    def execute_action(self, agent: PacManAgent, action: PacManAction | None) -> None:
        if agent.status != "Alive":
            print("Agent {} could not move because it {}.".format(agent, agent.status))
            return

        possible_actions = self.possible_actions_from_state(agent.state).get(agent.state, [])
        if action not in possible_actions:
            raise ValueError(f"Action {action} is not valid from state {agent.state}")

        agent.state = self.move(agent, action)

        if agent.state == self.goal_location and self.food_dot_locations == []:
            agent.status = "Finished"
        
        agent.performance -= 1
        for enemy in self.ghost_locations:
            if agent.state == enemy:

                if self.maze is None:
                    continue

                if agent.performance <= 0.3 * self.maze.N():
                    agent.status = "Dead"
                    print("Agent {} encountered an enemy at location {} and has died.".format(agent, enemy[0]))
                else:
                    old_performance = agent.performance
                    new_performance = agent.performance * .10
                    agent.performance = old_performance - new_performance
                    print("Agent {} encountered an enemy at location {} and lost {} performance points. Remaining performance: {}.".format(agent, enemy[0], old_performance, agent.performance))

        
            if agent.state in self.food_dot_locations:
                print("Agent {} has eaten food at location {} and doubled its performance.".format(agent, agent.state))
                self.food_dot_locations.remove(agent.state)
                agent.performance *= 2

        if agent.performance <= 0:
            agent.status = "Dead"
            print("Agent {} has run out of performance and is dead.".format(agent))


    def get_random_empty_location(self) -> tuple[int, int] | None:
        if self.maze is None:
            return None
        n = len(self.maze)
        while True:
            x, y = (random.randint(0, n-1), random.randint(0, n-1))
            if self.maze.get(x, y) == PacManComponents.PATH.value:
                return (x, y)
    
    def is_done(self) -> bool:
        for agent in self.agents:
            if agent.problem.goal_test(agent.state):
                agent.status = "Finished"
        return not any(agent.status == "Alive" for agent in self.agents)

    def step(self) -> None:
        actions = []
        for agent in self.agents:
            if agent.status == "Alive":
                action = agent.pick_action()
                if action is None:
                    continue
                actions.append(action)
            else:
                actions.append("")
        for agent, action in zip(self.agents, actions):
            if agent.status != "Alive":
                continue
            self.execute_action(agent, action)
         
    def run(self, steps=10) -> None:
        super().run(steps)

    def add_agent(self, agent: PacManAgent) -> None:
        self.agents.append(agent)
    
    def show_graph(self, filename:str="PacManGame.html"):
        from pyvis.network import Network
        from src.maze2025GraphClass import mazeGraph
        from src.mazeData import mazeStatesLocations
        from src.mazeData import intTupleTostr

        maze_actions = self.definePacManActions()

        mazePossibleActs = {}
        for state, value in maze_actions.items():
            key = self.possible_actions_from_state(state)
            for i, j in key.items():
                mazePossibleActs[i] = j
        
        maze1TM = {}
        maze1TM = self.makePacManTransformationModel(mazePossibleActs)
        mazeWorldGraph = mazeGraph(maze1TM, mazeStatesLocations(list(maze1TM.keys())))

        net_maze = Network( heading="Lab5. PacMan Maze",
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%") # do this
        
        nodeColors={
            "start":"green",
            "food":"yellow",
            "agent":"purple",
            "ghost":"red",
            "path":"white",
            "wall":"grey",
            "end":"blue"
        }

        nodeColorsList=[]
        for node in mazeWorldGraph.origin.keys():
            node_value = self.maze.get(node[0], node[1])
            if node == self.agents[0].state:
                nodeColorsList.append(nodeColors["agent"])
            elif node == self.goal_location:
                nodeColorsList.append(nodeColors["end"])
            elif node == self.initial_location:
                nodeColorsList.append(nodeColors["start"])
            elif node_value==0:
                nodeColorsList.append(nodeColors["path"])
            elif node_value==1:
                nodeColorsList.append(nodeColors["wall"])
            elif node_value==2:
                nodeColorsList.append(nodeColors["food"])
            elif node_value==3:
                nodeColorsList.append(nodeColors["ghost"])

        nodes=["-".join(str(item) for item in el) for el in mazeWorldGraph.origin.keys()]

        x_coords = []
        y_coords = []

        for node in mazeWorldGraph.origin.keys():
            x,y=mazeWorldGraph.getLocation(node)
            x_coords.append(x)
            y_coords.append(y)
        
        sizes=[10]*len(nodes)

        net_maze.add_nodes(nodes, color=nodeColorsList, x=x_coords, y=y_coords, size=sizes, title=nodes)
        
        for node in net_maze.nodes:
            node['label']=''

        edge_weights = {}
        for init_state, list_of_edges in mazeWorldGraph.origin.items():
            state_str = intTupleTostr(init_state)
            for move, target in list_of_edges.items():
                target_str = intTupleTostr(target)
                edge_weights[(state_str, target_str)] = move

        edges=[]
        for node_source in mazeWorldGraph.nodes():
            for node_target, action in mazeWorldGraph.get(node_source).items():
            #node_target or node_source is a tuple -> convert to str
                if (intTupleTostr(node_source),intTupleTostr(node_target)) not in edges:
                    net_maze.add_edge(intTupleTostr(node_source),intTupleTostr(node_target), title=edge_weights[(intTupleTostr(node_source),intTupleTostr(node_target))], smooth=True, lable="")
                    edges.append((intTupleTostr(node_source),intTupleTostr(node_target)))

        net_maze.toggle_physics(False)
        net_maze.save_graph(filename)
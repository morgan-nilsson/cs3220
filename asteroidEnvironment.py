from __future__ import annotations
from src.environmentClass import Environment
from enum import Enum
import numpy as np
from numpy import matrix
import random
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from SatelliteAgent import SatelliteAgent

class MazeComponents(Enum):
    PATH = 0
    ASTEROID = 1
    ENEMIES = 2

class AstroidMazeAction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class MatrixMaze:
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
    

class AsteroidEnvironment(Environment):
    def __init__(self, n):
        self.maze: MatrixMaze | None = None
        super().__init__()
        self.agents: list[SatelliteAgent] = []
        self.enemies: list[tuple[tuple[int, int], int]] = [] 
        self.createAsteroidEnvironment(n)
        self.initial_location = self.get_random_empty_location()
        if self.initial_location is None:
            raise ValueError("No empty location found for initial agent placement.")
        self.goal_location = self.get_random_empty_location()
        if self.goal_location is None:
            raise ValueError("No empty location found for goal placement.")

    def createAsteroidEnvironment(self, n) -> None:
        size = (n,n)
        prob_Path = .65
        prob_Asteroid = .25
        prob_Enemies = .10

        enemies_LowPower = int(n * n * .10)
        enemies_HighPower = int(n * n * .40)
        matFlat=np.random.choice([MazeComponents.ASTEROID.value, MazeComponents.ENEMIES.value, MazeComponents.PATH.value], size=size, p=[prob_Asteroid, prob_Enemies, prob_Path])
        mat: list[list[int]] = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(matFlat[i][j])
            mat.append(row)
        for x in range(n):
            for y in range(n):
                if matFlat[x, y] == MazeComponents.ENEMIES.value: 
                    self.enemies.append(((x, y), random.randint(enemies_LowPower, enemies_HighPower)))
            

        self.maze = MatrixMaze(mat, n)
    
    def defineMazeActions(self) -> dict[tuple[int, int], list[AstroidMazeAction]]:
        maze = self.maze
        if maze is None:
            return {}
        n = len(maze)
        mazeAvailableActions = {}
        for x in range(n):
            for y in range(n):
                if x == 0 and y == 0:
                    mazeAvailableActions[(x,y)] = [AstroidMazeAction.DOWN.value, AstroidMazeAction.RIGHT.value]
                elif x == 0 and y == n-1:
                    mazeAvailableActions[(x,y)] = [AstroidMazeAction.UP.value, AstroidMazeAction.RIGHT.value]
                elif x == n-1 and y == 0:
                    mazeAvailableActions[(x,y)] = [AstroidMazeAction.DOWN.value, AstroidMazeAction.LEFT.value]
                elif x == n-1 and y == n-1:
                    mazeAvailableActions[(x,y)] = [AstroidMazeAction.UP.value, AstroidMazeAction.LEFT.value]
                elif x == 0:
                    mazeAvailableActions[(x,y)] = [AstroidMazeAction.UP.value, AstroidMazeAction.DOWN.value, AstroidMazeAction.RIGHT.value]
                elif x == n-1:
                    mazeAvailableActions[(x,y)] = [AstroidMazeAction.UP.value, AstroidMazeAction.DOWN.value, AstroidMazeAction.LEFT.value]
                elif y == 0:
                    mazeAvailableActions[(x,y)] = [AstroidMazeAction.DOWN.value, AstroidMazeAction.LEFT.value, AstroidMazeAction.RIGHT.value]
                elif y == n-1:
                    mazeAvailableActions[(x,y)] = [AstroidMazeAction.UP.value, AstroidMazeAction.LEFT.value, AstroidMazeAction.RIGHT.value]
                else:
                    mazeAvailableActions[(x,y)] = [AstroidMazeAction.UP.value, AstroidMazeAction.DOWN.value, AstroidMazeAction.LEFT.value, AstroidMazeAction.RIGHT.value]
        return mazeAvailableActions

    def possible_actions_from_state(self, state: tuple[int, int]) -> dict[tuple[int, int], list[AstroidMazeAction]]:
        all_actions = self.defineMazeActions()
        all_from_state = all_actions.get(state)
        if all_from_state is None:
            return {}
        if self.maze is None:
            return {}
        x, y  = state
        n = len(self.maze)
        good: list[AstroidMazeAction] = []
        for action in all_from_state:
            if action == AstroidMazeAction.UP.value:
                if y - 1 >= 0 and self.maze.get(x, y-1) != MazeComponents.ASTEROID.value:
                    good.append(action)
            elif action == AstroidMazeAction.DOWN.value:
                if y + 1 < n and self.maze.get(x, y + 1) != MazeComponents.ASTEROID.value:
                    good.append(action)
            elif action == AstroidMazeAction.LEFT.value:
                if x - 1 >= 0 and self.maze.get(x - 1, y) != MazeComponents.ASTEROID.value:
                    good.append(action)
            elif action == AstroidMazeAction.RIGHT.value:
                if x + 1 < n and self.maze.get(x + 1, y) != MazeComponents.ASTEROID.value:
                    good.append(action)
        return {state: good}
    
    def makeMazeTransformationModel(self, mazeActs: dict[tuple[int, int], list[AstroidMazeAction]]):
        moves = {}  # reset for each state
        for key in mazeActs:
            for action in mazeActs[key]:
                if action == AstroidMazeAction.UP.value:
                    x=key[0]
                    y=key[1]-1
                    moves.setdefault(key, {})["up"] = (x, y)
                elif action == AstroidMazeAction.DOWN.value:
                    x=key[0]
                    y=key[1]+1
                    moves.setdefault(key, {})["down"] = (x, y)          
                elif action == AstroidMazeAction.RIGHT.value:
                    x=key[0]+1
                    y=key[1]
                    moves.setdefault(key, {})["right"] = (x, y)
                elif  action == AstroidMazeAction.LEFT.value:
                    x=key[0]-1
                    y=key[1]
                    moves.setdefault(key, {})["left"] = (x, y)
            if len(mazeActs[key])==0:
                moves.setdefault(key,{})
        return moves

        
    def move(self, agent: SatelliteAgent, action: AstroidMazeAction) -> tuple[int, int]:
        x, y = agent.state
        if action == AstroidMazeAction.UP.value:
            y -= 1            
        elif action == AstroidMazeAction.DOWN.value:
            y += 1
        elif action == AstroidMazeAction.LEFT.value:
            x -= 1
        elif action == AstroidMazeAction.RIGHT.value:
            x += 1

        return (x, y)

    def execute_action(self, agent: SatelliteAgent, action: AstroidMazeAction | None) -> None:
        if agent.status != "Alive":
            print("Agent {} could not move because it {}.".format(agent, agent.status))
            return

        possible_actions = self.possible_actions_from_state(agent.state).get(agent.state, [])
        if action not in possible_actions:
            raise ValueError(f"Action {action} is not valid from state {agent.state}")

        agent.state = self.move(agent, action)

        if agent.state == self.goal_location:
            agent.status = "Finished"
        
        agent.performance -= 1
        for enemy in self.enemies:
            if agent.state == enemy[0]:
                if(enemy[1] * 2 >= agent.performance):
                    agent.alive = False
                else:
                    old_performance = agent.performance
                    new_performance = agent.performance * .10
                    agent.performance = old_performance - new_performance
                    print("Agent {} encountered an enemy at location {} and lost {} performance points. Remaining performance: {}.".format(agent, enemy[0], old_performance, agent.performance))
        if agent.performance <= 0:
            agent.alive = False
            print("Agent {} has run out of performance and is dead.".format(agent))

    def get_random_empty_location(self) -> tuple[int, int] | None:
        if self.maze is None:
            return None
        n = len(self.maze)
        while True:
            x, y = (random.randint(0, n-1), random.randint(0, n-1))
            if self.maze.get(x, y) == MazeComponents.PATH.value:
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

    def add_agent(self, agent: SatelliteAgent) -> None:
        self.agents.append(agent)

    def show_graph(self, filename:str="AsteroidMaze.html"):
        from pyvis.network import Network
        from src.maze2025GraphClass import mazeGraph
        from src.mazeData import mazeStatesLocations
        from src.mazeData import intTupleTostr

        # Convert maze data to more usable graph
        maze_actions = self.defineMazeActions()
        maze_transformation = self.makeMazeTransformationModel(maze_actions)

        mazePossibleActs = {}
        for state, value in maze_actions.items():
            key = self.possible_actions_from_state(state)
            for i, j in key.items():
                mazePossibleActs[i] = j

        maze1TM = {}
        maze1TM = self.makeMazeTransformationModel(mazePossibleActs)
        mazeWorldGraph = mazeGraph(maze1TM, mazeStatesLocations(list(maze1TM.keys())))

        net_maze = Network( heading="Lab4. Examples of Maze World Problem",
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%") # do this
        nodeColors={
            "start":"green",
            "goal":"red",
            "agent1":"orange",
            "agent2":"purple",
            "both":"pink",
            "enemy":"blue",
            "asteroid":"grey",
            "path": "white"
        }
        nodeColorsList=[]
        for node in mazeWorldGraph.origin.keys():
            node_value = self.maze.get(node[0], node[1])
            if node == self.agents[0].state and node == self.agents[1].state:
                nodeColorsList.append(nodeColors["both"])
            elif node == self.agents[0].state:
                nodeColorsList.append(nodeColors["agent1"])
            elif node == self.agents[1].state:
                nodeColorsList.append(nodeColors["agent2"])
            elif node == self.initial_location:
                nodeColorsList.append(nodeColors["start"])
            elif node == self.goal_location:
                nodeColorsList.append(nodeColors["goal"])
            elif node_value == MazeComponents.ENEMIES.value:
                nodeColorsList.append(nodeColors["enemy"])
            elif node_value == MazeComponents.ASTEROID.value:
                nodeColorsList.append(nodeColors["asteroid"])
            else:
                nodeColorsList.append(nodeColors["path"])

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
                if (intTupleTostr(node_source),intTupleTostr(node_target)) not in edges and (intTupleTostr(node_target), intTupleTostr(node_source)):
                    net_maze.add_edge(intTupleTostr(node_source),intTupleTostr(node_target), label=edge_weights[(intTupleTostr(node_source),intTupleTostr(node_target))])
                    edges.append((intTupleTostr(node_source),intTupleTostr(node_target)))
        net_maze.toggle_physics(False)
        net_maze.save_graph(filename)

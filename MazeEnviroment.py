from data.mazeData import mazeData, mazeLocations
from src.graphClass import Graph
from src.problemClass import Problem
import random

class MazeEnviroment():
    def __init__(self, agent=None):
        self.data = mazeData
        self.treasure_nodes = self.populate_treasure()
        self.directions = ["north", "east", "south", "west"]
        self.facing = self.directions[1]  # initially facing east
        self.captured_treasure = False
        self.agent = agent
        self.current_state = "start"
        self.goal = "treasure"
        self.is_dead = False
        self.is_done = False

    def populate_treasure(self) -> list:
        treasure_nodes = {"gold": None, "diamond": None, "pizza": None, "20 points": None}
        possible_treasure_nodes = list(self.data.keys())
        possible_treasure_nodes.remove("start")
        possible_treasure_nodes.remove("end")

        for treasure in treasure_nodes.keys():
            node = random.choice(possible_treasure_nodes)
            treasure_nodes[treasure] = node
            possible_treasure_nodes.remove(node)

        return treasure_nodes

    def actions(self, state):
        # if not facing a next node, can't advance
        my_node = self.mazeGraph.get(state)
        for direction, next_node in my_node:
            # forward
            if direction == self.facing.lower() and next_node is not None:
                yield Actions.Advance
            # left
            if direction == self.directions[(self.directions.index(self.facing) - 1) % 4]:
                yield Actions.Left
            # right
            if direction == self.directions[(self.directions.index(self.facing) + 1) % 4]:
                yield Actions.Right
            
    
    def step(self):
        self.goal_test(self.current_state)
        if self.is_done == False and self.is_dead == False:
            # we can assume only one agent in a maze at a time
            action = self.agent.decide(self.data, self.current_state, self.facing, self.captured_treasure, self.treasure_nodes, self.goal)
            print(f"Agent decided to do {action}.")

            self.execute_action(self.agent, action, self.current_state)
            print(f"Agent is now at {self.current_state}, facing {self.facing}, has_treasure {self.captured_treasure}, goal {self.goal}")
        else:
            print("Agent has either reached the goal or is dead.")

    def execute_action(self, agent, action, state):
        my_node = self.data[state]
        for direction, next_node in my_node:
            if action == Actions.Advance and direction == self.facing:
                self.current_state = next_node
                break

            elif action == Actions.Left and direction == self.directions[(self.directions.index(self.facing) - 1 + 4) % 4]:
                self.current_state = next_node
                self.facing = self.directions[(self.directions.index(self.facing) - 1 + 4) % 4]
                break

            elif action == Actions.Right and direction == self.directions[(self.directions.index(self.facing) + 1 + 4) % 4]:
                self.current_state = next_node
                self.facing = self.directions[(self.directions.index(self.facing) + 1 + 4) % 4]
                break

        # if in a dead end, turn around
        if len(self.data[self.current_state]) == 1:
            print("Agent has reached a dead end")
            self.facing = self.directions[(self.directions.index(self.facing) + 2 + 4) % 4]

        # check if we are on a treasure node
        if self.current_state in self.treasure_nodes.values():
            self.captured_treasure = True
            self.goal = "end"
            print("Agent has captured the treasure!")


        agent.performance -= 1
        if agent.performance <= 0:
            agent.is_dead = True
            print("Agent is out of performance points and is dead.")

    def goal_test(self, state):
        if state == self.goal and self.captured_treasure:
            self.is_done = True

    def show_graph(self, filename="mazeGraph.html"):
        from pyvis.network import Network

        # convert maze data to more usabe graph
        graph_data = {}
        for node, edges in self.data.items():
            graph_data[node] = {}
            for direction, destinaton in edges:
                graph_data[node][destinaton] = ""
            

        self.mazeGraph = Graph(graph_data)

        net = Network( 
            bgcolor ="#242020",
            font_color = "white",
            height = "750px",
            width = "100%"
        )

        for node in self.mazeGraph.nodes():

            net.add_node(node, label=node, x=mazeLocations[node]["x"], y=mazeLocations[node]["y"], physics=False)
                    
        nodeColors = {
            "start": "green",
            "end": "red",
            "deadend": "gray",
            "path": "blue",
            "treasure": "gold",
            "agent": "orange"
        }

        for node in self.mazeGraph.nodes():
            if node == self.current_state:
                net.get_node(node)["color"] = nodeColors["agent"]
            elif node == "start":
                net.get_node(node)["color"] = nodeColors["start"]
            elif node == "end":
                net.get_node(node)["color"] = nodeColors["end"]
            elif node in self.treasure_nodes.values():
                net.get_node(node)["color"] = nodeColors["treasure"]
            elif len(self.mazeGraph.get(node)) == 1:
                net.get_node(node)["color"] = nodeColors["deadend"]
            else:
                net.get_node(node)["color"] = nodeColors["path"]

        edges=[]
        edges_labels=[]

        for node_source in self.mazeGraph.nodes():
            for node_target, dist in self.mazeGraph.get(node_source).items():
                if set((node_source,node_target)) not in edges:
                    net.add_edge(node_source,node_target, label=str(dist))
                    edges.append(set((node_source,node_target)))
                    edges_labels.append(str(dist))

        net.save_graph(filename)

from enum import Enum
class Actions(Enum):
    Advance = 1
    Left = 2
    Right = 3
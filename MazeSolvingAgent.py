from src.agentClass import Agent
from MazeEnviroment import MazeEnviroment, Actions
from queue import PriorityQueue
from src.nodeClass import Node
import random

class MazeSolvingAgent(Agent):
    def __init__(self):
        super().__init__(program=self.decide)
        self.performance = 1000000000
        self.goal = ""
        self.plan = []

    def make_plan(self, map, start, goal):
        node = Node(start)
        frontier = PriorityQueue()
        frontier.put((1, node))

        reached = {start: node}
        while len(frontier.queue) > 0:
            node = frontier.get()[1]

            if node.state == goal:
                return node.solution()

            for child in map[node.state]:
                if child[1] not in reached:
                    frontier.put((1, Node(child[1], node, child[0], 0)))
                    reached.update({child[1]: child})

    def translate_plan_to_directions(self, plan, facing):
        facing_directions = ["north", "east", "south", "west"]
        curr_facing = facing
        diretional_plan = []
        for direction in plan:
            diff = (facing_directions.index(direction) - facing_directions.index(curr_facing))
            if diff == 0:
                diretional_plan.append(Actions.Advance)
            elif diff == 1 or diff == -3:
                diretional_plan.append(Actions.Right)
                curr_facing = facing_directions[(facing_directions.index(curr_facing) + 1) % 4]
            elif diff == -1 or diff == 3:
                diretional_plan.append(Actions.Left)
                curr_facing = facing_directions[(facing_directions.index(curr_facing) - 1) % 4]
            else:
                print("Bad direction change")
                print(diff)
                diretional_plan.append(None)

        print(plan)
        print(diretional_plan)
        return diretional_plan

    def decide(self, map, state, facing, has_treasure, treasure_nodes, goal):

        print(f"Plan {self.plan}, state {state}, facing {facing}, has_treasure {has_treasure}, goal {goal}")
            
        if len(self.plan) > 0:
            print(self.plan, state, facing, has_treasure, self.goal)
            return self.plan.pop(0)

        else:
            if self.goal != "treasure" and has_treasure == False:
                self.goal = "treasure"
                plans = []
                for treasure in treasure_nodes.values():
                    plans.append(self.make_plan(map, state, treasure))
                self.plan = self.translate_plan_to_directions(min(plans, key=len), facing)

            elif self.goal != "end" and has_treasure == True:
                self.goal = "end"
                self.plan = self.translate_plan_to_directions(self.make_plan(map, state, "end"), facing)
            else:
                self.plan = self.translate_plan_to_directions(self.make_plan(map, state, self.goal), facing)
        
        return self.plan.pop(0)
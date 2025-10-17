from asteroidEnvironment import AstroidMazeAction
from SatelliteAgent import SatelliteAgent
from asteroidMazeProblem import AsteroidMazeProblem
from src.nodeClass import Node
from typing import Literal
from queue import PriorityQueue

class SatelliteAgentUniformCostSearch(SatelliteAgent):
    def __init__(self, problem: AsteroidMazeProblem, initial_performance: float) -> None:
        super().__init__(problem, initial_performance)

    def __repr__(self) -> str:
        return super().__repr__()

    def make_plan(self) -> list[AstroidMazeAction]:
        # Best first search implementation on uniform cost
        # problem.path_cost is used to determine the cost of each action
        frontier: PriorityQueue[tuple[float, Node]] = PriorityQueue()
        start_node = Node(self.problem.initial)
        frontier.put((0, start_node))
        explored: set[tuple[int, int]] = set()

        while not frontier.empty():
            _, current_node = frontier.get()

            if self.problem.goal_test(current_node.state):
                return current_node.solution()

            explored.add(current_node.state)

            for action in self.problem.actions(current_node.state) or []:
                child_state = self.problem.result(current_node.state, action)
                if child_state is None:
                    continue
                child_node = Node(child_state, current_node, action,
                                  self.problem.path_cost(current_node.path_cost, current_node.state, action, child_state))

                if child_state not in explored and all(child_state != n.state for _, n in frontier.queue):
                    frontier.put((child_node.path_cost, child_node))
                elif any(child_state == n.state and child_node.path_cost < n.path_cost for _, n in frontier.queue):
                    # Replace the node in the frontier with the new lower-cost node
                    frontier.queue = [(cost, n) for cost, n in frontier.queue if n.state != child_state]
                    frontier.put((child_node.path_cost, child_node))
        self.status = "Stuck"
        return []
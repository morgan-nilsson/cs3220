from asteroidEnvironment import AstroidMazeAction
from src.problemClass import Problem
from SatelliteAgent import SatelliteAgent
from asteroidMazeProblem import AsteroidMazeProblem
from src.nodeClass import Node
from typing import Literal

class SatelliteAgentIterativeDeepeningSearch(SatelliteAgent):
    def __init__(self, problem, initial_performance: float):
        super().__init__(problem, initial_performance)

    def __repr__(self) -> str:
        return super().__repr__()

    def make_plan(self) -> list[AstroidMazeAction]:
        depth = 1
        while True:
            result = self.depth_limited_search(self.problem, depth)
            if result == "fail":
                print("No solution found.")
                self.status = "Stuck"
                return []
            if result != 'cutoff':
                return result
            depth += 1

    def depth_limited_search(self, problem: AsteroidMazeProblem, limit: int):

        visited: set[tuple[int, int]] = set()

        def recursive_dls(node: Node, problem: AsteroidMazeProblem, limit: int):
            cutoff_occurred = False
            visited.add(node.state)

            if problem.goal_test(node.state) == True:
                return node.solution()

            elif limit == 0:
                return 'cutoff'

            else:
                actions = problem.actions(node.state) or []
                for action in actions:

                    new_coords = problem.result(node.state, action)
                    # print(f"Exploring action {action} from state {node.state} new coords {new_coords} at depth {node.depth}")
                    if new_coords is None:
                        continue

                    if new_coords in visited:
                        continue

                    result = recursive_dls(Node(new_coords, node, action, node.path_cost + 1), problem, limit - 1)
                    if result == 'cutoff':
                        cutoff_occurred = True

                    elif result != "fail":
                        return result

            if cutoff_occurred:
                return 'cutoff'

            else:
                return "fail"

        return recursive_dls(Node(problem.initial), problem, limit)
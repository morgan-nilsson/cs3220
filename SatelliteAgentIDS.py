from asteroidEnvironment import AstroidMazeAction
from src.problemClass import Problem
from SatelliteAgent import SatelliteAgent
from asteroidMazeProblem import AsteroidMazeProblem
from src.nodeClass import Node
from typing import Literal, cast

class SatelliteAgentIterativeDeepeningSearch(SatelliteAgent):
    def __init__(self, problem, initial_performance: float):
        super().__init__(problem, initial_performance)

    def make_plan(self) -> list[AstroidMazeAction | None]:
        depth = 0
        while True:
            result = self.depth_limited_search(self.problem, depth)
            if result != 'cutoff':
                if result is None:
                    raise Exception("No solution found")
                if result is not None:
                    r = list(map(lambda node: cast(AstroidMazeAction | None, node.action), result))
                    return r
            depth += 1

    def depth_limited_search(self, problem: AsteroidMazeProblem, limit: int):

        def recursive_dls(node: Node, problem: AsteroidMazeProblem, limit: int) -> list[Node] | None | Literal['cutoff']:
            cutoff_occurred = False
            if problem.goal_test(node.state):
                print(f"Goal test passed at state {node.state} at depth {node.depth}")
                return node.solution()
            elif limit == 0:
                return 'cutoff'
            else:
                for action in problem.actions(node.state) or []:
                    print(f"Exploring action {action} from state {node.state} at depth {node.depth}")
                    result = recursive_dls(Node(problem.result(node.state, action), node, action, 1), problem, limit - 1)
                    if result == 'cutoff':
                        cutoff_occurred = True
                    elif result is not None:
                        print(f"Goal found! Action sequence: {result}")
                        return result
            if cutoff_occurred:
                return 'cutoff'
            else:
                return None

        return recursive_dls(Node(problem.initial), problem, limit)
from src.problemClass import Problem
from pacmanEnvironment import PacManEnvironment, PacManAction
from numpy import matrix

class PacManProblem(Problem):
    def __init__(self, initial: tuple[int, int], environment: PacManEnvironment, goal: tuple[int, int] | None = None):
        self.environment = environment
        self.initial: tuple[int, int] = initial
        self.goal = goal

    def actions(self, state: tuple[int, int]) -> list[PacManAction] | None:
        return self.environment.possible_actions_from_state(state).get(state)

    def result(self, state: tuple[int, int], action: PacManAction):
        x, y = state
        if action == PacManAction.UP.value:
            return (x, y - 1)
        elif action == PacManAction.DOWN.value:
            return (x, y + 1)
        elif action == PacManAction.LEFT.value:
            return (x - 1, y)
        elif action == PacManAction.RIGHT.value:
            return (x + 1, y)
        else:
            raise ValueError(f"Action {action} is not recognized")

    def goal_test(self, state: tuple[int, int]) -> bool:
        return state == self.environment.goal_location

    def path_cost(self, c, state1, action: PacManAction, state2):
        if action in [PacManAction.LEFT.value, PacManAction.RIGHT.value]:
            return c + 2
        elif action == PacManAction.UP.value:
            return c + 4
        elif action == PacManAction.DOWN.value:
            return c + 1
        else:
            raise ValueError(f"Action {action} is not recognized")

    def heuristic_function(self, current_state: tuple[int, int], destination_state: tuple[int, int]) -> int:
        return self.environment.manhattan_distance(current_state, destination_state)
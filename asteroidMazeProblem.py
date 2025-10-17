from src.problemClass import Problem
from asteroidEnvironment import AsteroidEnvironment, AstroidMazeAction
from numpy import matrix

class AsteroidMazeProblem(Problem):
    def __init__(self, initial: tuple[int, int], environment: AsteroidEnvironment, goal: tuple[int, int] | None = None):
        self.environment = environment
        self.initial: tuple[int, int] = initial
        self.goal = goal

    def actions(self, state: tuple[int, int]) -> list[AstroidMazeAction] | None:
        return self.environment.possible_actions_from_state(state).get(state)

    def result(self, state: tuple[int, int], action: AstroidMazeAction):
        x, y = state
        if action == AstroidMazeAction.UP.value:
            return (x, y - 1)
        elif action == AstroidMazeAction.DOWN.value:
            return (x, y + 1)
        elif action == AstroidMazeAction.LEFT.value:
            return (x - 1, y)
        elif action == AstroidMazeAction.RIGHT.value:
            return (x + 1, y)
        else:
            raise ValueError(f"Action {action} is not recognized")

    def goal_test(self, state: tuple[int, int]) -> bool:
        return state == self.environment.goal_location

    def path_cost(self, c, state1, action: AstroidMazeAction, state2):
        if action in [AstroidMazeAction.LEFT.value, AstroidMazeAction.RIGHT.value]:
            return c + 2
        elif action == AstroidMazeAction.UP.value:
            return c + 4
        elif action == AstroidMazeAction.DOWN.value:
            return c + 1
        else:
            raise ValueError(f"Action {action} is not recognized")
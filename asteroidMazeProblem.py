from src.problemClass import Problem
from asteroidEnvironment import AsteroidEnvironment, AstroidMazeAction
from numpy import matrix

class AsteroidMazeProblem(Problem):
    def __init__(self, initial: tuple[int, int], environment: AsteroidEnvironment, goal: tuple[int, int] | None = None):
        self.environment = environment
        self.initial: tuple[int, int] = initial
        self.goal = goal

    def actions(self, state: tuple[int, int]) -> list[AstroidMazeAction] | None:
        set_of_actions = self.environment.defineMazeActions()
        return set_of_actions.get(state)

    def result(self, state: tuple[int, int], action: AstroidMazeAction) -> tuple[int, int]:
        # is valid action from current state
        possible_actions = self.environment.possible_actions_from_state(state)
        if possible_actions and action in possible_actions:
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
        else:
            raise ValueError(f"Action {action} is not valid from state {state}")

    def goal_test(self, state: tuple[int, int]) -> bool:
        return state == self.environment.goal_location

    def path_cost(self, c, state1, action, state2):
        return super().path_cost(c, state1, action, state2)
from src.problemClass import Problem
from asteroidEnvironment import AstroidMazeAction
from asteroidMazeProblem import AsteroidMazeProblem

class SatelliteAgent:
    def __init__(self, problem: AsteroidMazeProblem, initial_performance: float) -> None:
        self.problem = problem
        self.state = problem.initial
        self.alive = True
        self.performance = initial_performance
        self.plan: list[AstroidMazeAction | None] = []

    def pick_action(self) -> AstroidMazeAction | None:
        if not self.plan:
            self.plan.append(*self.make_plan())
        return self.plan.pop(0)

    def make_plan(self) -> list[AstroidMazeAction | None]:
        raise NotImplementedError("This method should be overridden by subclasses")
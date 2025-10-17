from src.problemClass import Problem
from asteroidEnvironment import AstroidMazeAction
from asteroidMazeProblem import AsteroidMazeProblem
from typing import Literal

class SatelliteAgent:
    def __init__(self, problem: AsteroidMazeProblem, initial_performance: float) -> None:
        self.problem = problem
        self.state = problem.initial
        self.status: Literal["Alive", "Dead", "Finished", "Stuck"] = "Alive"
        self.performance = initial_performance
        self.plan = []
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def pick_action(self) -> AstroidMazeAction:
        if not self.plan:
            self.plan += self.make_plan()
        # if still no plan there is likely no solution
        if not self.plan:
            self.alive = False
        return self.plan.pop(0)

    def make_plan(self) -> list[AstroidMazeAction]:
        raise NotImplementedError("This method should be overridden by subclasses")
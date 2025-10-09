from src.problemSolvingAgentProgramClass import SimpleProblemSolvingAgentProgram
from wolfProblem import WolfProblem, Actions, Character
 
class wolfProblemSolvingAgentClass(SimpleProblemSolvingAgentProgram):
    def __init__(self, initial_state=None, dataGraph=None, goal=None):
      super().__init__(initial_state)
      self.dataGraph=dataGraph
      self.goal=goal

    def update_state(self, state, percept):
        return percept

    def formulate_goal(self, state):
      if self.goal is not None:
        return self.goal
      else:
         print("No goal! can't work!")
         return None
    
    def formulate_problem(self, state, goal):
       problem = WolfProblem()
       return problem
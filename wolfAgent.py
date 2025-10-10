from src.problemSolvingAgentProgramClass import SimpleProblemSolvingAgentProgram
from src.PS_agentPrograms import BestFirstSearchAgentProgram
from wolfProblem import WolfProblem
 
class wolfProblemSolvingAgentClass(SimpleProblemSolvingAgentProgram):
    def __init__(self, initial_state=None, dataGraph=None, goal=None):
      super().__init__(initial_state)
      self.dataGraph=dataGraph
      self.goal=goal

    def update_state(self, state, percept):
        return percept

    def formulate_goal(self, state):
      # The goal is defined in the WolfProblem class
      # We can return None here since the problem already has the goal
      return None
    
    def formulate_problem(self, state, goal):
       problem = WolfProblem()
       return problem
    
    def search(self, problem):
        search_program = BestFirstSearchAgentProgram()
        result = search_program(problem)
        if result:
            return result.solution()
        return None
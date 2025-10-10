from wolfAgent import wolfProblemSolvingAgentClass

# Create the wolf problem solving agent
# The search method is now built into the agent class
agent = wolfProblemSolvingAgentClass()

# Test the agent
initial_state = None  # The agent will get the initial state from the problem
agent(initial_state)

# The agent stores the solution in self.seq
if agent.seq:
    print("Solution found!")
    print("Solution sequence:", agent.seq)
    print("Number of steps:", len(agent.seq))
else:
    print("No solution found")

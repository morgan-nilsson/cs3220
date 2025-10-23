from pacmanEnvironment import PacManEnvironment
from pacmanProblem import PacManProblem
from pacmanAgentAstar import PacManAgentAStar



if __name__ == "__main__":
    #create pacman environment of specified size
    n = 10
    environment = PacManEnvironment(n)

    if environment.initial_location is None:
        raise ValueError("Initial location is not defined in the environment.")

    problem = PacManProblem(environment.initial_location, environment)

    if environment.maze is None:
        raise ValueError("Maze is not defined in the environment.")
    agent = PacManAgentAStar(problem, initial_performance=50) #0.3 * environment.maze.N())

    environment.add_agent(agent)

    print("Initial Environment:\n", environment.maze)
    print("Initial Agent State: ", agent.state)
    print("Initial Agent Performance: ", agent.performance)
    print("Food at locations: ", environment.food_dot_locations)

    while not environment.is_done():
        print("Environment:\n", environment.maze)
        print("Agent State: ", agent.state)

        environment.step()

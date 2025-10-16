from asteroidEnvironment import AsteroidEnvironment
from SatelliteAgentIDS import SatelliteAgentIterativeDeepeningSearch
from asteroidMazeProblem import AsteroidMazeProblem

if __name__ == "__main__":
    # Create the asteroid environment with a specified size
    n = 7
    environment = AsteroidEnvironment(n)

    # Create the problem instance with the initial and goal locations
    if environment.initial_location is None or environment.goal_location is None:
        raise ValueError("Initial or goal location is not set in the environment.")
    problem = AsteroidMazeProblem(environment.initial_location, environment, environment.goal_location)

    # Create the agent
    agent = SatelliteAgentIterativeDeepeningSearch(problem, 1000)

    # add the agent to the environment
    environment.add_agent(agent)

    print(f"Initial Location: {environment.initial_location}")
    print(f"Goal Location: {environment.goal_location}")
    # Run the environment
    while not environment.is_done():
        print(environment.maze)
        print(f"Agent Location: {agent.state}")
        print(f"Agent Performance: {agent.performance}")
        environment.step()
from asteroidEnvironment import AsteroidEnvironment
from SatelliteAgentIDS import SatelliteAgentIterativeDeepeningSearch
from SatelliteAgentUcost import SatelliteAgentUniformCostSearch
from asteroidMazeProblem import AsteroidMazeProblem

if __name__ == "__main__":
    # Create the asteroid environment with a specified size
    n = 7
    environment = AsteroidEnvironment(n)

    # Create the problem instance with the initial and goal locations
    if environment.initial_location is None or environment.goal_location is None:
        raise ValueError("Initial or goal location is not set in the environment.")
    problem = AsteroidMazeProblem(environment.initial_location, environment, environment.goal_location)

    if environment.maze is None:
        raise ValueError("Maze has not been initialized in the environment.")

    # Create the agent
    agent_IDS = SatelliteAgentIterativeDeepeningSearch(problem, environment.maze.N() / 2)
    agent_UCost = SatelliteAgentUniformCostSearch(problem, environment.maze.N() / 2)

    # add the agent to the environment
    environment.add_agent(agent_IDS)
    environment.add_agent(agent_UCost)

    print(f"Initial Location: {environment.initial_location}")
    print(f"Goal Location: {environment.goal_location}")
    print(f"Initial Maze:\n{environment.maze}")
    # Run the environment
    while not environment.is_done():
        environment.step()

    print("The agents are done.")
    for agent in environment.agents:
        if agent.status == "Finished":
            print(f"Agent {agent} has reached the goal!")
        elif not agent.alive:
            print(f"Agent {agent} has died.")
        else:
            print(f"Agent {agent} is still alive but did not reach the goal.")
        print(f"Agent {agent} Final Location: {agent.state}")
        print(f"Agent {agent} Final Performance: {agent.performance}")

    best_agent = max(environment.agents, key=lambda a: a.performance)
    print(f"The best agent was {best_agent} with a performance of {best_agent.performance}.")
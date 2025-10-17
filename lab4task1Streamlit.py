import streamlit as st
from pyvis.network import Network
import os
import streamlit.components.v1 as components
from SatelliteAgentIDS import SatelliteAgentIterativeDeepeningSearch
from SatelliteAgentUcost import SatelliteAgentUniformCostSearch
from asteroidMazeProblem import AsteroidMazeProblem
from asteroidEnvironment import AsteroidEnvironment

if 'environment' not in st.session_state:
    n = 7
    environment = AsteroidEnvironment(n)
    problem = AsteroidMazeProblem(environment.initial_location, environment, environment.goal_location)
    agent_IDS = SatelliteAgentIterativeDeepeningSearch(problem, environment.maze.N() / 2)
    agent_UCost = SatelliteAgentUniformCostSearch(problem, environment.maze.N() / 2)
    environment.add_agent(agent_IDS)
    environment.add_agent(agent_UCost)
    st.session_state.environment = environment
    st.session_state.agent_IDS = agent_IDS
    st.session_state.agent_UCost = agent_UCost
else:
    environment = st.session_state.environment
    agent_IDS = st.session_state.agent_IDS
    agent_UCost = st.session_state.agent_UCost

st.set_page_config(layout="wide")
st.title("Asteroid Maze")

# Add reset button
if st.button("Reset Maze"):
    # Clear session state to start fresh
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if st.button("Step Maze"):
    environment.step()
    for agent in environment.agents:
        print(f"Agent {agent} is at {agent.state}")

# Create a container for the graph that will be updated
graph_container = st.container()

# Display the current state in the container
with graph_container:
    environment.show_graph("Streamlit_Maze.html")
    HTMLFile = open('Streamlit_Maze.html', 'r', encoding='utf-8')
    components.html(HTMLFile.read(), height=800, width=1000)

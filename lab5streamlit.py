import streamlit as st
from pyvis.network import Network
import os
import streamlit.components.v1 as components
from pacmanAgentAstar import PacManAgentAStar
from pacmanProblem import PacManProblem
from pacmanEnvironment import PacManEnvironment


if 'environment' not in st.session_state:
    n = 7
    environment = PacManEnvironment(n)
    problem = PacManProblem(environment.initial_location, environment, environment.goal_location)
    agent_Astar = PacManAgentAStar(problem, environment.maze.N() * 0.3)
    environment.add_agent(agent_Astar)
    st.session_state.environment = environment
    st.session_state.agent_Astar = agent_Astar
else:
    environment = st.session_state.environment
    agent_Astar = st.session_state.agent_Astar

st.set_page_config(layout="wide")
st.title("PacMan env")

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
    environment.show_graph("PacMan_StreamLit.html")
    HTMLFile = open('PacMan_StreamLit.html', 'r', encoding='utf-8')
    components.html(HTMLFile.read(), height=800, width=1000)

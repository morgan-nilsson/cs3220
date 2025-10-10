import streamlit as st
from pyvis.network import Network
import os
import streamlit.components.v1 as components
from MazeSolvingAgent import MazeSolvingAgent
from MazeEnviroment import MazeEnviroment

if 'ev' not in st.session_state:
    agent = MazeSolvingAgent()
    maze = MazeEnviroment(agent)
    st.session_state.ev = maze
else:
    maze = st.session_state.ev


st.set_page_config(layout="wide")
st.title("Network")

if st.button("Step Maze"):

    maze.step()

    net = maze.show_graph("pyvis_graph.html")

    HtmlFile = open('pyvis_graph.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=800, width=1000)


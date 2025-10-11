import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from wolfProblem import WolfProblem
from wolfStateSpace import get_valid_states, encode_state, make_wolf_world, wolfStatesLocations
from wolfAgent import wolfProblemSolvingAgentClass
from wolfGraph import wolfGraph

def create_graph():
    """Build the complete state space graph for the wolf problem"""
    states = get_valid_states()
    wolf_world = make_wolf_world(states)
    locations = wolfStatesLocations(states)
    return wolfGraph(wolf_world, locations)

def build_graph(graph_data, solution_path=None):
    """Build graph visualization"""
    net = Network(
        heading="Wolf Problem State Space",
        bgcolor="#222222",
        font_color="white",
        height="600px",
        width="100%",
        directed=True
    )
    
    # Add nodes with colors
    for node in graph_data.nodes():
        if node == "LLLL":
            color = "blue"  # Starting state
        elif node == "RRRR":
            color = "green"  # Goal state
        elif solution_path and node in solution_path:
            color = "yellow"  # States in solution path
        else:
            color = "white"  # Regular states
        
        net.add_node(node, color=color, label=node)
    
    # Connect states with edges representing possible transitions
    for source, targets in graph_data.graph_dict.items():
        for target in targets.keys():
            net.add_edge(source, target)
    
    net.save_graph('wolf_graph.html')
    
    with open('wolf_graph.html', 'r', encoding='utf-8') as f:
        return f.read()

def run_agent():
    """Run the agent and return solution"""

    agent = wolfProblemSolvingAgentClass()
    problem = WolfProblem()
    solution = agent.search(problem)
        
    if solution:
        # Trace the complete path from start to goal
        solution_states = ["LLLL"]  # Begin with initial state
        current_state = problem.initial
        for action in solution:
            current_state = problem.result(current_state, action)
            solution_states.append(encode_state(current_state))
        return solution, solution_states
    return None, None

def main():
    st.title("Wolf Problem - State Space View")
    
    # Create graph
    graph_data = create_graph()
    
    # Run agent button
    if st.button("Run Agent"):
        with st.spinner("Running agent..."):
            solution, solution_path = run_agent()
            
            if solution:
                st.success(f"Solution found in {len(solution)} steps!")
                
                # Show solution steps
                st.write("**Solution Sequence:**")
                for i, action in enumerate(solution):
                    st.write(f"Step {i+1}: {action}")
                
                # Show graph with solution
                html = build_graph(graph_data, solution_path)
                components.html(html, height=600)
            else:
                st.error("No solution found")
                # Show graph without solution
                html = build_graph(graph_data)
                components.html(html, height=600)
    else:
        # Show initial graph
        html = build_graph(graph_data)
        components.html(html, height=600)
    
    # Show basic info
    st.write(f"**Total States:** {len(graph_data.nodes())}")
    st.write("**Legend:** Blue=Start, Green=Goal, Yellow=Solution Path")

if __name__ == '__main__':
    main()
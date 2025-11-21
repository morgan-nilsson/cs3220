import streamlit as st
from pyvis.network import Network
import os
import streamlit.components.v1 as components

from src.algorithms import BacktrackStepper, backtracking_search

from seatingCSP import seatingCSP



def buildCSP():
    neighbors = "1: 2 6; 2: 3; 3: 4; 4: 5; 5: 6; 6: "
    variables = ['1', '2', '3', '4', '5', '6']
    domain = ['A', 'B', 'C', 'D', 'E', 'F']
    filled = {}

    def seating_constraint(X, x, Y, y):
        forbidden = {
            ('A', 'B'), ('B', 'A'),
            ('B', 'E'), ('E', 'B'),
            ('B', 'C'), ('C', 'B'),
        }
        
        return (x, y) not in forbidden
    constraint = seating_constraint
    
    CSP = seatingCSP(variables, neighbors, domain, filled, constraint)
    return CSP


def buildGraph(CSP, current_filled = None):
    nodes = CSP.variables
    net_sudoku = Network( heading="Lab7. Seating CSP",
                bgcolor ="#1C1919",
                font_color = "white",
                height = "750px",
                width = "100%",
                directed= False
            )
    

    nodeColors = {
        'A' : "red",
        'B' : "blue",
        'C' : 'green',
        'D' : 'yellow',
        'E' : 'orange',
        'F' : 'purple',
        'unfilled': 'gray'
    }

    sizes=[10]*len(nodes)

    x_coords = []
    y_coords = []

    for node in nodes:
        if node.lower()=="1":
            x_coords.append(0)
            y_coords.append(0)
        elif node.lower()=="2":
            x_coords.append(50)
            y_coords.append(50)
        elif node.lower()=="3":
            x_coords.append(50)
            y_coords.append(125)
        elif node.lower()=="4":
            x_coords.append(0)
            y_coords.append(175)
        elif node.lower()=="5":
            x_coords.append(-50)
            y_coords.append(125)
        elif node.lower()=="6":
            x_coords.append(-50)
            y_coords.append(50)


    for i, node in enumerate(nodes):
        node_domain = ""
        node_label = f"Seat: {i}"
        colorPicked = 'unfilled'
        for j in CSP.domains[node]:
            node_domain += " " + str(j)
        if current_filled and node in current_filled:
            colorPicked = current_filled[node]
            node_label += f"\nEmployee: {current_filled[node]}"

        net_sudoku.add_node(
            node, 
            color=nodeColors[colorPicked],
            label= node_label,
            title = node_domain,
            size=sizes[i], 
            x=x_coords[i], 
            y=y_coords[i]
        )
    

    for nodeFrom in CSP.neighbors.keys():
        for nodeTo in CSP.neighbors[nodeFrom]:
            net_sudoku.add_edge(nodeFrom, nodeTo, color="white")

    net_sudoku.toggle_physics(False)


    net_sudoku.save_graph('LAB7TASK1.html')
    HtmlFile = open(f'LAB7TASK1.html', 'r', encoding='utf-8')
    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height = 800,width=1500)


if 'CSP' not in st.session_state:
    CSP = buildCSP()
    st.session_state.CSP = CSP
    stepper = BacktrackStepper(CSP)
    st.session_state.stepper = stepper
else:
    CSP = st.session_state.CSP
    stepper = st.session_state.stepper


st.set_page_config(layout="wide")
st.title("LAB7 TASK1")


placeholder = st.empty()

step = st.button("Step Full Solution")
reset_clicked = st.button("Reset")
full_solution = st.button("Full solution")

if step:
    placeholder.empty()
    result = stepper.step()
    current_filled = result[1]
    print(current_filled)

    if(current_filled is not None and len(current_filled) <= len(CSP.domains)):
        with placeholder:
            buildGraph(CSP, current_filled)
    else:
        with placeholder:
            resultFull = backtracking_search(CSP)
            buildGraph(CSP, resultFull)


elif full_solution:
    placeholder.empty()
    resultFull = backtracking_search(CSP)
    with placeholder:
        buildGraph(CSP, resultFull)

elif reset_clicked:
    placeholder.empty()
    stepper = BacktrackStepper(CSP)
    st.session_state.stepper = stepper
    with placeholder:
        buildGraph(CSP)

else:
    # initial render
    with placeholder:
        buildGraph(CSP)
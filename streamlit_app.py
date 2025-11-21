from astSodokuCSP import AstSodokuCSP
from src.algorithms import backtracking_search, BacktrackStepper
from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components

def main():
    if 'CSP' not in st.session_state:
        CSP = buildCSP()
        CSP.AC3()
        st.session_state.CSP = CSP
        stepper = BacktrackStepper(CSP)
        st.session_state.stepper = stepper
        st.session_state.initial_render = True
        initial_render = True
    else:
        CSP = st.session_state.CSP
        stepper = st.session_state.stepper
        initial_render = st.session_state.initial_render

    st.set_page_config(layout="wide")
    st.title("LAB7 TASK2")

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
                build_visualization(CSP, current_filled)
        else:
            with placeholder:
                full_result = backtracking_search(CSP)
                build_visualization(CSP, full_result)

    if full_solution:
        placeholder.empty()
        resultFull = backtracking_search(CSP)
        with placeholder:
            build_visualization(CSP, resultFull)

    elif reset_clicked:
        placeholder.empty()
        stepper = BacktrackStepper(CSP)
        st.session_state.stepper = stepper
        with placeholder:
            build_visualization(CSP, {})

    # initial render
    elif initial_render:
        initial_render = False
        st.session_state.initial_render = initial_render
        with placeholder:
            build_visualization(CSP, {})

def buildCSP():
    initial = {
        "A2": 1, "A8": 6,
        "B1": 3, "B3": 9, "B7": 1, "B9": 5,
        "C2": 8, "C4": 3, "C6": 5, "C8": 7,
        "D3": 2, "D5": 7, "D7": 8,
        "E4": 6, "E6": 8,
        "F3": 8, "F5": 9, "F7": 2,
        "G2": 2, "G4": 4, "G6": 1, "G8": 9,
        "H1": 9, "H3": 4, "H7": 6, "H9": 1,
        "I2": 3, "I8": 8
    }

    astCSP = AstSodokuCSP(9, initial)
    return astCSP

def build_visualization(CSP, current_domain, filename="sudoku.html"):
    print(current_domain)
    network = Network(
        font_color = "white",
        height = "750px",
        width = "100%",
        directed= False
    )

    node_colors = {
        'given': '#4CAF50',      # Green for given numbers
        'filled': '#2196F3',     # Blue for filled numbers
        'empty': '#9E9E9E',      # Grey for empty cells
    }

    for var in CSP.variables:
        value = None
        if var in current_domain:
            domain_values = current_domain[var]
            if isinstance(domain_values, int):
                value = domain_values

        if var in CSP.domains and len(CSP.domains[var]) == 1:
            color = node_colors['given']
        elif value is not None:
            color = node_colors['filled']
        else:
            color = node_colors['empty']

        label = str(value) if value is not None else ""

        x = (int(var[1:]) - 1) * 80
        y = (ord(var[0]) - ord('A')) * 80

        network.add_node(
            var,
            label=label,
            color=color,
            shape="circle",
            x=x,
            y=y
        )

    network.toggle_physics(False)

    network.save_graph(filename)
    HtmlFile = open(filename, 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=800, width=800)


if __name__ == "__main__":
    main()   

import streamlit as st
import pandas as pd
from src.CompanyEnvironmentClass import CompanyEnvironment
from src.Task3YourClasses import Student, ITStaff, OfficeManager
from src.agents import ReflexAgentA2pro

# Initialize ce once per user session
if 'ce' not in st.session_state:
    ce = CompanyEnvironment()

    ce.add_thing(ITStaff())
    ce.add_thing(Student())
    ce.add_thing(OfficeManager())
    ce.add_thing(ReflexAgentA2pro())

    st.session_state.ce = ce
else:
    ce = st.session_state.ce

def render_enviroment_state(ce: CompanyEnvironment, actions: list[str] | None):
    enviroment = ["", "", "", ""]
    for thing in ce.things:
        room_index = ce.locations.index(thing.location)
        enviroment[room_index] = enviroment[room_index] + str(thing) + " "
    for agent in ce.agents:
        room_index = ce.locations.index(agent.location)
        enviroment[room_index] = enviroment[room_index] + str(agent) + " "
        if not agent.is_alive():
            enviroment[room_index] += "(dead) "

    if actions:
        st.text(f"Action taken: {actions[0]}")
        if ce.is_done():
            st.text("The environment is done. All agents are dead.")

    df = pd.DataFrame([enviroment], columns=[f"Location {i+1}" for i in range(len(ce.locations))])
    st.table(df)

def main():
    
    render_enviroment_state(ce, None)

    if st.button("Run Environment Step", disabled=ce.is_done()):
        actions = ce.step()
        render_enviroment_state(ce, actions)

if __name__ == '__main__':
    main()

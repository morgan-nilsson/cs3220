import streamlit as st
import pandas as pd
from src.agentCatClass import AgentCat
from src.catFriendlyHouseClass import Milk, Sausage
from src.catFriendlyHouseClass import CatFriendlyHouse

if 'ev' not in st.session_state:
    ev = CatFriendlyHouse()
    ev.add_thing(AgentCat())
    st.session_state.ev = ev
else:
    ev = st.session_state.ev

def render_enviroment_state(ev: CatFriendlyHouse, actions):
    enviroment = ["", ""]
    for room in ev.status:
        enviroment[ev.locations.index(room)] += str(ev.status[room]) + " "
    for agent in ev.agents:
        room_index = ev.locations.index(agent.location)
        enviroment[room_index] = enviroment[room_index] + str(agent) + "<pref:" + str(agent.performance) + "> "
        if not agent.is_alive():
            enviroment[room_index] += "(dead) "

    if actions:
        st.text(f"Action taken: {actions[0]}")
        if ev.is_done():
            st.text("The environment is done. All agents are dead.")

    df = pd.DataFrame([enviroment], columns=[f"Location {i+1}" for i in range(len(ev.locations))])
    st.table(df)

def main():
    
    render_enviroment_state(ev, None)

    if st.button("Run Environment Step"):
        actions = ev.step()
        render_enviroment_state(ev, actions)

if __name__ == '__main__':
    main()
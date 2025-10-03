import streamlit as st
import pandas as pd
from crazyHouseEnvironmentClass import crazyHouseEnvironment
from inheritedThingClass import Mouse, Milk, Dog
from src.agents import RandomCatAgent
from src.agentClass import Agent

if 'ev' not in st.session_state:
    ev = crazyHouseEnvironment()

    mouse = Mouse()
    milk = Milk()
    dog = Dog()
    cat = RandomCatAgent()

    ev.add_thing(mouse)
    ev.add_thing(milk)
    ev.add_thing(dog)
    ev.add_thing(cat)
    ev.correct_placments()
    st.session_state.ev = ev
else:
    ev = st.session_state.ev

def render_enviroment_state(ev, actions):
    enviroment = ["", "", "", "", ""]
    for room in ev.status:
        for thing in ev.status[room]:
            if isinstance(thing, Agent):
                enviroment[room] += "Cat "
                if thing.alive == False:
                    enviroment[room] += "(Asleep), "
                else:
                    enviroment[room] += f"(P:{thing.performance}), "
            else:
                enviroment[room] += str(thing) + ", "

    if actions:
        st.text(f"Action taken: {actions[0]}")
        if ev.is_done():
            st.text("The environment is done. The cat is now asleep.")

    df = pd.DataFrame([enviroment], columns=[f"Location {i+1}" for i in range(len(ev.locations))])
    st.table(df)

def main():
    
    render_enviroment_state(ev, None)

    if st.button("Run Environment Step"):
        actions = ev.step()
        render_enviroment_state(ev, actions)

if __name__ == '__main__':
    main()
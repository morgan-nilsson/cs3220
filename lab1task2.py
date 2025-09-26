# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code
import pandas as pd
import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object

from src.DynastyClass import Dynasty
from src.GameOfThronesGraphClass import GameOfThronesGraph
import json
import matplotlib.pyplot as plt
import seaborn as sns

with open('data/game-of-thrones-characters-groups.json') as f:
    json_data = json.load(f)

corpusData = json_data["groups"]
GameOfThronesHouses = GameOfThronesGraph(corpusData)
    
# build graph
visualisationData={}
legendData=[]
for house in GameOfThronesHouses:
  visualisationData[house.name]=house.getStrength()
  legendData.append(house.name)

x = list(visualisationData.keys())
y = list(visualisationData.values())
    
ax = sns.barplot(x=x, y=y)
    
ax.legend(legendData)
sns.move_legend(ax, "upper left", bbox_to_anchor=(1.05, 1))
ax.set(
  xlabel = "Houses",
    ylabel = 'Strength (N family members)',
    title = 'Strength of GameOfThronesHouses'
)
    
plt.xticks(rotation=45)

g = nx.Graph()

# build network
N_houses = 0
colorKeys = []
for house in GameOfThronesHouses:
  if house.name != "Include":
    N_houses += 1
    colorKeys.append(house.name)
sns.color_palette("husl", N_houses)

nodeColors = dict(zip(colorKeys, [tuple(int(c * 255) for c in cs) for cs in sns.color_palette("husl", N_houses)]))
for house in GameOfThronesHouses:
    if house.name != "Include":
        g.add_node(house.name, size=house.getStrength())

for house in GameOfThronesHouses:
    if house.name != "Include":
        for ch in house:
            g.add_node(ch)

myEdges = []

for house in GameOfThronesHouses:
    if house.name != "Include":
        for ch in house:
            myEdges.append((ch, house.name))
            for ch2 in house:
                if ch2 != ch:
                    myEdges.append((ch2, ch))
g.add_edges_from(myEdges)

GameOfThronesNet = Network(
    bgcolor ="#242020",
    font_color = "white",
    height = "1000px",
    width = "100%",
    notebook=True,
    cdn_resources = "remote"
)

GameOfThronesNet.from_nx(g)

for node in GameOfThronesNet.nodes:
    if node["id"] in GameOfThronesHouses:
        node["color"] = '#%02x%02x%02x' % nodeColors[node["id"]]
    else:
        for house in GameOfThronesHouses:
            if house.name != "Include":
                if node["id"] in house:
                    node["color"] = '#%02x%02x%02x' % nodeColors[house.name]
# save graph in html file
GameOfThronesNet.save_graph('L1T2_network.html')

def main():
    st.title("Task2: infographic of relationships between characters in the Game of Thrones")
        
    selected = st.tabs(["Game Of Thrones Houses", "Members of Houses", "Graph for Game Of Thrones Houses"])

    with selected[0]:
        st.text("Game Of Thrones Houses:")
        for house in GameOfThronesHouses:
            st.markdown(f'- {house}: Strength {house.getStrength()}')

        st.pyplot(plt.gcf())
        
    with selected[1]:
        for house in GameOfThronesHouses:
            st.text(f'This is the house of {house.name}')
            for ch in house:
                st.markdown(f'- {ch}')
            st.text(f'We have {house.getStrength()} family members!!!')

    with selected[2]:
        st.subheader("Lab1. Task2.")
        HtmlFile = open('L1T2_network.html', 'r', encoding='utf-8')
        components.html(HtmlFile.read(), height=1200, width=1000)
        
if __name__ == '__main__':
    main()
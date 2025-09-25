# Import dependencies
import tempfile
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code
import pandas as pd
import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object

def load_data():
    """Load and return the game of thrones battles dataset"""
    try:
        data = pd.read_csv("data/game-of-thrones-battles.csv")
        return data
    except FileNotFoundError:
        st.error("Error: Could not find 'data/game-of-thrones-battles.csv'. Please ensure the file exists.")
        return None

def data_proc(data):
    """Process the battles data to extract relevant columns and clean it"""
    battles_df = data.loc[:, ['name', 'attacker_king', 'defender_king', 'attacker_size', 'defender_size']]
    battles_df_cleaned = battles_df.dropna()
    return battles_df_cleaned

def get_kings_info(battles_df_cleaned):
    """Extract information about attacking and defending kings"""
    attacker_king = battles_df_cleaned.attacker_king.unique()
    defender_king = battles_df_cleaned.defender_king.unique()
    kingList = set(attacker_king) | set(defender_king)
    return kingList

def join_battle(x):
    """Helper function to join battle names"""
    return ', '.join(x)

def create_network_graph(battles_df_cleaned):

    # Instantiate a Network object from pyvis.network.
    net5kings = Network(
    bgcolor ="#242020",
    font_color = "white",
    height = "1000px",
    width = "100%",
    directed = True, # we have directed graph
    notebook = True,
    cdn_resources = "remote")   # do this

    # Define nodes - the list of unique names of all kings
    kingList = get_kings_info(battles_df_cleaned)

    # Add nodes to the graph. Output them via netkings.nodes after that.
    net5kings.add_nodes(kingList)

    # Calculate edge data (battles between kings)
    full_edges = (battles_df_cleaned.groupby(['attacker_king', 'defender_king']).agg(
        n_battles=('name', 'count'),
        title=('name', join_battle)
    )).reset_index()

    # Add edges with their weights to the net5kings (via .add_edge) and output results as follows:
    for index, row in full_edges.iterrows():
        net5kings.add_edge(row['attacker_king'], row['defender_king'],value=row['n_battles'], title=row['title'])
    
    # Calculate node values and colors based on number of enemies attacked
    enemies_map = net5kings.get_adj_list()

    # Use the following color dictionary to assign a color to a node according to its value (specified earlier):
    nodeColors={
        0:"blue",
        1: "green",
        2: "orange",
        3: "purple",
        4: "gold",
        5:"red"
    }

    # Assign values and color to nodes. Output results via net5kings.nodes
    for node in net5kings.nodes:
        king_name = node['id']
        enemies = enemies_map.get(king_name, [])
        N = len(set(enemies)) + 1
        node['value'] = N
        node['color'] = nodeColors[node['value']]
    
    net5kings.save_graph('Jehads_lab1Task1_net5kings_streamlit.html')
    st.header("Network Visualization")
    HtmlFile = open(f'Jehads_lab1Task1_net5kings_streamlit.html', 'r', encoding='utf-8')
    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height = 1200,width=1000)
def main():
    #set the title
    st.title("Game of Thrones - War of the Five Kings Battle Network")

    # Load
    data = load_data()

    # Process data
    battles_df_cleaned = data_proc(data)
    create_network_graph(battles_df_cleaned)




if __name__ == '__main__':
    main()
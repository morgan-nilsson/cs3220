from astSodokuCSP import AstSodokuCSP

def main():

    initial = {
        "A2": 1,
        "A8": 6,
        "B1": 3,
        "B3": 9,
        "B7": 1,
        "B9": 5,
        "C2": 8,
        "C4": 3,
        "C6": 5,
        "C8": 7,
        "D3": 2,
        "D5": 7,
        "D7": 8,
        "E4": 6,
        "E6": 8,
        "F3": 8,
        "F5": 9,
        "F7": 2,
        "G2": 2,
        "G4": 4,
        "G5": 1,
        "G8": 9,
        "H1": 9,
        "H3": 4,
        "H7": 6,
        "H9": 1,
        "I2": 3,
        "I8": 8
    }

    astCSP = AstSodokuCSP(9, initial)

    # initial = {
    #     "A1": 3,
    #     "A2": 2,
    #     "B1": 1,
    # }
    # astCSP = AstSodokuCSP(3, initial)

    build_pyvis_from_domain(astCSP.domains, astCSP.variables, astCSP.neighbors, "ast_sudoku_initial.html")
    build_pyvis_from_domain(astCSP.curr_domains, astCSP.variables, astCSP.neighbors, "ast_sudoku_ac3.html")

def build_pyvis_from_domain(domains, nodes, neighbors, outfile):
    from pyvis.network import Network

    net_sudoku = Network( heading="Lab6. Simple Sudoku constraints",
        bgcolor ="#242020",
        font_color = "white",
        height = "750px",
        width = "100%"
    )

    nodeColors = {
        "empty": "white",
        "filled": "yellow",
    }

    nodeColorsList=[]
    nodeTitles=[]

    for node in nodes:
        if len(domains[node])==1:
            nodeColorsList.append(nodeColors["filled"])
            nodeTitles.append(str(domains[node][0]))
        else:
            nodeColorsList.append(nodeColors["empty"])
            nodeTitles.append(str(domains[node]))

    sizes=[10]*len(nodes)
    nodes=list(nodes)

    x_coords = []
    y_coords = []

    for node in nodes:
        row = ord(node[0]) - ord('A')
        col = int(node[1:]) - 1
        x_coords.append(col * 100)
        y_coords.append(row * 100)

    net_sudoku.add_nodes(nodes, title=nodeTitles, color=nodeColorsList, size=sizes, x=x_coords, y=y_coords)

    for nodeFrom in neighbors.keys():
        for nodeTo in neighbors[nodeFrom]:
            if nodeFrom[0]==nodeTo[0]: # row const-s
                net_sudoku.add_edge(nodeFrom,nodeTo, color="red")
            elif nodeFrom[1]==nodeTo[1]: # col const-s
                net_sudoku.add_edge(nodeFrom,nodeTo, color="blue")
            else:
                net_sudoku.add_edge(nodeFrom,nodeTo, color="green") # diag con-s
            
    net_sudoku.toggle_physics(False)
    net_sudoku.show(outfile, notebook=False)

if __name__ == "__main__":
    main()
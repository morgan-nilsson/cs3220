from astSodokuCSP import AstSodokuCSP
from src.algorithms import backtracking_search
from pyvis.network import Network

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
        "G6": 1,
        "G8": 9,
        "H1": 9,
        "H3": 4,
        "H7": 6,
        "H9": 1,
        "I2": 3,
        "I8": 8
    }

    astCSP = AstSodokuCSP(9, initial)

    astCSP.AC3()
    # csp.curr_domains is now AC3 reduced domains

    # initial = {
    #     "A1": 3,
    #     "A2": 2,
    #     "B1": 1,
    # }
    # astCSP = AstSodokuCSP(3, initial)
    # astCSP.AC3()
    result = backtracking_search(astCSP)
    print("Final Result:", result)

    build_visualization(result, "sudoku.html")

def build_visualization(result, filename="sudoku.html"):
    rows = "ABCDEFGHI"
    cols = "123456789"

    astroid_nodes = ['B5', 'C3', 'C7', 'E2', 'E5', 'E8', 'G3', 'G7', 'H5']

    net = Network(height="800px", width="800px", notebook=False, directed=False)

    net.toggle_physics(False)

    # Create nodes with fixed positions
    for r_i, r in enumerate(rows):
        for c_i, c in enumerate(cols):

            key = f"{r}{c}"
            value = result.get(key, 0)

            label = str(value) if value != 0 else ""

            node_id = key

            x = c_i * 80
            y = r_i * 80

            if key in astroid_nodes:
                color = "#ff4c4c"
            else:
                color = "#97c2fc"

            net.add_node(
                node_id,
                label=label,
                title=f"{key}: {label}",
                x=x,
                y=y,
                physics=False,
                color=color,
                shape="circle"
            )

    # Connect horizontal neighbors
    for r in rows:
        for c_i in range(8):
            a = f"{r}{cols[c_i]}"
            b = f"{r}{cols[c_i+1]}"
            net.add_edge(a, b, color="#cccccc")
    
    # Connect vertical neighbors
    for c in cols:
        for r_i in range(8):
            a = f"{rows[r_i]}{c}"
            b = f"{rows[r_i+1]}{c}"
            net.add_edge(a, b, color="#cccccc")

    net.show(filename, notebook=False)
    print(f"Sudoku visualization saved to {filename}")


if __name__ == "__main__":
    main()
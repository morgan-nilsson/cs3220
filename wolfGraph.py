from src.graphClass import Graph

class wolfGraph(Graph):
    def __init__(self, graph_dict=None):
        super().__init__(graph_dict)
    
    def make_graph(self):
        super().make_graph()

    def get(self, a, b=None):
        return super().get(a, b)
    
    def nodes(self):
        return super().nodes()

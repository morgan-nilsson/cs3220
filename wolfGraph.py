from src.graphClass import Graph

class wolfGraph(Graph):
    def __init__(self, graph_dict=None, locations=None):
        self.origin = graph_dict
        self.graph_dict = dict()

        #super().__init__(graph_dict)

        self.make_graph(graph_dict)
        self.locations = locations
    
    def make_graph(self, graph_dict):
        for a in graph_dict.keys():
            for (act, b) in graph_dict[a].items():
                self.connect(a, b, 1)                
    
    def connect(self, A, B, distance):
        self.graph_dict.setdefault(A, {})[B] = distance

    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)
    
    def getLocation(self,a):
        return self.locations.get(a)
    
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k for v in self.graph_dict.values() for k in v.keys()])
        nodes = s1.union(s2)
        return list(nodes)
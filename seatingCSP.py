from src.CSPclass import CSP
from src.utils import parse_neighbors

class seatingCSP(CSP):
    def __init__(self, varibles, neighbors, domain, filled, constraint):
        """
        Initialize CSP for exams.
        :param variables: list of course names
        :param domains: dict mapping each course to its possible days
        """

        self.variables = varibles
        self.domain = domain
        self.filled = filled
        self.neighbors = self.makeNeighbors(varibles, neighbors)
        self.domains = self.makeDomains(varibles, domain, filled)

        super().__init__(self.variables, self.domains, self.neighbors, constraint)

    
    def makeNeighbors(self, varibles, neighbors):
        """Each variable is a neighbor of every other."""
        Neighbors = {}
        n = parse_neighbors(neighbors)
        for i in varibles:
            Neighbors[i] = n[i]         
        return Neighbors
    
    def makeDomains(self, varibles, domain, filled):
        Domains = {}
        for i in varibles:
            if i in filled:
                Domains[i] = [filled[i]]
            else:
                Domains[i] = list(domain)
        return Domains
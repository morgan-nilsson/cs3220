from src.CSPclass import CSP
from src.utils import parse_neighbors

class examScheduleCSP(CSP):
    def __init__(self, varibles, neighbors, domain, filled, constraints):
        """
        Initialize CSP for exams.
        :param variables: list of course names
        :param domains: dict mapping each course to its possible days
        """

        self.variables = varibles
        self.domain = domain
        self.filled = filled
        self.constraints = constraints
        self.neighbors = self.makeNeighbors(varibles, neighbors)
        self.domains = self.makeDomains(varibles, domain, filled)

        super().__init__(self.variables, self.domains, self.neighbors, self.constraints)

    
    def makeNeighbors(self, varibles, neighbors):
        """Each variable is a neighbor of every other."""
        examNeighbors = {}
        n = parse_neighbors(neighbors)
        for i in varibles:
            examNeighbors[i] = n[i]         
        return examNeighbors
    
    def makeDomains(self, varibles, domain, filled):
        examDomains = {}
        for i in varibles:
            if i in filled:
                examDomains[i] = [filled[i]]
            else:
                examDomains[i] = list(domain)
        return examDomains
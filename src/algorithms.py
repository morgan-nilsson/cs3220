from queue import Queue
from copy import deepcopy

from src.utils import first

def AC3(csp):
  queue = Queue()
  
  print(f"Running AC3")
  for Xi in csp.variables:
    for Xk in csp.neighbors[Xi]:
      queue.put((Xi, Xk))
      #print((Xi, Xk), end=" ")
    #print()
   
  csp.support_pruning()
  checks = 0
  while list(queue.queue):
    (Xi, Xj) = queue.get()
    #print(f'Arc {(Xi, Xj)} is cheking')
    revised, checks = revise(csp, Xi, Xj, checks)
    if revised:
      if not csp.curr_domains[Xi]:
        return False, checks  # CSP is inconsistent
      for Xk in csp.neighbors[Xi]:
        if Xk != Xj:
          queue.put((Xk, Xi))
    #print(f"Queue: {list(queue.queue)}")

    '''print(f'Arc {(Xj, Xi)} is cheking')
    revised, checks1 = back_revise(csp, Xi, Xj, checks)
    if revised:
      if not csp.curr_domains[Xj]:
        return False, checks  # CSP is inconsistent
      for Xk in csp.neighbors[Xj]:
        if Xk != Xi:
          queue.add((Xk, Xj))'''

      
  return True, checks  # CSP is satisfiable


def revise(csp, Xi, Xj, checks=0):
    """Return true if we remove a value."""
    revised = False
    #print(f'Arc {(Xi, Xj)} is cheking')
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        #print(csp.curr_domains[Xj])
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x)
            print(f'The val {x} was deleted from {Xi} domain')
            revised = True
    return revised, checks


def back_revise(csp, Xi, Xj, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        conflict = False
        for y in csp.curr_domains[Xj]:
            conflict = False
            #print(y)
            if csp.constraints(Xi, x, Xj, y)==False:
              #print(x,y)
              conflict = True
            checks +=1
            '''if not conflict:
                break'''
            if conflict:
              csp.prune(Xj, y)
              print(f'The val {y} was deleted from {Xj} domain')
              #print(y)
              revised = True
    return revised, checks


# CSP Backtracking Search
# Variable ordering
def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    return first([var for var in csp.variables if var not in assignment])


# Value ordering
def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)


def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable, order_domain_values=unordered_domain_values):
    
    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment

        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if csp.nconflicts(var, value, assignment)==0:
                csp.assign(var, value, assignment)
                result = backtrack(assignment)
                if result is not None:
                  return result
                
            csp.unassign(var, assignment)
        return None

    result = backtrack({})
    return result


class BacktrackStepper:
    def __init__(self, cps, select_unassigned_variable=first_unassigned_variable, order_domain_values=unordered_domain_values) -> None:
        self.cps = cps
        self.select_unassigned_variable = select_unassigned_variable
        self.order_domain_values = order_domain_values
        self.backtrack_stack: list[dict[str, int]] = [{}]
        self.completed = False
  
    def step(self) -> tuple[dict | None, bool]:
        # print("Backtrack stack: ", self.backtrack_stack)

        if self.completed:
            return (self.backtrack_stack[-1], True)

        # get the current assignment stack
        assignment = self.backtrack_stack[-1]

        # check if the assignment is invalid
        for var in assignment:
            if self.cps.nconflicts(var, assignment[var], assignment) > 0:
                # backtrack
                self.backtrack_stack.pop()
                if not self.backtrack_stack:
                    return (None, True)
                return (self.backtrack_stack[-1], False)

        # check if assignment is complete
        if len(assignment) == len(self.cps.variables):
            self.completed = True
            return (assignment, False)
    
        # else push a set of new assignments to the stack
        self.backtrack_stack.pop()
        assigned = False
        var = self.select_unassigned_variable(assignment, self.cps)
        for value in self.order_domain_values(var, assignment, self.cps):
            copy = deepcopy(assignment)
            copy[var] = value
            self.backtrack_stack.append(copy)
            assigned = True

        # if we could not assign any value, backtrack
        if assigned == False:
            self.backtrack_stack.pop()
            if not self.backtrack_stack:
                return (None, True)
            return (self.backtrack_stack[-1], False)

        return (self.backtrack_stack[-1], False)

    def yield_steps(self):
        while not self.completed:
            yield self.step()
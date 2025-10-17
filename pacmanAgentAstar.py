from pacmanAgent import PacManAgent
from pacmanEnvironment import PacManAction
from src.nodeClass import Node

#lower f-score indicates that a node is closer to the goal state.
#expansion prioritized for nodes with lower f-score
#f(n) = actual cost g(n) + estimated cost h(n)

MAX_ITERATIONS = 1000000000

class PacManAgentAStar(PacManAgent):
    def make_plan(self) -> list[PacManAction]:
        all_locations = self.problem.environment.food_dot_locations
        if len(all_locations) == 0:
            all_locations = [self.problem.environment.goal_location]
        mapping = {}
        for location in all_locations:
            self.problem.goal = location
            mapping[location] = self.aStarPlan()


        min_index = 0
        for i in range(1, len(all_locations)):
            if len(mapping[all_locations[i]]) < len(mapping[all_locations[min_index]]):
                min_index = i

        self.problem.goal = all_locations[min_index]
        return mapping[all_locations[min_index]]

    def aStarPlan(self):

        seen_list: set[Node] = set() 

        def DFS_contour(node: Node, f_limit: int):
            if node.state in seen_list:
                return None, MAX_ITERATIONS

            if self.problem.goal == None:
                raise ValueError("Goal state is not defined in the problem.")

            f_cost = self.problem.heuristic_function(node.state, self.problem.goal) + node.path_cost
            if f_cost > f_limit:
                return None, f_cost

            seen_list.add(node)

            if self.problem.goal_test(node.state):
                return node, f_limit

            next_f = MAX_ITERATIONS

            successors = self.problem.actions(node.state)
            if successors == None:
                raise ValueError("No successors.")

            for s in successors:
                s_loc = self.problem.result(node.state, s)
               
                child_cost = self.problem.heuristic_function(node.state, s_loc) + f_cost
                solution, new_f = DFS_contour(Node(s_loc, node, s, child_cost), f_limit)

                if solution is not None:
                    return solution, f_limit

                next_f = min(next_f, new_f)

            return None, next_f

        root = Node(self.state, None, None, 0)
        f_limit = 0
        while True:
            solution, f_limit = DFS_contour(root, f_limit)
            if solution is not None:
                return solution.solution()
            if f_limit >= MAX_ITERATIONS:
                return "failure"
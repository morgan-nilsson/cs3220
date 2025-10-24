from pacmanAgent import PacManAgent
from pacmanEnvironment import PacManAction
from src.nodeClass import Node

#lower f-score indicates that a node is closer to the goal state.
#expansion prioritized for nodes with lower f-score
#f(n) = actual cost g(n) + estimated cost h(n)

MAX_ITERATIONS = 50

class PacManAgentAStar(PacManAgent):
    def make_plan(self) -> list[PacManAction]:
        all_locations = self.problem.environment.food_dot_locations
        if len(all_locations) == 0:
            all_locations = [self.problem.environment.goal_location]
        mapping = {}
        for location in all_locations:
            if location is None:
                continue
            plan = self.aStarPlan(location)
            if plan == "failure":
                mapping[location] = []
            else:
                mapping[location] = plan
        print("Mapping of locations to plans: ", mapping)


        min_index = 0
        for i in range(1, len(all_locations)):
            if mapping[all_locations[i]] == []:
                continue
            if len(mapping[all_locations[i]]) < len(mapping[all_locations[min_index]]):
                min_index = i

        self.problem.goal = all_locations[min_index]
        return mapping[all_locations[min_index]]

    
    def aStarPlan(self, goal: tuple[int, int]):

        def DFS_contour(node: Node, goal: tuple[int, int], f_limit: float):
            if goal is None:
                return None, float('inf')
            f_cost = self.problem.heuristic_function(node.state, goal) + node.path_cost

            next_f = float('inf')

            if f_cost > f_limit:
                return None, f_cost

            if goal == node.state:
                return node, f_cost

            actions = self.problem.actions(node.state)
            if actions is None:
                return None, float('inf')
            for action in actions:
                child_state = self.problem.result(node.state, action)
                child_cost = node.path_cost + self.problem.path_cost(node.path_cost, node.state, action, child_state)
                child_node = Node(child_state, node, action, child_cost)

                if any(n.state == child_state for n in seen_list):
                    index = seen_list.index(next(n for n in seen_list if n.state == child_state))
                    if seen_list[index].path_cost <= child_node.path_cost:
                        continue
                    else:
                        del seen_list[index]

                seen_list.append(child_node)

                solution, new_f = DFS_contour(child_node, goal, f_limit)

                if solution is not None:
                    return solution, f_limit

                next_f = min(next_f, new_f)

            return None, next_f

        root = Node(self.state, None, None, 0)
        f_limit = self.problem.heuristic_function(root.state, goal)

        while True:
            seen_list: list[Node] = [root]
            solution, new_limit = DFS_contour(root, goal, f_limit)

            if solution is not None:
                return solution.solution()  # Reconstructs the path

            if new_limit == float('inf'):
                return "failure"

            f_limit = new_limit

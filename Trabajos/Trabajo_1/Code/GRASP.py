import numpy as np
from collections import defaultdict
import random

class GRASP():
    def __init__(self, problem_information, dist_matrix, demands) -> None:
        print("GRASP")

        self.number_of_nodes        = problem_information[0]
        self.number_of_vehicles     = int(problem_information[1])
        self.capacity_of_vehicles   = problem_information[2]
        self.max_distance           = problem_information[3]

        self.dist_matrix            = dist_matrix
        self.demands                = demands

        self.visited_nodes          = defaultdict(lambda: False)

    def build_initial_solution(self):
        solution = [[] for _ in self.number_of_vehicles]

        number_missing_nodes = self.number_of_nodes
        missing_nodes = set(range(self.number_of_nodes))

        while missing_nodes > 0:
            vehicle = random.randint(0, self.number_of_vehicles - 1)

            sorted()

    def compute_cost(self, solution):
        ''''''

    def grasp(self, max_iterations, k):
        best_solution = None
        best_cost = float("inf")

        for i in range(max_iterations):
            solution = self.build_initial_solution()
            cost = self.compute_cost(solution)

            if cost < best_cost:
                best_solution = solution
                best_cost = cost

        return best_solution, best_cost





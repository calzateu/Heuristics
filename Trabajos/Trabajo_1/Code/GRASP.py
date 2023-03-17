import numpy as np
from collections import defaultdict
import random

class GRASP():
    def __init__(self, problem_information, dist_matrix, demands, max_iterations, k) -> None:
        print("GRASP")

        self.number_of_nodes        = int(problem_information[0])
        self.number_of_vehicles     = int(problem_information[1])
        self.capacity_of_vehicles   = problem_information[2]
        self.max_distance           = problem_information[3]

        self.dist_matrix            = dist_matrix
        self.demands                = demands

        self.visited_nodes          = defaultdict(lambda: False)

        self.max_iterations = max_iterations
        self.k = k

    def build_initial_solution(self):
        solution = [[0] for _ in range(self.number_of_vehicles)]

        missing_nodes = set(range(self.number_of_nodes))

        capacities = [self.capacity_of_vehicles]*self.number_of_vehicles

        while missing_nodes:
            vehicle = random.randint(0, self.number_of_vehicles - 1)

            distances = self.dist_matrix[solution[vehicle][-1]]
            max_distance = max(distances)

            metrics = [float('inf')]*len(distances)
            # for i in missing_nodes:
            #     metrics[i] = distances[i]/max_distance - (self.dist_matrix[i][0]/max_distance)*(capacities[vehicle]/self.capacity_of_vehicles)*(1 - capacities[vehicle]/self.capacity_of_vehicles)

            for i in missing_nodes:
                metrics[i] = distances[i]

            sorted_metrics = set(sorted(metrics)[:self.k])

            rcl = []
            for i in missing_nodes:
                if metrics[i] in sorted_metrics:
                    #print(i, metrics[i])
                    rcl.append(i)

            #print("rcl", rcl)
            next_node = random.choice(rcl)
            #print("next_node", next_node)
            solution[vehicle].append(next_node)

            missing_nodes.remove(next_node)

        for i in range(self.number_of_vehicles):
            if solution[i][-1] != 0:
                solution[i].append(0)

        return solution

    def __traveled_distance_and_capacity(self, path):
        distance = 0
        ocupation = 0
        res_ocupation = 1
        for i in range(len(path)-1):
            distance += self.dist_matrix[path[i], path[i+1]]

            if i == 0:
                if ocupation > self.capacity_of_vehicles:
                    res_ocupation = 0
                ocupation = 0
            else:
                ocupation += self.demands[i]

        if path[-1] == 0:
            if ocupation > self.capacity_of_vehicles:
                res_ocupation = 0
            ocupation = 0
        else:
            ocupation += self.demands[i]


        return distance, res_ocupation

    def __capacity(self, path):
        ocupation = 0
        for j in path:
            if j == 0:
                if ocupation > self.capacity_of_vehicles:
                    return 0
                ocupation = 0
            else:
                ocupation += self.demands[j]

        return 1

    def compute_cost(self, solution):
        cost = 0
        for path in solution:
            distance, res_ocupation = self.__traveled_distance_and_capacity(path)
            if distance > self.max_distance:
                cost += distance*3+ res_ocupation*distance*10
            else:
                cost += distance

        return cost

    def search_paths(self):
        best_solution = None
        best_cost = float("inf")

        for i in range(self.max_iterations):
            solution = self.build_initial_solution()
            #print("Solution", solution)
            cost = self.compute_cost(solution)

            if cost < best_cost:
                best_solution = solution
                best_cost = cost

            if i%100 == 0:
                print(i)

        return best_solution#, best_cost





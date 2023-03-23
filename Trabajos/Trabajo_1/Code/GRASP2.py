import numpy as np
from collections import defaultdict
import random

class GRASP2():
    def __init__(self, problem_information, dist_matrix, demands, **kwargs):# max_iterations, k) -> None:

        self.number_of_nodes        = int(problem_information[0])
        self.number_of_vehicles     = int(problem_information[1])
        self.capacity_of_vehicles   = problem_information[2]
        self.max_distance           = problem_information[3]

        self.dist_matrix            = dist_matrix
        self.demands                = demands

        self.visited_nodes          = defaultdict(lambda: False)

        self.max_iterations = kwargs["max_iterations"]
        self.k = kwargs["k"]

    def __order_vehicles(self, traveled_distances):
        indexed_numbers = [(index, number) for index, number in enumerate(traveled_distances)]
        sorted_indexed_numbers = sorted(indexed_numbers, key=lambda x: x[1])
        sorted_numbers = [number for _, number in sorted_indexed_numbers]
        indices = [index for index, _ in sorted_indexed_numbers]

        for i in range(len(sorted_numbers)):
            j = i + 1
            while j < len(sorted_numbers) and sorted_numbers[j] == sorted_numbers[i]:
                j += 1
            if j - i > 1:
                indices[i:j] = sorted(indices[i:j])

        return indices


    def __select_next_node(self, demands, distances, capacity, actual_node_vehicle, visited_nodes):
        next_node  = 0
        new_capacity = 0

        max_distance = max(distances)

        metrics = [float('inf')]*len(distances)

        candidates = []
        for i in range(len(demands)):
            if not visited_nodes[i] and capacity >= demands[i]:
                if i != actual_node_vehicle:
                    candidates.append(i)

        for i in candidates:
            metrics[i] = distances[i]

        # for i in candidates:
        #     metrics[i] = distances[i]/max_distance - (self.dist_matrix[i][0]/max_distance)*(capacity/self.capacity_of_vehicles)*(1 - capacity/self.capacity_of_vehicles)

        sorted_metrics = set(sorted(metrics)[:self.k])

        rcl = []
        for i in candidates:
            if not visited_nodes[i]:
                if metrics[i] in sorted_metrics:
                    rcl.append(i)

        candidates_copy = candidates.copy()
        if len(candidates_copy) > 0:
            for i in range(self.k - len(rcl) - 1):
                choise = random.choice(candidates_copy)
                candidates_copy.remove(choise)
                rcl.append(choise)

        if len(rcl) > 0:
            next_node = random.choice(rcl)
        elif len(candidates)>0:
            next_node = random.choice(candidates)

        if next_node != 0:
            new_capacity = capacity - demands[next_node]
        else:
            new_capacity = self.capacity_of_vehicles

        demands[next_node] = np.inf

        return next_node, new_capacity

    def build_initial_solution(self, demands):
        paths = []
        for i in range(int(self.number_of_vehicles)):
            paths.append([0])

        missing_nodes = self.number_of_nodes # Because the depot doesn't count
        actual_node_vehicles = [0]*self.number_of_vehicles
        capacities = [self.capacity_of_vehicles]*self.number_of_vehicles
        traveled_distances = [0]*self.number_of_vehicles

        visited_nodes = self.visited_nodes.copy()

        while missing_nodes > 0:
            for i in self.__order_vehicles(traveled_distances):     # Hacer un foreach ordenando el recorrido
                                                # de los vehículos de menor a mayor
                stop = False
                while not stop:
                    distances = self.dist_matrix[actual_node_vehicles[i]]

                    next_node, new_capacity = self.__select_next_node(
                            demands=demands,
                            distances=distances,
                            capacity=capacities[i],
                            actual_node_vehicle=actual_node_vehicles[i],
                            visited_nodes=visited_nodes
                    )

                    paths[i].append(next_node)

                    if next_node != 0:
                        visited_nodes[next_node] = True
                        missing_nodes -= 1
                    else:
                        stop = True

                    actual_node_vehicles[i] = next_node
                    capacities[i] = new_capacity
                    traveled_distances[i] += distances[next_node]


        for i in range(self.number_of_vehicles):
            if paths[i][-1] != 0:
                paths[i].append(0)

        return paths

    def __traveled_distance(self, path):
        distance = 0
        for i in range(len(path)-1):
            distance += self.dist_matrix[path[i], path[i+1]]

        return distance

    def compute_cost(self, solution):
        cost = 0
        for path in solution:
            distance = self.__traveled_distance(path)
            if distance > self.max_distance:
                cost += distance*10
            else:
                cost += distance

        return cost

    def search_paths(self):
        best_solution = None
        best_cost = float("inf")

        for i in range(self.max_iterations):
            solution = self.build_initial_solution(self.demands.copy())
            cost = self.compute_cost(solution)

            if cost < best_cost:
                best_solution = solution
                best_cost = cost

        return best_solution





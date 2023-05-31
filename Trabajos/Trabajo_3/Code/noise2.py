
import numpy as np
from collections import defaultdict

class Noise2():
    def __init__(self, utils, **kwargs) -> None:

        self.utils = utils

        self.std                    = kwargs["std"]
        self.max_iterations         = kwargs["max_iterations"]

        self.visited_nodes          = defaultdict(lambda: False)

    def __select_next_node(self, demands, visited_nodes, distances, capacity, actual_node_vehicle):
        next_node  = 0
        new_capacity = 0
        min_metric_node   = np.inf

        max_distance = max(distances)

        metrics = [0]*len(distances)
        random_numbers = np.random.uniform(-self.std, self.std, size=len(distances))
        for i in range(len(distances)):
            metrics[i] = distances[i]/max_distance - (self.utils.dist_matrix[i][0]/max_distance)*(capacity/self.utils.max_capacity) + random_numbers[i]

        for i in range(len(demands)):
            if not visited_nodes[i] and capacity >= demands[i]:
                if i != actual_node_vehicle and metrics[i] < min_metric_node:
                    min_metric_node = metrics[i]
                    next_node = i

        if next_node != 0:
            new_capacity = capacity - demands[next_node]
        else:
            new_capacity = self.utils.max_capacity

        demands[next_node] = np.inf

        return next_node, new_capacity

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

    def __traveled_distance(self, path):
        distance = 0
        for i in range(len(path)-1):
            distance += self.utils.dist_matrix[path[i], path[i+1]]

        return distance

    def compute_cost(self, solution):
        cost = 0
        for path in solution:
            cost += self.__traveled_distance(path)

        traveled_distances = self.utils.traveled_distances_vector(solution)
        cost += self.utils.distance_exceed(traveled_distances)*10

        return cost

    def build_solution(self, demands):
        paths = []
        for i in range(int(self.utils.num_vehicles)):
            paths.append([0])

        missing_nodes = self.utils.number_of_nodes # Because the depot doesn't count
        actual_node_vehicles = [0]*self.utils.num_vehicles
        capacities = [self.utils.max_capacity]*self.utils.num_vehicles
        traveled_distances = [0]*self.utils.num_vehicles

        visited_nodes = self.visited_nodes.copy()

        while missing_nodes > 0:
            for i in self.__order_vehicles(traveled_distances):     # Hacer un foreach ordenando el recorrido
                                                # de los vehículos de menor a mayor
                stop = False
                while not stop:
                    distances = self.utils.dist_matrix[actual_node_vehicles[i]]

                    next_node, new_capacity = self.__select_next_node(
                            demands=demands,
                            visited_nodes=visited_nodes,
                            distances=distances,
                            capacity=capacities[i],
                            actual_node_vehicle=actual_node_vehicles[i]
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

        for i in range(self.utils.num_vehicles):
            if paths[i][-1] != 0:
                paths[i].append(0)

        # for path in paths:
        #     for trip in path:
        #         while trip[-1] == 0 and trip[-2] == 0:
        #             trip.pop()

        return paths

    def search_paths(self, split=True):
        best_solution = None
        best_cost = float("inf")

        for i in range(self.max_iterations):
            solution = self.build_solution(self.utils.demands.copy())
            cost = self.compute_cost(solution)

            if cost < best_cost:
                best_solution = solution
                best_cost = cost

        return best_solution
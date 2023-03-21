
import numpy as np
from collections import defaultdict

class ConstructiveMethod2():
    def __init__(self, problem_information, dist_matrix, demands) -> None:
        print("Constructive")

        self.number_of_nodes        = problem_information[0]
        self.number_of_vehicles     = int(problem_information[1])
        self.capacity_of_vehicles   = problem_information[2]
        self.max_distance           = problem_information[3]

        self.dist_matrix            = dist_matrix
        self.demands                = demands

        self.visited_nodes          = defaultdict(lambda: False)

    def __select_next_node(self, demands, distances, capacity, actual_node_vehicle):
        next_node  = 0
        new_capacity = 0
        min_metric_node   = np.inf

        max_distance = max(distances)

        metrics = [0]*len(distances)
        for i in range(len(distances)):
            metrics[i] = distances[i]/max_distance - (self.dist_matrix[i][0]/max_distance)*(capacity/self.capacity_of_vehicles)*(1 - capacity/self.capacity_of_vehicles)

        for i in range(len(demands)):
            if not self.visited_nodes[i] and capacity >= demands[i]:
                if i != actual_node_vehicle and metrics[i] < min_metric_node:
                    min_metric_node = metrics[i]
                    next_node = i

        if next_node != 0:
            new_capacity = capacity - demands[next_node]
        else:
            new_capacity = self.capacity_of_vehicles

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


    def search_paths(self):
        paths = []
        for i in range(int(self.number_of_vehicles)):
            paths.append([0])

        missing_nodes = self.number_of_nodes # Because the depot doesn't count
        actual_node_vehicles = [0]*self.number_of_vehicles
        capacities = [self.capacity_of_vehicles]*self.number_of_vehicles
        traveled_distances = [0]*self.number_of_vehicles

        while missing_nodes > 0:
            for i in self.__order_vehicles(traveled_distances):     # Hacer un foreach ordenando el recorrido
                                                # de los vehículos de menor a mayor
                stop = False
                while not stop:
                    distances = self.dist_matrix[actual_node_vehicles[i]]

                    next_node, new_capacity = self.__select_next_node(
                            demands=self.demands,
                            distances=distances,
                            capacity=capacities[i],
                            actual_node_vehicle=actual_node_vehicles[i]
                    )

                    paths[i].append(next_node)

                    if next_node != 0:
                        self.visited_nodes[next_node] = True
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

import numpy as np
from collections import defaultdict

class ConstructiveMethod():
    def __init__(self, problem_information, dist_matrix, demands, alpha) -> None:
        print("Constructive")

        self.number_of_nodes        = problem_information[0]
        self.number_of_vehicles     = int(problem_information[1])
        self.capacity_of_vehicles   = problem_information[2]
        self.max_distance           = problem_information[3]

        self.dist_matrix            = dist_matrix
        self.demands                = demands
        self.alpha                  = alpha

        self.visited_nodes          = defaultdict(lambda: False)

    def __select_next_node(self, demands, distances, capacity, actual_node_vehicle):
        demands_copy = demands.copy()
        distances_copy = distances.copy()

        next_node  = 0
        new_capacity = 0
        min_metric_node   = np.inf

        max_demand = max(demands_copy)
        min_deman = min(demands_copy)
        max_distance = max(distances_copy)
        min_distance = min(distances_copy)

        demands_copy = list(map(lambda x: (x - min_deman)/(max_demand - min_deman), demands_copy))
        distances_copy = list(map(lambda x: (x - min_distance)/(max_distance - min_distance), distances_copy))

        metrics = list(
                map(lambda t: self.alpha*t[0] + (1-self.alpha)*t[1], zip(demands_copy, distances_copy))
        )

        for i in range(len(demands_copy)):
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

    def search_paths(self):
        paths = []
        for i in range(int(self.number_of_vehicles)):
            paths.append([0])

        missing_nodes = self.number_of_nodes # Because the depot doesn't count
        actual_node_vehicles = [0]*self.number_of_vehicles
        capacities = [self.capacity_of_vehicles]*self.number_of_vehicles

        while missing_nodes > 0:
            for i in range(self.number_of_vehicles):
                distances = self.dist_matrix[actual_node_vehicles[i]]

                next_node, new_capacity = self.__select_next_node(
                        demands=self.demands,
                        distances=distances,
                        capacity=capacities[i],
                        actual_node_vehicle=actual_node_vehicles[i]
                )

                if not (paths[i][-1] == 0 and next_node == 0):
                    paths[i].append(next_node)

                    if next_node != 0:
                        self.visited_nodes[next_node] = True
                        missing_nodes -= 1

                    actual_node_vehicles[i] = next_node
                    capacities[i] = new_capacity

        for i in range(self.number_of_vehicles):
            if paths[i][-1] != 0:
                paths[i].append(0)

        return paths
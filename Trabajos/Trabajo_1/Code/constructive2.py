
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
        # demands_copy = demands.copy()
        # distances_copy = distances.copy()

        next_node  = 0
        new_capacity = 0
        min_metric_node   = np.inf

        # max_demand = max(demands_copy)
        # min_deman = min(demands_copy)
        # max_distance = max(distances_copy)
        # min_distance = min(distances_copy)

        # demands_copy = list(map(lambda x: (x - min_deman)/(max_demand - min_deman), demands_copy))
        # distances_copy = list(map(lambda x: (x - min_distance)/(max_distance - min_distance), distances_copy))

        # metrics = list(
        #         map(lambda t: self.alpha*t[0] + (1-self.alpha)*t[1], zip(demands_copy, distances_copy))
        # )

        metrics = [0]*len(distances)
        for i in range(len(distances)):
            metrics[i] = distances[i] - (self.dist_matrix[i][0])*(capacity/self.capacity_of_vehicles)

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

    # def __order_vehicles(self, traveled_distances):
    #     ''''''
    #     dicc = dict()
    #     for index, num in enumerate(traveled_distances):
    #         dicc[num] = index

    #     print(traveled_distances)
    #     traveled_distances = sorted(traveled_distances)

    #     indices = [dicc[i] for i in traveled_distances]
    #     print(indices)
    #     return indices

    def __order_vehicles(self, traveled_distances):
        """
            Given a list of numbers, sorts the list and returns the original indices of the sorted numbers.

        Parameters:
        numbers (list of int or float): The list of numbers to sort.

        Returns:
        indices (list of int): The indices of the sorted numbers.
        sorted_numbers (list of int or float): The sorted list of numbers.
        """
        # Create a list of tuples, where each tuple contains the original index and the number at that index.
        indexed_numbers = [(index, number) for index, number in enumerate(traveled_distances)]

        # Sort the list of tuples by the number in each tuple.
        sorted_indexed_numbers = sorted(indexed_numbers, key=lambda x: x[1])

        # Create a list of the sorted numbers by extracting the number from each tuple.
        sorted_numbers = [number for _, number in sorted_indexed_numbers]

        # Create a list of the indices of the sorted numbers by extracting the index from each tuple.
        indices = [index for index, _ in sorted_indexed_numbers]

        # Handle ties by sorting the tied indices in ascending order.
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

                    #if not (paths[i][-1] == 0 and next_node == 0):
                    paths[i].append(next_node)

                    if next_node != 0:
                        self.visited_nodes[next_node] = True
                        missing_nodes -= 1
                    else:
                        stop = True
                        #print("Parar")

                    actual_node_vehicles[i] = next_node
                    capacities[i] = new_capacity
                    traveled_distances[i] += distances[next_node]

        for i in range(self.number_of_vehicles):
            if paths[i][-1] != 0:
                paths[i].append(0)

        return paths
# Used libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

import openpyxl

# My modules
from constructive import ConstructiveMethod
from constructive2 import ConstructiveMethod2
from GRASP import GRASP
from GRASP2 import GRASP2
from noise import Noise

class MainMethods():
    def __init__(self) -> None:
        self.__MAX_NUM_NODOS  = 201

    def read_data(self, file_name):
        nodes       = np.zeros((self.__MAX_NUM_NODOS , 4))

        cont = 0
        with open(file_name, 'r') as file:
            for line in file:
                line         = list(map(int, line.split()))
                nodes[cont]  = line
                cont         += 1

        self.problem_information = nodes[0]
        self.nodes  = nodes[1:cont]
        self.cont   = cont - 1

        return self.problem_information, self.nodes, self.cont

    def compute_distances(self):
        n = len(self.nodes)
        dist_matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(i+1, n):
                # Compute the Euclidean distance between nodes i and j
                x1, y1 = self.nodes[i][1], self.nodes[i][2]
                x2, y2 = self.nodes[j][1], self.nodes[j][2]
                dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

                # Update the distance matrix with the computed distance
                dist_matrix[i, j] = dist
                dist_matrix[j, i] = dist

        self.dist_matrix = dist_matrix

        return dist_matrix

    def __traveled_distance(self, path):
        distance = 0
        for i in range(len(path)-1):
            distance += self.dist_matrix[path[i], path[i+1]]

        return distance

    def __validate_solutions(self, paths, method, print_validation):
        total_distances_traveled = 0
        nodes_visited = 0

        for i in paths:
            ocupation = 0
            for j in i:
                if j == 0:
                    if ocupation > method.capacity_of_vehicles:
                        if print_validation:
                            print("Max capacity exceed", ocupation)
                            print(i)
                        break
                    ocupation = 0
                else:
                    ocupation += self.nodes[j, 3]

            distance = self.__traveled_distance(i)

            total_distances_traveled += distance
            nodes_visited += len(i)

            i.append(distance)

            if print_validation and distance > method.max_distance:
                        print("Max distance exceed", distance)
                        print(i)

            if distance > method.max_distance:
                i.append(1)
            else:
                i.append(0)

        if print_validation:
            print(paths)
            print("Total distance: ", total_distances_traveled)
            print("Num nodes visited", nodes_visited)

    def plot_routes(self, routes):
        plt.plot(self.nodes[0][1], self.nodes[0][2], "o")
        x = self.nodes[1:,1]
        y = self.nodes[1:,2]
        plt.plot(x, y, "o")

        for i in range(len(x)):
            plt.text(x[i], y[i]+0.5, '{}'.format(i+1))

        for i in range(len(routes)):
            x = self.nodes[routes[i], [1]*len(routes[i])]
            y = self.nodes[routes[i], [2]*len(routes[i])]
            plt.plot(x, y, label="Vehicle: " + str(i+1))

        plt.legend()

        plt.show()

    def save_solution(self, instances, name):
        # Create a new Excel workbook
        workbook = openpyxl.Workbook()

        # Loop through each instance and create a new worksheet for it
        for instance in instances:
            # Select the active worksheet
            worksheet = workbook.create_sheet(instance['name'])

            # Write the list of lists of nodes to the worksheet row by row
            for row in instance['nodes']:
                worksheet.append(row)

        # Save the workbook
        workbook.save(name)


    def run_method(self, method, verbose, print_validation):
        paths = method.search_paths()

        if verbose:
            self.plot_routes(paths)

        self.__validate_solutions(paths=paths, method=method, print_validation=print_validation)

        return paths

    def run_instances(self, Method, name, verbose, print_validation, **kwargs):
        folder_path = "/home/cristian/Descargas/Universidad/7_2023-1/Heuristica/Heuristics/Trabajos/Trabajo_1/mtVRP Instances"
        files = os.listdir(folder_path)
        files = sorted(files)

        instances = []
        for file in files:
            print(file)

            problem_information, nodes, cont = self.read_data(folder_path + "/" + file)
            dist_matrix = self.compute_distances()
            demands = nodes[:, 3].copy()

            method_instance = Method(problem_information, dist_matrix, demands, **kwargs)
            instances.append(
                {'name': file,
                 'nodes': self.run_method(method=method_instance, verbose=verbose, print_validation=print_validation)
                }
            )

        self.save_solution(instances=instances, name=name)


if __name__ == '__main__':

    run_individual_instance = False

    if run_individual_instance:
        file = '/home/cristian/Descargas/Universidad/7_2023-1/Heuristica/Heuristics/Trabajos/Trabajo_1/mtVRP Instances/mtVRP2.txt'
        exec = MainMethods()
        problem_information, nodes, cont = exec.read_data(file_name=file)
        dist_matrix = exec.compute_distances()

        demands = nodes[:, 3].copy()
        exec.run_method(method=ConstructiveMethod2(problem_information, dist_matrix, demands), verbose=True, print_validation=True)

        max_iterations = 1000
        k = 2
        demands = nodes[:, 3].copy()
        exec.run_method(method=GRASP2(problem_information, dist_matrix, demands, max_iterations=max_iterations, k=k), verbose=True, print_validation=True)

        std = 0.01
        max_iterations = 1000
        demands = nodes[:, 3].copy()
        exec.run_method(method=Noise(problem_information, dist_matrix, demands, std=std, max_iterations=max_iterations), verbose=True, print_validation=True)


    run_all_instances = True

    if run_all_instances:
        exec = MainMethods()

        exec.run_instances(Method=ConstructiveMethod2, name="mtVRP_Cristian_Alzate_Urrea_constructivo.xlsx", verbose=False, print_validation=False)

        max_iterations_GRASP = 100
        k = 2
        exec.run_instances(Method=GRASP2, name="mtVRP_Cristian_Alzate_Urrea_GRASP.xlsx", verbose=False, print_validation=False, max_iterations=max_iterations_GRASP, k=k)

        max_iterations_Noise = 100
        std = 0.01
        exec.run_instances(Method=Noise, name="mtVRP_Cristian_Alzate_Urrea_Noise.xlsx", verbose=False, print_validation=False, std=std, max_iterations=max_iterations_Noise)
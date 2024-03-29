# Used libraries
import numpy as np
import matplotlib.pyplot as plt
import os
import time


import openpyxl

# My modules
from constructive import ConstructiveMethod
from constructive1 import ConstructiveMethod1
from constructive2 import ConstructiveMethod2
from constructive3 import ConstructiveMethod3
from GRASP import GRASP
from GRASP2 import GRASP2
from GRASP3 import GRASP3
from noise import Noise
from noise2 import Noise2

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

    def __validate_solutions(self, paths, method, verbose):
        total_distances_traveled = 0
        feasible_path = 0
        nodes_visited = 0

        for i in paths:
            ocupation = 0
            for j in i:
                if j == 0:
                    if ocupation > method.capacity_of_vehicles:
                        if verbose:
                            print("Max capacity exceed", ocupation)
                            print(i)
                        break
                    ocupation = 0
                else:
                    ocupation += self.nodes[j, 3]

            distance = self.__traveled_distance(i)

            total_distances_traveled += distance
            nodes_visited += len(i)

            if verbose and distance > method.max_distance:
                        print("Max distance exceed", distance)
                        print(i)

            i.append(distance)

            if distance > method.max_distance:
                i.append(1)
                feasible_path = 1
            else:
                i.append(0)

        if verbose:
            print(paths)
            print("Total distance: ", total_distances_traveled)
            print("Num nodes visited", nodes_visited)

        return total_distances_traveled, feasible_path

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

        # Delete the default sheet (index 0)
        sheet_to_delete = workbook['Sheet']
        del workbook[sheet_to_delete.title]

        # Save the workbook
        workbook.save(name)


    def run_method(self, method, verbose=False, graph=False):
        start = time.time()
        paths = method.search_paths()
        end = time.time()
        total_time = end - start

        if graph:
            self.plot_routes(paths)

        total_distances_traveled, feasible_path = self.__validate_solutions(paths=paths, method=method, verbose=verbose)

        paths.append([total_distances_traveled, total_time, feasible_path])

        return paths

    def run_instances(self, Method, name, verbose=False, graph=False, **kwargs):
        folder_path = "../../mtVRP Instances"
        folder_path = os.path.abspath(folder_path)
        files = os.listdir(folder_path)
        files = sorted(files)

        instances = []
        for file in files:
            if verbose:
                print(file)

            problem_information, nodes, cont = self.read_data(folder_path + "/" + file)
            dist_matrix = self.compute_distances()
            demands = nodes[:, 3].copy()


            method_instance = Method(problem_information, dist_matrix, demands, **kwargs)
            instances.append(
                {'name': file,
                 'nodes': self.run_method(method=method_instance, verbose=verbose, graph=graph)
                }
            )

        self.save_solution(instances=instances, name=name)


if __name__ == '__main__':

    run_individual_instance = True

    if run_individual_instance:
        folder_path = "../../mtVRP Instances"
        folder_path = os.path.abspath(folder_path)
        file = folder_path + '/mtVRP7.txt'
        exec = MainMethods()
        problem_information, nodes, cont = exec.read_data(file_name=file)
        dist_matrix = exec.compute_distances()


        verbose=True
        graph=True

        demands = nodes[:, 3].copy()
        exec.run_method(method=ConstructiveMethod3(problem_information, dist_matrix, demands), verbose=verbose, graph=graph)

        max_iterations = 1000
        k = 2
        demands = nodes[:, 3].copy()
        exec.run_method(method=GRASP3(problem_information, dist_matrix, demands, max_iterations=max_iterations, k=k), verbose=verbose, graph=graph)

        std = 0.01
        max_iterations = 1000
        demands = nodes[:, 3].copy()
        exec.run_method(method=Noise2(problem_information, dist_matrix, demands, std=std, max_iterations=max_iterations), verbose=verbose, graph=graph)


    run_all_instances = False

    if run_all_instances:
        exec = MainMethods()

        verbose=False
        graph=False

        exec.run_instances(Method=ConstructiveMethod3, name="mtVRP_Cristian_Alzate_Urrea_constructivo2.xlsx", verbose=verbose, graph=graph)

        max_iterations_GRASP = 200
        k = 2
        exec.run_instances(Method=GRASP3, name="mtVRP_Cristian_Alzate_Urrea_GRASP2.xlsx", verbose=verbose, graph=graph,max_iterations=max_iterations_GRASP, k=k)

        max_iterations_Noise = 200
        std = 0.01
        exec.run_instances(Method=Noise2, name="mtVRP_Cristian_Alzate_Urrea_Noise2.xlsx", verbose=verbose, graph=graph, std=std, max_iterations=max_iterations_Noise)
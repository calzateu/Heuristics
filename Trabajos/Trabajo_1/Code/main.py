# Used libraries
import numpy as np

# My modules
import constructive

class MainMethods():
    def __init__(self, file_name) -> None:
        self.__MAX_NUM_NODOS  = 201
        self.__FILE_NAME      = file_name

        self.read_data()

    def read_data(self):
        nodes       = np.zeros((self.__MAX_NUM_NODOS , 4))

        cont = 0
        with open(self.__FILE_NAME, 'r') as file:
            for line in file:
                line         = list(map(int, line.split()))
                nodes[cont]  = line
                cont         += 1

        self.problem_information = nodes[0]
        self.nodes  = nodes[1:cont]
        self.cont   = cont - 1

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

    def __traveled_distance(self, path):
        distance = 0
        for i in range(len(path)-1):
            distance += self.dist_matrix[path[i], path[i+1]]

        return distance

    def __validate_solutions(self, paths, method):
        total_distances_traveled = 0
        nodes_visited = 0

        for i in paths:
            ocupation = 0
            for j in i:
                if j == 0:
                    if ocupation > method.capacity_of_vehicles:
                        print("Max capacity exceed", ocupation)
                        print(i)
                        break
                    ocupation = 0
                else:
                    ocupation += self.nodes[j, 3]

            distance = self.__traveled_distance(i)

            total_distances_traveled += distance
            nodes_visited += len(i)

            if distance > method.max_distance:
                        print("Max distance exceed", distance)
                        print(i)

        print(paths)
        print("Total distance: ", total_distances_traveled)
        print("Num nodes visited", nodes_visited)

    def run_method(self, Method):
        problem_information = self.problem_information
        demands = self.nodes[:, 3].copy()
        method = Method(problem_information, self.dist_matrix, demands)
        paths = method.search_paths()

        self.__validate_solutions(paths=paths, method=method)



if __name__ == '__main__':
    exec = MainMethods('/home/cristian/Descargas/Universidad/7_2023-1/Heuristica/Trabajos/Trabajo_1/mtVRP Instances/mtVRP1.txt')
    exec.compute_distances()

    exec.run_method(Method=constructive.ConstructiveMethod)




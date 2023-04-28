# Used libraries
import os


# My modules
from constructive3 import ConstructiveMethod3
from GRASP3 import GRASP3
from noise2 import Noise2

from utils import Utils

if __name__ == '__main__':

    run_individual_instance = True

    if run_individual_instance:
        folder_path = "../../mtVRP Instances"
        folder_path = os.path.abspath(folder_path)
        file = folder_path + '/mtVRP7.txt'
        exec = Utils()
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


    run_all_instances = True

    if run_all_instances:
        exec = Utils()

        verbose=False
        graph=False

        exec.run_instances(Method=ConstructiveMethod3, name="mtVRP_Cristian_Alzate_Urrea_constructivo2.xlsx", verbose=verbose, graph=graph)

        max_iterations_GRASP = 200
        k = 2
        exec.run_instances(Method=GRASP3, name="mtVRP_Cristian_Alzate_Urrea_GRASP2.xlsx", verbose=verbose, graph=graph,max_iterations=max_iterations_GRASP, k=k)

        max_iterations_Noise = 200
        std = 0.01
        exec.run_instances(Method=Noise2, name="mtVRP_Cristian_Alzate_Urrea_Noise2.xlsx", verbose=verbose, graph=graph, std=std, max_iterations=max_iterations_Noise)
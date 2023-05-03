# Used libraries
import os


# My modules
from utils import Utils
from neighborhoods import *
from VND import *
from ELS import ELS
from MS_ELS import MS_ELS

if __name__ == '__main__':

    utils = Utils()

    folder_path = "../../mtVRP Instances"
    folder_path = os.path.abspath(folder_path)
    instance = 'mtVRP1.txt'
    file_data = folder_path + '/' + instance

    problem_information, nodes, cont = utils.read_data(file_name=file_data)
    dist_matrix = utils.compute_distances()
    demands = nodes[:, 3].copy()

    #solutions = utils.read_solutions('../../Trabajo_1/Code/mtVRP_Cristian_Alzate_Urrea_constructivo.xlsx')
    solutions = utils.read_solutions('../../Trabajo_1/Code/mtVRP_Cristian_Alzate_Urrea_Noise.xlsx')
    neighborhoods = [two_opt, insertion, brute_force_relocation]# relocation]

    max_capacity = problem_information[2]
    max_distance = problem_information[1]

    #utils.apply_VND_all_instances(solutions)
    #solution, traveled_distances = VND(solutions[instance], neighborhoods, dist_matrix, demands=nodes[:, 3], max_capacity=max_capacity)


    #solution, traveled_distances = ELS(utils, problem_information, dist_matrix, demands, max_capacity, max_distance, ni=5, nc=2)
    solution, traveled_distances = MS_ELS(utils, problem_information, dist_matrix,
        demands, max_capacity, max_distance, num_insertions=100,
        num_relocations=100, ni=10, nc=10, nsol=5, std=0.15, max_iterations=200)


    print(solution)
    print(traveled_distances)
    print(sum(traveled_distances))


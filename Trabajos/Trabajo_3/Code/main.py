# Used libraries
import os


# My modules
from utils import Utils
from neighborhoods import *
from VND import *


if __name__ == '__main__':

    utils = Utils()

    folder_path = "../../mtVRP Instances"
    folder_path = os.path.abspath(folder_path)
    instance = 'mtVRP1.txt'
    file_data = folder_path + '/' + instance

    problem_information, nodes, cont = utils.read_data(file_name=file_data)
    dist_matrix = utils.compute_distances()
    demands = nodes[:, 3].copy()

    solutions = utils.read_solutions('../../Trabajo_1/Code/mtVRP_Cristian_Alzate_Urrea_Noise.xlsx')
    print(solutions[instance])


    neighborhoods = [inter_trips_2opt, two_opt_trips, brute_force_relocation]# relocation]

    num_cars = int(problem_information[1])
    max_capacity = problem_information[2]
    max_distance = problem_information[3]

    # solution, traveled_distances = VND(solutions[instance], neighborhoods, dist_matrix, demands=nodes[:, 3], max_capacity=max_capacity, num_vehicles=num_cars)
    name = "mtVRP_Cristian_Alzate_Urrea_sancocho.xlsx"
    #utils.apply_VND_all_instances(solutions, neighborhoods, name=name)





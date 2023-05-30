# Used libraries
import os


# My modules
from utils import Utils
from neighborhoods import *
from noise2 import Noise2
from VND import *


if __name__ == '__main__':

    utils = Utils()

    folder_path = "../../mtVRP Instances"
    folder_path = os.path.abspath(folder_path)
    instance = 'mtVRP1.txt'
    file_data = folder_path + '/' + instance

    utils.read_data(file_name=file_data)
    utils.compute_distances()
    neighborhoods = [inter_trips_2opt, two_opt_trips, brute_force_relocation]# relocation]
    utils.set_neighborhoods(neighborhoods)

    std = 0.01
    max_iterations = 100
    noise = Noise2(utils, std=std, max_iterations=max_iterations)
    solution_noise = noise.search_paths(split=True)


    solution, traveled_distances = VND(solution_noise, utils)


    #name = "mtVRP_Cristian_Alzate_Urrea_sancocho.xlsx"
    #utils.apply_VND_all_instances(solutions, neighborhoods, name=name)


    print(solution)
    #print(traveled_distances)
    #print(sum(traveled_distances))

    print()
    lista_1 = [item for vehicle in solution for trip in vehicle for item in trip]


    print(sorted(list(set(lista_1))))
    print(len(sorted(list(set(lista_1)))))

    print(utils.check_capacity_vehicles(solution))


    traveled_distances_temp = []
    for vehicle in solution:
        traveled_distances_temp.append(utils.traveled_distance(vehicle))

    print(traveled_distances_temp)



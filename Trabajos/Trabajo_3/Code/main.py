# Used libraries
import os
import time

# My modules
from utils import Utils
from neighborhoods import *
from noise2 import Noise2
from VND import *
from evolutivo import AlgoritmoGeneticoHibrido, apply_evolutivo_all_instances


if __name__ == '__main__':

    utils = Utils()

    folder_path = "../../mtVRP Instances"
    folder_path = os.path.abspath(folder_path)
    instance = 'mtVRP7.txt'
    file_data = folder_path + '/' + instance

    utils.read_data(file_name=file_data)
    utils.compute_distances()
    #neighborhoods = [inter_trips_2opt, two_opt_trips, brute_force_relocation]
    neighborhoods = [inter_trips_2opt, two_opt_trips]
    utils.set_neighborhoods(neighborhoods)

    std = 0.01
    max_iterations = 20
    noise = Noise2(utils, std=std, max_iterations=max_iterations)
    #solution_noise = noise.search_paths(split=True)


    # size_population = 20
    # num_generations = 30
    # probability_mutation = 0.5
    # start = time.time()
    # evolutivo = AlgoritmoGeneticoHibrido(size_population, num_generations, utils, generation_method=noise)
    # solution, traveled_distances = evolutivo.run(probability_mutation)
    # end = time.time()

    # print('Elapsed time:', end-start)


    name = "mtVRP_Cristian_Alzate_Urrea_sancocho.xlsx"

    size_population = 20
    num_generations = 30
    probability_mutation = 0.5
    start = time.time()
    apply_evolutivo_all_instances(size_population, num_generations, utils, generation_method=noise, name=name, probability_mutation=probability_mutation)
    end = time.time()

    print('Elapsed time:', end-start)



    # print(solution)
    # print(traveled_distances)
    # print(sum(traveled_distances))

    # print()
    # lista_1 = [item for vehicle in solution for trip in vehicle for item in trip]


    # print(sorted(list(set(lista_1))))
    # print(len(sorted(list(set(lista_1)))))

    # print(utils.check_capacity_vehicles(solution))


    # traveled_distances_temp = []
    # for vehicle in solution:
    #     traveled_distances_temp.append(utils.traveled_distance(vehicle))

    # print(traveled_distances_temp)



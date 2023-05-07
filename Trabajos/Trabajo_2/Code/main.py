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
    print(solutions[instance])


    neighborhoods = [inter_trips_2opt, two_opt_trips, brute_force_relocation]# relocation]
    #neighborhoods = [two_opt_vehicles]

    num_cars = int(problem_information[1])
    max_capacity = problem_information[2]
    max_distance = problem_information[3]

    #utils.apply_VND_all_instances(solutions)
    # solution, traveled_distances = VND(solutions[instance], neighborhoods, dist_matrix, demands=nodes[:, 3], max_capacity=max_capacity, num_vehicles=num_cars)

    # print(solution)
    # print(traveled_distances)
    # print(sum(traveled_distances))

    #utils.plot_routes(solution)

    # solution, traveled_distances = ELS(utils, problem_information, dist_matrix, demands, max_capacity, max_distance, num_cars=num_cars, num_insertions=10, num_relocations=100, num_mutations=5, ni=5, nc=2, neighborhoods=neighborhoods, std=0.01, max_iterations=200)
    solution, traveled_distances = MS_ELS(utils, problem_information, dist_matrix,
        demands, max_capacity, max_distance, num_cars=num_cars, num_insertions=10,
        num_relocations=100, num_mutations=5, ni=10, nc=10, nsol=5, neighborhoods=neighborhoods, std=0.01, max_iterations=200, ruido=True)

    # utils.plot_routes(solution)

    print(solution)
    print(traveled_distances)
    print(sum(traveled_distances))

    print()
    lista_1 = [item for vehicle in solution for trip in vehicle for item in trip]


    print(sorted(list(set(lista_1))))
    print(len(sorted(list(set(lista_1)))))

    print(check_capacity_vehicles(solution, demands=demands, max_capacity=max_capacity))


    traveled_distances_temp = []
    for vehicle in solution:
        traveled_distances_temp.append(traveled_distance(vehicle, dist_matrix))

    print(traveled_distances_temp)

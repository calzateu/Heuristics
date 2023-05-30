from neighborhoods import traveled_distance, distance_path


def __split_path(path_information):
    # Dividir la lista cada vez que aparezca el cero (deposito)
    sub_lists = []
    sub_list = []
    for item in path_information['ruta']:
        if item == 0:
            if sub_list != []:
                sub_lists.append([0] + sub_list + [0])
            sub_list = []
        else:
            sub_list.append(item)

    if sub_list != []:
        sub_lists.append(sub_list)

    return sub_lists

def __split_information(solution, num_vehicles):

    trips = []

    for path_information in solution[:-1]:
        trips.append(__split_path(path_information))

    return trips

def __initial_solution(solution, dist_matrix, num_vehicles):
    trips = __split_information(solution, num_vehicles)

    traveled_distances = []

    for i in range(num_vehicles):
        traveled_distances.append(traveled_distance(trips[i], dist_matrix))

    return trips, traveled_distances

def VND(solution_VND, neighborhoods, dist_matrix, demands, max_capacity, num_vehicles, num_insertions=1000, num_relocations=1000, preprocess=True, traveled_distances=None, ruido=False):

    if preprocess:
        trips, traveled_distances = __initial_solution(solution_VND, dist_matrix, num_vehicles)
    else:
        trips = solution_VND.copy()

    # print('################# Initial solution #################')
    # print(trips)
    # print(traveled_distances)
    # print(sum(traveled_distances))

    #self.plot_routes(trips)

    j = 0
    while j < len(neighborhoods):
        new_trips, new_traveled_distances, better = neighborhoods[j](trips,
            traveled_distances, dist_matrix, demands = demands,
            max_capacity=max_capacity, num_vehicles=num_vehicles, num_insertions=num_insertions, num_relocations=num_relocations, ruido=ruido)
        if better:
            j = 0
            trips = new_trips
            traveled_distances = new_traveled_distances

        else:
            j = j+1

    # print()
    # print('################# Final solution #################')
    # print(trips)
    # print(traveled_distances)
    # print(sum(traveled_distances))

    #self.plot_routes(trips)

    return trips, traveled_distances


def apply_VND_all_instances(solutions):

    for key in solutions.keys():
        print(f'######### {key} #########')
        VND(solutions[key])

    return None
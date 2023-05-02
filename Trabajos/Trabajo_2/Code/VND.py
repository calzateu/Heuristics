from neighborhoods import traveled_distance


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

def __split_information(solution):

    trips = []

    for path_information in solution[:-1]:
        trips.extend(__split_path(path_information))

    return trips

def __initial_solution(solution, dist_matrix):
    trips = __split_information(solution)

    traveled_distances = []

    for trip in trips:
        traveled_distances.append(traveled_distance(trip, dist_matrix))

    return trips, traveled_distances

def VND(solution, neighborhoods, dist_matrix, demands, max_capacity, preprocess=True, traveled_distances=None):
    if preprocess:
        trips, traveled_distances = __initial_solution(solution, dist_matrix)
    else:
        trips = solution

    # print('################# Initial solution #################')
    # print(trips)
    # print(traveled_distances)
    # print(sum(traveled_distances))

    #self.plot_routes(trips)

    j = 0
    while j < len(neighborhoods):
        new_trip, new_traveled_distances, better = neighborhoods[j](trips,
            traveled_distances, dist_matrix, demands = demands,
            max_capacity=max_capacity, num_insertions=10000, num_relocations=1000000)
        if better:
            j = 0
            trips = new_trip
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
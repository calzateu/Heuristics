
def __initial_solution(solution, utils):
    trips = utils.split_information(solution)

    traveled_distances = []

    for i in range(utils.num_vehicles):
        traveled_distances.append(utils.traveled_distance(trips[i]))

    return trips, traveled_distances

def VND(solution_VND, utils, preprocess=True, traveled_distances=None):

    if preprocess:
        trips, traveled_distances = __initial_solution(solution_VND, utils)
    else:
        trips = solution_VND.copy()

    # print('################# Initial solution #################')
    # print(trips)
    # print(traveled_distances)
    # print(sum(traveled_distances))

    #self.plot_routes(trips)

    j = 0
    while j < len(utils.neighborhoods):
        new_trips, new_traveled_distances, better = utils.neighborhoods[j](trips,
            traveled_distances, utils)
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
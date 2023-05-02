
from noise2 import Noise2
from neighborhoods import traveled_distance, check_capacity
from utils import Utils

def __split_path(path):
    # Dividir la lista cada vez que aparezca el cero (deposito)
    sub_lists = []
    sub_list = []
    for item in path:
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

    for path in solution:
        trips.extend(__split_path(path))

    return trips

def ELS(utils, problem_information, dist_matrix, demands, max_capacity, **kwargs):

    random_generator = Noise2(problem_information, dist_matrix, demands, std=0.01, max_iterations=200)
    solution = utils.run_method(method=random_generator, verbose=False, graph=False)

    solution = __split_information(solution)

    traveled_distances = []
    for path in solution:
        traveled_distances.append(traveled_distance(path, dist_matrix))

    capacity = 0
    for path in solution:
        capacity += check_capacity(path, demands, max_capacity)

    print(solution)
    print(traveled_distances)
    print(sum(traveled_distances))
    print(capacity)

    return




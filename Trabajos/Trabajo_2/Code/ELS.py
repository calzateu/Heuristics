
from noise2 import Noise2
from neighborhoods import traveled_distance, check_capacity
from utils import Utils, distance_exceed
from VND import *
from neighborhoods import *

def split_path(path):
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

def split_information(solution):

    trips = []

    for path in solution:
        trips.extend(split_path(path))

    return trips

#def mutate(solution):
# Define the insertion neighborhood structure
def mutate_random(trips, traveled_distances, dist_matrix, **kwargs):

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']

    for _ in range(kwargs['num_relocations']):
        # print('len(trips)', len(trips))
        if len(trips) < 2:
            return trips, traveled_distances
        i, j = random.sample(range(len(trips)), 2)

        # print(i, j)
        # print('len trips[i]', len(trips[i]))
        # print('len trips[j]', len(trips[j]))
        while len(trips[i]) <= 2 or len(trips[j]) <= 2:
            if len(trips[i]) <= 2:
                del(trips[i])
                del(traveled_distances[i])
            elif len(trips[j]) <= 2:
                del(trips[j])
                del(traveled_distances[j])

            i, j = random.sample(range(len(trips)), 2)


            if len(trips) < 1:
                return trips, traveled_distances

        k = random.randint(1, len(trips[i])-2)
        l = random.randint(1, len(trips[j])-2)

        costumer = trips[i].pop(k)
        trips[j].insert(l, costumer)

        capacity_i = check_capacity(trips[i], demands, max_capacity)
        capacity_j = check_capacity(trips[j], demands, max_capacity)
        valid = capacity_i + capacity_j # Es válido si los dos suman cero. Sino,
                                        # se excedió la capacidad y es igual a inf

        if valid >= float('inf'):
            # Si es peor devuelve los cambios
            #print(valid)
            restored_customer = trips[j].pop(l)
            trips[i].insert(k, restored_customer)
        else:
            traveled_distances[i] = traveled_distance(trips[i], dist_matrix)
            traveled_distances[j] = traveled_distance(trips[j], dist_matrix)
            # print('Mutacion', sum(traveled_distances))

            if len(trips[i]) <= 2:
                print(trips[i])
                del(trips[i])
                del(traveled_distances[i])
            elif len(trips[j]) <= 2:
                print(trips[j])
                del(trips[j])
                del(traveled_distances[j])

            if len(trips) < 2:
                    return trips, traveled_distances

            i, j = random.sample(range(len(trips)), 2)



    return trips, traveled_distances


def ELS(utils, problem_information, dist_matrix, demands, max_capacity, max_distance, ni, nc, generate_initial_solution=True, **kwargs):

    if generate_initial_solution:
        random_generator = Noise2(problem_information, dist_matrix, demands, std=0.01, max_iterations=200)
        solution = utils.run_method(method=random_generator, verbose=False, graph=False)
        solution = split_information(solution)
        traveled_distances = []
        for path in solution:
            traveled_distances.append(traveled_distance(path, dist_matrix))
    else:
        solution = kwargs['solution']
        traveled_distances = kwargs['traveled_distances']

    for j in range(ni):
        f_ = float('inf')
        S_ = None
        traveled_distances_ = None
        for k in range(nc):
            S = solution.copy()
            traveled_distances_S = traveled_distances.copy()
            #S = mutate(S)
            S, traveled_distances_S = mutate_random(S, traveled_distances_S, dist_matrix, num_relocations=10, demands=demands, max_capacity=max_capacity)
            neighborhoods = [two_opt, insertion, brute_force_relocation]
            S, traveled_distances_S = VND(S, neighborhoods, dist_matrix, demands, max_capacity, preprocess=False, traveled_distances=traveled_distances_S)

            #if sum(traveled_distances_S) < f_:
            if distance_exceed(traveled_distances_S, max_distance) < f_:
                f_ = distance_exceed(traveled_distances_S, max_distance)
                S_ = S
                traveled_distances_ = traveled_distances_S

        #if f_ < sum(traveled_distances):
        if f_ < distance_exceed(traveled_distances, max_distance):
            solution = S_
            traveled_distances = traveled_distances_


    # capacity = 0
    # for path in solution:
    #     capacity += check_capacity(path, demands, max_capacity)

    # print(solution)
    # print(traveled_distances)
    # print(sum(traveled_distances))
    # print(capacity)

    return solution, traveled_distances




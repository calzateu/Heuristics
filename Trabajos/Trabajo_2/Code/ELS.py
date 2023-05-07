
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

    trips_vehicles = []

    for path in solution:
        trips_vehicles.append(split_path(path))

    return trips_vehicles

#def mutate(solution):
# Define the insertion neighborhood structure
def mutate_random(trips_vehicles, traveled_distances, dist_matrix, **kwargs):

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']
    num_cars = kwargs['num_cars']

    for _ in range(kwargs['num_mutations']):
        # print('len(trips)', len(trips))
        if len(trips_vehicles) < num_cars:
            print('mutate inside 1',check_capacity_vehicles(trips_vehicles, demands=demands, max_capacity=max_capacity))
            return trips_vehicles, traveled_distances
        vehicle1 = random.randint(0, len(trips_vehicles) - 1)
        vehicle2 = random.randint(0, len(trips_vehicles) - 1)
        i = random.randint(0, len(trips_vehicles[vehicle1]) - 1)
        j = random.randint(0, len(trips_vehicles[vehicle2]) - 1)

        # print(i, j)
        # print('len trips[i]', len(trips[i]))
        # print('len trips[j]', len(trips[j]))
        while len(trips_vehicles[vehicle1][i]) <= 2 or len(trips_vehicles[vehicle2][j]) <= 2:
            if len(trips_vehicles[vehicle1][i]) <= 2:
                del(trips_vehicles[vehicle1][i])
                traveled_distances[vehicle1] = traveled_distance(trips_vehicles[vehicle1], dist_matrix)
            elif len(trips_vehicles[vehicle2][j]) <= 2:
                del(trips_vehicles[vehicle2][j])
                traveled_distances[vehicle2] = traveled_distance(trips_vehicles[vehicle2], dist_matrix)


            # if len(trips) < 2:
            #     return trips, traveled_distances

            # i, j = random.sample(range(len(trips)), 2)

            i = random.randint(0, len(trips_vehicles[vehicle1]) - 1)
            j = random.randint(0, len(trips_vehicles[vehicle2]) - 1)

        # print(trips_vehicles[vehicle1][i])
        k = random.randint(1, len(trips_vehicles[vehicle1][i])-3)
        # print(trips_vehicles[vehicle2][j])
        l = random.randint(1, len(trips_vehicles[vehicle2][j])-3)

        costumer = trips_vehicles[vehicle1][i].pop(k)
        trips_vehicles[vehicle2][j].insert(l, costumer)

        # capacity_i = check_capacity_vehicles(trips_vehicles[vehicle1], demands, max_capacity)
        # capacity_j = check_capacity_vehicles(trips_vehicles[vehicle2], demands, max_capacity)
        # valid = capacity_i + capacity_j # Es válido si los dos suman cero. Sino,
        #                                 # se excedió la capacidad y es igual a inf

        valid = check_capacity_vehicles(trips_vehicles, demands, max_capacity) # Es válido si los dos suman cero. Sino,
                                        # se excedió la capacidad y es igual a inf

        if valid == float('inf'):
            # Si es peor devuelve los cambios
            #print(valid)
            restored_customer = trips_vehicles[vehicle2][j].pop(l)
            trips_vehicles[vehicle1][i].insert(k, restored_customer)
        else:
            # print()
            # print(valid)
            # print(check_capacity_vehicles(trips_vehicles, demands, max_capacity))
            # print()
            traveled_distances[vehicle1] = traveled_distance(trips_vehicles[vehicle1], dist_matrix)
            traveled_distances[vehicle2] = traveled_distance(trips_vehicles[vehicle2], dist_matrix)
            # print('Mutacion', sum(traveled_distances))

            if len(trips_vehicles[vehicle1][i]) <= 2:
                print(trips_vehicles[vehicle1][i])
                del(trips_vehicles[vehicle1][i])
                #del(traveled_distances[i])
                traveled_distances[vehicle1] = traveled_distance(trips_vehicles[vehicle1], dist_matrix)
            elif len(trips_vehicles[vehicle2][j]) <= 2:
                print(trips_vehicles[vehicle2][j])
                del(trips_vehicles[vehicle2][j])
                #del(traveled_distances[j])
                traveled_distances[vehicle2] = traveled_distance(trips_vehicles[vehicle2], dist_matrix)

            # if len(trips) < 2:
            #         return trips, traveled_distances

            # i, j = random.sample(range(len(trips)), 2)



    print('mutate inside 2',check_capacity_vehicles(trips_vehicles, demands=demands, max_capacity=max_capacity))
    return trips_vehicles, traveled_distances


def ELS(utils, problem_information, dist_matrix, demands, max_capacity, max_distance, num_cars, ni, nc, neighborhoods, generate_initial_solution=True, **kwargs):

    if generate_initial_solution:
        random_generator = Noise2(problem_information, dist_matrix, demands, std=kwargs['std'], max_iterations=kwargs['max_iterations'])
        solution = utils.run_method(method=random_generator, verbose=False, graph=False)
        solution = split_information(solution)
        traveled_distances = []
        for trip_vehicle in solution:
            traveled_distances.append(traveled_distance(trip_vehicle, dist_matrix))
    else:
        solution = kwargs['solution']
        traveled_distances = kwargs['traveled_distances']

    num_insertions=kwargs['num_insertions']
    num_relocations=kwargs['num_relocations']
    num_mutations=kwargs['num_mutations']

    for j in range(ni):
        f_ = float('inf')
        S_ = None
        traveled_distances_ = None
        for k in range(nc):
            #S = [trip.copy() for trip in solution] ###### Cuidado con esto
            S = [[trip.copy() for trip in vehicle] for vehicle in solution]
            traveled_distances_S = traveled_distances.copy()
            #S = mutate(S)
            #neighborhoods = [two_opt, insertion, brute_force_relocation]
            S, traveled_distances_S = VND(S, neighborhoods, dist_matrix, demands, max_capacity, num_vehicles=num_cars, num_insertions=num_insertions, num_relocations=num_relocations, preprocess=False, traveled_distances=traveled_distances_S)

            #if sum(traveled_distances_S) < f_:
            if distance_exceed(traveled_distances_S, max_distance, num_cars) < f_:
                f_ = distance_exceed(traveled_distances_S, max_distance, num_cars)
                S_ = S
                traveled_distances_ = traveled_distances_S


        #if f_ < sum(traveled_distances):
        if f_ < distance_exceed(traveled_distances, max_distance, num_cars):
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




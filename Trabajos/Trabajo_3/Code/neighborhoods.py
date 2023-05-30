import random

def distance_path(path, dist_matrix):
        distance = 0
        for i in range(len(path)-1):
            distance += dist_matrix[int(path[i]), int(path[i+1])]

        return distance

def traveled_distance(trips_vehicle, dist_matrix):
        distance = 0
        for trip in trips_vehicle:
            distance += distance_path(trip, dist_matrix)

        return distance


def check_capacity(trip, demands, max_capacity):
    ocupation = 0

    for j in trip:
        if j == 0:
            if ocupation > max_capacity:
                #print('ocupation exceed', ocupation)
                return float('inf')
            ocupation = 0
        else:
            ocupation += demands[int(j)]

    return 0

def check_capacity_vehicles(trips_vehicles, demands, max_capacity):
    ocupation = 0
    for vehicle in trips_vehicles:
        for trip in vehicle:
            ocupation += check_capacity(trip, demands, max_capacity)

    return ocupation

def two_opt_trips(trips_vehicles, traveled_distances, dist_matrix, **kwargs):

    better = False

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']

    for i in range(len(trips_vehicles)):
        for j in range(len(trips_vehicles[i])):
            n = len(trips_vehicles[i][j])
            for k in range(1, n-1):
                for l in range(j+1, n):
                    new_trip = trips_vehicles[i][j][:k] + trips_vehicles[i][j][k:l][::-1] + trips_vehicles[i][j][l:]

                    distance_before = traveled_distances[i] - distance_path(trips_vehicles[i][j], dist_matrix)
                    new_traveled_distance_trip = distance_path(new_trip, dist_matrix)

                    new_traveled_distance = new_traveled_distance_trip + distance_before

                    # # Es válido si los dos suman cero. Sino,
                    # # se excedió la capacidad y es igual a inf
                    # capacity_new_trip = check_capacity(new_trip, demands, max_capacity)

                    valid = check_capacity_vehicles(trips_vehicles, demands, max_capacity) # Es válido si los dos suman cero. Sino,
                                        # se excedió la capacidad y es igual a inf


                    if new_traveled_distance + valid < traveled_distances[i]:
                        trips_vehicles[i][j] = new_trip
                        traveled_distances[i] = new_traveled_distance
                        better = True


    return trips_vehicles, traveled_distances, better


def join_trips_vehicles(trips_vehicles):
    len_solution = sum([sum([len(trip) for trip in vehicle]) for vehicle in trips_vehicles])
    solution = [0]*len_solution
    cars_and_trips = dict()

    cont = 1
    for i in range(len(trips_vehicles)):
        num_trips = 0
        for trip in trips_vehicles[i]:
            for j in range(1, len(trip)):
                solution[cont] = trip[j]
                cont += 1

            num_trips += 1

        cars_and_trips[i] = num_trips

    while solution [-1] == 0 and solution[-2] == 0:
        solution.pop()

    return solution, cars_and_trips

def split_trips_vehicles(path, cars_and_trips):
    solution = [[] for _ in range(len(cars_and_trips.keys()))]
    vehicle = 0
    num_trip = 0
    trip = [0]
    for i in range(1,len(path)):
        if path[i] == 0:
            trip.append(0)
            solution[vehicle].append(trip)
            trip = [0]
            num_trip += 1

            if num_trip > cars_and_trips[vehicle]:
                vehicle += 1
        else:
           trip.append(path[i])


    return solution


def __validate_solutions(path, dist_matrix, demands, capacity_of_vehicles, verbose=False):
    total_distances_traveled = 0
    feasible_path = True
    nodes_visited = 0

    ocupation = 0
    for i in range(1, len(path)):
        if path[i] == 0:
            if ocupation > capacity_of_vehicles:
                if verbose:
                    print("Max capacity exceed", ocupation)
                    print(i)

                feasible_path = False
            else:
                ocupation = 0
        else:
            ocupation += demands[int(path[i])]

        total_distances_traveled += dist_matrix[int(path[i-1]), int(path[i])]

    return total_distances_traveled, feasible_path

def inter_trips_2opt(trips_vehicles, traveled_distance_trips, dist_matrix, **kwargs):

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']
    ruido = kwargs['max_capacity']

    aux = [[trip.copy() for trip in vehicle] for vehicle in trips_vehicles]
    aux2 = traveled_distance_trips.copy()

    better = False
    improved = True
    cont = 0
    cont_improved = 0
    while improved:
        if cont != cont_improved:
            return aux, aux2, False
        better = False
        for vehicle1 in range(len(trips_vehicles)):
            for vehicle2 in range(vehicle1+1, len(trips_vehicles)):
                i = 0
                while i < len(trips_vehicles[vehicle1]):
                    j = 0
                    while j < len(trips_vehicles[vehicle2]):
                        k = 1
                        while k < len(trips_vehicles[vehicle1][i]):
                            l = 1
                            while l < len(trips_vehicles[vehicle2][j]):
                                temp1 = trips_vehicles[vehicle1][i].copy()
                                temp2 = trips_vehicles[vehicle2][j].copy()
                                # trips_vehicles[vehicle1][i] = trips_vehicles[vehicle1][i][1:k] + trips_vehicles[vehicle2][j][l:-1]
                                # trips_vehicles[vehicle2][j] = trips_vehicles[vehicle2][j][1:l] + trips_vehicles[vehicle1][i][k:-1]

                                new_trip_i = trips_vehicles[vehicle1][i][:k].copy() + trips_vehicles[vehicle2][j][l:].copy()
                                new_trip_j = trips_vehicles[vehicle2][j][:l].copy() + trips_vehicles[vehicle1][i][k:].copy()
                                # lista_1 = [item for trip in [temp1, temp2] for item in trip]
                                # lista_2 = [item for trip in [new_trip_i, new_trip_j] for item in trip]
                                # print(len(list(set(lista_1))) == len(list(set(lista_2))))
                                # print('Vehiculos',len(sorted(list(set(lista_1)))))

                                # if k == len(trips_vehicles[vehicle2][j]) - 1:
                                #     print(vehicle1, vehicle2)
                                #     print(temp1)
                                #     print(temp2)
                                #     print()
                                #     print(new_trip_i)
                                #     print(new_trip_j)
                                #     exit()

                                if len( trips_vehicles[vehicle1][i]) < 2:
                                    print(' trips_vehicles[vehicle1][i]', trips_vehicles[vehicle1][i])
                                if len( trips_vehicles[vehicle2][j]) < 2:
                                    print(' trips_vehicles[vehicle2][j]', trips_vehicles[vehicle2][j])

                                distance_before_i = distance_path(temp1, dist_matrix)
                                distance_before_j = distance_path(temp2, dist_matrix)
                                distances_before = distance_before_i + distance_before_j

                                new_traveled_distance_trip_i = distance_path(new_trip_i, dist_matrix)
                                new_traveled_distance_trip_j = distance_path(new_trip_j, dist_matrix)
                                new_traveled_distance = new_traveled_distance_trip_i + new_traveled_distance_trip_j

                                # # Es válido si los dos suman cero. Sino,
                                # # se excedió la capacidad y es igual a inf
                                # capacity_new_trip_i = check_capacity(new_trip_j, demands, max_capacity)
                                # capacity_new_trip_j = check_capacity(new_trip_j, demands, max_capacity)
                                # valid = capacity_new_trip_i + capacity_new_trip_j # Es válido si los dos suman cero. Sino,
                                #                                 # se excedió la capacidad y es igual a inf

                                trips_vehicles[vehicle1][i] = new_trip_i
                                trips_vehicles[vehicle2][j] = new_trip_j

                                valid = check_capacity_vehicles(trips_vehicles, demands, max_capacity) # Es válido si los dos suman cero. Sino,
                                        # se excedió la capacidad y es igual a inf


                                if new_traveled_distance + valid >= distances_before: # Devolver los cambios
                                    #print('new_traveled_distance', new_traveled_distance)
                                    #print('distances_before', distances_before)
                                    trips_vehicles[vehicle1][i] = temp1
                                    trips_vehicles[vehicle2][j] = temp2
                                    improved = False
                                else:
                                    if len(trips_vehicles[vehicle1][i]) <= 2:
                                        print(trips_vehicles[vehicle1][i])
                                        trips_vehicles[vehicle1].pop(i)
                                        return trips_vehicles, traveled_distance_trips, True
                                    if len(trips_vehicles[vehicle2][j]) <= 2:
                                        print(trips_vehicles[vehicle2][j])
                                        trips_vehicles[vehicle2].pop(j)
                                        return trips_vehicles, traveled_distance_trips, True

                                    traveled_distance_trips[vehicle1] = traveled_distance(trips_vehicles[vehicle1], dist_matrix)
                                    traveled_distance_trips[vehicle2] = traveled_distance(trips_vehicles[vehicle2], dist_matrix)
                                    # print(sum(traveled_distance_trips))

                                    better = True
                                    improved = True
                                    cont_improved += 1

                                l += 1
                            k += 1
                        j += 1
                    i += 1
        cont += 1

        # if check_capacity_vehicles(trips_vehicles, demands, max_capacity) == float('inf'):
        #     print(trips_vehicles)

    return trips_vehicles, traveled_distance_trips, better


# Define the insertion neighborhood structure
def relocation(trips, traveled_distances, dist_matrix, **kwargs):
    num_trips = len(trips)

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']

    for _ in range(kwargs['num_relocations']):
        better = False

        if len(trips) < 2:
            return trips, traveled_distances, better

        i, j = random.sample(range(num_trips), 2)

        while len(trips[i]) <= 2 or len(trips[j]) <= 2:
            if len(trips[i]) <= 2:
                del(trips[i])
                del(traveled_distances[i])
                i, j = random.sample(range(len(trips)), 2)
            elif len(trips[j]) <= 2:
                del(trips[j])
                del(traveled_distances[j])
                i, j = random.sample(range(len(trips)), 2)


            if len(trips) < 1:
                return trips, traveled_distances, better

        k = random.randint(1, len(trips[i])-2)
        l = random.randint(1, len(trips[j])-2)

        costumer = trips[i].pop(k)
        trips[j].insert(l, costumer)

        capacity_i = check_capacity(trips[i], demands, max_capacity)
        capacity_j = check_capacity(trips[j], demands, max_capacity)
        valid = capacity_i + capacity_j # Es válido si los dos suman cero. Sino,
                                        # se excedió la capacidad y es igual a inf

        # Acá debo multiplicar por una variable binaria de si se cumple la capacidad o no
        if traveled_distance(trips[i], dist_matrix)+traveled_distance(trips[j],
                dist_matrix) + valid > traveled_distances[i] + traveled_distances[j]:
            # Si es peor devuelve los cambios
            #print(valid)
            restored_customer = trips[j].pop(l)
            trips[i].insert(k, restored_customer)
        else:
            traveled_distances[i] = traveled_distance(trips[i], dist_matrix)
            traveled_distances[j] = traveled_distance(trips[j], dist_matrix)
            print('Mejoro', sum(traveled_distances))
            better = True


    return trips, traveled_distances, better


def brute_force_relocation(trips_vehicles, traveled_distances, dist_matrix, **kwargs):

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']
    max_capacity = kwargs['max_capacity']
    num_vehicles = kwargs['num_vehicles']

    # for i in range(len(trips)):
    #     for j in range(len(trips)):
    #         print(i,j)
    #         for k in range(len(trips[i])):
    #             for l in range(len(trips[j])):

    i = 0
    j = 0
    k = 1
    l = 1
    for vehicle1 in range(num_vehicles):
        for vehicle2 in range(num_vehicles):
            #print(f'vehicle1 {vehicle1} vehicle2 {vehicle2}')
            while i < len(trips_vehicles[vehicle1]):
                while j < len(trips_vehicles[vehicle2]):
                    while k < len(trips_vehicles[vehicle1][i]) - 1:
                        while l < len(trips_vehicles[vehicle2][j]) - 1:

                            better = False

                            # i, j = random.sample(range(num_trips), 2)

                            # k = random.randint(1, len(trips[i])-2)
                            # l = random.randint(1, len(trips[j])-2)

                            costumer = trips_vehicles[vehicle1][i].pop(k)
                            trips_vehicles[vehicle2][j].insert(l, costumer)

                            # capacity_i = check_capacity(trips_vehicles[vehicle1][i], demands, max_capacity)
                            # capacity_j = check_capacity(trips_vehicles[vehicle2][j], demands, max_capacity)
                            # valid = capacity_i + capacity_j # Es válido si los dos suman cero. Sino,
                            #                                 # se excedió la capacidad y es igual a inf

                            valid = check_capacity_vehicles(trips_vehicles, demands, max_capacity) # Es válido si los dos suman cero. Sino,
                                        # se excedió la capacidad y es igual a inf

                            # Acá debo multiplicar por una variable binaria de si se cumple la capacidad o no
                            if traveled_distance(trips_vehicles[vehicle1], dist_matrix) + traveled_distance(trips_vehicles[vehicle2],
                                    dist_matrix) + valid > traveled_distances[vehicle1] + traveled_distances[vehicle2]:
                                # Si es peor devuelve los cambios
                                #print(valid)
                                restored_customer = trips_vehicles[vehicle2][j].pop(l)
                                trips_vehicles[vehicle1][i].insert(k, restored_customer)
                            else:
                                traveled_distances[vehicle1] = traveled_distance(trips_vehicles[vehicle1], dist_matrix)
                                traveled_distances[vehicle2] = traveled_distance(trips_vehicles[vehicle2], dist_matrix)
                                #traveled_distances[j] = traveled_distance(trips_vehicles[vehicle][j], dist_matrix)
                                #print('Mejoro', sum(traveled_distances))
                                better = True


                            l += 1
                        k += 1
                    j += 1
                i += 1

    return trips_vehicles, traveled_distances, better

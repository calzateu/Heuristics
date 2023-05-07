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
                return float('inf')
            ocupation = 0
        else:
            ocupation += demands[int(j)]

    return 0

def check_capacity_vehicles(trips_vehicles, demands, max_capacity):
    ocupation = 0
    for trip in trips_vehicles:
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

                    # Es válido si los dos suman cero. Sino,
                    # se excedió la capacidad y es igual a inf
                    capacity_new_trip = check_capacity(new_trip, demands, max_capacity)


                    if new_traveled_distance + capacity_new_trip < traveled_distances[i]:
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

def two_opt_vehicles(trips_vehicles, traveled_distance_trips, dist_matrix, **kwargs):

    reference = trips_vehicles.copy()
    better = False

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']

    trips_vehicles_joined, cars_and_trips = join_trips_vehicles(trips_vehicles)
    new_traveled_distance_trips, feasible = __validate_solutions(trips_vehicles_joined, dist_matrix, demands, capacity_of_vehicles=max_capacity, verbose=False)
    traveled_trips_vehicles_joined = new_traveled_distance_trips

    #print('initial', trips_vehicles_joined)

    n = len(trips_vehicles_joined)
    for k in range(1, n-1):
        for l in range(k+1, n):
            new_trip = trips_vehicles_joined[:k] + trips_vehicles_joined[k:l][::-1] + trips_vehicles_joined[l:]

            new_traveled_distance_trips, feasible = __validate_solutions(new_trip, dist_matrix, demands, capacity_of_vehicles=max_capacity, verbose=False)

            #print(feasible)

            if feasible and (new_traveled_distance_trips < traveled_trips_vehicles_joined):
                #print('intermediate', new_trip)
                #print(trips_vehicles_joined == new_trip)
                trips_vehicles_joined = new_trip
                traveled_trips_vehicles_joined = new_traveled_distance_trips
                better = True

    #print('final', trips_vehicles_joined)
    if better:
        trips_vehicles = split_trips_vehicles(trips_vehicles_joined, cars_and_trips)

        traveled_distance_trips = [traveled_distance(vehicle, dist_matrix) for vehicle in trips_vehicles]

        print(reference==trips_vehicles)
        return trips_vehicles, traveled_distance_trips, better
    else:
        return trips_vehicles, traveled_distance_trips, better


def inter_trips_2opt(trips_vehicles, traveled_distance_trips, dist_matrix, **kwargs):

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']
    better = True
    while better:
        better = False
        for vehicle in range(len(trips_vehicles)):
            for i in range(len(trips_vehicles[vehicle])-1):
                for j in range(i+1, len(trips_vehicles[vehicle])):
                    for k in range(1, len(trips_vehicles[vehicle][i])-1):
                        for l in range(1, len(trips_vehicles[vehicle][j])-1):
                            new_route_i = trips_vehicles[vehicle][i][:k] + trips_vehicles[vehicle][j][l:]
                            new_route_j = trips_vehicles[vehicle][j][:l] + trips_vehicles[vehicle][i][k:]

                            distance_before_i = distance_path(trips_vehicles[vehicle][i], dist_matrix)
                            distance_before_j = distance_path(trips_vehicles[vehicle][j], dist_matrix)
                            distances_before = distance_before_i + distance_before_j

                            new_traveled_distance_trip_i = distance_path(new_route_i, dist_matrix)
                            new_traveled_distance_trip_j = distance_path(new_route_j, dist_matrix)
                            new_traveled_distance = new_traveled_distance_trip_i + new_traveled_distance_trip_j

                            # Es válido si los dos suman cero. Sino,
                            # se excedió la capacidad y es igual a inf
                            capacity_new_trip_i = check_capacity(trips_vehicles[vehicle][i], demands, max_capacity)
                            capacity_new_trip_j = check_capacity(trips_vehicles[vehicle][i], demands, max_capacity)
                            capacity_new_trip = capacity_new_trip_i + capacity_new_trip_j # Es válido si los dos suman cero. Sino,
                                                            # se excedió la capacidad y es igual a inf


                            if new_traveled_distance + capacity_new_trip < distances_before:
                                print('new_traveled_distance', new_traveled_distance)
                                print('distances_before', distances_before)
                                trips_vehicles[vehicle][i], trips_vehicles[vehicle][j] = new_route_i, new_route_j
                                traveled_distance_trips[vehicle] = traveled_distance(trips_vehicles[vehicle], dist_matrix)
                                better = True
        return trips_vehicles, traveled_distance_trips, better



# Define the insertion neighborhood structure
def insertion(trips, traveled_distances, dist_matrix, **kwargs):

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']

    for _ in range(kwargs['num_insertions']):
        better = False

        if len(trips) < 2:
            return trips, traveled_distances, better

        i, j = random.sample(range(len(trips)), 2)

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

        trips[i][k], trips[j][l] = trips[j][l], trips[i][k]

        capacity_i = check_capacity(trips[i], demands, max_capacity)
        capacity_j = check_capacity(trips[j], demands, max_capacity)
        valid = capacity_i + capacity_j # Es válido si los dos suman cero. Sino,
                                        # se excedió la capacidad y es igual a inf

        # Acá debo multiplicar por una variable binaria de si se cumple la capacidad o no
        if traveled_distance(trips[i], dist_matrix)+traveled_distance(trips[j],
                dist_matrix) + valid > traveled_distances[i] + traveled_distances[j]:
            # Si es peor devuelve los cambios
            trips[i][k], trips[j][l] = trips[j][l], trips[i][k]
        else:
            traveled_distances[i] = traveled_distance(trips[i], dist_matrix)
            traveled_distances[j] = traveled_distance(trips[j], dist_matrix)
            better = True


    return trips, traveled_distances, better


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


def brute_force_relocation(trips, traveled_distances, dist_matrix, **kwargs):

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']

    # for i in range(len(trips)):
    #     for j in range(len(trips)):
    #         print(i,j)
    #         for k in range(len(trips[i])):
    #             for l in range(len(trips[j])):

    i = 0
    j = 0
    k = 1
    l = 1
    while i < len(trips):
        while j < len(trips):
            while k < len(trips[i]) - 1:
                while l < len(trips[j]) - 1:

                    better = False

                    # i, j = random.sample(range(num_trips), 2)

                    # k = random.randint(1, len(trips[i])-2)
                    # l = random.randint(1, len(trips[j])-2)

                    costumer = trips[i].pop(k)
                    trips[j].insert(l, costumer)

                    capacity_i = check_capacity(trips[i], demands, max_capacity)
                    capacity_j = check_capacity(trips[j], demands, max_capacity)
                    valid = capacity_i + capacity_j # Es válido si los dos suman cero. Sino,
                                                    # se excedió la capacidad y es igual a inf

                    # Acá debo multiplicar por una variable binaria de si se cumple la capacidad o no
                    if traveled_distance(trips[i], dist_matrix)+traveled_distance(trips[j],
                            dist_matrix) + valid >= traveled_distances[i] + traveled_distances[j]:
                        # Si es peor devuelve los cambios
                        #print(valid)
                        restored_customer = trips[j].pop(l)
                        trips[i].insert(k, restored_customer)
                    else:
                        traveled_distances[i] = traveled_distance(trips[i], dist_matrix)
                        traveled_distances[j] = traveled_distance(trips[j], dist_matrix)
                        #print('Mejoro', sum(traveled_distances))
                        better = True


                    l += 1
                k += 1
            j += 1
        i += 1

    return trips, traveled_distances, better

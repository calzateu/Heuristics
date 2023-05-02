import random


def traveled_distance(path, dist_matrix):
        distance = 0
        for i in range(len(path)-1):
            distance += dist_matrix[int(path[i]), int(path[i+1])]

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

def two_opt(trips, traveled_distances, dist_matrix, **kwargs):

    better = False

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']

    #print('len(trips)', len(trips))
    #print('len(traveled_distances)', len(traveled_distances))

    for i in range(len(trips)):
        n = len(trips[i])
        for j in range(1, n-1):
            for k in range(j+1, n):
                new_trip = trips[i][:j] + trips[i][j:k][::-1] + trips[i][k:]
                new_traveled_distance = traveled_distance(new_trip, dist_matrix)

                # Es válido si los dos suman cero. Sino,
                # se excedió la capacidad y es igual a inf
                capacity_new_trip = check_capacity(new_trip, demands, max_capacity)


                if new_traveled_distance + capacity_new_trip < traveled_distances[i]:
                    trips[i] = new_trip
                    traveled_distances[i] = new_traveled_distance
                    better = True


    return trips, traveled_distances, better

# Define the insertion neighborhood structure
def insertion(trips, traveled_distances, dist_matrix, **kwargs):
    num_trips = len(trips)

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']

    for _ in range(kwargs['num_insertions']):
        better = False
        i, j = random.sample(range(num_trips), 2)

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
        i, j = random.sample(range(num_trips), 2)

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

                        k -= 1

                    l += 1
                k += 1
            j += 1
        i += 1

    return trips, traveled_distances, better

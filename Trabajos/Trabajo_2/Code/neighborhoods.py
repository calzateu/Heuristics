import random


def __traveled_distance(path, dist_matrix):
        distance = 0
        for i in range(len(path)-1):
            distance += dist_matrix[int(path[i]), int(path[i+1])]

        return distance


def __check_capacity(trip, demands, max_capacity):
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

    for i in range(len(trips)):
        n = len(trips[i])
        for j in range(1, n-1):
            for k in range(j+1, n):
                new_trip = trips[i][:j] + trips[i][j:k][::-1] + trips[i][k:]
                new_traveled_distance = __traveled_distance(new_trip, dist_matrix)

                # Es válido si los dos suman cero. Sino,
                # se excedió la capacidad y es igual a inf
                capacity_new_trip = __check_capacity(new_trip, demands, max_capacity)


                if new_traveled_distance + capacity_new_trip < traveled_distances[i]:
                    trips[i] = new_trip
                    traveled_distances[i] = new_traveled_distance
                    better = True


    return trips, traveled_distances, better

# Define the insertion neighborhood structure
def swap_customers(trips, traveled_distances, dist_matrix, **kwargs):
    num_trips = len(trips)

    demands = kwargs['demands']
    max_capacity = kwargs['max_capacity']

    for _ in range(kwargs['num_swaps']):
        better = False
        i, j = random.sample(range(num_trips), 2)

        k = random.randint(1, len(trips[i])-2)
        l = random.randint(1, len(trips[j])-2)

        trips[i][k], trips[j][l] = trips[j][l], trips[i][k]

        capacity_i = __check_capacity(trips[i], demands, max_capacity)
        capacity_j = __check_capacity(trips[j], demands, max_capacity)
        valid = capacity_i + capacity_j # Es válido si los dos suman cero. Sino,
                                        # se excedió la capacidad y es igual a inf

        # Acá debo multiplicar por una variable binaria de si se cumple la capacidad o no
        if __traveled_distance(trips[i], dist_matrix) + __traveled_distance(trips[j], dist_matrix) + valid > traveled_distances[i] + traveled_distances[j]:
            # Si es peor devuelve los cambios
            trips[i][k], trips[j][l] = trips[j][l], trips[i][k]
            traveled_distances[i] = __traveled_distance(trips[i], dist_matrix)
            traveled_distances[j] = __traveled_distance(trips[j], dist_matrix)
        else:
            better = True


    return trips, traveled_distances, better




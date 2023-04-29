import random


def __traveled_distance(path, dist_matrix):
        distance = 0
        for i in range(len(path)-1):
            distance += dist_matrix[int(path[i]), int(path[i+1])]

        return distance

def two_opt(trips, traveled_distances, dist_matrix):

    better = False

    for i in range(len(trips)):
        n = len(trips[i])
        for j in range(1, n-1):
            for k in range(j+1, n):
                new_trip = trips[i][:j] + trips[i][j:k][::-1] + trips[i][k:]
                new_traveled_distance = __traveled_distance(new_trip, dist_matrix)

                if new_traveled_distance < traveled_distances[i]:
                    trips[i] = new_trip
                    traveled_distances[i] = new_traveled_distance
                    better = True


    return trips, traveled_distances, better

# Define the insertion neighborhood structure
def insertion_customers(route):
    n = len(route)
    i, j = random.sample(range(n), 2)
    if i > j:
        i, j = j, i
    customer = route.pop(i)
    route.insert(j-1, customer)
    return route


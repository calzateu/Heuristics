import random

def crossover(parent1, parent2):
    # Choose crossover points
    crossover_point1 = random.randint(1, len(parent1) - 2)
    crossover_point2 = random.randint(crossover_point1 + 1, len(parent1) - 1)

    # Create offspring as copies of parents
    offspring1 = [route.copy() for route in parent1]
    offspring2 = [route.copy() for route in parent2]

    # Perform partially-mapped crossover
    for i in range(crossover_point1, crossover_point2 + 1):
        node1 = parent1[i]
        node2 = parent2[i]

        print('Node 1')
        print(node1)

        # Swap corresponding nodes in the offspring
        for route in offspring1:
            if node2 in route:
                index1 = route.index(node1)
                route[index1] = node2
                route[route.index(node2)] = node1

        for route in offspring2:
            if node1 in route:
                index2 = route.index(node2)
                route[index2] = node1
                route[route.index(node1)] = node2

    return offspring1, offspring2


parent1 = [
    [[0, 20, 35, 36, 3, 28, 31, 26, 8, 48, 23, 0]],
    [[0, 22, 29, 21, 34, 30, 10, 39, 33, 45, 15, 44, 37, 17, 0]],
    [[0, 46, 38, 9, 50, 16, 2, 11, 32, 1, 27, 6, 0], [0, 49, 5, 12, 47, 18, 14, 0]],
    [[0, 4, 42, 19, 40, 41, 13, 25, 24, 43, 7, 0]]]
parent2 = [[[0, 49, 39, 33, 45, 15, 44, 42, 19, 40, 41, 4, 0]], [[0, 46, 5, 10, 30, 34, 21, 29, 20, 35, 36, 3, 0]], [[0, 1, 22, 28, 31, 8, 26, 7, 43, 24, 23, 48, 27, 0]], [[0, 32, 2, 16, 50, 9, 38, 11, 12, 37, 17, 0], [0, 47, 18, 13, 25, 14, 6, 0]]]
print(crossover(parent1, parent2))


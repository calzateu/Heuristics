
import numpy as np
from VND import *


class AlgoritmoGeneticoHibrido:
    def __init__(self, size_population, num_generations, utils, generation_method) -> None:
        self.size_population = size_population
        self.num_generations = num_generations
        self.utils = utils
        self.generation_method = generation_method

    def population_initialization(self):
        self.population = [0]*(self.size_population*2)
        self.traveled_distances_population = [0]*(self.size_population*2)

        self.active_population = 0
        for i in range(self.size_population):
            solution = self.generation_method.search_paths(split=True)
            self.population[i], self.traveled_distances_population[i] = self.utils.initial_solution(solution)
            self.active_population += 1

    def select_parents(self):
        parent1, parent2 = np.random.choice(range(self.size_population), size=2)

        return parent1, parent2

    def __select_nodes(self, parent1, parent2):
        index_vehicle1  = np.random.choice(range(len(parent1)))
        while len(parent1[index_vehicle1]) == 0:
            del(parent1[index_vehicle1])
            index_vehicle1  = np.random.choice(range(len(parent1)))
        index_trip1      = np.random.choice(range(len(parent1[index_vehicle1])))
        while len(parent1[index_vehicle1][index_trip1]) == 0:
            del(parent1[index_vehicle1][index_trip1])
            index_trip1      = np.random.choice(range(len(parent1[index_vehicle1])))
        index_node1       = np.random.choice(range(len(parent1[index_vehicle1][index_trip1])))

        index_vehicle2  = np.random.choice(range(len(parent2)))
        while len(parent2[index_vehicle2]) == 0:
            del(parent2[index_vehicle2])
            index_vehicle2  = np.random.choice(range(len(parent2)))
        index_trip2      = np.random.choice(range(len(parent2[index_vehicle2])))
        while len(parent2[index_vehicle2][index_trip2]) == 0:
            del(parent2[index_vehicle2][index_trip2])
            index_trip2      = np.random.choice(range(len(parent2[index_vehicle2])))
        index_node2       = np.random.choice(range(len(parent2[index_vehicle2][index_trip2])))

        return (index_vehicle1, index_trip1, index_node1), (index_vehicle2, index_trip2, index_node2)

    def __change(self, parent1_child, parent2_child, index1, index2,
                 index_vehicle1, index_trip1, index_node1, index_vehicle2, index_trip2, index_node2):
        status = 0
        if index1[0] < len(parent1_child):
            if index1[1] < len(parent1_child[index1[0]]):
                if index1[2] < len(parent1_child[index1[0]][index1[1]]):
                    if index_vehicle1 < len(parent1_child):
                        if index_trip1 < len(parent1_child[index_vehicle1]):
                            if index_node1 < len(parent1_child[index_vehicle1][index_trip1]):
                                parent1_child[index_vehicle1][index_trip1][index_node1], parent1_child[index1[0]][index1[1]][index1[2]] = parent1_child[index1[0]][index1[1]][index1[2]], parent1_child[index_vehicle1][index_trip1][index_node1]
                                status += 1

        if index2[0] < len(parent2_child):
            if index2[1] < len(parent2_child[index2[0]]):
                print(index2[1], parent2_child[index2[0]])
                if index2[2] < len(parent2_child[index2[0]][index2[1]]):
                    if index_vehicle2 < len(parent2_child):
                        if index_trip2 < len(parent2_child[index_vehicle2]):
                            if index_node2 < len(parent2_child[index_vehicle2][index_trip2]):
                                parent2_child[index_vehicle2][index_trip2][index_node2], parent2_child[index2[0]][index2[1]][index2[2]] = parent2_child[index2[0]][index2[1]][index2[2]], parent2_child[index_vehicle2][index_trip2][index_node2]
                                status += 1

        return status

    def crossover(self, parent1, parent2):
        parent1_child = [[trip.copy() for trip in vehicle] for vehicle in parent1]
        parent2_child = [[trip.copy() for trip in vehicle] for vehicle in parent2]

        index_parent_1, index_parent_2 = self.__select_nodes(parent1, parent2)
        index_vehicle1, index_trip1, index_node1 = index_parent_1
        index_vehicle2, index_trip2, index_node2 = index_parent_2

        index1 = self.utils.search_node(parent1[index_vehicle1][index_trip1][index_node1], parent1)
        index2 = self.utils.search_node(parent2[index_vehicle2][index_trip2][index_node2], parent2)

        status = self.__change(parent1_child, parent2_child, index1, index2,
                 index_vehicle1, index_trip1, index_node1, index_vehicle2, index_trip2, index_node2)

        if status == 2:
            self.population[self.active_population] = parent1_child
            self.traveled_distances_population[self.active_population] = self.utils.traveled_distances_solution_splitted(parent1_child)
            self.active_population += 1
            #print(self.active_population)
            self.population[self.active_population] = parent2_child
            self.traveled_distances_population[self.active_population] = self.utils.traveled_distances_solution_splitted(parent2_child)
            self.active_population += 1
            #print(self.active_population)

    def mutation(self, parent1_index, parent2_index):
        self.population[parent1_index], self.traveled_distances_population[parent1_index] = VND(self.population[parent1_index], self.utils, preprocess=False, traveled_distances=self.traveled_distances_population[parent1_index])
        self.population[parent2_index], self.traveled_distances_population[parent2_index] = VND(self.population[parent2_index], self.utils, preprocess=False, traveled_distances=self.traveled_distances_population[parent2_index])

    def update_base_population(self, return_better=False):
        costs = dict()

        for i in range(self.active_population):
            cost = self.utils.compute_cost(self.population[i], self.traveled_distances_population[i])
            costs[(cost, i)] = i

        costs_sorted = sorted(list(costs.keys()))

        if return_better:
            return self.population[costs[costs_sorted[i]]], self.traveled_distances_population[costs[costs_sorted[i]]]

        for i in range(self.size_population):
            self.population[i] = self.population[costs[costs_sorted[i]]]
            self.traveled_distances_population[i] = self.traveled_distances_population[costs[costs_sorted[i]]]


    def run(self):
        better_solution = None
        better_traveled_distance = None

        self.population_initialization()

        for i in range(self.num_generations):
            print(i)
            for j in range(int(self.size_population/2)): # Num childrens
                parent1_index, parent2_index = self.select_parents()

                self.crossover(self.population[parent1_index], self.population[parent2_index])

                if np.random.random() < 0.5:
                    self.mutation(parent1_index, parent2_index)


            if i == self.num_generations - 1:
                better_solution, better_traveled_distance = self.update_base_population(return_better=True)
            else:
                self.update_base_population()

            self.active_population = self.size_population


        return better_solution, better_traveled_distance



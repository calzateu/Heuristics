
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

    def crossover(self, parent1, parent2):
        parent1_child = [[trip.copy() for trip in vehicle] for vehicle in parent1]
        parent2_child = [[trip.copy() for trip in vehicle] for vehicle in parent2]

        index_vehicle1  = np.random.choice(range(len(parent1)))
        index_trip1      = np.random.choice(range(len(parent1[index_vehicle1])))
        #print('parent1', parent1[index_vehicle1][index_trip1])
        index_node1       = np.random.choice(range(len(parent1[index_vehicle1][index_trip1])))

        index_vehicle2  = np.random.choice(range(len(parent2)))
        index_trip2      = np.random.choice(range(len(parent2[index_vehicle2])))
        #print('parent2', parent2[index_vehicle2][index_trip2])
        index_node2       = np.random.choice(range(len(parent2[index_vehicle2][index_trip2])))

        index1 = self.utils.search_node(parent1[index_vehicle1][index_trip1][index_node1], parent1)
        index2 = self.utils.search_node(parent2[index_vehicle2][index_trip2][index_node2], parent2)

        parent1_child[index_vehicle1][index_trip1][index_node1], parent1_child[index1[0]][index1[1]][index1[2]] = parent1_child[index1[0]][index1[1]][index1[2]], parent1_child[index_vehicle1][index_trip1][index_node1]
        parent2_child[index_vehicle2][index_trip2][index_node2], parent2[index2[0]][index2[1]][index2[2]] = parent2_child[index2[0]][index2[1]][index2[2]], parent2[index_vehicle2][index_trip2][index_node2]

        self.population[self.active_population] = parent1_child
        self.traveled_distances_population[self.active_population] = self.utils.traveled_distances_solution_splitted(parent1_child)
        self.active_population += 1
        self.population[self.active_population] = parent2_child
        self.traveled_distances_population[self.active_population] = self.utils.traveled_distances_solution_splitted(parent2_child)
        self.active_population += 1

    def mutation(self, parent1_index, parent2_index):
        self.population[parent1_index], self.traveled_distances[parent1_index] = VND(self.population[parent1_index], self.utils)
        self.population[parent2_index], self.traveled_distances[parent2_index] = VND(self.population[parent2_index], self.utils)


    def run(self):
        self.population_initialization()

        for i in range(self.num_generations):
            for j in range(int(self.size_population/2)): # Num childrens
                parent1_index, parent2_index = self.select_parents()

                self.crossover(self.population[parent1_index], self.population[parent2_index])

                if np.random.random() < 0.5:
                    self.mutation(self, parent1_index, parent2_index)

            self.active_population = self.size_population

        #print(self.population)



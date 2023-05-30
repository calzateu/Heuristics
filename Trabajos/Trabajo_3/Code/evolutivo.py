



class AlgoritmoGeneticoHibrido:
    def __init__(self, size_population, num_generations, utils, generation_method) -> None:
        self.size_population = size_population
        self.num_generations = num_generations
        self.utils = utils
        self.generation_method = generation_method

    def population_initialization(self):
        self.population = [0]*self.size_population

        for i in range(self.size_population):
            self.population[i] = self.generation_method.search_paths(split=True)

    def run(self):
        self.population_initialization()




from ELS import *

def MS_ELS(utils, problem_information, dist_matrix, demands, max_capacity, max_distance, num_cars, num_insertions, num_relocations, num_mutations, ni=5, nc=2, nsol=5, neighborhoods=[inter_trips_2opt, two_opt_trips, brute_force_relocation], std=0.1, max_iterations=200, ruido=False):
    f_asteristo = float('inf')
    s_asterisco = None
    traveled_distances_asterisco = None

    random_generator = Noise2(problem_information, dist_matrix, demands, std=std, max_iterations=max_iterations)
    #neighborhoods = [two_opt, insertion, brute_force_relocation]
    for h in range(nsol):
        print(f'################# {h+1} #################')
        S = utils.run_method(method=random_generator, verbose=False, graph=False)
        S = split_information(S)
        traveled_distances_S = []
        for vehicle in S:
            traveled_distances_S.append(traveled_distance(vehicle, dist_matrix))

        S, traveled_distances_S = VND(S, neighborhoods, dist_matrix, demands, max_capacity, num_cars, num_insertions, num_relocations, preprocess=False, traveled_distances=traveled_distances_S, ruido=ruido)

        #if sum(traveled_distances_S) < f_asteristo:
        if utils.distance_exceed(traveled_distances_S, max_distance, num_cars) < f_asteristo:
            s_asterisco = S.copy()
            traveled_distances_asterisco = traveled_distances_S.copy()
            f_asteristo = utils.distance_exceed(traveled_distances_S, max_distance, num_cars)

        # Creo que hay un problema, se están eliminando nodos
        S_prima, traveled_distances_prima = ELS(utils, problem_information, dist_matrix,
            demands, max_capacity, max_distance, num_cars, ni, nc, neighborhoods, generate_initial_solution=False,
            solution=S, traveled_distances=traveled_distances_S,
            num_insertions=num_insertions, num_relocations=num_relocations, num_mutations=num_mutations)

        #if sum(traveled_distances_prima) < f_asteristo:
        if utils.distance_exceed(traveled_distances_prima, max_distance, num_cars) < f_asteristo:
            s_asterisco = S_prima.copy()
            traveled_distances_asterisco = traveled_distances_prima.copy()
            f_asteristo = utils.distance_exceed(traveled_distances_S, max_distance, num_cars)

    return s_asterisco, traveled_distances_asterisco

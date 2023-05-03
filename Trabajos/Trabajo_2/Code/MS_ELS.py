from ELS import *


def MS_ELS(utils, problem_information, dist_matrix, demands, max_capacity, max_distance, num_insertions, num_relocations, ni=5, nc=2, nsol=5, std=0.1, max_iterations=200):
    f_asteristo = float('inf')
    s_asterisco = None
    traveled_distances_asterisco = None

    random_generator = Noise2(problem_information, dist_matrix, demands, std=std, max_iterations=max_iterations)
    neighborhoods = [two_opt, insertion, brute_force_relocation]
    for h in range(nsol):
        print(f'################# {h+1} #################')
        S = utils.run_method(method=random_generator, verbose=False, graph=False)
        S = split_information(S)
        traveled_distances_S = []
        for path in S:
            traveled_distances_S.append(traveled_distance(path, dist_matrix))

        S, traveled_distances_S = VND(S, neighborhoods, dist_matrix, demands, max_capacity, num_insertions, num_relocations, preprocess=False, traveled_distances=traveled_distances_S)

        #if sum(traveled_distances_S) < f_asteristo:
        if distance_exceed(traveled_distances_S, max_distance) < f_asteristo:
            s_asterisco = S.copy()
            traveled_distances_asterisco = traveled_distances_S.copy()
            f_asteristo = distance_exceed(traveled_distances_S, max_distance)

        # Creo que hay un problema, se están eliminando nodos
        S_prima, traveled_distances_prima = ELS(utils, problem_information, dist_matrix,
            demands, max_capacity, max_distance, ni, nc, generate_initial_solution=False,
            solution=S, traveled_distances=traveled_distances_S,
            num_insertions=num_insertions, num_relocations=num_relocations)

        #if sum(traveled_distances_prima) < f_asteristo:
        if distance_exceed(traveled_distances_prima, max_distance) < f_asteristo:
            s_asterisco = S_prima.copy()
            traveled_distances_asterisco = traveled_distances_prima.copy()
            f_asteristo = distance_exceed(traveled_distances_S, max_distance)

    return s_asterisco, traveled_distances_asterisco

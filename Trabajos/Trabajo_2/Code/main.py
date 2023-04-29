# Used libraries
import os


# My modules
from utils import Utils
from neighborhoods import *

if __name__ == '__main__':

    utils = Utils()

    folder_path = "../../mtVRP Instances"
    folder_path = os.path.abspath(folder_path)
    file = folder_path + '/mtVRP1.txt'

    utils.read_data(file_name=file)
    dist_matrix = utils.compute_distances()

    #solutions = utils.read_solutions('../../Trabajo_1/Code/mtVRP_Cristian_Alzate_Urrea_constructivo.xlsx')
    solutions = utils.read_solutions('../../Trabajo_1/Code/mtVRP_Cristian_Alzate_Urrea_Noise.xlsx')
    neighborhoods = [two_opt]

    #utils.apply_VND_all_instances(solutions)
    trips, traveled_distances = utils.VND(solutions['mtVRP1.txt'], neighborhoods, dist_matrix)

    print()
    print(trips, traveled_distances)

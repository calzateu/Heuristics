# Used libraries
import os


# My modules
from utils import Utils

if __name__ == '__main__':

    utils = Utils()
    solutions = utils.read_solutions('../../Trabajo_1/Code/mtVRP_Cristian_Alzate_Urrea_Noise.xlsx')

    print(solutions['mtVRP1.txt'])
# Used libraries
import os


# My modules
from constructive3 import ConstructiveMethod3
from GRASP3 import GRASP3
from noise2 import Noise2

from utils import Utils

if __name__ == '__main__':

    utils = Utils()
    solutions = utils.read_solutions('../../Trabajo_1/Code/mtVRP_Cristian_Alzate_Urrea_Noise.xlsx')

    print(solutions['mtVRP1.txt'])
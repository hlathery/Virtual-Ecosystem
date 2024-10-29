from Test_Gen import *
import random

# The order of weight values for each terrain type:
#WEIGHTS = [WEIGHT_OCEAN3, WEIGHT_OCEAN2, WEIGHT_OCEAN1, WEIGHT_BEACH, WEIGHT_GRASS, WEIGHT_FOREST]
WEIGHTS = [20, 15, 15, 15, 50, 50]     # Lakes

rand_seed = random.randint(0,1000)
test_generate_world(WEIGHTS, random_seed = rand_seed)
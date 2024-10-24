from World import World
from World_Drawer import *
from Util import *


def test_generate_world(weights, random_seed):
    world = World(WORLD_X, WORLD_Y, random_seed)
    tile_map = world.get_tiled_map(weights)
    world_drawer = WorldDrawer(tile_map)
    world_drawer.draw()


def test_emerge(target_weights, random_seed):
    world_drawer = WorldDrawer()
    world = World(WORLD_X, WORLD_Y, random_seed)
    weights = [target_weights[OCEAN3] - 1, 0, 0, 0, 0, 0]
    done = False

    while not done:
        tile_map = world.get_tiled_map(weights)
        world_drawer.draw(tile_map)

        if weights[OCEAN3] < target_weights[OCEAN3]:
            weights[OCEAN3] += 1
        elif weights[OCEAN2] < target_weights[OCEAN2]:
            weights[OCEAN2] += 1
        elif weights[OCEAN1] < target_weights[OCEAN1]:
            weights[OCEAN1] += 1
        elif weights[BEACH] < target_weights[BEACH]:
            weights[BEACH] += 1
        elif weights[GRASS] < target_weights[GRASS]:
            weights[GRASS] += 1
        elif weights[FOREST] < target_weights[FOREST]:
            weights[FOREST] += 1
        else:
            done = True

    done = False
    target_weights = [weights[OCEAN3] - 1, 0, 0, 0, 0, 0]

    while not done:
        tile_map = world.get_tiled_map(weights)
        world_drawer.draw(tile_map)

        if weights[FOREST] >= target_weights[FOREST] and weights[FOREST] > 0:
            weights[FOREST] -= 1
        elif weights[GRASS] >= target_weights[GRASS] and weights[GRASS] > 0:
            weights[GRASS] -= 1
        elif weights[BEACH] >= target_weights[BEACH] and weights[BEACH] > 0:
            weights[BEACH] -= 1
        elif weights[OCEAN1] >= target_weights[OCEAN1] and weights[OCEAN1] > 0:
            weights[OCEAN1] -= 1
        elif weights[OCEAN2] >= target_weights[OCEAN2] and weights[OCEAN2] > 0:
            weights[OCEAN2] -= 1
        elif weights[OCEAN3] >= target_weights[OCEAN3] and weights[OCEAN3] > 0:
            weights[OCEAN3] -= 1
        else:
            done = True
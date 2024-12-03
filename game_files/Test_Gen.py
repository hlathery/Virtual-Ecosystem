from World import World
from World_Drawer import *
from Util import *
from dotenv import load_dotenv

load_dotenv()

def test_generate_world(weights, random_seed):
    world = World(WORLD_X, WORLD_Y, random_seed)
    tile_map = world.get_tiled_map(weights)
    
    # add count biomes
    biome_counts = world.count_biomes(tile_map)
    print("Biome counts:", biome_counts)
    
    try:
         # Get token from .env file
        access_token = os.getenv('API_KEY')
        
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "access_token": access_token  # Using token from .env
        }
        
        # Transform the counts to match expected format
        formatted_counts = {
            "ocean": biome_counts.get('Ocean', 0),
            "forest": biome_counts.get('Forest', 0),
            "grassland": biome_counts.get('Grassland', 0),
            "beach": biome_counts.get('Beach', 0)
        }
        
        url = "http://127.0.0.1:3000/eco/biomes/"
        print(f"Sending request to: {url}")
        
        response = requests.post(
            url,
            json=formatted_counts,  # Use formatted counts instead of original
            headers=headers
        )
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            print("Successfully posted biome counts to database")
        else:
            print(f"Failed to post biome counts: {response.status_code}")
    except Exception as e:
        print(f"Error posting biome counts: {e}")
    
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
    
    
from perlin_noise import PerlinNoise
from Util import *
import requests
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import os

class World():

    def __init__(self, size_x, size_y, random_seed):
        self.generate_noisemap(size_x, size_y, random_seed)

        # Get min and max noise values
        flat_list = [item for sublist in self.noise_map for item in sublist]
        self.min_value = min(flat_list)
        self.max_value = max(flat_list)


    def generate_noisemap(self, size_x, size_y, random_seed):
        self.noise_map = []

        noise1 = PerlinNoise(octaves=3, seed=random_seed)
        noise2 = PerlinNoise(octaves=6, seed=random_seed)
        noise3 = PerlinNoise(octaves=12, seed=random_seed)
        noise4 = PerlinNoise(octaves=24, seed=random_seed)

        xpix, ypix = size_x + 1, size_y + 1
        for j in range(ypix):
            row = []
            for i in range(xpix):
                noise_val = noise1([i/xpix, j/ypix])
                noise_val += 0.5 * noise2([i/xpix, j/ypix])
                noise_val += 0.25 * noise3([i/xpix, j/ypix])
                noise_val += 0.125 * noise4([i/xpix, j/ypix])
                row.append(noise_val)
            self.noise_map.append(row)


    def get_noise_map(self):
        return self.noise_map


    def get_tiled_map(self, weights):
        total_weights = sum(weights)
        total_range = self.max_value - self.min_value

        # calculate maximum height for each terrain type, based on weight values
        max_terrain_heights = []
        previous_height = self.min_value
        for terrain_type in ALL_TERRAIN_TYPES:
            height = total_range * (weights[terrain_type] / total_weights) + previous_height
            max_terrain_heights.append(height)
            previous_height = height
        max_terrain_heights[FOREST] = self.max_value

        map_int = []

        for row in self.noise_map:
            map_row = []
            for value in row:
                for terrain_type in ALL_TERRAIN_TYPES:
                    if value <= max_terrain_heights[terrain_type]:
                        map_row.append(terrain_type)
                        break

            map_int.append(map_row)

        return map_int


    def count_biomes(self, tile_map):
        visited = set()
        biome_counts = {
            "ocean": 0,
            "beach": 0,
            "grassland": 0,
            "forest": 0
        }
        
        MIN_BIOME_SIZES = { # our bounds
            "ocean": 20,   
            "beach": 100,   
            "grassland": 300,
            "forest": 30       
        }
        
        def get_biome_name(tile_type):
            if tile_type in [OCEAN1, OCEAN2, OCEAN3]: 
                return "ocean"
            elif tile_type == BEACH:
                return "beach"
            elif tile_type == GRASS:
                return "grassland"
            elif tile_type == FOREST:
                return "forest"
        
        def flood_fill(start_x, start_y, target_type):
            v = []
            stack = [(start_x, start_y)]
            region_size = 0
            
            if (start_x, start_y) in visited:
                return 0
            
            while stack:
                x, y = stack.pop()
                
                if (x < 0 or x >= len(tile_map[0]) or 
                    y < 0 or y >= len(tile_map) or
                    (x, y) in visited):
                    continue
                    
                current_type = tile_map[y][x]
                
                
                if target_type in [OCEAN1, OCEAN2, OCEAN3]:
                    if current_type not in [OCEAN1, OCEAN2, OCEAN3]:
                        continue
                elif current_type != target_type:
                    continue
                    
                visited.add((x, y))
                v.append((x,y))
                region_size += 1
                
                # Check all 8 directions
                directions = [
                    (x+1, y), (x-1, y), (x, y+1), (x, y-1),
                    (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)
                ]
                
                for next_x, next_y in directions:
                    stack.append((next_x, next_y))
            
            return region_size, v

        
        order = []
        for y in range(len(tile_map)):
            for x in range(len(tile_map[0])):
                if (x, y) not in visited:
                    current_type = tile_map[y][x]
                    biome_name = get_biome_name(current_type)
                    if biome_name:
                        size, ord = flood_fill(x, y, current_type)
                        if size >= MIN_BIOME_SIZES[biome_name]:
                            order.append({"biome":biome_name,"order":ord})
                            biome_counts[biome_name] += 1
        res = requests.post("http://127.0.0.1:3000/eco/biomes/", json=biome_counts, headers={"accept": "application/json", "access_token": "hlath", "Content-Type": "application/json"})
        return order
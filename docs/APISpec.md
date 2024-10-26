# API Specification for Virtual Ecosystem

## 1. Village

All API calls for entities of the village.

### 1 /Village/ (GET) <--- Village overview 

Response: 

{ 

“num_buildings”: int,  

“num_villagers”: int, 

“storage.amount”: int 

} 

### 1.2. `village/villagers/` (GET)

Returns a list of all villagers with their respective attributes.

### 1.3. /new_villager/ (POST) <--- Creates a new villager, unassigned 

Request: 
[{ 

“Name”:  string, 

“ID”: int, 

“age”: int, 

“nourishment”: string 

}] 

Response:  

{“success”: boolean} 

### 1.4. Village/villagers_all/ (GET)  <--- returns all villagers across the village 

Response: 

[{ 

“ID”: int, 

“Name”: string, 

“age”: int, 

“nourishment”: string, 

“job_id”: int, 

“building_id”: int 

}] 

### 1.5. Village/buildings/villagers (GET) <--- returns all villagers in a building 

Request: 

{“building_id”: int} 

 

Response: 

[{ 

“villager.ID”: int, 

“villager. Name”: string, 

“villager. age”: int, 

“villager. nourishment”: string, 

“villager. job_id”: int, 

}] 

AND 

The total number of villagers 

### 1.6. Village/assign_villager/ (PUT) <--- assigns villager job and building 

Request: 

[{ 

“villager.ID”: int  

}] 

Response: 

[{ 

“villager_ID”: int, 

“villager_job_id”: int, 

“villager_building_id”: int 

}] 

### 1.7. /village/build_building/ (POST) 

Request: 

[{ 

“resource_name”: string, 

“amount”: int 

“building_id”: int 

 

}] 

Response: 

{“success”: boolean} 

### 1.8. /village/fill_inventory/ (PUT) <--- fill inventory of specific building

Request: 

[{ 

“building_storage_id”: int, 

“resource_name”: string, 

“amount”: int 

}] 

Response: 

{“success”: boolean} 

### 1.9 /village/building_inventory/ (GET) <--- gets inventory of that specific building 

Request: 

{“building_id”: int} 

Response: 

[{ 

“resource_name”: string, 

“amount”: int 

}] 

### 1.9.1 /village/village_inventory/ (GET) <--- gets inventory across all buildings 
Response: 

[{ 

“resource_name”: string, 

“amount”: int 

}] 


## 2. Eco

All API calls for the ecosystem.

### 2.1. /eco/grow_trees/ (PUT) <--- used for planting seeds

Request: 

[{ 

“resource_name": string (takes seeds) 

“amount”: int, 

“biome_id”: int 

}] 

Response: 

{“success”: boolean} 

### 2.2. /eco/trees/ (GET)  

Response: 

[{ 

“plant_id”: int, 

“amount”: int 

}] 

### 2.3. `eco/life/prey/` (GET)

Response: 

[{ 

“plant_id”: int, 

“amount”: int 

}] 

### 2.4. /eco/grow_plants/ (PUT) <--- used for planting seeds 

Request: 

[{ 

“resource_name": string (takes seeds) 

“amount”: int, 

“biome_id”: int 

}] 

Response: 

{“success”: boolean} 

/eco/plants/ (GET)  

Response: 

[{ 

“plant_id”: int, 

“amount”: int 

}] 

### 2.5. /eco/grab_water/ (PUT) <--- villagers will collect water as needed 

Request: 

[{ 

“water_id”: int, // (which water source it came from) 

“amount”: int, 

“nourishment”: string, // (how clean is this water?) 

“biome_id”: int 

}] 

 
Response: 

{“success”: boolean} 

### 2.6 /eco/spawn_prey/ (POST) <--- spawning prey to a specific biome, worth noting this call can also reduce the number of prey (maybe they died due to nourshiment or killed off by hunters/predators 

Request: 

[{ 

“prey_id”: int, 

“nourishment”: string, 

“amount”: int, 

“biome_id”: int 

}] 

Response: 

{“success”: boolean} 

### 2.7 /eco/prey/ (GET) <--- grabbing prey given a specific biome

Request: 

[{ 

“biome_id”: int 

}] 

Response: 

[{ 

“prey_id”: int, 

“amount”: int 

}] 

### 2.8 /eco/spawn_predator/ (POST) <--- spawning predator to a specific biome, worth noting this call can also reduce the number of prey (maybe they died due to nourshiment or killed off by hunters/predators 

Request: 

[{ 

“predator_id”: int, 

“nourishment”: string, 

“amount”: int, 

“biome_id”: int 

}] 

Response: 

{“success”: boolean} 

### 2.9 /eco/ predator/ (GET) <--- grabbing predator given a specific biome 

Request: 

[{ 

“biome_id”: int 

}] 

Response: 

[{ 

“predator_id”: int, 

“amount”: int 

}] 

## 3. Admin

Used for resseting the game

### 3.1. /admin/reset (PUT) <--- resets everything to original start of the game state 

Response: 

{“success”: boolean} 

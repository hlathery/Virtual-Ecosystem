# API Specification for Virtual Ecosystem

## 1. Village

All API calls for entities of the village.

### 1.1. Village Overview - `/village/` (GET)
Returns an overview of the village

**Response:**

```json
    { 
        "num_buildings": "int",  
        "num_villagers": "int", 
        "storage_amount": "int" 
    } 
```

### 1.2. Create villager - `/new_villager/` (POST)
Creates a new villager, unassigned 

**Request:** 
```json
[
    { 
        "name":  "string", 
        "id": "int", 
        "age": "int",
        "nourishment": "string" 
    }
] 
```

**Response:**  

```json
    {
        "success": "boolean"
    }
``` 

### 1.3. All villagers - `village/villagers_all/` (GET) 
Returns a list of all villagers with their respective attributes.

**Response:** 

```json
[
    { 
        "id": "int", 
        "name": "string", 
        "age": "int", 
        "nourishment": "string", 
        "job_id": "int", 
        "building_id": "int" 
    }
]
```

### 1.4. Villagers in building - `village/buildings/villagers` (GET) 
Returns all villagers in a building

**Request:**

```json
{
    "building_id": "int"
} 
```

**Response:** 

```json
[
    { 
        "villager_id": "int", 
        "villager_name": "string", 
        "villager_age": "int", 
        "villager_nourishment": "string", 
        "villager_job_id": "int", 
    }
]
```  

### 1.5. Build structure - `/village/build_building/` (POST) 

**Request:** 

```json
[
    { 
        "resource_name": "string", 
        "amount": "int",
        "building_id": "int" 
    }
]
``` 

**Response:**

```json
{
    "success": "boolean"
}
``` 

### 1.6. Adjust storage `/village/fill_inventory/` (PUT) 
Fill inventory of specific building(s)

**Request:** 

```json
[
    { 
        "building_storage_id": "int", 
        "resource_name": "string", 
        "amount": "int" 
    }
]
```

**Response:** 

```json
{
    "success": "boolean"
}
``` 

### 1.7. View building inventory - `/village/building_inventory/` (GET)
Gets inventory of specific building  

**Request:** 

```json
{
    "building_id": "int"
}
``` 

**Response:** 

```json
[
    { 
        "resource_name": "string", 
        "amount": "int" 
    }
]
``` 

### 1.8. View village inventory `/village/village_inventory/` (GET) 
Gets inventory across all buildings

**Response:** 

```json
[
    { 
        "resource_name": "string", 
        "amount": "int" 
    }
] 
```

## 2. Eco

All API calls for the ecosystem.

### 2.1. Plant seed - `/eco/grow_plants/` (PUT)
Allows the user to plant seeds for trees and plants

**Request:** 

```json
[
    { 
        "resource_name": "string", 
        "amount": "int", 
        "biome_id": "int" 
    }
]
```

**Response:** 

```json
{
    "success": "boolean"
}
``` 

### 2.2. View plants - `/eco/trees/` (GET)  

**Response:** 

```json
[
    { 
        "plant_id": "int", 
        "amount": "int" 
    }
]
``` 

### 2.3. View prey -`eco/life/prey/` (GET)
View overall prey(?)

**Response:** 

```json
[
    { 
        "prey_id": "int", 
        "amount": "int" 
    }
] 
```

### 2.4. Collect water - `/eco/grab_water/` (PUT) 

Allows user to collect water as needed for village

**Request:** 

```json
[
    { 
        "water_id": "int", // (which water source it came from) 
        "amount": "int", 
        "nourishment": "string", // (how clean is this water?) 
        "biome_id": "int" 
    }
] 
```

**Response:** 

```json
{
    "success": "boolean"
}
``` 

### 2.5. Spawn prey - `/eco/spawn_prey/` (POST)
Spawning prey to a specific biome, worth noting this call can also reduce 
the number of prey (maybe they died due to nourshiment or killed off by hunters/predators) 

**Request:** 

```json
[
    { 
        "prey_id": "int", 
        "nourishment": "string", 
        "amount": "int", 
        "biome_id": "int" 
    }
]
``` 

**Response:** 

```json
{
    "success": "boolean"
}
``` 

### 2.6. View prey in biome -`/eco/prey/` (GET)
Grabbing prey given a specific biome

**Request:** 

```json
[
    { 
        "biome_id": "int" 
    }
]
``` 

**Response:** 

```json
[
    { 
        "prey_id": "int", 
        "amount": "int" 
    }
]
``` 

### 2.7. Spawn predator -`/eco/spawn_predator/` (POST)
Spawning predator to a specific biome, worth noting this call can also reduce
the number of prey (maybe they died due to nourshiment or killed off by hunters/predators)

**Request:** 

```json
[
    { 
        "predator_id": "int", 
        "nourishment": "string", 
        "amount": "int", 
        "biome_id": "int" 
    }
]
```

**Response:** 

```json
{
    "success": "boolean"
}
``` 

### 2.8. View predators - `/eco/predator/` (GET)
View total amount predators in a specific biome 

**Request:** 

```json
[
    { 
        "biome_id": "int" 
    }
]
```

**Response:** 

```json
[
    { 
        "predator_id": "int", 
        "amount": "int" 
    }
] 
```

## 3. Assignments

Used for assigning jobs

### 3.1. Get job list - `assignments/get_job_list` (GET)

**Response:**

```json
[
    {
        "job_title" : "string",
        "villagers_assigned" : "int"
    }
]
```

### 3.2. Assign job - `assignments/assign_villager/` (PUT)

**Request:** 

```json
[
    { 
        "villager_id": "int"  
    }
]
``` 

**Response:** 

```json
[
    { 
        "villager_id": "int", 
        "villager_job_id": "int", 
        "villager_building_id": "int" 
    }
]
``` 


## 4. Admin

Used for resseting the game

### 4.1. Reset World - `/admin/reset` (PUT) 
Resets everything to original start of the game state 

**Response:** 

```json
{
    "success": "boolean"
}
``` 

# API Specification for Virtual Ecosystem

## 1. Village

All API calls for entities of the village.

### 1.1. Village Overview - `/village/` (GET)
Returns an overview of the village

**Response:**

```json
    { 
        "num_buildings": "int",  
        "num_villagers": "int"
    } 
```

### 1.2. Create villager - `/villager` (POST)
Creates a new villager, unassigned 

**Request:** 
```json
[
    { 
        "age": "int",
        "nourishment": "int" 
    }
] 
```

**Response:**  

```json
    {
        "Villager(s) successfully created"
    }
``` 

### 1.3 Remove villager - `/villager` (DELETE)
Kills the oldest amount of villagers depending on amount passed in

**Request:** 
```json
[
    { 
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


### 1.4. Build structure - `/village/build_building` (POST) 

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

### 1.5. Adjust storage `/village/fill_inventory` (PUT) 
Fill inventory of specific building(s)

**Request:** 

```json
[
    { 
        "building_id": "int", 
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

### 1.6. View village inventory `/village/village_inventory/` (GET) 
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

### 2.1. Ecosystem Overview - `/eco/` (POST)

Returns all biomes with their respective entities and entity nourishment

**Response**

```json
[
    {
        "biome_id": int,
        "biome_name": string,
        "entities": [{"name": string, "nourishment": int}]
    }
]

```
(Complex)
### 2.2. Posts Biomes `/eco/biomes/`
A flood fill search algorithm is ran when the map is created. The results are sent to this endpoint.

**Request**
```json
{
  "ocean": int,
  "forest": int,
  "grassland": int,
  "beach": int
}
```

**Response**

```
{
  "message": "Biome counts recorded successfully"
}
```

### 2.3. View plants - `/eco/plants/` (GET)  

Grabs the total sum nourishment of plants of the entire ecosystem

**Response:** 

```json
[
    { 
        "entity_type": "string", 
        "nourishment": "int" 
    }
]
``` 
 

### 2.4. Spawn entity - `/eco/entity` (POST)
Spawns entities to a specific biome. User controls plants, predators, prey, and trees to spawn.

**Request:** 

```json
[
    { 
        "nourishment": "int",
        "entity_type": "string",
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

### 2.5 Updates Nourishment - `/entity/nourishment` (PUT)
Updates nourishment given the entity id

**Request**

```json
[
  {
    "id": int,
    "nourishment": int
  }
]
``` 

**Response:** 

```json
{
  "message": "Nourishment updated successfully"
}
``` 

### 2.5. View prey in biome -`/eco/prey/{biome_id}` (GET)
Grabbing nourishment of prey given a specific biome

**Response:** 

```json
[
    { 
        "entity_type": "string",
        "nourishment": "int" 
    }
]
``` 

### 2.6. View predators - `/eco/predator/{biome_id}` (GET)
Grabbing nourishment of predators given a specific biome 

**Response:** 

```json
[
    { 
        "entity_type": "string",
        "nourishment": "int" 
    }
] 
```

## 3. Jobs

Used for assigning jobs

### 3.1. Get job list - `jobs/` (GET)

**Response:**

```json
[
    {
        "job_name" : "string",
        "villagers_assigned" : "int"
    }
]
```

### 3.2. Assign job - `jobs/assignments` (PUT)

**Request:** 

```json
[
    {   
        "job_name": "string",
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

### 5.1. Reset World - `/admin/reset` (PUT) 
Resets everything to original start of the game state 

**Response:** 

```json
{
    "success": "boolean"
}
``` 

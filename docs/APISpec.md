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
        "name":  "string", 
        "id": "int", 
        "age": "int",
        "nourishment": "int" 
    }
] 
```

**Response:**  

```json
    {
        "success": "boolean"
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

### 2.1. Plant seed - `/eco/grow_plants` (PUT)
Allows the user to plant seeds for trees and plants

**Request:** 

```json
[
    { 
        "quantity": "int",
        "nourishment": "int",
        "entity_type": "string", /* Should be "plants" */
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

### 2.2. View plants - `/eco/plants/` (GET)  

**Response:** 

```json
[
    { 
        "entity_type": "string", /* Should be "plants" */
        "quantity": "int" 
    }
]
``` 

### 2.3. Collect water - `/eco/grab_water` (PUT) 

Allows user to collect water as needed for village

**Request:** 

```json
[
    { 
        "water_id": "int", 
        "amount": "int", 
        "nourishment": "int",
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

### 2.4. Spawn entity - `/eco/entity` (POST)
Spawning entities to a specific biome, worth noting this call can also reduce 
the number of entities (maybe they died due to nourshiment or killed off by hunters/predators) 

**Request:** 

```json
[
    { 
        "quantity": "int",
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

### 2.5. View prey in biome -`/eco/prey/{biome_id}` (GET)
Grabbing prey given a specific biome

**Response:** 

```json
[
    { 
        "entity_type": "string", /* Should be "prey" */ 
        "amount": "int" 
    }
]
``` 

### 2.6. View predators - `/eco/predator/{biome_id}` (GET)
View total amount predators in a specific biome 

**Response:** 

```json
[
    { 
        "entity_type": "string", /* Should be "predator" */ 
        "amount": "int" 
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
        "job_title" : "string",
        "villagers_assigned" : "int"
    }
]
```

### 3.2. Assign job - `jobs/assignments` (PUT)

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

## 4. Info

Grabs information about the game world

### 4.1. Get Time - `/info/current_time/` (GET)

**Response:**

```json
{
    "year" : "int",
    "month" : "int",
    "day" : "int"
}
```

## 5. Admin

Used for resseting the game

### 5.1. Reset World - `/admin/reset` (PUT) 
Resets everything to original start of the game state 

**Response:** 

```json
{
    "success": "boolean"
}
``` 

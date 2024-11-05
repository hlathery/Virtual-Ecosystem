# Example workflow

## User Assigning Villager Jobs

When a user realizes that their village's food source is beginning to dwindle, they find this by calling `GET village/inventory/`,which gives a list of village resources.
They realize that they need to assign villagers to hunt and gather food to keep their village alive. The user will call `GET assignments/` to see a list of all jobs available and the amount of villagers in each.
After noticing there is a low number of villagers in forager and hunter jobs. They do the following:

- `POST assignments/plan`. And the user will be prompted to return the json for the new amount of villagers in each job so they increase the amount of villagers in the "forager" and "hunter" jobs “villagers_assigned”, and the correct amount of villagers will be allocated to each job

After this is completed, the villagers will successfully increase the amount of resources available to keep their villagers alive and ‘PUT village/new_villager’ along with ‘POST /village/kill_villager’ will be called to populate the village more or less respectively to that we can assign new villagers made to villager’s jobs that have died.

# Testing results
## Step 1: Calling "GET village/village_inventory"


1. curl -X 'POST' \
 'http://127.0.0.1:3000/village/village_inventory' \
 -H 'accept: application/json' \
 -H 'access_token: hlath' \
 -d ''
2. {
   "Wood": 100,
   "Food": 50,
   "Water": 50
  }


## Step 2: Calling "GET assignments/"


1. curl -X 'GET' \
 'http://127.0.0.1:3000/assignments/' \
 -H 'accept: application/json' \
 -H 'access_token: hlath'


2. [
 {
   "job_id": 2,
   "job_title": "forager",
   "villagers_assigned": 0
 },
 {
   "job_id": 3,
   "job_title": "farmer",
   "villagers_assigned": 0
 },
 {
   "job_id": 5,
   "job_title": "lumberjack",
   "villagers_assigned": 0
 },
 {
   "job_id": 4,
   "job_title": "butcher",
   "villagers_assigned": 0
 },
 {
   "job_id": 6,
   "job_title": "miner",
   "villagers_assigned": 0
 },
 {
   "job_id": 0,
   "job_title": "unassigned",
   "villagers_assigned": 2
 },
 {
   "job_id": 1,
   "job_title": "hunter",
   "villagers_assigned": 0
 }
]


## Step 3: Calling "POST assignments/plan"


1. curl -X 'POST' \
 'http://127.0.0.1:3000/assignments/plan' \
 -H 'accept: application/json' \
 -H 'access_token: hlath' \
 -H 'Content-Type: application/json' \
 -d '[
 {
   "job_id": 2,
   "job_title": "forager",
   "villagers_assigned": 1
 },
 {
   "job_id": 3,
   "job_title": "farmer",
   "villagers_assigned": 0
 },
 {
   "job_id": 5,
   "job_title": "lumberjack",
   "villagers_assigned": 0
 },
 {
   "job_id": 4,
   "job_title": "butcher",
   "villagers_assigned": 0
 },
 {
   "job_id": 6,
   "job_title": "miner",
   "villagers_assigned": 0
 },
 {
   "job_id": 0,
   "job_title": "unassigned",
   "villagers_assigned": 0
 },
 {
   "job_id": 1,
   "job_title": "hunter",
   "villagers_assigned": 1
 }
]'


2. "OK"
## Step 4: ‘PUT village/new_villager’
1. curl -X 'PUT' \
  'http://127.0.0.1:3000/village/new_villager' \
  -H 'accept: application/json' \
  -H 'access_token: hlath' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "job_id": 0,
    "age": 20,
    "nourishment": 100
  }
]'
2. [
  "Villager(s) successfully created"
]
## Step 5: ‘POST /village/kill_villager’
1. curl -X 'POST' \
  'http://127.0.0.1:3000/village/kill_villager?amount=2' \
  -H 'accept: application/json' \
  -H 'access_token: hlath' \
  -d ''
2. “OK”



# User expanding village
When a user has the need to build new buildings to increase production of a certain resource or provide more jobs to villagers, the user would start by calling `GET /village/` to get a general overview of building types, the amount of each building that there is, and the total population of the village.

Say the user sees that there are no Hunter/Forager Huts or Farms that are producing food for the village and a few villagers unassigned to a job, so they feel the need to build these buildings. They would then call `GET village/catalog` to see all available buildings to build, their costs, and the amount of funds they have to build buildings.

Once they have indicated how much of each building to build, their list of buildings to build gets passed to the `POST /village/build_building` and this updates the buildings table to reflect the new number of each building after the new ones are built. In this case we now have 1 Town Hall, 1 Villager Hut, 1 Farm, and 1 Hunter/Forager Hut.

Then, `POST /village/fill_inventory` is called to update the amount of resources after they have been spent on the buildings. In this case we now have 25 wood in total after 75 wood was spent.

# Testing Results
## Step 1: Calling ‘GET /village/’
1. curl -X 'GET' \
  'http://127.0.0.1:3000/village/' \
  -H 'accept: application/json' \
  -H 'access_token: hlath'
2. {
  "buildings": [
    "Town Hall",
    "Farm",
    "Lumber Mill",
    "Mine",
    "Villager Hut",
    "Hunter/Forager Hut"
  ],
  "num_buildings": [
    1,
    0,
    0,
    0,
    1,
    0
  ],
  "num_villager": 4
}
## Step 2: Calling ‘GET /village/catalog’
1. curl -X 'GET' \
  'http://127.0.0.1:3000/village/catalog' \
  -H 'accept: application/json' \
  -H 'access_token: hlath'
2. {
  "buildings": [
    "Villager Hut",
    "Hunter/Forager Hut",
    "Farm",
    "Lumber Mill",
    "Mine"
  ],
  "costs": [
    30,
    35,
    40,
    25,
    25
  ],
  "funds": 100
}
## Step 3: Calling ‘POST /village/build_building’
1. curl -X 'POST' \
  'http://127.0.0.1:3000/village/build_building' \
  -H 'accept: application/json' \
  -H 'access_token: hlath' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "quantity": 1,
    "building_name": "Hunter/Forager Hut"
  },
  {
    "quantity": 1,
    "building_name": "Farm"
  }
]'
2. “OK”
## Step 4: Calling ‘POST /village/fill_inventory’
1. curl -X 'PUT' \
  'http://127.0.0.1:3000/village/fill_inventory' \
  -H 'accept: application/json' \
  -H 'access_token: hlath' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "resource_name": "wood",
    "amount": -75
  }
]'
2. "Success"

# User prey and predators
When a user sees that the nourishment of biome 1 (identified by biome_id) is dwindling and needs to see the status of each entity (plants, prey, predators) in that biome ecosystem, the user would start by calling `GET/eco/prey/{biome_id}` and `POST/eco/predators{biome_id}` to get an overview of that biome’s prey and predators.

Say the user sees that the nourishment of the forest biome is low because they have over hunted the prey, leaving the amount of predators to decline as a result (as they are out of food). The user wants to raise the nourishment level to prevent the destruction and extinction of the biome (when nourishment = 0). The user would then call `POST eco/spawn_prey` and `POST eco/spawn_predator` specifying the biome in the request body. Note that the user is limited to spawn a quantity of 10 (which provides a nourishment of 10, which maxes out at 100) per entity per decision year. 

# Testing Results
## Step 1: Calling ‘POST/eco/prey/{biome_id}’
1. curl -X 'GET' \
  'http://127.0.0.1:3000/eco/prey/1' \
  -H 'accept: application/json' \
  -H 'access_token: hlath'
2. {
  "entity_type": "prey",
  "amount": 29
}

## Step 2: Calling ‘POST/eco/predator/{biome_id}’
1. curl -X 'GET' \
  'http://127.0.0.1:3000/eco/predator/1' \
  -H 'accept: application/json' \
  -H 'access_token: hlath'
2. {
  "entity_type": "predator",
  "amount": 25
}

## Step 3: Calling ‘POST eco/spawn_prey’
1. curl -X 'POST' \
  'http://127.0.0.1:3000/eco/spawn_prey' \
  -H 'accept: application/json' \
  -H 'access_token: hlath' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "quantity": 10,
    "nourishment": 10,
    "entity_type": "prey",
    "biome_id": 1
  }
]'

2. "OK"

## Step 4: Calling ‘POST eco/spawn_prey’
1. curl -X 'POST' \
  'http://127.0.0.1:3000/eco/spawn_predator/' \
  -H 'accept: application/json' \
  -H 'access_token: hlath' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "quantity": 10,
    "nourishment": 10,
    "entity_type": "predator",
    "biome_id": 1
  }
]'

2. "OK"

# User Controlling Plants
The user sees that the nourishment of the entire ecosystem (all biomes) is low, but the amount of prey and predators are relatively high. First the user would need to see the status of plants in the ecosystem, so they would need to call `GET eco/plants/` which would return an overview of all plants in the ecosystem.

Say the user wants to plant seeds in each biome to increase the amount of overall plants and raise the plant nourishment of each biome. The user would call `PUT eco/grow_plants` which takes in a list of plants to be planted in the given biome. The user is limited to planting 10 seeds, which increases the plant nourishment in that biome by 10, which maxes out at 100.
# Testing Results
## Step 1: Calling ‘GET eco/plants'
1. curl -X 'GET' \
  'http://127.0.0.1:3000/eco/plants/' \
  -H 'accept: application/json' \
  -H 'access_token: hlath'

2. [
  {
    "entity_type": "plants",
    "quantity": 210
  }
]

## Step 2: Calling ‘PUT eco/grow_plants’
1. curl -X 'PUT' \
  'http://127.0.0.1:3000/eco/grow_plants' \
  -H 'accept: application/json' \
  -H 'access_token: hlath' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "quantity": 10,
    "nourishment": 10,
    "entity_type": "plants",
    "biome_id": 1
  },
  {
    "quantity": 10,
    "nourishment": 10,
    "entity_type": "plants",
    "biome_id": 2
  }
]'
2. "OK"

## Step 3: Calling ‘POST /eco/biome/’
1. curl -X 'POST' \
  'http://127.0.0.1:3000/eco/biomes/' \
  -H 'accept: application/json' \
  -H 'access_token: hlath' \
  -H 'Content-Type: application/json' \
  -d '{
  "Ocean": 2,
  "Trees": 2,
  "Grass": 2,
  "Beach": 2
}'
2. "OK"

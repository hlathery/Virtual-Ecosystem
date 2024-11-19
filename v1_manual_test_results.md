# Example workflow

## User Assigning Villager Jobs

When a user realizes that their village's food source is beginning to dwindle, they find this by calling `GET village/village_inventory`, which gives a list of village resources.
They realize that they need to assign villagers to hunt and gather food to keep their village alive. The user will call `GET jobs/` to see a list of all jobs available and the amount of villagers in each.
After noticing there is a low number of villagers in forager and hunter jobs. They do the following:

- `POST jobs/assignments`. And the user will be prompted to return the json for the new amount of villagers in each job so they increase the amount of villagers in the "forager" and "hunter" jobs “villagers_assigned”, and the correct amount of villagers will be allocated to each job

After this is completed, the villagers will successfully increase the amount of resources available to keep their villagers alive.


# Testing results
## Step 1: Calling "GET village/village_inventory"

1. curl -X 'GET' \
  'http://127.0.0.1:3000/village/village_inventory' \
  -H 'accept: application/json' \
  -H 'access_token: hlath'

2. [{
    "resource_name": "water",
    "quantity": 50
  },

    {
    "resource_name": "food",
    "quantity": 50
  },

    {
    "resource_name": "wood",
    "quantity": 100
  }]

## Step 2: Calling "GET jobs/"

1. curl -X 'GET' \
  'http://127.0.0.1:3000/jobs/' \
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
    "villagers_assigned": 0
  },

    {
    "job_id": 1,
    "job_title": "hunter",
    "villagers_assigned": 0
  }
]

## Step 3: Calling "POST jobs/assignment"

1. curl -X 'PUT' \
  'http://127.0.0.1:3000/jobs/assignments' \
  -H 'accept: application/json' \
  -H 'access_token: hlath' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "job_id": 3,
    "job_title": "Farmer",
    "villagers_assigned": 1
  }
]'

2. "1 villager sucesfully assigned as a farmer"
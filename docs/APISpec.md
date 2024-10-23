# API Specification for Virtual Ecosystem

## 1. Village Info

Provides the user with information regarding the status of their villagers, village resources, etc.

### 1.1. `village/` (GET)

Returns a general overview of village characteristics such as: Jobs with how many villagers
are in each one, inventory items and how much of each item you have, and 
the types of buildings you have along with how much of each type you have.

### 1.2. `village/villagers/` (GET)

Returns a list of all villagers with their respective attributes.

### 1.3. `village/villagers/{villager_id}` (GET)

Accepts a specific villager id as input and gets their job and age.

### 1.4. `village/inventory` (GET)

Returns a list of all village resources and how much of that resource is available.

### 1.5. `village/inventory/{resource_id}` (GET)

Accepts a resource id and returns how much of that item is in the inventory.

### 1.6. `village/buildings/` (GET)

Returns an overview of the types of buildings (Farm, Mine, House) you 
have and how much of each type you have and how many villagers are in each type.

### 1.7. `village/buildings/{building_id}` (GET)

Accepts a building id (which refers to a type of building) and returns 
how many villagers are working in that building type.


## 2. Ecological Info

Provides the user with information regarding the state of certain ecological entities.

### 2.1. `eco/` (GET)

Returns a general overview of the ecosystem and its characteristics such as: predators and prey and 
how many there are, the characteristics of each body of water and their id, plants and 
how many there are, resources (trees for wood, mine shafts for mining, etc.).

### 2.2. `eco/life/predators/ ` (GET)

Returns how many predators there are in the surrounding ecosystem.

### 2.3. `eco/life/prey/` (GET)

Returns how much prey there is in the surrounding ecosystem.

### 2.4. `eco/life/plants/` (GET)

Returns how many plants there are in the surrounding ecosystem.

### 2.5. `eco/resources/{body_id}/` (GET)

Accepts a body id (referring to a specific body of water) and returns the 
water level and dryness of the area.


## 3. Expansion 

Methods which will allow the user to expand their village.

### 3.1. `expansion/catalog` (GET)

Returns building types and the amount of each building is available 
to build based upon available resources.

### 3.2. `expansion/plan` (POST)

The user passes in each building type they want to build
and how many of each type.


## 4. Assignments

Methods which will allow the user to assign certain tasks and jobs to villagers.

### 4.1. `assignments/` (GET)

Returns a list of all jobs and the amount of active workers at each job. 

### 4.2. `assignments/plan` (POST)

The call passes in a catalog of each job type and how many villagers are working in each job type. 
The user would return back new values, if any, of how many villagers they want in each job.

## 5. Admin

Methods which will allow major resets and such.

### 5.1. `admin/reset` (POST)

Resets all data in user inventory, village, and ecosystem to default values.

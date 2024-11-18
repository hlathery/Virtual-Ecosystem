# Virtual Ecosystem Example Flows

## User Expanding Village

A user who favors expansion and increasing the population as soon as possible wants to increase the amount of buildings to house villagers. 
After a series of decisions that sends workers to forest mass amounts of trees over a span of a couple of years, the user now has ample amounts of wood to build multiple buildings. 
The user checks what they can buy with their resources by calling  `GET /catalog`. The user sees they can build 5 small homes with building_name `SMALL_HOME` for 10 wood each that’ll increase population by 10 each. 

The user initializes the building of 5 `SMALL_HOMES` and makes the following requests:

- Start by making a `POST expansion/plan` which assigns each new building with a unique building id and queues in the plan for new buildings to be placed the next cycle
- After letting a year cycle run (it takes a year to build said buildings) the user makes a `GET village/buildings/` to see the new
village structures
- The user sends a `GET village/buildings/{building_id}/` for each building to see how many villagers live in the building and who lives there, identified by `villager_id `

## User Managing Ecosystem

A user is between decisions either regretful or proud of what they have done to their people or their environment.
They want to see specific numbers but have to wait until the decision time. Once the decision time comes, the user calls `GET /eco/`.
The user sees that they have hunted far too much prey and have nearly made them extinct.
To simplify the data they are looking at they call `GET /eco/prey/` and `GET /eco/predators/{biome_id} `to make a comparison between the number of predators and prey.
They see that the predator to prey ratio is 15:1 so, with this new info, they make the informed decision of taking the risk of mainly hunting predators for the year.
They then go to make village decisions and, to inform themselves on this front, they call `GET /village/`.
Upon looking through the data they notice they have the wood to build more buildings and some villagers are unemployed.
They then call `GET /assignments/` to see an overview of buildings to see their type, their job relation, and how many villagers are in each.
After looking at this, they now know what jobs are in desperate need of villagers and what jobs have too many villagers.
So, they call `GET /expansion/catalog/` to see available buildings to build to put unemployed villagers or villagers in over saturated jobs and can make informed decisions on that front as well.
With the info gathered from these calls, they can make the informed changes with `POST /assignments/plan` and `POST /expansion/plan`.

## User Assigning Villager Jobs

When a user realizes that their village's food source is beginning to dwindle, they find this by calling `GET village/inventory/`,which gives a list of village resources.
They realize that they need to assign villagers to hunt and gather food to keep their village alive. The user will call `GET assignments/get_job_list` to see a list of all jobs available and the amount of villagers in each.
After noticing there is a low number of villagers in forager and hunter jobs. They do the following:

- `POST assignments/plan`. And the user will be prompted to return the json for the new amount of villagers in each job so they increase the amount of villagers in the "forager" and "hunter" jobs “villagers_assigned”, and the correct amount of villagers will be allocated to each job

After this is completed, the villagers will successfully increase the amount of resources available to keep their villagers alive.

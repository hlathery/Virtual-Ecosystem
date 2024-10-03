# User Stories

1.) As an environmentalist and a fan of city-management games, I would like to simulate the makings of a village/civilization whilst also studying the effects of major village decisions on village upkeep on surrounding ecosystems to keep the people of said village happy and healthy. 

2.) As an engineer, I want to optimize resources and make carefully considered decisions so that the human race can amplify and enhance the building of structures (ex: build houses as fast as possible with the least amount of labor/resources).

3.) As an explorer and expansionist, I would like to expand my village to its full potential by lumbering vast amounts of the surrounding forest whilst trying to keep it alive and sprawling.

4.) As an industrialist, I want to expand the village to its fullest potential with multiple structures by lumbering all of the forest so that there are no trees in sight and the ecosystem is dominated by humans.

5.) As a minimalist, I would like to keep the village small and modest with a limited population so that the village is more self sustainable/controllable and the surrounding ecosystem can also thrive.

6.) As an avid hunter, I would like to simulate how an ecosystem would react to various levels of hunting/gathering over certain amounts of time.

7.) As a hoarder, I want to store and gather as many resources as possible with no regard for its natural effect on my surroundings because all that matters is that I have everything that is possible to attain.

8.) As an avid fan of clash of clans, I want to run my village in a similar sense by collecting resources, but  in a much more realistic simulated manner.So that I can grow the biggest village I possibly can.

9.) As an environmental science student, I want to manage a village and ecosystem, so that I can better learn how wildlife and our ecosystem can be affected by the interference of humans.

10.) As an anarchist, I want to destroy the village and cause damage so that the population and village dies as fast as possible.

11.) As a fan of mining simulation games, I want to allocate workers to go mining, so that they may bring back resources like iron and coal to further my village.

12.) As an admirer of forests, I want my surrounding ecosystem and village living area to be all forested. I will plant as many trees as possible whilst keeping the ecosystem watered and fed to encourage growth.


# Exceptions

_Exception_: No more forest/surrounding lumber  

If a user attempts to lumber with no more trees in their area, the system will give back an error telling them that there are no more trees and asking them to plant more with any remaining saplings.

_Exception_: No more water

If a user attempts to gather water (from a river, for example) with no more rivers/lakes surrounding them, the system will give back an error telling them that there is no more water, they are in a major drought, and asking them to conserve their water storage and pray for rain.

_Exception_: Insufficient resources

If a user is attempting to build a home or structure but does not contain the sufficient amount of resources (lumber), the system will throw an error saying they do not have enough resources and they need to harvest more.

_Exception_: Insufficient wildlife
If a user attempts to hunt wildlife and have made them extinct, the system will send an error asking them to gather/hunt other forms of life or if there is no more life, prepare for famine and disease.

_Exception_: Planting in an incorrect area
If a user attempts to plant a sapling in an area that doesn’t contain soil, it will return an error stating it cannot plant there. Ex (planting on a river, house, sand, etc.)

_Exception_: Insufficient space/Invalid placement
If a user attempts to place a building without the space needed or place a building where something is already built or growing, then the system will throw an error asking them to allocate space or place their building or planned growth elsewhere.

_Exception_: Hunting with no tool
If a user sends a hunter to go hunting with no weapon, it will result in an error stating that a (bow/spear/etc.) must be required to send the hunter out.

_Exception_: Insufficient job placement 
If a user attempts to move someone out of a job in which there is only one person, the system will throw an error telling them that there must be at least one person in each job and that they cannot move that person out of the job to another one.

_Exception_: Out of Bounds
If a user clicks out of the playable area or grid, the system will return an error stating that the user must work on a valid cell in bounds.

_Exception_: Incorrect task assignment
If a user sends a person with a mining job for example to go hunt, it will return an error stating incorrect task assignment

_Exception_: Job limit exceeded
If a user attempts to assign a new villager to a job title that already has a filled amount of slots, it will return an error stating that the job title is full.

_Exception_: Building cannot be destroyed/salvaged

If the user attempts to destroy or salvage resources from a building where there is only one person doing the job in that building for the entire village, for example, if there is only one farmer and one farm, if they destroy that, then it fails the requirement that there must be at least one person in each job. The system will throw an error saying the building cannot be destroyed/salvaged and will ask them to salvage another building or allocate another building of the same type elsewhere.
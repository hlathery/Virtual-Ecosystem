# Code Review Fixes

## Dionne Gregorio.

### 1. In village.py in line 33 you could just do a .scalar() instead of a scalar_one(). a .scalar() will return none if no results instead of raising an exception

-- Changed from scalar_one() to scalar()

### 2. In assign_villager in assignment endpoint, you set all the villagers job_id to be 0. Then update again, all that are 0. I looks like your changing all

-- The endpoint has been changed completely, this is no longer a problem.

### 3. In assign_villager in assignment endpoint, you set all the villagers job_id to be 0. Then update again, all that are 0. I looks like your changing all

-- Same as 2.

### 4. For the second example flow, the functions used is different from what is implemented. It makes it confusing as to what function is used for certain tasks Example: there is a prey_overview but the predator overview is called biome_predator. Also, eco overview needs to be implemented

-- Example flows have been changed to match the functions

### 5. In the grow plants function, you can restructure the for loop and query variable before and outside the with statement and SQL query.

-- Loops have been pulled out of connection calls across all endpoints.

### 6.In the plants_overview() query, you could just use a .one() instead of fetchone(). Instead of indexing the result, you can just do plants_table.entity and plants_table.total. The append could be moved outside the with statement.

Endpoint has been changed.

### 7. In prey_overview(), biome_prey/predator, you can do result.column instead of indexing.

-- We've stopped indexing

### 8. In spawn_prey/predator, you can structure the for loop and values outside then do the SQL after.

-- Loops have been pulled out of connection calls across all endpoints.

### 9. For the post functions, you could return a more descriptive return statements instead of an "OK". Example: in the kill_villager, you could return which villager got removed.

-- Made statements more descriptive, with some returning actual values

### 10. You could log which villagers are assigned which jobs instead of just having "OK". This way you could tell which villagers are assigned when the function is called

-- Shows how many villagers were given jobs.

### 11. In village/catalog instead of doing a scalar_one() you could just do a .scalar().

-- Fixed.

### 12. In get/catalog, the query variable and for loop can be moved outside of the with statement.

-- Loops have been pulled out of connection calls across all endpoints.


## Cory Cowden

### 1. “Environmental” spelled wrong on readme.md

-- Fixed.

### 2. Many functions are commented off. If they are unwanted, consider deleting them.

-- Fixed.

### 3. In assign_villager, make sure to check that villagers_assigned is not a negative number before updating

-- Fixed.

### 4. Consider checking for empty lists before running queries like in spawn_prey and grow_plants

-- Fixed

### 5. Check to make sure that valid biome ids are being passed in eco.py, for example in spawn_prey, make sure that the biome id matches one available option. If not, throw an error

-- Fixed

### 6. Make sure that the get endpoints like biome_prey, catalog, get_job_list, etc. can handle empty lists. For example, if biome_prey searches but has no data, consider returning something like “No prey found!” for clarity

-- Fixed

### 7. Consider adding ledgers for data like jobs for job_history, villagers_created, or population so it is easier to keep track and debug if needed

-- We've reorganized some of our tables, but we decided to keep our structure because we have more of a game-like state.

### 8. Consider adding comments on less straightforward endpoints such as post_biome_counts so it is easier to read.

-- Added.

### 9. Consider adding errors and error messages for when an invalid building/biome type is passed in build_building, spawn_predator, spawn_prey, etc.

-- Added

### 10. Consider adding errors and error messages for when a user tries to kill more villagers than are available

-- This isn't a big issue, as when there are no more villagers, the game pretty much ends, and if 3 villagers are supposed to die and there are only 2, it will still kill the 2 without issue.

### 11. Consider adding logs or ledgers for user actions, such as when a user tries to create/kill villagers

-- To Talk About.

### 12. For some PUT endpoints like assign_villager, consider returning something more useful than “OK” for example, you could return how many villagers were reassigned

-- Added.


## Amir Minabian

### 1. Naming Conventions: Consider renaming variables like id, name, and quantity to more descriptive alternatives where possible. For instance, village_id or resource_name to clarify the context in each module.

-- I can see the want for this, but when joining tables or calling tables, it seems more obvious what column belongs to which table (i.e. villagers.id and buildings.id). The change feels a little redundant.

### 2. Code Modularization: Large functions such as those in assignments.py and eco.py can be broken down into smaller, modular functions. For instance, separating data validation and processing logic in assignments.py could improve readability and debugging.

-- A lot of these files have been revised and changed, not too many of the functions are all that big, but mostly have been changed.

### 3. Repeated Code: There are repetitive API response structures, particularly in handling requests in main.py. Consider creating a utility function to handle common response formatting and error responses to make the code DRY (Don’t Repeat Yourself).

-- This has been fixed.

### 4. Error Handling: Expand on error handling, especially in endpoints like village/inventory and village/catalog. Adding specific exceptions for different types of failures (e.g., ValueError for invalid inputs) could make debugging and user feedback clearer.

-- This has been a common critiscm and has been fixed.

### 5. Documentation: Add more detailed docstrings for complex functions, particularly in eco.py. Explaining parameters, return values, and any expected exceptions would improve maintainability.

-- Done, the endpoints are explained more clearly on their inputs and outputs.

### 6. Code Comments: Certain blocks in auth.py could benefit from inline comments explaining the purpose of complex operations, particularly around token validation and authentication checks.

-- I added comments to most error handling to explain the reasoning behind it, most the code is not too complicated, but to code that was I added more comments.

### 7. Optimization: The function in assignments.py that handles job assignments could be optimized by leveraging dictionary lookups instead of nested loops, which would improve its performance, especially with a larger dataset.

-- Assignments.py no longer exists, however, I found this particular endpoint, there is no longer a nested for loop; instead it's done in a single for loop, however the data set is not, and probably never will be, big enough to really need a dictionary.

### 8. File Structure: Consider restructuring the project to separate API logic, database models, and utility functions into different folders. This would improve maintainability as the project grows.

-- We considered doing this, however, it feels easier to access and move through our files when our endpoints are all together in one API folder.

### 9. Logging: Implement logging in critical areas, such as user authentication and job assignments. This will help in tracking issues in production without relying solely on debugging.

-- We added more user error handling to ensure only specific values get passed through.

### 10. Redundant Code: There are instances of redundant variable declarations in database.py. These can be consolidated or streamlined to reduce code clutter.

-- database.py is all cleaned up.

### 11. Security Concerns: Ensure that sensitive data, such as user tokens, is masked or sanitized in log files to avoid potential security risks.

-- I've gone through and checked for any leaked API keys, I've found one in Test_gen.py and masked it.

### 12. Testing Utilities: Add utility functions for testing in test_utils.py to handle repetitive setup tasks in test scripts. This will make test scripts more readable and reduce setup redundancy.

-- test_utils.py has been removed.

## Katie Slobodsky

### 1. In post_biome_counts in eco.py, parameterize the SQL statement instead of using an f string to avoid SQL injection

-- All f-strings have been removed.

### 2. Consider deleting unneeded code (especially in village.py) that is commented out to improve readability

-- Done. All code not being used has been removed.

### 3. Since name and quantity for buildings are part of the same table, maybe when returning values for get_village_overview() you can combine the name and count and return a single list of dictionaries with name and count in each building item.

-- We looked at this, and decided for the game state, it was best to keep this the way it was, only because for the game, it's best to see total of everything to watch the overall gamestate.

### 4. In adjust_storage, you can reduce the number of database calls by combining the logic under one “with db.engine.begin() as connection:” instead of 2. This would reduce runtime.

-- Fixed, only one database call.

### 5. For kill_villager, instead of just returning “OK” maybe you can return a list of dictionaries of deleted villagers information, such as their name, id, and age. This could confirm that the correct villagers were deleted.

-- Updated to display id and age when deleted (the villagers are nameless).

### 6. In build_structure, make sure to check if the player has enough resources before updating building quantity. You can do this by comparing the requested resources and available resources.

-- Logic for this will be handled in game files.

### 7. Consider adding more error handling, for example in adjust_storage, in the case where the resource quantity is less than the requested storage adjustment, this would throw an error

-- Gone through and made sure error handling statements were used where needed for certain values.

### 8. There could be more logging, such as when a villager is created or killed, storage is adjusted, or a building is built. This could help with testing.

-- We were testing with some logging, and now it has been removed while closing in on the final version.

### 9. Instead of looping through each job, you can group villagers by job and update them in a single operation where possible; this can reduce the number of queries

--  All database calls have been pulled out of loops, and better query calls across files have been made.

### 10. A possible improvement for get_job_list could be to add sorting or filtering for more organization (e.g. sorting by job_name)

-- The query call is already pretty simple, so we decided not to change it.

### 11. For functions that require updating, add more checks to ensure that the update could be completed to avoid miscalculations and mismatches in data. If not, roll back the transaction and ensure that nothing was updated to avoid concurrency errors.

-- SQLAlchemy has built-in transaction management, if there is an exception (which we've added), everything will be rolled back.

#### 12. “Entitys” spelled wrong in eco.py - consider changing to “entities”

-- Corrected.

## Timothy Matthies

### 1 .You can make prey_overview more readable when setting entity_type and total by using prey_table.entity_type and prey_table.Total, respectively.

-- prey_overview doesn't exist anymore, it's been combined into another endpoint. However, it should be more readable.

### 2. It's very hard to read the first two lines of post_biome_counts. I'd say either clean it up or comment on what's going on. It might also just be my unfamiliarity with Python.

-- The endpoint has a better description (as well as an entire rehaul in its functionality), should be much more readable.

### 3. See Got assignments workflow working. NOTE: Perlin no longer works for no… #1 but for plants_overview.

-- Perlin has been worked on and fixed for the endpoints.

### 4. Why are results being put in a list if there's only on item in plants_overview and prey_overview? I think it should be a single object instead of a list.

-- This was a similar concern from another reviewer, due to our game state we want to show the overall total.

### 5. In spawn_prey, it seems perfectly set up to be legerized instead of just updating values. Almost all that would need to happen would be change it from update to insert. Would be easier than looking for individual lines to update.

-- We've reorganized some of our tables, but we decided to keep our structure because we have more of a game-like state.

### 6. See Got assignments workflow working. NOTE: Perlin no longer works for no… #1 but for biome_prey.

-- Perlin has been worked on and fixed for the endpoints.

### 7. See Got assignments workflow working. NOTE: Perlin no longer works for no… #1 but for biome_predator.

-- Perlin has been worked on and fixed for the endpoints.

### 8. What is the point of the post_time function? The time is not being posted, a get shouldn't be used to change the database, and is does not even call the database??? What is it supposed to do?

-- post_time has been removed.

### 9. With how your set up is right now, I'd recommend being able to choose which villager to kill off via ids in kill_villagers, instead of just killing the oldest ones. Could also be interesting if there were something like natural disasters in the game.

-- We added natural disasters that randomly kill villagers, because of this, we're keeping killing off the oldest ones as there is now a means for any villager to die a different way.

### 10. Should there be checks in build_structures? At the moment it looks as though anything could be bought without care for money. It also does not subtract resources used, so even if I were to play the game as intended, only buying what I were supposed to, it would cost me no money.

-- The "money" is the resources the user has to build.

### 11. In adjust_storage, do the materials need to be split across all buildings like it is? How you are treating it right now, it seems like it would be easier and have the same effect if you were to just keep one storage place, and add storage to it if any buildings are bought.

-- Each building is suppose to come with its own storage, so buying a building allows more villagers and its own storage as well.

### 12. For the code in assign_villager, it looks like a different style of multi-line input to sqlalchemy is being used. I think that the other style used, where a single text is created and multiple dictionaries are passed, looks like it would work better. I'll be implementing it into my own code so that loops are not continuously making database calls.

-- the assign_villager endpoint has been changed (most of the endpoints have) and now have the same style.

# Schema/API Design Fixes

## Timothy Matthies

### I'd like to keep the timestamps in the tables, and also start aiming for legerization. Makes it so much easier to debug and test your database.

-- This is a good idea to implement some sort of ledgerization for the sake of simplicity and debugging but that would require a significant rehaul of the database and would take too much time to change everything given the closeness to the presentation and due dates.

### In your code you make reference to the fact that there are three specific biomes, but I do not see those being inserted in the schema, so I'm not sure how those are supposed to be used and kept track of.

-- The biomes are added to the database tables when flood fill is ran

### Got an error when trying out GET /info/current_time. GET methods should not have a body passed with them.

-- We have since removed this function so this is no longer an issue

### Odd return objects on GET /village/ and GET /village/catalog. I'd guess it works, but I'd like to see buildings and num/cost of paired up and easily readable.

-- Both num_buildings and cost are paired in their respective arrays and are displayed in a readable way to the user in the game

### A lot of API calls are redundantly named. I.e.: PUT /eco/spawn_prey or GET /assignments/get_job_list. The spawn/put and get are already known because of what HTTP method they are, there's not much of a need to include it in the name. I'd recommend renaming them to something like PUT /eco/prey and GET/assignments/jobs so that it's easier to tell what resource they operate on, and makes it feel less cluttered when view all of the API names. I also learned that this is a standard practice in industry from my CSC 307 class.

-- We have since fixed this issue

### Maybe change POST /village/kill_villager to DELETE /village/villager so it's clear from the HTTP method what's supposed to happen.

-- We have since fixed this issue

### I'm confused about why PUT /eco/grow_plants is a PUT, while all the other similar (i.e. spawn_prey) methods are POSTs. Is there a design choice to this?

-- This function has since been removed and this issue no longer exists

### Change the description of PUT /assignments/assign_villager. It makes no sense and describes the method incorrectly.

-- This has since been fixed

### What is the point of adding "job_title" in the PUT /assignments/assign_villager? I was able to change it to whatever I wanted and it still only cared about the job_id.

-- This has since een fixed and it only takes in job title

### Getting a 500 error on POST /eco/biomes , while using it as I believe is intended. Passed: { "Ocean":4, "Forest":6}

-- This has since been fixed

### Got a 500 error on GET /eco/plants

-- This has since been fixed

### Got a 500 error on GET /eco/prey

-- This has since been fixed

## Katie Slobodsky

### Consider adding a unique constraint to the biome_name field in biomes to make sure that each biome name is unique

-- We would not want to do this as there could be multipe of one biome so we have an 'id' field as our unique constraint

### Ensure that columns like biome_name, resource_name, and job_name are not null

-- This issue has been resolved

### Add a created_at timestamp column to track the creation times of entities to tables such as biomes, buildings, jobs, and villagers.

-- I do not think there is a need for this as there is no forseeable use case for this

### Add a check constraint for the quantity field in tables such as buildings and storage to ensure that the value cannot go negative

-- This issue has been resolved

### Maybe you can add a level column to the jobs table as an extended feature of the game. This can open up more capabilities for each role of characters based on their level.

-- This would be a nice addition to the game and make it more interesting, however given the time constraint we have, we will not have time to addd this and get it fully running in time

### Instead of being stored as a string, maybe biome_name can draw from a separate biome_types table with predefined unique biome names; that way there would be less redundancy

-- It would still be same amount of redundancy because if it draws from another table with unique biome names, then there would be ids for each biome name and the same biome ids could appear in the biomes table just as the same biome names would appear

### Consider adding a boolean “built” field for the buildings table to track if the building is already finished or is under construction (default = FALSE)

-- We do not have unique rows per bulding, there are only unique building types along with their respective amount

### 1.3. All villagers - village/villagers_all/ (GET) endpoint could potentially just be changed the village/villagers

-- This function has since been removed and this is no longer an issue

### Add pagination for /village/villagers_all/ in the case of returning a very large list

-- This function has since been removed and this is no longer an issue

### You can combine /village/fill_inventory and /village/building_inventory into a single /village/inventory endpoint with parameters for viewing or adjusting/building inventory

-- I think it would be best to keep GET and POST functions separate to signify their specific function and make the code more friendly and readable

### In 2. Eco, "entity_type": "string", /* Should be "plants" */ Here, maybe instead of storing entity_type as a string, you could have an entity_id field that references an entities table that stores entity_id and the entity_type so that there is a clear predefined list of entity types.

-- I do not think this is a necessary change that needs to be made as the user would know from the display that the only entities are plants, predators, water, trees, and prey

### “nourishment” could have more clearer specifications, such as if it needs to be within a certain numerical range

-- This has now been specified in the API spec

## Amir Minabian

### Schema Normalization: The villagers table could be normalized further by separating job_id details into a relationship table for better scalability, especially if villagers can have multiple roles.

-- Villagers cannot have multiple roles, and there is a separate table for jobs that villagers references to determined what job that villager is asigned to.

### Foreign Keys: Ensure foreign keys are indexed, such as building_id in the catalog table, to improve query performance when joining tables on these keys.

-- Thi issue has been resolved

### Data Types: Consider using specific data types for certain fields. For example, a boolean field for status flags (like is_active for villagers) instead of integer values where applicable.

-- All columns take in specific data types for their use cases

### Redundant Fields: In the jobs and buildings tables, there appears to be some redundancy in quantity. Consider combining similar tables or fields if they serve the same purpose to minimize redundancy.

-- These tables have different columns and different use cases so this would not be possible

### Primary Key Use: Primary keys are appropriately used, but consider adding unique constraints for fields like biome_name in the biomes table to prevent duplicate records.

-- This issue has since been resolved

### Endpoint Naming: Use plural nouns for collections in endpoints (e.g., /villages instead of /village) to follow RESTful conventions and make the API more intuitive.

-- I do not think this is a necassary change that needs to be made as it does not change functionality but we will take this into account

### Consistent Responses: Ensure all endpoints return a consistent structure, including metadata (status codes, timestamps) and data objects, to improve API usability.

-- This issue has been resolved

### API Documentation: Ensure each endpoint is documented with expected inputs, outputs, and examples. The /docs route provides some information, but adding detailed explanations of each parameter in the API spec would be beneficial.

-- This issue has been resolved

### Error Handling in Endpoints: Implement consistent error messages across endpoints. For instance, if a resource is not found, use a standardized error response with a helpful message for users.

-- This issue has been resolved

### Endpoint Permissions: Set role-based permissions for sensitive operations, such as creating or deleting resources. Only authenticated users should be allowed to perform certain actions to enhance security.

-- creating and deleting rows is a part of the logic of the game so this must be allowed during the entire game time to the user. It should not be possible to delete rows that should not be deleted in our endpoints.

### Caching Opportunities: Implement caching for endpoints that return static or infrequently updated data, like /village/catalog, to reduce load and improve response time.

-- We do cache reurns from endpoints in the game and only call the endpoints when necessary

### Rate Limiting: Introduce rate limiting on critical endpoints to prevent abuse and ensure service availability.

-- All endpoints are only called when necessary and it is not possible to abuse these endpoints from the users end through the game.

## Cory Cowden

### Many foreign keys are set up as “null”. Consider making “not null” if they need to always exist – for example, a villager may always need a job_id, even if 0 for unassigned.

-- This issue has been resolved

### Instead of having separate rows for each building cost in the catalog table, consider combining it to create a new column in the buildings table to display the cost, instead of having a separate catalog table

-- We have these separate for readability purposes so we know we are accessing the table for building

### Rename “entitys” table to “entities” for correct spelling

-- This issue has been resolved

### Villagers and biomes are not connected. Consider adding a biome_id to villagers table to be able to track what biome the villager is in

-- This is not necessary as the villagers will be in the village at all times and it is not necessary to track a villagers location

### Consider restricting nourishment from 0-100. Restricting the values could make it clearer

-- We do keep nourishment in a range from 0-100

### Consider renaming primary key, “inventory_pkey” from the buildings table to “buildings_pkey” for clarity

-- This issue has since been resolved

### Consider restricting what values can be set for values like quantity, like only positive numbers

-- This issue has since been resolved

### Consider adding a status column to villagers table to identify if a villager is alive, dead, or dying (if nourishment is too low or age is too high)

-- All dead villagers are deleted from the villagers table and the user can tell if a villager is dying from thier nourishment levels

### Consider adding a default biome for villagers to prevent incomplete values when creating a villager

-- We do not keep track of the biome the villager is in

### Consider making important values such as biome_id in villagers set to “not null”

-- All important fields are st to not null and we do not keep track of the biome for the villagers

### Consider setting restrictions on job types, so that only valid inputs can be passed

-- This issue has been resolved

### Consider setting default values in buildings, such as 0 for quantity so that you do not end up with null errors

-- This issue has been resolved

## Dionne Gregorio

### For building_id, you could move the quantity into the catalog table, leaving only building id and building name

-- We would want to keep quantity and cost separate for simplicity

### For the entitys table you can break up entity type to another table and have each entity have their own entity id. also i think its spelled entities

-- The spelling has been fixed, and adding a table would not be necessary as it has the same redundancy and would just take up more space

### You could add a separate resource table instead of having it a column for the storage table.

-- Our resources are stored separatley in the storage table already

### In the biomes table the biome_name is nullable, you wouldn't want to create an id without a name. Also in the Buildings table, the name is nullable

-- This issue has been resolved

### For the catalogs table, having building id and cost be nullable isn't good practice. Should be not nullable

-- This issue has been resolved

### I don't think there is a relationship between how many villagers are in the biomes.

-- We do not keep track of biomes for villagers

### Catalog could be moved to its own endpoint instead of having it in the village.py

-- I do not think this is a necessary change as it would only take up more space adding another file that has maybe one enpoint

### Village inventory could be moved to an inventory endpoint. You could set a cap on how many villagers you could have and provide a way to expand your biome

-- Viewing the village inventory is already its own endpoint and biomes cannot be expanded
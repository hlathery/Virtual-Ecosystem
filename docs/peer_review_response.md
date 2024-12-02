# Dionne Gregorio.

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


# Cory Cowden

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


# Amir Minabian

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

# Katie Slobodsky

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

# Timothy Matthies

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

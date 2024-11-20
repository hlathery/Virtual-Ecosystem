# Dionne Gregorio.

## 1. In village.py in line 33 you could just do a .scalar() instead of a scalar_one(). a .scalar() will return none if no results instead of raising an exception

-- Changed from scalar_one() to scalar()

## 2. In assign_villager in assignment endpoint, you set all the villagers job_id to be 0. Then update again, all that are 0. I looks like your changing all

-- The endpoint has been changed completely, this is no longer a problem.

## 3. In assign_villager in assignment endpoint, you set all the villagers job_id to be 0. Then update again, all that are 0. I looks like your changing all

-- Same as 2.

## 4. For the second example flow, the functions used is different from what is implemented. It makes it confusing as to what function is used for certain tasks Example: there is a prey_overview but the predator overview is called biome_predator. Also, eco overview needs to be implemented

-- Example flows have been changed to match the functions

## 5. In the grow plants function, you can restructure the for loop and query variable before and outside the with statement and SQL query.

-- Loops have been pulled out of connection calls across all endpoints.

## 6.In the plants_overview() query, you could just use a .one() instead of fetchone(). Instead of indexing the result, you can just do plants_table.entity and plants_table.total. The append could be moved outside the with statement.

Endpoint has been changed.

## 7. In prey_overview(), biome_prey/predator, you can do result.column instead of indexing.

-- We've stopped indexing

## 8. In spawn_prey/predator, you can structure the for loop and values outside then do the SQL after.

-- Loops have been pulled out of connection calls across all endpoints.

## 9. For the post functions, you could return a more descriptive return statements instead of an "OK". Example: in the kill_villager, you could return which villager got removed.

-- Made statements more descriptive, with some returning actual values

## 10. You could log which villagers are assigned which jobs instead of just having "OK". This way you could tell which villagers are assigned when the function is called

-- Shows how many villagers were given jobs.

## 11. In village/catalog instead of doing a scalar_one() you could just do a .scalar().

-- Fixed.

## 12. In get/catalog, the query variable and for loop can be moved outside of the with statement.

-- Loops have been pulled out of connection calls across all endpoints.

# Fake Data Modeling
Python File to Spawn 1 million rows: https://github.com/hlathery/Virtual-Ecosystem/blob/main/src/api/random_spawn.py 

The amount of final rows in the villagers table is approximately 1,212,248 rows/records (as shown below). biomes contains 10 rows, buildings has 7 rows, catalog has 5, entities has 12, jobs has 7, and storage has 3.

![image](https://github.com/user-attachments/assets/cb9fef7b-1a7e-4562-95b4-fd7a7b1e505f)

The reason our project is only scaled towards villagers is because the other tables act as keys or catalogs that are referenced as foreign keys in other tables (for example there are only 7 jobs that exist in the game, but each villager is assigned one of these jobs).
Other tables do not make sense to scale to large values due to frontend limitations. Biomes only has 10 rows due to the frontend being limited to only showing an x number of biomes.
Villagers are the only quantity that can be appended to, other tables are updates only. One consideration was implementing a ledgerized design for resources in the storage table which would be another avenue to scale, but due to time constraints we were unable to.

# Performance Results of Hitting Endpoints:
### Admin
- admin/reset runtime: 0:00:01.394086

### Village
 - village/ runtime: 0:00:00.144376
 - village/catalog runtime: 0:00:00.012040
 - PUT village/villager runtime: 0:00:01.349416 (Inserting 1000 villagers)
 - DELETE village/villager runtime: 0:00:00.479722 (Deleting 1000 villagers) 
 - village/villager_update runtime: 0:00:10.744642
 - POST village/building runtime: 0:00:00.007635
 - PUT village/inventory runtime: 0:00:00.020511 (Adding food)
 - village/village_inventory runtime: 0:00:00.011003

### Ecological
 - eco/ runtime: 0:00:00.102123
 - eco/biomes runtime: 0:00:00.052241

Request for biomes:
```
{
  	"ocean": 1,
  	"forest": 2,
  	"grassland": 3,
  	"beach": 4
}
```

 - eco/plants runtime: 0:00:00.011714 (with 100 plants per biome w/ 4 biomes
 - eco/entity runtime: 0:00:00.022300 (Inserting entity into biome)
 - eco/entity/nourishment runtime: 0:00:00.023006
 - eco/prey/biome_id runtime: 0:00:00.018261
 - eco/predator/biome_id runtime: 0:00:00.007993
 - eco/disaster TRUE runtime: 0:00:00.417198 (Killed 4 villagers with Plague)
 - eco/disaster FALSE runtime: 0:00:00
 - eco/disaster TRUE runtime: 0:00:00.294763 (Killed 3 villager with Rebellion)


### Jobs
 - jobs/ runtime: 0:00:00.503610
 - jobs/assignments runtime: 0:00:02.170144 (updating 90000 rows)

Request for Assignments:
```
[
  {
    "job_name": "miner",
    "villagers_assigned": 90000
  }
]
```

## Slowest Endpoints:
 - village/villager_update runtime: 0:00:10.744642
 - jobs/assignments runtime: 0:00:02.170144
 - PUT village/villager runtime: 0:00:01.349416 (Inserting 1000 villagers)

# Performance Tuning
### village/villager_update
Query:
```
water = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM storage WHERE resource_name = 'water'")).scalar_one()
        food = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM storage WHERE resource_name = 'food'")).scalar_one()
UPDATE villagers
SET
age = age+1,
nourishment = nourishment+:water+:food-100
```
Explain:
| QUERY PLAN                                                               |
| ------------------------------------------------------------------------ |
| Update on villagers  (cost=0.00..30973.03 rows=0 width=0)                |
|   ->  Seq Scan on villagers  (cost=0.00..30973.03 rows=1200002 width=14) |

Query: 

The explain shows that the query planner is using a Sequential Scan, meaning the query is progressing through every single row/record sequentially and updating. Some index solutions could be creating an index on each villager via villager_id, however PostGres already does this automatically due to the unique field constraint on villager_id. Another Index to do 

Index Command:
Explain:

### jobs/assignments
Query:
```
```


Index Command:
Explain:
### village/villager
Query:
```
for _ in range(0, amount):    
        update_list.append({"age": 18,
                            "nourishment":100})
    insert_query = """
        INSERT INTO villagers (age, nourishment)
        VALUES (:age, :nourishment)
    """
```
Explain (Runs Explain analyze): 
| QUERY PLAN                                                                                      |
| ----------------------------------------------------------------------------------------------- |
| Insert on villagers  (cost=0.00..0.01 rows=0 width=0) (actual time=0.286..0.287 rows=0 loops=1) |
|   ->  Result  (cost=0.00..0.01 rows=1 width=16) (actual time=0.093..0.094 rows=1 loops=1)       |
| Planning Time: 0.054 ms                                                                         |
| Trigger for constraint villagers_job_id_fkey: time=1.056 calls=1                                |
| Execution Time: 1.451 ms                                                                        |

Since this is simply an insert, the query planner simply does an insert. One potential index to use is indexing the actual 





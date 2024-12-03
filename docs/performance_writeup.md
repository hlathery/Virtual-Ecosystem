# Fake Data Modeling
Python File to Spawn 1 million rows: https://github.com/hlathery/Virtual-Ecosystem/blob/main/src/api/random_spawn.py 

The amount of final rows in the villagers table is approximately 1,212,248 rows/records (as shown below). biomes contains 10 rows, buildings has 7 rows, catalog has 5, entities has 12, jobs has 7, and storage has 3.

![image](https://github.com/user-attachments/assets/cb9fef7b-1a7e-4562-95b4-fd7a7b1e505f)

The reason our project is only scaled towards villagers is because the other tables act as keys or catalogs that are referenced as foreign keys in other tables (for example there are only 7 jobs that exist in the game, but each villager is assigned one of these jobs).
Other tables do not make sense to scale to large values due to frontend limitations. Biomes only has 10 rows due to the frontend being limited to only showing an x number of biomes.
Villagers are the only quantity that can be appended to, other tables are updates only. One consideration was implementing a ledgerized design for resources in the storage table which would be another avenue to scale, but due to time constraints we were unable to.

# Performance Results of Hitting Endpoints:
### Admin
- admin/reset runtime: 1340.086 ms

### Village
 - village/ runtime: 144.376 ms
 - village/catalog runtime: 12.040 ms
 - PUT village/villager runtime: 1349.416 ms (Inserting 1000 villagers)
 - DELETE village/villager runtime: 479.722 ms (Deleting 1000 villagers) 
 - village/villager_update runtime: 10744.642 ms
 - POST village/building runtime: 7.635 ms
 - PUT village/inventory runtime: 20.511 ms (Adding food)
 - village/village_inventory runtime: 11.003 ms

### Ecological
 - eco/ runtime: 102.123 ms
 - eco/biomes runtime: 52.241 ms

Request for biomes:
```
{
  	"ocean": 1,
  	"forest": 2,
  	"grassland": 3,
  	"beach": 4
}
```

 - eco/plants runtime: 11.714 ms (with 100 plants per biome w/ 4 biomes)
 - eco/entity runtime: 22.300 ms (Inserting entity into biome)
 - eco/entity/nourishment runtime: 23.006 ms
 - eco/prey/biome_id runtime: 18.261 ms
 - eco/predator/biome_id runtime: 7.993 ms
 - eco/disaster TRUE runtime: 417.198 ms (Killed 4 villagers with Plague)
 - eco/disaster FALSE runtime: 0 ms
 - eco/disaster TRUE runtime: 294.763 ms (Killed 3 villager with Rebellion)


### Jobs
 - jobs/ runtime: 503.610 ms
 - jobs/assignments runtime: 2170.144 ms (updating 90000 rows)

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
 - village/villager_update runtime: 10744.642 ms
 - jobs/assignments runtime: 2170.144 ms (Updating 90000 rows)
 - PUT village/villager runtime: 1349.416 ms (Inserting 1000 villagers)

# Performance Tuning
### village/villager_update
Query:
```
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

The explain shows that the query planner is using a Sequential Scan, meaning the query is progressing through every single row/record sequentially and updating. Some index solutions could be creating an index on each villager via villager_id, however PostGres already does this automatically due to the unique field constraint on villager_id. 

Index Command: create index villagers_index ON villagers (id)

Explain:

| QUERY PLAN                                                               |
| ------------------------------------------------------------------------ |
| Update on villagers  (cost=0.00..30973.03 rows=0 width=0)                |
|   ->  Seq Scan on villagers  (cost=0.00..30973.03 rows=1200002 width=14) |

As expected, this did not have any performance lift as sequential search is needed to traverse every single row and update each row individually. Indexing by any other row (such as age and nourishment) will hurt performance as the index will need to change everytime the row value changes.

Query: 
```
SELECT SUM(quantity) FROM storage WHERE resource_name = 'water'
```
Explain:

| QUERY PLAN                                                   |
| ------------------------------------------------------------ |
| Aggregate  (cost=24.14..24.15 rows=1 width=8)                |
|   ->  Seq Scan on storage  (cost=0.00..24.12 rows=6 width=4) |
|         Filter: (resource_name = 'water'::text)              |

Explain shows that the planner is using a sequential scan to sum each quantity where resource name is 'water' and this filtering should reduce the amount of rows looked at. Indexing by the resource name, in this case water, may help.

Index Command: create index resource_idx ON storage (resource_name)

Explain:

| QUERY PLAN                                                  |
| ----------------------------------------------------------- |
| Aggregate  (cost=1.04..1.05 rows=1 width=8)                 |
|   ->  Seq Scan on storage  (cost=0.00..1.04 rows=1 width=4) |
|         Filter: (resource_name = 'water'::text)             |

The index did not have any performance uplift, mainly due to the lack of rows on the storage table (only having 3 rows). The query planner uses sequential search as it's still faster as all the data is on a single page.

Query:
```
SELECT SUM(quantity) FROM storage WHERE resource_name = 'food'"
```
Explain:

| QUERY PLAN                                                  |
| ----------------------------------------------------------- |
| Aggregate  (cost=1.04..1.05 rows=1 width=8)                 |
|   ->  Seq Scan on storage  (cost=0.00..1.04 rows=1 width=4) |
|         Filter: (resource_name = 'food'::text)              |

Similar to the previous query, indexing will not help as the storage table is too small and fits on one page.

Index Command: create index resource_idx ON storage (resource_name)

Explain:

| QUERY PLAN                                                  |
| ----------------------------------------------------------- |
| Aggregate  (cost=1.04..1.05 rows=1 width=8)                 |
|   ->  Seq Scan on storage  (cost=0.00..1.04 rows=1 width=4) |
|         Filter: (resource_name = 'food'::text)              |

As expected, no performance uplift.

### jobs/assignments
Query:
```
UPDATE villagers 
        SET job_id = (
            SELECT id 
            FROM jobs 
            WHERE job_name = :job_name
        )
        WHERE id IN (
            SELECT id 
            FROM villagers 
            WHERE job_id = 0 
            LIMIT :assigned
        )
        RETURNING id
```
EXPLAIN (Using :assigned = 1000):

| QUERY PLAN                                                                                                 |
| ---------------------------------------------------------------------------------------------------------- |
| Update on villagers  (cost=140.09..7915.33 rows=1000 width=38)                                             |
|   InitPlan 1 (returns $0)                                                                                  |
|     ->  Index Scan using jobs_job_name_key on jobs  (cost=0.15..8.17 rows=1 width=4)                       |
|           Index Cond: (job_name = 'hunter'::text)                                                          |
|   ->  Nested Loop  (cost=131.92..7907.16 rows=1000 width=38)                                               |
|         ->  HashAggregate  (cost=131.49..141.49 rows=1000 width=32)                                        |
|               Group Key: "ANY_subquery".id                                                                 |
|               ->  Subquery Scan on "ANY_subquery"  (cost=0.00..128.99 rows=1000 width=32)                  |
|                     ->  Limit  (cost=0.00..118.99 rows=1000 width=4)                                       |
|                           ->  Seq Scan on villagers villagers_1  (cost=0.00..27973.03 rows=235080 width=4) |
|                                 Filter: (job_id = 0)                                                       |
|         ->  Index Scan using villagers_index on villagers  (cost=0.43..7.77 rows=1 width=10)               |
|               Index Cond: (id = "ANY_subquery".id)                                                         |

Explain shows that the first sub query that finds the job id where the id matches the name already uses an index, automically assigned by PostGres due to the schema having job_name unique. The next subquery searches the villagers table where job_id = 0 using sequential scan. Since we always search the villagers where job_id = 0 (meaning unassigned job), it would be worth giving it an index. The last part of the planner uses an index to search those villagers by id (unique, index made by PostGres).

Index Command: create index villager_unassigned_idx ON villagers (job_id) WHERE (job_id = 0)

create index job_villagers_idx ON villagers (job_id)

Explain:

| QUERY PLAN                                                                                                 |
| ---------------------------------------------------------------------------------------------------------- |
| Update on villagers  (cost=140.09..7915.33 rows=1000 width=38)                                             |
|   InitPlan 1 (returns $0)                                                                                  |
|     ->  Index Scan using jobs_job_name_key on jobs  (cost=0.15..8.17 rows=1 width=4)                       |
|           Index Cond: (job_name = 'hunter'::text)                                                          |
|   ->  Nested Loop  (cost=131.92..7907.16 rows=1000 width=38)                                               |
|         ->  HashAggregate  (cost=131.49..141.49 rows=1000 width=32)                                        |
|               Group Key: "ANY_subquery".id                                                                 |
|               ->  Subquery Scan on "ANY_subquery"  (cost=0.00..128.99 rows=1000 width=32)                  |
|                     ->  Limit  (cost=0.00..118.99 rows=1000 width=4)                                       |
|                           ->  Seq Scan on villagers villagers_1  (cost=0.00..27973.03 rows=235080 width=4) |
|                                 Filter: (job_id = 1)                                                       |
|         ->  Index Scan using villagers_index on villagers  (cost=0.43..7.77 rows=1 width=10)               |
|               Index Cond: (id = "ANY_subquery".id)                                                         |

Unfortunately the index does not improve performance. This may be due to the amount of rows (235,080 rows) needed to index where traversing sequnetially is faster. Since the width is only 4 it isn't enough data to extend another page, so using the index would not make sense (indexing would require checking the index page then the data). This does work with jobs with small amounts of villagers (see below), since the index will directly lead to the small amount of data rather than traversing sequentially; but this does not help this endpoint

Explain: 

| QUERY PLAN                                                                                                                  |
| --------------------------------------------------------------------------------------------------------------------------- |
| Update on villagers  (cost=17.05..25.08 rows=1 width=38)                                                                    |
|   InitPlan 1 (returns $0)                                                                                                   |
|     ->  Index Scan using jobs_job_name_key on jobs  (cost=0.15..8.17 rows=1 width=4)                                        |
|           Index Cond: (job_name = 'hunter'::text)                                                                           |
|   ->  Nested Loop  (cost=8.88..16.91 rows=1 width=38)                                                                       |
|         ->  HashAggregate  (cost=8.46..8.47 rows=1 width=32)                                                                |
|               Group Key: "ANY_subquery".id                                                                                  |
|               ->  Subquery Scan on "ANY_subquery"  (cost=0.43..8.46 rows=1 width=32)                                        |
|                     ->  Limit  (cost=0.43..8.45 rows=1 width=4)                                                             |
|                           ->  Index Scan using job_villagers_idx on villagers villagers_1  (cost=0.43..8.45 rows=1 width=4) |
|                                 Index Cond: (job_id = 6)                                                                    |
|         ->  Index Scan using villagers_index on villagers  (cost=0.43..8.45 rows=1 width=10)                                |
|               Index Cond: (id = "ANY_subquery".id)                                                                          |


### village/villager
Query:
```
        INSERT INTO villagers (age, nourishment)
        VALUES (:age, :nourishment)
```

Explain: 
| QUERY PLAN                                            |
| ----------------------------------------------------- |
| Insert on villagers  (cost=0.00..0.01 rows=0 width=0) |
|   ->  Result  (cost=0.00..0.01 rows=1 width=16)       |

Since this is simply an insert, the query planner simply does an insert. villager_id indexing is running in the background to auto increment the id. The only way to speed up this query is by removing indexing (less writing to the db) but that is not possible.





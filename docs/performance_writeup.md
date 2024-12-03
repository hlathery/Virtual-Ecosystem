# Fake Data Modeling
Python File to Spawn 1 million rows: 

The amount of final rows in the villagers table is approximately 1,212,248 rows/records (as shown below). biomes contains 10 rows, buildings has 7 rows, catalog has 5, entities has 12, jobs has 7, and storage has 3.

![image](https://github.com/user-attachments/assets/cb9fef7b-1a7e-4562-95b4-fd7a7b1e505f)

The reason our project is only scaled towards villagers is because the other tables act as keys or catalogs that are referenced as foreign keys in other tables (for example there are only 7 jobs that exist in the game, but each villager is assigned one of these jobs).
Other tables do not make sense to scale to large values due to frontend limitations. Biomes only has 10 rows due to the frontend being limited to only showing an x number of biomes.
Villagers are the only quantity that can be appended to, other tables are updates only. One consideration was implementing a ledgerized design for resources in the storage table which would be another avenue to scale, but due to time constraints we were unable to.

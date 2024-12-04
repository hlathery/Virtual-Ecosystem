from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from sqlalchemy import update, text, bindparam
from sqlalchemy.orm import session
from src import database as db
from enum import Enum
from typing import Dict
from fastapi import HTTPException, status
import random

router = APIRouter(
    prefix="/eco",
    tags=["ecological"],
    dependencies=[Depends(auth.get_api_key)],
)

class EntityType(str, Enum):
    predators = "predators"
    prey = "prey"
    trees = "trees"
    plants = "plants"
    water = "water"

class Entity(BaseModel):
    nourishment: int
    entity_type: EntityType
    biome_id: int

class EntityUpdate(BaseModel):
    id: int
    nourishment: float

class BiomeCounts(BaseModel):
    ocean: int = 0
    forest: int = 0
    grassland: int = 0
    beach: int = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "ocean": 9,
                "forest": 6,
                "grassland": 1,
                "beach": 4
            }
        }

class DisasterType:
    FLOOD = "flood"  # Affects coastal biomes more
    PLAGUE = "plague"  # Affects densely populated areas
    FAMINE = "famine"  # Reduces food/nourishment
    STORM = "storm"  # General damage
    REBELLION = "rebellion"  # Based on low satisfaction/resources


@router.get("/")
def get_eco_overview():
    """
    Returns a general overview of the ecosystem with each biome listed once, showing all entities
    and their nourishment levels within that biome.
    """
    
    overview_query = """
        SELECT 
            biomes.id,
            biome_name,
            STRING_AGG(
                entity_type || ': ' || nourishment::text,
                ', ' 
                ORDER BY entity_type
            ) as entity_details
        FROM biomes
        LEFT JOIN entities ON biomes.id = entities.biome_id
        GROUP BY biomes.id, biome_name
        ORDER BY biomes.id;
    """
    
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text(overview_query))
    
    overview = []   
    for row in result:
        overview.append({
                "biome_id": row.id,
                "biome_name": row.biome_name,
                "entities": row.entity_details if row.entity_details else "No entities"
            })

    return overview

# COMPLEX ENDPOINT
@router.post("/biomes")
def post_biome_counts(biomes: BiomeCounts):
    """
    Posts the biome counts from flood fill.
    Creates new biome entries based on the counts.
    """

    try: # trying to connect and retrieve the data from flood fill
        biomes_dict = biomes.dict()
        print("Received biomes:", biomes_dict)

        insert_data = []
        for biome_name, count in biomes_dict.items():
            if count > 0:
                insert_data.extend([(biome_name.lower(),) for _ in range(count)])
        
        if insert_data:
            insert_query = """
                INSERT INTO biomes (biome_name)
                VALUES (:biome_name)
            """
            with db.engine.begin() as connection:
                connection.execute(
                    sqlalchemy.text(insert_query),
                    [{"biome_name": biome_name} for biome_name, in insert_data]
                )

        return {"message": "Biome counts recorded successfully"}
    except Exception as e:
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to insert biome counts: {str(e)}"
        )
    

@router.get("/plants/{biome_id}", status_code=status.HTTP_200_OK, response_description="Success")
def biome_plants(biome_id: int):
    """
    Returns the id and nourishment of plants in the requested biome.
    """
    with db.engine.begin() as connection:
        biome_check_query = """
            SELECT id FROM biomes WHERE id = :biome_id
        """
        biome = connection.execute(
            sqlalchemy.text(biome_check_query), 
            {"biome_id": biome_id}
        ).fetchone()
        
        if not biome: # if the biome doesnt exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Biome with id {biome_id} not found"
            )
        
        plants_query = """
            SELECT
                id,
                entity_type AS type,
                nourishment
            FROM entities
            WHERE entity_type = 'plants'
                AND biome_id = :biome_id
            """
        plants = connection.execute(
            sqlalchemy.text(plants_query), 
            {"biome_id": biome_id}
        ).fetchone()
        
        if not plants:
            return {
                "entity_type": "plants",
                "nourishment": 0
            }

    return {
        "id": plants.id,
        "entity_type": plants.type,
        "nourishment": plants.nourishment
    }

    
@router.post("/entity", status_code=status.HTTP_201_CREATED, response_description="Success Creation")
def spawn_entity(entity_to_spawn: list[Entity]):
    """
    Takes in a list of entities to be spawned in the requested biome.
    Will only create new entities if they don't already exist in the specified biome.
    Returns early if no entities are provided.
    """
   
    if not entity_to_spawn:
        return {
            "message": "No entities provided to spawn",
            "entities_created": 0
        }
    
    biome_ids = {entity.biome_id for entity in entity_to_spawn}
    
    with db.engine.begin() as connection:
        biome_check_query = """
            SELECT id FROM biomes WHERE id = ANY(:biome_ids)
        """
        existing_biomes = connection.execute(
            sqlalchemy.text(biome_check_query),
            {"biome_ids": list(biome_ids)}
        ).fetchall()
        
        existing_biome_ids = {row.id for row in existing_biomes}
        missing_biomes = biome_ids - existing_biome_ids
        
        if missing_biomes: # if that biome doesnt exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Biomes not found: {', '.join(str(id) for id in missing_biomes)}"
            )
        
        check_query = """
            SELECT entity_type, biome_id 
            FROM entities 
            WHERE (entity_type, biome_id) IN :entity_biome_pairs
        """
        
        entity_biome_pairs = tuple(
            (entity.entity_type, entity.biome_id) 
            for entity in entity_to_spawn
        )
        
        existing = connection.execute(
            sqlalchemy.text(check_query),
            {"entity_biome_pairs": entity_biome_pairs}
        ).fetchall()

        if existing: # checking to see if that biome exists
            conflicts = [f"{row.entity_type} in biome {row.biome_id}" for row in existing]
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cannot spawn entities: {', '.join(conflicts)} already exist"
            )
        
        insert_query = """
            INSERT INTO entities (entity_type, biome_id, nourishment)
            VALUES (:entity_type, :biome_id, :nourishment)
        """
        
        entity_list = [
            {
                "nourishment": entity.nourishment,
                "entity_type": entity.entity_type,
                "biome_id": entity.biome_id
            }
            for entity in entity_to_spawn
        ]
        
        connection.execute(sqlalchemy.text(insert_query), entity_list)

    return {
        "message": "Entities successfully spawned",
        "entities_created": len(entity_list)
    }
    

@router.put("/entity/nourishment", response_description="Nourishment Updated")
def update_nourishment(entity_updates: list[EntityUpdate]):
    """
    Updates nourishment values for specific entities by their IDs.
    Ensures no negative IDs are allowed.
    """   
    
    if not entity_updates: 
        return {
            "message": "No updates provided",
            "entities_updated": 0
        }
    
    for update in entity_updates: # used for error handling if the id goes negative
        if update.id < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Negative ID not allowed: {update.id}"
            )
    
    update_list = [
        {
            "id": update.id,
            "nourishment": update.nourishment
        }
        for update in entity_updates
    ]
    
    update_query = """
        UPDATE entities
        SET nourishment = nourishment + :nourishment
        WHERE id = :id
    """
    
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(update_query), update_list)
        connection.execute(sqlalchemy.text("UPDATE entities SET nourishment = 100 WHERE nourishment > 100"))

    if result.rowcount == 0:
        return {
        "message": "Provided id does not exist",
        "entities_updated": result.rowcount
        }
    elif result.rowcount > 0:
        return {
            "message": "Nourishment updated successfully",
            "entities_updated": len(update_list)
        }


@router.get("/prey/{biome_id}", status_code=status.HTTP_200_OK, response_description="Success")
def biome_prey(biome_id: int):
    """
    Returns the id and nourishment of prey in the requested biome.
    """

   
    with db.engine.begin() as connection:
        biome_check_query = """
            SELECT id FROM biomes WHERE id = :biome_id
        """
        biome = connection.execute(
            sqlalchemy.text(biome_check_query), 
            {"biome_id": biome_id}
        ).fetchone()
        
        if not biome: # if the biome doesnt exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Biome with id {biome_id} not found"
            )
        
        prey_query = """
            SELECT
                id,
                entity_type AS type,
                nourishment
            FROM entities
            WHERE entity_type = 'prey'
                AND biome_id = :biome_id
            """
        prey = connection.execute(
            sqlalchemy.text(prey_query), 
            {"biome_id": biome_id}
        ).fetchone()
        
        if not prey:
            return {
                "entity_type": "prey",
                "nourishment": 0
            }

    
    return {
        "id": prey.id,
        "entity_type": prey.type,
        "nourishment": prey.nourishment
    }


@router.get("/predator/{biome_id}", status_code=status.HTTP_200_OK, response_description="Success")
def biome_predator(biome_id: int):
   """
   Returns a list of predator and their id and nourishment in the requested biome.
   """
   
   with db.engine.begin() as connection:
       biome_check_query = """
           SELECT id FROM biomes WHERE id = :biome_id
       """
       biome = connection.execute(
           sqlalchemy.text(biome_check_query), 
           {"biome_id": biome_id}
       ).fetchone()
       
       if not biome: # if the biome doesnt exist
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Biome with id {biome_id} not found"
           )
       
       predator_query = """
           SELECT
                id,
                entity_type AS type,
                nourishment
           FROM entities
           WHERE entity_type = 'predators'
               AND biome_id = :biome_id
       """
       predator = connection.execute(
           sqlalchemy.text(predator_query), 
           {"biome_id": biome_id}
       ).fetchone()
       
       if not predator:
           return {
               "entity_type": "predators", 
               "nourishment": 0
           }
    
   return {
       "id": predator.id,
       "entity_type": predator.type,
       "nourishment": predator.nourishment
   }


@router.get("/water/{biome_id}", status_code=status.HTTP_200_OK, response_description="Success")
def biome_water(biome_id: int):
   """
   Returns a list of water and their id and nourishment in the requested biome.
   """
   with db.engine.begin() as connection:
       biome_check_query = """
           SELECT id FROM biomes WHERE id = :biome_id
       """
       biome = connection.execute(
           sqlalchemy.text(biome_check_query), 
           {"biome_id": biome_id}
       ).fetchone()
       
       if not biome: # if the biome doesnt exist
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Biome with id {biome_id} not found"
           )
       
       water_query = """
           SELECT
                id,
                entity_type AS type,
                nourishment
           FROM entities
           WHERE entity_type = 'water'
               AND biome_id = :biome_id
       """
       water = connection.execute(
           sqlalchemy.text(water_query), 
           {"biome_id": biome_id}
       ).fetchone()
       
       if not water:
           return {
               "entity_type": "water",
               "nourishment": 0
           }

   return {
       "id": water.id,
       "entity_type": water.type,
       "nourishment": water.nourishment
   }


@router.get("/trees/{biome_id}", status_code=status.HTTP_200_OK, response_description="Success")
def biome_trees(biome_id: int):
   """
   Returns a list of trees and their id and nourishment in the requested biome.
   """
   with db.engine.begin() as connection:
       biome_check_query = """
           SELECT id FROM biomes WHERE id = :biome_id
       """
       biome = connection.execute(
           sqlalchemy.text(biome_check_query), 
           {"biome_id": biome_id}
       ).fetchone()
       
       if not biome: # if the biome doesnt exist
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Biome with id {biome_id} not found"
           )
       
       trees_query = """
           SELECT
                id,
                entity_type AS type,
                nourishment
           FROM entities
           WHERE entity_type = 'trees'
               AND biome_id = :biome_id
       """
       trees = connection.execute(
           sqlalchemy.text(trees_query), 
           {"biome_id": biome_id}
       ).fetchone()
       
       if not trees:
           return {
               "entity_type": "trees",
               "nourishment": 0
           }

   return {
       "id": trees.id,
       "entity_type": trees.type,
       "nourishment": trees.nourishment
   }


@router.delete("/clean/", status_code=status.HTTP_200_OK, response_description="Success")
def clean():
    """
    Deletes any entities with nourishment 0 or below
    """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("DELETE FROM entities WHERE nourishment <= 0"))
        res = connection.execute(sqlalchemy.text(
            """
                SELECT
                    biomes.id,
                    COALESCE(COUNT(entities.id),0) AS cnt
                FROM entities
                JOIN biomes ON entities.biome_id = biomes.id
                GROUP BY biomes.id
            """
        ))
        update = []
        for row in res:
            if row.cnt == 0:
                update.append({'id': row.id})
        if update:
            connection.execute(sqlalchemy.text("DELETE FROM biomes WHERE id = :id"), update)

    return "Successfully Deleted Enities With Nourishment 0 Or Below and Biomes With no Entities"


# global variable for disasters
disaster_counter = 0

# random disaster
@router.post("/disaster", response_description="Disaster Check")
def check_disaster():
    """
    Has a chance to cause a random disaster, increases chance of disaster by 2% until one occurs.
    When a disaster occurs, up to 5 villagers can be killed.
    """   

    global disaster_counter
    
    try:
        base_probability = 0.1 + (disaster_counter * 0.02)
        print(f"Current disaster probability: {base_probability * 100}%")

        # disaster occurred
        if random.random() < base_probability:
            disaster_counter = 0
            
            disaster_type = random.choice([ # creating the disasters
                DisasterType.FLOOD,
                DisasterType.PLAGUE,
                DisasterType.FAMINE,
                DisasterType.STORM,
                DisasterType.REBELLION
            ])
            
            with db.engine.begin() as connection:
                # 0-5 villagers may die
                affected_count = random.randint(0, 5)
                
                # choosing a disaster
                if disaster_type in [DisasterType.FLOOD, DisasterType.PLAGUE, DisasterType.STORM, DisasterType.REBELLION]:
                    damage_query = """
                        WITH random_villagers AS (
                            SELECT id 
                            FROM villagers
                            WHERE id > 0
                            ORDER BY RANDOM()
                            LIMIT :count
                        )
                        DELETE FROM villagers 
                        WHERE id IN (
                            SELECT id 
                            FROM random_villagers
                        )
                        RETURNING id;
                    """
                    result = connection.execute(
                        sqlalchemy.text(damage_query), 
                        {"count": affected_count}
                    )
                    deleted = len(result.fetchall())
                
                elif disaster_type == DisasterType.FAMINE: # this disaster destroys plants
                    plants_prey_dmg = """
                        UPDATE entities
                        SET nourishment = nourishment * 0.7
                        WHERE entity_type IN ('plants', 'prey')
                        RETURNING id;
                    """
                    connection.execute(sqlalchemy.text(plants_prey_dmg))

                    damage_query = """
                        WITH random_villagers AS (
                            SELECT id 
                            FROM villagers
                            WHERE id > 0
                            ORDER BY RANDOM()
                            LIMIT :count
                        )
                        DELETE FROM villagers 
                        WHERE id IN (
                            SELECT id 
                            FROM random_villagers
                        )
                        RETURNING id;
                    """
                    result = connection.execute(
                        sqlalchemy.text(damage_query), 
                        {"count": affected_count}
                    )

                    deleted = len(result.fetchall())
            
    
            return {
                "message": f"Disaster occurred: {disaster_type}",
                "Villagers Killed": deleted
            }
        
        else:
            disaster_counter += 1

    
            return {
                "message": "No disaster occurred",
                "current_probability": f"{base_probability * 100}%",
                "days_without_disaster": disaster_counter
            }
            
    except Exception as e:
        print(f"Disaster system error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process disaster check: {str(e)}"
        )

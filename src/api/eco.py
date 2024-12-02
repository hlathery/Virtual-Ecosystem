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
@router.post("/biomes/")
def post_biome_counts(biomes: BiomeCounts):
    """
    Posts the biome counts from flood fill.
    Creates new biome entries based on the counts.
    """

    try:
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
    

@router.get("/plants/{biome_id}", status_code = status.HTTP_200_OK, response_description="Success")
def plants_overview(biome_id: int):
    """
    Returns the total nourishment of plants in the entire ecosystem
    """
    
    plants_query =  """
                        SELECT id,
                            entity_type AS type,
                            nourishment
                        FROM entities
                        WHERE entity_type = 'plants'
                            AND biome_id = :biome_id
                    """
    
    with db.engine.begin() as connection:
        plants_table = connection.execute(sqlalchemy.text(plants_query), {'biome_id':biome_id}).fetchone()
        id = plants_table.id
        entity_type = plants_table.type
        total = plants_table.nourishment

    return {"id": id,
            "entity_type": entity_type,
            "nourishment": total}
    

    
@router.post("/entity", status_code=status.HTTP_201_CREATED, response_description="Success Creation")
def spawn_entity(entity_to_spawn: list[Entity]):
    """
    Takes in a list of entities to be spawned in the requested biome.
    Will only create new entities if they don't already exist in the specified biome.
    """
    

    if not entity_to_spawn:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot spawn entities: Empty list provided"
        )
    

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
        
        if missing_biomes:
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

        if existing:
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

    return {"message": "Entities successfully spawned"}
    

@router.put("/entity/nourishment", response_description="Nourishment Updated")
def update_nourishment(entity_updates: list[EntityUpdate]):
    """
    Updates nourishment values for specific entities by their IDs.
    """
    
    if not entity_updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No updates provided"
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
        connection.execute(sqlalchemy.text(update_query), update_list)
    
    return {"message": "Nourishment updated successfully"}


@router.get("/prey/{biome_id}", status_code = status.HTTP_200_OK, response_description="Success")
def biome_prey(biome_id: int):
    """
    Returns the nourishment of prey in the requested biome 
    """
    with db.engine.begin() as connection:
        
        prey_query = """
                        SELECT id,
                            entity_type AS type,
                            nourishment
                        FROM entities
                        WHERE entity_type = 'prey'
                            AND biome_id = :biome_id
                     """
        prey = connection.execute(sqlalchemy.text(prey_query), {"biome_id":biome_id}).fetchone()

    id = prey.id
    entity_type = prey.type
    amount = prey.nourishment
    return {
            "id": id,
            "entity_type": entity_type,
            "nourishment": amount
        }


@router.get("/predator/{biome_id}", status_code = status.HTTP_200_OK, response_description="Success")
def biome_predator(biome_id: int):
    """
    Returns a list of predator and their nourishment in the requested biome
    """
    with db.engine.begin() as connection:
        predator_query = """
                        SELECT id,
                            entity_type AS type,
                            nourishment
                        FROM entities
                        WHERE entity_type = 'predators'
                            AND biome_id = :biome_id
                     """
        predator = connection.execute(sqlalchemy.text(predator_query), {"biome_id":biome_id}).fetchone()

    id = predator.id
    entity_type = predator.type
    nourish_amount = predator.nourishment
    return {
            "id": id,
            "entity_type": entity_type,
            "nourishment": nourish_amount
        }


@router.get("/water/{biome_id}", status_code = status.HTTP_200_OK, response_description="Success")
def biome_water(biome_id: int):
    """
    Returns the water nourishment of the given biome
    """
    with db.engine.begin() as connection:
        water_query = """
                        SELECT id,
                            entity_type AS type,
                            nourishment
                        FROM entities
                        WHERE entity_type = 'water'
                            AND biome_id = :biome_id
                     """
        water = connection.execute(sqlalchemy.text(water_query), {"biome_id":biome_id}).fetchone()

    id = water.id
    entity_type = water.type
    nourish_amount = water.nourishment
    return {
            "id": id,
            "entity_type": entity_type,
            "nourishment": nourish_amount
        }

@router.get("/trees/{biome_id}", status_code = status.HTTP_200_OK, response_description="Success")
def biome_trees(biome_id: int):
    """
    Returns the tree nourishment of the given biome
    """
    with db.engine.begin() as connection:
        water_query = """
                        SELECT id,
                            entity_type AS type,
                            nourishment
                        FROM entities
                        WHERE entity_type = 'trees'
                            AND biome_id = :biome_id
                     """
        trees = connection.execute(sqlalchemy.text(water_query), {"biome_id":biome_id}).fetchone()

    id = trees.id
    entity_type = trees.type
    nourish_amount = trees.nourishment
    return {
            "id": id,
            "entity_type": entity_type,
            "nourishment": nourish_amount
        }

@router.delete("/clean/", status_code = status.HTTP_200_OK, response_description="Success")
def clean_entities():
    """
    Deletes biomes that have zero nourishment or below
    """
    with db.engine.begin() as connection:
        clean_query = """
                        DELETE
                        FROM entities
                        WHERE nourishment <= 0
                     """
        connection.execute(sqlalchemy.text(clean_query))

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
            
            disaster_type = random.choice([
                DisasterType.FLOOD,
                DisasterType.PLAGUE,
                DisasterType.FAMINE,
                DisasterType.STORM,
                DisasterType.REBELLION
            ])
            
            with db.engine.begin() as connection:
                # 0-5 villagers may die
                affected_count = random.randint(0, 5)
                
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
                
                elif disaster_type == DisasterType.FAMINE:
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

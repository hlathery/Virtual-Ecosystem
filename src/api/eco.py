from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from sqlalchemy import update
from sqlalchemy.orm import session
from src import database as db
from enum import Enum
from typing import Dict
from fastapi import HTTPException, status

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



@router.post("/")
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
def post_biome_counts(biomes: Dict[str, int]):

    # Every time a map is generated, a flood fill algorithm is called and all biomes are pushed into the database.

    """
    Posts the biome counts from flood fill.
    Creates new biome entries based on the counts using a single database call.
    """
    print("Received biomes:", biomes)

    try:
    
        insert_values = []
        for biome_name, count in biomes.items():
            if count > 0:
                insert_values.extend([{"biome_name": biome_name.lower()} for _ in range(count)])

        if insert_values:
            insert_query = """
                INSERT INTO biomes (biome_name)
                SELECT val.biome_name
                FROM unnest(:values)
                AS val(biome_name);
            """
            
            with db.engine.begin() as connection:
                connection.execute(
                    sqlalchemy.text(insert_query),
                    {"values": insert_values}
                )
            
        return {"message": "Biome counts recorded successfully"}
    except Exception as e:
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to insert biome counts: {str(e)}"
        )



@router.get("/plants/", status_code = status.HTTP_200_OK, response_description="Success")
def plants_overview():
    """
    Returns the total nourishment of plants in the entire ecosystem
    """
    
    plants_query =  """
                        SELECT entity_type AS type, 
                            SUM(nourishment) AS nourishment
                        FROM entities
                        WHERE entity_type = 'plants'
                        GROUP BY entity_type
                    """
    
    with db.engine.begin() as connection:
        plants_table = connection.execute(sqlalchemy.text(plants_query)).fetchone()
        entity_type = plants_table.type
        total = plants_table.nourishment

    return {"entity_type": entity_type,
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
def biome_prey(biome_id : int):
    """
    Returns the nourishment of prey in the requested biome 
    """
    with db.engine.begin() as connection:
        
        prey_query = """
                        SELECT entity_type AS type, 
                            SUM(nourishment) AS nourishment
                        FROM entities
                        WHERE entity_type = 'prey'
                            AND biome_id = :biome_id
                        GROUP BY entity_type
                     """
        prey = connection.execute(sqlalchemy.text(prey_query), {"biome_id":biome_id}).fetchone()

    entity_type = prey.type
    amount = prey.nourishment
    return({
        "entity_type": entity_type,
        "nourishment": amount
    })


@router.get("/predator/{biome_id}", status_code = status.HTTP_200_OK, response_description="Success")
def biome_predator(biome_id: int):
    """
    Returns a list of predator and their nourishment in the requested biome
    """
    with db.engine.begin() as connection:
        predator_query = """
                        SELECT entity_type AS type, 
                            SUM(nourishment) AS nourishment
                        FROM entities
                        WHERE entity_type = 'predators'
                            AND biome_id = :biome_id
                        GROUP BY entity_type
                     """
        predator = connection.execute(sqlalchemy.text(predator_query), {"biome_id":biome_id}).fetchone()

    entity_type = predator.type
    nourish_amount = predator.nourishment
    return({
        "entity_type": entity_type,
        "nourishment": nourish_amount
    })





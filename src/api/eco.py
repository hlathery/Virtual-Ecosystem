from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from sqlalchemy import update
from sqlalchemy.orm import session
from src import database as db
from enum import Enum
from typing import Dict

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
    quantity: int
    nourishment: int
    entity_type: EntityType
    biome_id: int




# @router.post("/")
# def get_eco_overview():
#     """
#     Returns a general overview of the ecosystem and its characteristics such as: 
#     predators and prey and how many there are, the characteristics of each body of water and their id, 
#     plants and how many there are, resources (trees for wood, mine shafts for mining, etc.).
#     """

#     return "OK"

@router.post("/biomes/")
def post_biome_counts(biomes: Dict[str, int]):
    """
    Posts the biome counts from flood fill.
    """
    ocean_values = ", ".join(["('ocean')"] * biomes.get("Ocean", 0))
    forest_values = ", ".join(["('forest')"] * biomes.get("Forest", 0))

    with db.engine.begin() as connection:

        if biomes.get("Ocean", 0) > 0:
            connection.execute(sqlalchemy.text("INSERT INTO biomes (biome_type) VALUES (:ocean_values)"),
                               {"ocean_values": ocean_values})
        
        if biomes.get("Forest", 0) > 0:
            connection.execute(sqlalchemy.text("INSERT INTO biomes (biome_type) VALUES (:forest_values)"),
                               {"forest_values": forest_values})



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
    

    
@router.post("/entity", status_code = status.HTTP_201_CREATED, response_description="Success Creation")
def spawn_entity(entity_to_spawn : list[Entity]):
    """
    Takes in a list of entities to be spawned in the requested biome
    """
    with db.engine.begin() as connection:
        entity_list = []
        for entity in entity_to_spawn:
            entity_list.append({"nourishment": entity.nourishment,
                                "entity_type": entity.entity_type,
                                "biome_id": entity.biome_id})    
        entity_query = """
                        UPDATE entities
                        SET nourishment = nourishment + :nourishment
                        WHERE entity_type = :entity_type
                            AND biome_id = :biome_id
                      """
        connection.execute(sqlalchemy.text(entity_query),entity_list)
    return {"success"}
    



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





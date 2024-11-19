from fastapi import APIRouter, Depends
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
    predator = "predator"
    prey = "prey"
    tree = "tree"
    plants = "plants"
    water = "water"

class Entity(BaseModel):
    # ent_id: int
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



@router.get("/plants/")
def plants_overview():
    """
    Returns the amount of plants in the entire ecosystem
    """
    
    plants_query =  """
                        SELECT entity_type AS type, 
                            SUM(quantity) AS total
                        FROM entitys
                        WHERE entity_type = 'plants'
                        GROUP BY entity_type
                    """
    
    with db.engine.begin() as connection:
        plants_table = connection.execute(sqlalchemy.text(plants_query)).fetchone()
        entity_type = plants_table.type
        total = plants_table.total

    return {"entity_type": entity_type,
            "quantity": total}
    

# @router.put("/grab_water")
# def collect_water(water_bodies: list[Entity]):
#     """
#     The call takes in a list of bodies of water that the user will harvest water from 
#     """
#     return "OK"




@router.post("/entity")
def spawn_entity(prey_to_spawn : list[Entity]):
    """
    Takes in a list of entities to be spawned in the requested biome
    AVAILABLE BIOMES (biome_id : name)
    1 : Forest
    2 : Grasslands
    3 : Beach
    """
    with db.engine.begin() as connection:
        entity_list = []
        for entity in prey_to_spawn:
            entity_list.append({"nourishment": entity.nourishment,
                                "entity_type": entity.entity_type,
                                "biome_id": entity.biome_id})    
        prey_query = """
                        UPDATE entitys
                        SET nourishment = nourishment + :nourishment
                        WHERE entity_type = :entity_type
                            AND biome_id = :biome_id
                      """
        connection.execute(sqlalchemy.text(prey_query),entity_list)
    return "OK"
    



@router.get("/prey/{biome_id}")
def biome_prey(biome_id : int):
    """
    Returns the amount of prey in the requested biome 
    AVAILABLE BIOMES (biome_id : name)
    1 : Forest
    2 : Grasslands
    3 : Beach
    """
    with db.engine.begin() as connection:
        prey_query = """
                        SELECT entity_type AS type, 
                            SUM(quantity) AS total
                        FROM entitys
                        WHERE entity_type = 'prey'
                            AND biome_id = :biome_id
                        GROUP BY entity_type
                     """
        prey = connection.execute(sqlalchemy.text(prey_query), {"biome_id":biome_id}).fetchone()

    entity_type = prey.type
    amount = prey.total
    return({
        "entity_type": entity_type,
        "amount": amount
    })


@router.get("/predator/{biome_id}")
def biome_predator(biome_id: int):
    """
    Returns a list of predator and their amounts in the requested biome
    AVAILABLE BIOMES (biome_id : name)
    1 : Forest
    2 : Grasslands
    3 : Beach
    """
    with db.engine.begin() as connection:
        predator_query = """
                        SELECT entity_type AS type, 
                            SUM(quantity) AS total
                        FROM entitys
                        WHERE entity_type = 'predator'
                            AND biome_id = :biome_id
                        GROUP BY entity_type
                     """
        predator = connection.execute(sqlalchemy.text(predator_query), {"biome_id":biome_id}).fetchone()

    entity_type = predator.type
    amount = predator.total
    return({
        "entity_type": entity_type,
        "amount": amount
    })





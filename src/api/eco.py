from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from sqlalchemy import update
from sqlalchemy.orm import session
from src import database as db
from typing import Dict

router = APIRouter(
    prefix="/eco",
    tags=["ecological"],
    dependencies=[Depends(auth.get_api_key)],
)

class Entity(BaseModel):
    # ent_id: int
    quantity: int
    nourishment: int
    entity_type: str
    biome_id: int




@router.post("/")
def get_eco_overview():
    """
    Returns a general overview of the ecosystem and its characteristics such as: 
    predators and prey and how many there are, the characteristics of each body of water and their id, 
    plants and how many there are, resources (trees for wood, mine shafts for mining, etc.).
    """
    with db.engine.begin() as connection: 
        result = connection.execute(sqlalchemy.text("SELECT biome_name, COUNT(*) FROM biomes GROUP BY biome_name"))


    biome_counts = {row[0]: row[1] for row in result}

    print(biome_counts)


    return "OK"

@router.post("/biomes/")
def post_biome_counts(biomes: Dict[str, int]):
    """
    Posts the biome counts from flood fill.
    """
    
    with db.engine.begin() as connection:
        insert_values = []
        
        if biomes.get("Ocean", 0) > 0:
            ocean_count = biomes["Ocean"]
            insert_values.extend(["('ocean')"] * ocean_count)
            
        if biomes.get("Forest", 0) > 0:
            forest_count = biomes["Forest"]
            insert_values.extend(["('forest')"] * forest_count) 

        if biomes.get("Beach", 0) > 0:
            forest_count = biomes["Beach"]
            insert_values.extend(["('beach')"] * forest_count)
        
         
        if biomes.get("Grass", 0) > 0:
            forest_count = biomes["Grass"]
            insert_values.extend(["('grass')"] * forest_count)


        if insert_values:
            all_values = ', '.join(insert_values)
            insert_query = "INSERT INTO biomes (biome_name) VALUES " + all_values + ";" # i dont know why: it only works like this
            connection.execute(sqlalchemy.text(insert_query))

    return "Ok"


@router.put("/grow_plants")
def grow_plants(plants_to_grow: list[Entity]):
    """
    Takes in a request that contains of list of plant seeds to be planted in the 
    requested biome
    """
    with db.engine.begin() as connection:
        plants_list = []
        for plant in plants_to_grow:
            plants_list.append({ "quantity": plant.quantity,
                                "nourishment": plant.nourishment,
                                "entity_type": plant.entity_type,
                                "biome_id": plant.biome_id})    
        plant_query = """
                        UPDATE entitys
                        SET quantity = quantity + :quantity,
                            nourishment = nourishment + :nourishment
                        WHERE entity_type = :entity_type
                            AND biome_id = :biome_id
                      """
        connection.execute(sqlalchemy.text(plant_query),plants_list)

    return "OK"




@router.get("/plants/")
def plants_overview():
    """
    Returns the amount of plants in the entire ecosystem
    """
    plants_list = []
    plants_query =  """
                        SELECT entity_type, 
                            SUM(quantity) as Total
                        FROM entitys
                        WHERE entity_type = 'plants'
                        GROUP BY entity_type
                    """
    
    with db.engine.begin() as connection:
        plants_table = connection.execute(sqlalchemy.text(plants_query)).fetchone()
        entity_type = plants_table[0]
        total = plants_table[1]

        plants_list.append({
            "entity_type": entity_type,
            "quantity": total
        })
        
    print(f"Total plants in ecosystem: {plants_list} ")
    return plants_list
    
    

@router.get("/prey/")
def prey_overview():
    """
    Returns a list of all prey and the amount in the entire ecosystem
    """
    prey_list = []
    prey_query =    """
                        SELECT entity_type,
                            SUM(quantity) as Total
                        FROM entitys
                        WHERE entity_type = 'prey'
                        GROUP BY entity_type
                    """

    with db.engine.begin() as connection:
        prey_table = connection.execute(sqlalchemy.text(prey_query)).fetchone()
        entity_type = prey_table[0]
        total = prey_table[1]

        prey_list.append({
            "entity_type": entity_type,
            "quantity": total
        })
        
    print(f"Total prey in ecosystem: {prey_list} ")
    return prey_list


@router.post("/spawn_prey")
def spawn_prey(prey_to_spawn : list[Entity]):
    """
    Takes in a list of prey to be spawned in the requested biome
    """
    with db.engine.begin() as connection:
        prey_list = []
        for prey in prey_to_spawn:
            prey_list.append({ "quantity": prey.quantity,
                                "nourishment": prey.nourishment,
                                "entity_type": prey.entity_type,
                                "biome_id": prey.biome_id})    
        prey_query = """
                        UPDATE entitys
                        SET quantity = quantity + :quantity,
                            nourishment = nourishment + :nourishment
                        WHERE entity_type = :entity_type
                            AND biome_id = :biome_id
                      """
        connection.execute(sqlalchemy.text(prey_query),prey_list)

    
    return "OK"
    



@router.post("/prey")
def biome_prey(biome_id : int):
    """
    Returns the amount of prey in the requested biome 
    """
    with db.engine.begin() as connection:
        prey_query = """
                        SELECT entity_type, 
                            SUM(quantity) as Total
                        FROM entitys
                        WHERE entity_type = 'prey'
                            AND biome_id = :biome_id
                        GROUP BY entity_type
                     """
        prey = connection.execute(sqlalchemy.text(prey_query), {"biome_id":biome_id}).fetchone()

    entity_type = prey[0]
    amount = prey[1]
    return({
        "entity_type": entity_type,
        "amount": amount
    })




@router.post("/spawn_predator/")
def spawn_predator(predators_to_spawn: list[Entity]):
    """
    Takes in a list of predators and spawns them in their respective biome
    """
    with db.engine.begin() as connection:
        predator_list = []
        for predator in predators_to_spawn:
            predator_list.append({ "quantity": predator.quantity,
                                "nourishment": predator.nourishment,
                                "entity_type": predator.entity_type,
                                "biome_id": predator.biome_id})    
        predator_query = """
                        UPDATE entitys
                        SET quantity = quantity + :quantity,
                            nourishment = nourishment + :nourishment
                        WHERE entity_type = :entity_type
                            AND biome_id = :biome_id
                      """
        connection.execute(sqlalchemy.text(predator_query),predator_list)

    
    return "OK"




@router.post("/predator/")
def biome_predator(biome_id: int):
    """
    Returns a list of predator and their amounts in the requested biome
    """
    with db.engine.begin() as connection:
        predator_query = """
                        SELECT entity_type, 
                            SUM(quantity) as Total
                        FROM entitys
                        WHERE entity_type = 'predator'
                            AND biome_id = :biome_id
                        GROUP BY entity_type
                     """
        predator = connection.execute(sqlalchemy.text(predator_query), {"biome_id":biome_id}).fetchone()

    entity_type = predator[0]
    amount = predator[1]
    return({
        "entity_type": entity_type,
        "amount": amount
    })





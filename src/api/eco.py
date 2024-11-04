from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/eco",
    tags=["ecological"],
    dependencies=[Depends(auth.get_api_key)],
)

class Entity(BaseModel):
    ent_id: int
    num_ent: int
    nourishment: int
    entity_type: str
    biome_id: int




# @router.post("/")
# def get_eco_overview():
#     """
#     Returns a general overview of the ecosystem and its characteristics such as: 
#     predators and prey and how many there are, the characteristics of each body of water and their id, 
#     plants and how many there are, resources (trees for wood, mine shafts for mining, etc.).
#     """

#     return "OK"

@router.put("/grow_plants")
def grow_plants(plants_to_grow: list[Entity]):
    """
    Takes in a request that contains of list of plant seeds to be planted in the 
    requested biome
    """
    with db.engine.begin() as connection:
        plant_list = {row.entity_id: row.quantity for row in plants_to_grow}
        plant_query = """
                        UPDATE entitys
                        SET quantity = quantity + :quantity
                            nourishment = nourishment + :nourishment
                        WHERE entity_type = :entity_type
                            AND biome_id = :biome_id
                      """
        
        #!!! THIS IS NOT FINISHED !!!#

        # connection.execute(sqlalchemy.text(plant_query),{"quantity":})


    return "OK"




@router.get("/trees/")
def plants_overview():
    """
    Returns a list of all plants and the amount in the entire ecosystem
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
        db_table = connection.execute(sqlalchemy.text(plants_query))
        plants_table = {row.entity_type:row.total for row in db_table}
        
    for plant in plants_table:
        plants_list.append({
            "plant_id": plant,
            "quantity": plants_table[plant] 
        })

    print(f"List of Plants in Ecosystem: {plants_list} ")
    return plants_list
        
    
    

@router.get("/life/prey/")
def prey_overview():
    """
    Returns a list of all prey and the amount in the entire ecosystem
    """
    prey_list = []
    prey_query =    """
                        SELECT entity_type, SUM(quantity) as Total
                        FROM entitys
                        WHERE entity_type = 'prey'
                        GROUP BY entity_type
                    """

    with db.engine.begin() as connection:
        db_table = connection.execute(sqlalchemy.text(prey_query))
        prey_table = {row.entity_type:row.total for row in db_table}

    for prey in prey_table:
        prey_list.append({
            "prey_id": prey,
            "quantity": prey_table[prey] 
        })

    print(f"List of Prey in Ecosystem: {prey_list} ")
    return prey_list




@router.put("/grab_water")
def collect_water(water_bodies: list[Entity]):
    """
    The call takes in a list of bodies of water that the user will harvest water from 
    """
    return "OK"




@router.post("/spawn_prey")
def spawn_prey(spawn_prey : Entity):
    """
    Takes in a list of prey to be spawned in the requested biome
    """
    



@router.post("/prey")
def get_prey(biome_id : int):
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
def spawn_predator(predators: list[Entity]):
    """
    Takes in a list of predators and spawns them in their respective biome
    """




@router.post("/predator/")
def get_predator(biome_id: int):
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





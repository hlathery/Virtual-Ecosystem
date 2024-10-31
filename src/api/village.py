from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/village",
    tags=["village"],
    dependencies=[Depends(auth.get_api_key)],
)

class Villagers(BaseModel):
    villager_id: int
    name: str
    job_id: int
    age: int
    nourishment: int

class Building(BaseModel):
    resource_name: str
    resource_cost: int
    quantity: int
    building_id: int
    

@router.get("/")
def get_village_overview():
    """
    Returns a general overview of village characteristics and villagers
    """
    with db.engine.begin() as connection:
        villager_count = connection.execute(sqlalchemy.text("SELECT COUNT(villagers.id) AS num_villagers FROM villagers")).scalar()
        buildings_count = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM buildings")).scalar()

    return {
                "num_buildings": buildings_count,
                "num_villagers": villager_count
            }


@router.post("/new_villager")
def create_villager(villagers: list[Villagers]):
    """
    
    """
    # SQL stuff to add villager
    created = True
    return {"success" : created}


@router.get("/villagers_all")
def get_villagers():
    """
    Returns a list of all villagers with their respective attributes. 
    """

    with db.engine.begin() as connection:
        villager_list_query =   """
                                    SELECT villagers.id, 
                                        villagers.name,
                                        jobs.job_name,
                                        villagers.age,
                                        villagers.nourishment
                                    FROM villagers
                                    JOIN jobs ON villagers.job_id = jobs.id
                                """
        result = connection.execute(sqlalchemy.text(villager_list_query)).fetchall()

    villagers = []
    for villager in result:
        villagers.append(
            {   
                "id" : villager.id,
                "name": villager.name,
                "job": villager.job_name,
                "job_id": villager.age,
                "health": villager.nourishment
            }
        )

    return villagers


@router.get("/buildings/villagers")
def get_occupying_villagers(building_id : int):
    """
    Gets all villagers in building
    """

    # SQL to get list of villagers : id, name, age, nourishment, and job id
    villagers_inside: list[Villagers]
    return villagers_inside


@router.post("/build_building")
def build_structure(buildings: list[Building]):
    """
    Takes in buildings user wants to build
    """
    # SQL to match building_id with name
    # Update quantity, etc
    created = True
    return {"success" : created}


@router.put("/fill_inventory")
def adjust_storage(buildings: list[Building]):
    """
    Adjusts storage amounts in buildings based off certain game logic
    """

    filled_flag = True
    return {"Success":filled_flag}


@router.post("/building_inventory")
def view_building_inventory(building_id: int):
    """
    Gets inventory of a specific building
    """

    #SQL to return resource name and amount
    pass


@router.get("/village_inventory")
def view_village_inventory():
    """
    Returns a list of all village resources and how much of that resource is available.
    """

    with db.engine.begin() as connection:
        query = """
                    SELECT resource_name AS resource, 
                        SUM(quantity) AS quantity
                    FROM storage
                    GROUP BY resource_name
                """
        resources = connection.execute(sqlalchemy.text(query)).fetchall()
        resource_list = list()

        for item in resources:
            resource_list.append({"resource_name" : item.resource,
                                 "quantity" : item.quantity})
            
        return resource_list
        
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
    

@router.post("/")
def get_village_overview():
    """
    Returns a general overview of village characteristics and villagers
    """
    with db.engine.begin() as connection:
        query = """
                    SELECT 
                        COUNT(DISTINCT buildings.id) AS num_buildings, 
                        SUM(storage.quantity) AS storage_amount
                    FROM buildings
                    LEFT JOIN storage ON storage.building_id = buildings.id
                """
        villager_count = connection.execute(sqlalchemy.text("SELECT COUNT(villagers.id) AS num_villagers FROM villagers")).fetchone()
        result = connection.execute(sqlalchemy.text(query)).fetchone()

    return [
                { 
                    "num_buildings": result.num_buildings,  
                    "num_villagers": villager_count.num_villagers, 
                    "storage_amount": result.storage_amount
                } 
            ]


@router.post("/villagers")
def get_villagers(villagers: list[Villagers]):
    """
    Returns a list of all villagers with their respective attributes. 
    """
    for v in villagers:
        print(f"Villager Name: {v.name}, id: {v.id}, job_id: {v.job_id}, Age: {v.age}, Nourishment: {v.nourishment}")

    return "OK"


@router.post("/villagers/{villager_id}")
def get_specific_villager(villager: list[Villagers]):
    """ 
    Accepts a specific villager id as input and gets their job and age.
    """

    return "OK"

@router.post("/inventory")
def get_invetory():
    """
    Returns a list of all village resources and how much of that resource is available.
    """

    return "OK"

@router.post("/inventory/{resource_id}")
def get_specific_resource_amount():
    """
    Accepts a resource id and returns how much of that item is in the inventory.
    """

    return "OK"

@router.post("/buildings")
def get_building_overview():
    """
    Returns an overview of the types of buildings (Farm, Mine, House) you have and how much of each type you have and how many villagers are in each type.
    """

    return "OK"

@router.post("/buildings/{building_id}")
def get_building_info():
    """
    Accepts a building id (which refers to a type of building) and returns how many villagers are working in that building type.
    """





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
                        buildings.name,
                        SUM(buildings.quantity) AS num_buildings, 
                        SUM(storage.quantity) AS storage_amount
                    FROM buildings
                    LEFT JOIN storage ON storage.building_id = buildings.id
                    GROUP BY buildings.name
                """
        villager_count = connection.execute(sqlalchemy.text("SELECT COUNT(villagers.id) AS num_villagers FROM villagers")).scalar()
        buildings_count = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM buildings")).scalar()
        storage_amount = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM storage")).scalar()

    return {
                "num_buildings": buildings_count,
                "num_villagers": villager_count,
                "storage_amount": storage_amount
            }


@router.post("/villagers")
def get_villagers():
    """
    Returns a list of all villagers with their respective attributes. 
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT villagers.name, jobs.job_name, villagers.age, villagers.nourishment FROM villagers JOIN jobs ON villagers.job_id = jobs.id"))

    villagers = []
    for row in result:
        villagers.append(
            {
                "Name": row.name,
                "Job": row.job_name,
                "Age": row.age,
                "Health": row.nourishment
            }
        )

    return villagers


@router.post("/villagers/{villager_id}")
def get_specific_villager(villager_id: int):
    """
    Accepts a specific villager id as input and gets their job and age.
    """

    with db.engine.begin() as connection:
        villager = connection.execute(sqlalchemy.text(f"SELECT villagers.name, jobs.job_name, villagers.age, villagers.nourishment FROM villagers JOIN jobs ON villagers.job_id = jobs.id WHERE villagers.id = {villager_id}")).fetchone()


    return {
                "Name": villager.name,
                "Job": villager.job_name,
                "Age": villager.age,
                "Health": villager.nourishment
            }

@router.post("/inventory")
def get_inventory():
    """
    Returns a list of all village resources and how much of that resource is available.
    """

    with db.engine.begin() as connection:
        food = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM storage WHERE resource_name = 'food'")).scalar()
        water = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM storage WHERE resource_name = 'water'")).scalar()
        wood = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM storage WHERE resource_name = 'wood'")).scalar()

    return {
        "Wood": wood,
        "Food": food,
        "Water": water
    }

@router.post("/inventory/{resource_name}")
def get_specific_resource_amount(resource_name: str):
    """
    Accepts a resource name and returns how much of that item is in the inventory.
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(f"SELECT SUM(quantity) FROM storage WHERE resource_name = '{resource_name}'")).scalar()

    return {
        resource_name: result
    }

@router.post("/buildings")
def get_building_overview():
    """
    Returns an overview of the types of buildings (Farm, Mine, House) you have and how much of each type you have and how many villagers are in each type.
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT buildings.name, buildings.quantity, COUNT(villagers.id) AS num_villagers FROM buildings LEFT JOIN jobs ON buildings.id = jobs.building_id LEFT JOIN villagers ON jobs.id = villagers.job_id GROUP BY buildings.name, buildings.quantity"))
        tot_villagers = connection.execute(sqlalchemy.text("SELECT COUNT(id) FROM villagers")).scalar()

    building_overview = []
    for row in result:
        if row.name == "Villager Hut":
            building_overview.append(
                {
                    "Name": row.name,
                    "Quantity": row.quantity,
                    "Number of Villagers": tot_villagers
                }
            )
        else:
            building_overview.append(
                {
                    "Name": row.name,
                    "Quantity": row.quantity,
                    "Number of Villagers": row.num_villagers
                }
            )

    return building_overview

@router.post("/buildings/{building_name}")
def get_building_info(building_name: str):
    """
    Accepts a building name (which refers to a type of building) and returns how many villagers are working in that building type.
    """

    if building_name == "Villager Hut":
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text(f"SELECT COUNT(villagers.id) FROM villagers")).scalar()
    else:
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text(f"SELECT COUNT(villagers.id) FROM villagers JOIN jobs ON villagers.job_id = jobs.id JOIN buildings ON jobs.building_id = buildings.id WHERE buildings.name = '{building_name}'")).scalar()

    return {"Number of Villagers": result}

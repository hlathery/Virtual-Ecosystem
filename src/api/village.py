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

class BuildingStorage(BaseModel):
    building_id: int
    resource_name: str
    amount: int
    
    

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
    Creates one or many villagers (id auto incrementing and job_id can start null)
    """
    update_list = list()
    for villager in villagers:
        update_list.append({"name":villager.name,
                            "age":villager.age,
                            "nourishment":villager.nourishment})
        
    insert_query =  """
                        INSERT INTO villagers (name, age, nourishment)
                        VALUES (:name, :age, :nourishment)
                    """

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(insert_query),update_list)

    return {"Villager(s) successfully created"}



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
                                    LEFT JOIN jobs ON villagers.job_id = jobs.id
                                """
        result = connection.execute(sqlalchemy.text(villager_list_query)).fetchall()

    villagers = list()
    for villager in result:
        villagers.append(
            {   
                "id" : villager.id,
                "name": villager.name,
                "job": villager.job_name,
                "age": villager.age,
                "health": villager.nourishment
            }
        )

    return villagers



@router.get("/buildings/villagers")
def get_occupying_villagers(building_id : int):
    """
    Gets all villagers in building
    """
    with db.engine.begin() as connection:

        villager_list_query =   """
                                    SELECT villagers.id AS id,
                                        villagers.name AS name,
                                        villagers.age AS age,
                                        jobs.job_name AS job_name
                                    FROM villagers
                                    LEFT JOIN jobs ON jobs.id = villagers.job_id
                                    WHERE building_id = :id
                                """
        
        villagers = connection.execute(sqlalchemy.text(villager_list_query),{"id": building_id}).fetchall()

    villagers_inside = list()
    for villager in villagers:
        villagers_inside.append({
                                    "id": villager.id, 
                                    "name": villager.name, 
                                    "job": villager.job_name,
                                    "age": villager.age
                                })

    return villagers_inside



@router.post("/build_building")
def build_structure(buildings: list[Building]):
    """
    Takes in buildings user wants to build
    """
    # Not sure what this part is doing in spec, couldn't we just take in an id based on what item they clicked on the catalog.
    # Then just allow them to "buy" it so long as they have correct amount of gold, and if they do subtract a certain
    # quantity of resources and gold?

    created = True
    return {"success" : created}



@router.put("/fill_inventory")
def adjust_storage(storages: list[BuildingStorage]):
    """
    Adjusts storage amounts in buildings based off certain game logic (make quantity values + or -),
    Ex: If getting food from farm you would make it 50, but if taking water to give to villagers make
    it -25. Since SQL statement is doing quantity + :quantity 
    """
    update_list = list()
    for storage in storages:
        update_list.append({"quantity":storage.amount,
                            "resource":storage.resource_name,
                            "building_id":storage.building_id})
        
    with db.engine.begin() as connection:

        storage_update_query =  """
                                UPDATE storage
                                SET quantity = quantity + :quantity
                                WHERE resource_name = :resource
                                    AND building_id = :building_id
                                """
        
        connection.execute(sqlalchemy.text(storage_update_query),update_list)
    
    return {"Success"}



@router.post("/building_inventory")
def view_building_inventory(building_id: int):
    """
    Gets inventory of a specific building
    """

    with db.engine.begin() as connection:

        select_query =   """
                            SELECT resource_name AS resource,
                                SUM(storage.quantity) AS quantity
                            FROM storage
                            JOIN buildings ON buildings.id = storage.building_id
                            WHERE building_id = :id
                            GROUP BY resource
                         """
        
        result = connection.execute(sqlalchemy.text(select_query),{"id": building_id}).fetchall()
    
    resources = list()
    for resource in result:
        resources.append({"resource_name" : resource.resource,
                            "amount" : resource.quantity})
    return resources



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
        
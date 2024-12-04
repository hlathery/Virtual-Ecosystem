from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
from enum import Enum
import datetime

router = APIRouter(
    prefix="/village",
    tags=["village"],
    dependencies=[Depends(auth.get_api_key)],
)

class ResourceType(str, Enum):
    food = "food"
    water = "water"
    wood = "wood"

class AvailableBuilding(str, Enum):
    town_hall = "Town Hall"
    villager_hut = "Villager Hut"
    hunter_hut = "Hunter Hut"
    forager_hut = "Forager Hut"
    farm = "Farm"
    mill = "Lumber Mill"
    mine = "Mine"

class Villagers(BaseModel):
    age: int
    nourishment: int

class Building(BaseModel):
    quantity: int
    building_name: AvailableBuilding

class BuildingStorage(BaseModel):
    resource_name: ResourceType
    amount: int


@router.get("/")
def get_village_overview():
    """
    Returns a general overview of village characteristics and villagers
    """

    with db.engine.begin() as connection:
        villager_count = connection.execute(sqlalchemy.text("SELECT COUNT(villagers.id) AS num_villagers FROM villagers")).scalar()
        buildings = connection.execute(sqlalchemy.text("SELECT name, quantity FROM buildings"))

    buildings_name = []
    buildings_count = []
    for row in buildings:
        buildings_name.append(row.name)
        buildings_count.append(row.quantity)

    
    endtime = datetime.datetime.now()
    runtime = endtime - start_time
    print("village/ runtime: " + str(runtime))

    return {
                "buildings": buildings_name,
                "num_buildings": buildings_count,
                "num_villager": villager_count
            }



@router.get("/catalog")
def catalog():
    """
    Gets the catalog of valid buildings available to build
    """

    select_query =  """
                            SELECT buildings.name AS type,
                                catalog.cost AS price
                            FROM buildings
                            JOIN catalog ON buildings.id = catalog.building_id
                       """
    with db.engine.begin() as connection:
        buildings = connection.execute(sqlalchemy.text(select_query))
        funds = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM storage WHERE resource_name = 'wood'")).scalar()

    types = []
    costs = []
    for row in buildings:
        if row.price < funds:
            types.append(row.type)
            costs.append(row.price)
    
    endtime = datetime.datetime.now()
    runtime = endtime - start_time
    print("village/catalog runtime: " + str(runtime))

    return {
            "buildings": types,
            "costs": costs,
            "funds": funds
        }


@router.put("/villager/{amount}")
def create_villager(amount: int):
    """
    Creates one or many villagers (id auto incrementing and job_id can start null).
    """

    if amount == 0:
        return "No villagers created"
    elif amount < 0:
        return "Amount must be greater than 0!"
   
    update_list = list()
    for _ in range(0, amount):
       
        update_list.append({"age": 18,
                            "nourishment":100})

    insert_query = """
        INSERT INTO villagers (age, nourishment)
        VALUES (:age, :nourishment)
    """

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(insert_query), update_list)
    
    endtime = datetime.datetime.now()
    runtime = endtime - start_time
    print("PUT village/villager runtime: " + str(runtime))

    return f"{amount} villager(s) succesfully created"


@router.delete("/villager/{amount}")
def remove_villager(amount: int):
    """
    Kills the oldest villagers. Based on the amount, it will order that many villagers to be killed by age (highest to lowest)
    Returns the id and age of each villager killed.
    """
    
    with db.engine.begin() as connection:
        villagers = connection.execute(sqlalchemy.text("SELECT COUNT(*) AS amount FROM villagers"))
        vil = villagers.fetchone()

        if amount == 0:
            return "No villagers removed."
        elif amount > vil.amount:
            return f"There are only {vil.amount} villager(s) able to be removed."
        elif amount < 0:
            return "Amount must be greater than 0."
         
        kill_villager_query =   """
                                    DELETE FROM villagers
                                    WHERE id IN (
                                        SELECT id FROM villagers
                                        ORDER BY age DESC
                                        LIMIT :num
                                        ) 
                                """
        connection.execute(sqlalchemy.text(kill_villager_query),{"num": amount})
    
    
    endtime = datetime.datetime.now()
    runtime = endtime - start_time
    print("DELETE village/villager runtime: " + str(runtime))

    return f"{amount} villager(s) succesfully removed"


@router.post("/villager_update")
def update_villager():
    """
    Updates villager population after decisions are made based on food and water income of that year
    """
    
    with db.engine.begin() as connection:
        water = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM storage WHERE resource_name = 'water'")).scalar_one()
        food = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM storage WHERE resource_name = 'food'")).scalar_one()
        update_villager_query = """
                                    UPDATE villagers
                                    SET
                                        age = age+1,
                                        nourishment = nourishment+:water+:food-100
                                """
        connection.execute(sqlalchemy.text(update_villager_query),{'water':water,'food':food})
        connection.execute(sqlalchemy.text("UPDATE villagers SET nourishment = 100 WHERE nourishment > 100"))

    
    endtime = datetime.datetime.now()
    runtime = endtime - start_time
    print("village/villager_update runtime: " + str(runtime))

    # Make sure you can't take more than available
    return "Villagers consumed food and water"  # PLACEHOLDER


@router.post("/building")
def build_structure(buildings: list[Building]):
    """
    Takes in buildings user wants to build or remove.
    Negative values to remove building, positive to add.
    Cannot go below 0.
    """

    if len(buildings) == 0:
        return "No structures built"

    buildings_sum = 0
    update_list = []
    for building in buildings:
        update_list.append({
            "amount": building.quantity,
            "name": building.building_name
        })

        if building.quantity <= 0:
            return "Building must have quantity greater than 0!"
        buildings_sum += building.quantity

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("UPDATE buildings SET quantity = quantity + :amount WHERE name = :name"), update_list)

    endtime = datetime.datetime.now()
    runtime = endtime - start_time
    print("village/building runtime: " + str(runtime))

    # return f"{buildings_sum} structure(s) built"
    return f"Structures built: {update_list}"


@router.put("/storage")
def adjust_storage(storages: list[BuildingStorage]):
    """
    Adjusts storage amounts in buildings based off certain game logic (make quantity values + or - as desired)
    """
    start_time = datetime.datetime.now()

    if len(storages) == 0:
        return {"error": "Must provide resources to adjust!"}

    with db.engine.begin() as connection:
        counts = connection.execute(sqlalchemy.text("SELECT resource_name, COUNT(*) AS tot FROM storage GROUP BY resource_name")).fetchall()

        update_list = list()
        for storage in storages:
            for count in counts:
                if count.resource_name == storage.resource_name:
                    
                    current_quantity = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM storage WHERE resource_name = :resource_name"),
                        {"resource_name": storage.resource_name},
                    ).scalar()

                    adjustment = storage.amount / count.tot
                    if current_quantity + adjustment < 0:
                        return f"Error: This would make {storage.resource_name} quantity to go below 0."
                            
                    update_list.append({
                        "quantity": storage.amount,
                        "resource": storage.resource_name,
                        "num": count.tot
                    })

        
        storage_update_query = """
            UPDATE storage
            SET quantity = quantity + :quantity/:num
            WHERE resource_name = :resource
                AND (quantity + :quantity/:num) >= 0
        """

        connection.execute(sqlalchemy.text(storage_update_query), update_list)

    
    endtime = datetime.datetime.now()
    runtime = endtime - start_time
    print("village/inventory runtime: " + str(runtime))

    return "Storage updated successfully!"



@router.get("/village_inventory")
def view_village_inventory():
    """
    Returns a list of all village resources and how much of that resource is available.
    """
    start_time = datetime.datetime.now()

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

    endtime = datetime.datetime.now()
    runtime = endtime - start_time
    print("village/village_inventory runtime: " + str(runtime))

    return resource_list
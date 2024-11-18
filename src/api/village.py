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
    job_id: int
    age: int
    nourishment: int

class Building(BaseModel):
    quantity: int
    building_name: str

class BuildingStorage(BaseModel):
    resource_name: str
    amount: int


@router.get("/")
def get_village_overview():
    """
    Returns a general overview of village characteristics and villagers
    """
    with db.engine.begin() as connection:
        villager_count = connection.execute(sqlalchemy.text("SELECT COUNT(villagers.id) AS num_villagers FROM villagers")).scalar_one()
        buildings = connection.execute(sqlalchemy.text("SELECT name, quantity FROM buildings"))

    buildings_name = []
    buildings_count = []
    for row in buildings:
        buildings_name.append(row.name)
        buildings_count.append(row.quantity)

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
    with db.engine.begin() as connection:
        select_query =  """
                            SELECT buildings.name AS type,
                                catalog.cost AS price
                            FROM buildings
                            JOIN catalog ON buildings.id = catalog.building_id
                        """
        buildings = connection.execute(sqlalchemy.text(select_query))
        funds = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM storage WHERE resource_name = 'wood'")).scalar_one()

        types = []
        costs = []
        for row in buildings:
            if row.price < funds:
                types.append(row.type)
                costs.append(row.price)

        return {
            "buildings": types,
            "costs": costs,
            "funds": funds
        }




@router.put("/new_villager")
def create_villager(villagers: list[Villagers]):
    """
    Creates one or many villagers (id auto incrementing and job_id can start null)
    """
    update_list = list()
    for villager in villagers:
        update_list.append({"age":villager.age,
                            "nourishment":villager.nourishment,
                            "job":villager.job_id})

    insert_query =  """
                        INSERT INTO villagers (job_id, age, nourishment)
                        VALUES (:job, :age, :nourishment)
                    """

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(insert_query),update_list)

    return {"Villager(s) successfully created"}

@router.post("/kill_villager")
def kill_villager(amount: int):
    """
    Kills the oldest amount of villagers depending on amount passed in
    """
    with db.engine.begin() as connection:
        kill_villager_query =   """
                                    DELETE FROM villagers
                                    WHERE id IN (
                                        SELECT id FROM villagers
                                        ORDER BY age DESC
                                        LIMIT :num
                                    )
                                """
        connection.execute(sqlalchemy.text(kill_villager_query),{"num":amount})

    return "OK"


@router.post("/build_building")
def build_structure(buildings: list[Building]):
    """
    Takes in buildings user wants to build
    """
    # Not sure what this part is doing in spec, couldn't we just take in an id based on what item they clicked on the catalog.
    # Then just allow them to "buy" it so long as they have correct amount of gold, and if they do subtract a certain
    # quantity of resources and gold?


    update_list = []
    for building in buildings:
        update_list.append({
            "amount": building.quantity,
            "id": building.building_name
        })

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("UPDATE buildings SET quantity = quantity + :amount WHERE name = :id"), update_list)

    return "OK"





@router.put("/fill_inventory")
def adjust_storage(storages: list[BuildingStorage]):
    """
    Adjusts storage amounts in buildings based off certain game logic (make quantity values + or -),
    Ex: If getting food from farm you would make it 50, but if taking water to give to villagers make
    it -25. Since SQL statement is doing quantity + :quantity 
    """
    with db.engine.begin() as connection:
        counts = connection.execute(sqlalchemy.text("SELECT resource_name, COUNT(*) AS tot FROM storage GROUP BY resource_name"))


    update_list = list()
    for storage in storages:
        for count in counts:
            if count.resource_name == storage.resource_name:
                update_list.append({"quantity":storage.amount,
                                    "resource":storage.resource_name,
                                    "num":count.tot})

    with db.engine.begin() as connection:
        storage_update_query =  """
                                UPDATE storage
                                SET quantity = quantity + :quantity/:num
                                WHERE resource_name = :resource
                                """

        connection.execute(sqlalchemy.text(storage_update_query),update_list)

    return {"Success"}



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

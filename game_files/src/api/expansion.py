from fastapi import APIRouter,Depends
import sqlalchemy
from game_files.src import database as db
from game_files.src.api import auth

router = APIRouter(
    prefix="/expansion",
    tags=["expansion"],
    dependencies=[Depends(auth.get_api_key)],)



@router.get("/catalog")
def get_catalog():
    """
    Returns building types and the amount of each building is available to build based upon available resources.
    """

    with db.engine.begin() as connection:
        wood = connection.execute(sqlalchemy.text("SELECT SUM(quantity) FROM storage WHERE resource_name = 'wood'")).fetchone()
        result = connection.execute(sqlalchemy.text(f"SELECT buildings.name AS name, ({wood}/catalog.cost) AS quantity FROM buildings JOIN catalog ON buildings.id = catalog.building_id GROUP BY name"))

    catalog = []
    for row in result:
        catalog.append(
            {
                "Building": row.name,
                "Quantity": row.quantity
            }
        )
    return catalog

@router.get("/plan")
def user_plan():
    """
    The user passes in each building type they want to build and how many of each type.
    """

    return "OK"



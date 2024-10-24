from fastapi import APIRouter,Depends
import sqlalchemy
from src import database as db
from src.api import auth

router = APIRouter(
    prefix="/expansion",
    tags=["expansion"],
    dependencies=[Depends(auth.get_api_key)],)

with db.engine.begin() as connection:
    result = connection.execute(sqlalchemy.text("SELECT quantity, resource_name FROM storage"))
    print(result.fetchall())


@router.get("/catalog")
def get_catalog():
    """
    Returns building types and the amount of each building is available to build based upon available resources.
    """

    return [
            {
                "Stuff": 5
            }
        ]

@router.get("/plan")
def user_plan():
    """
    The user passes in each building type they want to build and how many of each type.
    """
    return "OK"



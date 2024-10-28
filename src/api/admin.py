from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/reset")
def reset():
    """
    Resets all data in user inventory, village, and ecosystem to default values.
    """

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("DELETE FROM biomes"))
        connection.execute(sqlalchemy.text("DELETE FROM entitys"))
        connection.execute(sqlalchemy.text("DELETE FROM storage"))
        connection.execute(sqlalchemy.text("INSERT INTO storage (resource_name, quantity, building_id) VALUES ('wood', 100, 0), ('food', 50, 0), ('water', 50, 0)"))
        connection.execute(sqlalchemy.text("DELETE FROM villagers"))
        connection.execute(sqlalchemy.text("UPDATE buildings SET quantity = 1 WHERE id = 0 OR id = 1"))
        connection.execute(sqlalchemy.text("UPDATE buildings SET quantity = 0 WHERE id != 0 OR id != 1"))


    return "OK"


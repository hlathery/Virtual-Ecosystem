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
        
        query = """
                    DELETE FROM biomes;

                    DELETE FROM entities;

                    DELETE FROM storage;

                    INSERT INTO storage (resource_name, quantity, building_id) 
                    VALUES
                        :wood, 
                        :food, 
                        :water;
                    
                    DELETE FROM villagers;

                    INSERT INTO villagers (job_id, age, nourishment)
                    VALUES
                        :vil,
                        :vil,
                        :vil,
                        :vil,
                        :vil;

                    UPDATE buildings SET quantity = 0;

                    UPDATE buildings SET quantity = 1 WHERE id = 0 OR id = 1
                """
        # ['resource_name', quantity, building_id] , 0 in this case points to starter town hall
        default_wood = ['wood', 50, 0] 
        default_food = ['food', 100, 0]
        default_water = ['water', 100, 0]
        default_villager = [0, 18, 100]

        connection.execute(sqlalchemy.text(query), {"wood": tuple(default_wood),
                                                    "food": tuple(default_food),
                                                    "water": tuple(default_water),
                                                    "vil": tuple(default_villager)})
    

    return "Reset Complete"
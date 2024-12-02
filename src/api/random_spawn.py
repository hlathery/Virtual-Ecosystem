from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from sqlalchemy import update, text, bindparam
from sqlalchemy.orm import session
from src import database as db
from enum import Enum
from typing import Dict
from fastapi import HTTPException, status
import random
import datetime

router = APIRouter(
    prefix="/spawn",
    tags=["spawn"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/")
def random_spawn(): 
    """
    Randomly Spawns villagers and resources (in a ledgerized design)
    """

    # In format HH:MM:SS.mS
    start_time = datetime.datetime.now()

    spawn_query =   """
                    INSERT INTO villagers (job_id, age, nourishment)
                    VALUES (:job_id, :age, :nourishment)
                    """

    with db.engine.begin() as connection:
        villager_addition = []
        for villager in range(90000):
            job = random.randint(1,5) # Foreign Key relation to the buildings table
            age = random.randint(0,100)
            nourishment = 50
            villager_addition.append({
                "job_id": job,
                "age": age,
                "nourishment": nourishment
            })
        
        connection.execute(sqlalchemy.text(spawn_query),villager_addition)
    
    
    endtime =datetime.datetime.now()
    runtime = endtime - start_time
    print("random_spawn runtime: " + str(runtime))

    
        


        


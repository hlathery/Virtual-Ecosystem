from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from sqlalchemy import update, text, bindparam
from sqlalchemy.orm import session
from src import database as db
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
    Randomly Spawns villagers
    """

    # In format HH:MM:SS.mS
    start_time = datetime.datetime.now()

    spawn_query =   """
                    INSERT INTO villagers (job_id, age, nourishment)
                    VALUES (:job_id, :age, :nourishment)
                    """

    with db.engine.begin() as connection:
        
        for i in range(5):
            villager_addition = []
            for j in range(200000):
                job = random.randint(1,5) # Foreign Key relation to the buildings table
                age = random.randint(0,100)
                nourishment = random.randint(20,100)
                villager_addition.append({
                    "job_id": job,
                    "age": age,
                    "nourishment": nourishment
                })
            print("pass #" + j)
            connection.execute(sqlalchemy.text(spawn_query),villager_addition)
    
    endtime =datetime.datetime.now()
    runtime = endtime - start_time
    print("random_spawn runtime: " + str(runtime))

    
        


        


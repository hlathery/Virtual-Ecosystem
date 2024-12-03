from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import database as db
from enum import Enum
import sqlalchemy
from fastapi import HTTPException, status

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    dependencies=[Depends(auth.get_api_key)],
)

class JobsAvailable(str, Enum):
    unassigned = "unassigned"
    hunter = "hunter"
    forager = "forager"
    farmer = "farmer"
    butcher = "butcher"
    lumberjack = "lumberjack"
    miner = "miner"


class Jobs(BaseModel):
    job_name: JobsAvailable
    villagers_assigned: int


@router.get("/")
def get_job_list():
    """
    Returns a list of all jobs and the amount of active workers at each job.
    """

    with db.engine.begin() as connection:

        job_list_query = """ 
                            SELECT 
                                jobs.job_name AS name,
                                COUNT(villagers.job_id) AS quantity
                            FROM jobs
                            LEFT JOIN villagers ON jobs.id = villagers.job_id
                            GROUP BY jobs.id, job_name
                        """
        result = connection.execute(sqlalchemy.text(job_list_query))

    job_list = []
    for row in result:
        job_list.append(
            {
                "job_name": row.name,
                "villagers_assigned": row.quantity
            }
        )
    
    return job_list

@router.put("/assignments")
def assign_villager(job_list: list[Jobs]):
    """
    Takes a number of unassigned villagers and gives them a job.
    """
    
    # checks for negative values
    for job in job_list:
        if job.villagers_assigned < 0: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid assignment request: Cannot assign negative number of villagers ({job.villagers_assigned}) to {job.job_name}"
            )
    
    assignments = [
        {
            "job_name": job.job_name,
            "assigned": job.villagers_assigned
        }
        for job in job_list
        if job.villagers_assigned > 0
    ]

    if not assignments:
        return {"villagers_assigned": 0}

    assign_query = """
        UPDATE villagers 
        SET job_id = (
            SELECT id 
            FROM jobs 
            WHERE job_name = :job_name
        )
        WHERE id IN (
            SELECT id 
            FROM villagers 
            WHERE job_id = 0 
            LIMIT :assigned
        )
        RETURNING id
    """
    
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(assign_query),
            assignments
        )
        total_assigned = len(result.fetchall())

    return {"villagers_assigned": total_assigned}
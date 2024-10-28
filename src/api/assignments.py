from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/assignments",
    tags=["assignments"],
    dependencies=[Depends(auth.get_api_key)],
)

class Jobs(BaseModel):
    job_id: int
    job_title: str
    villagers_assigned: int


@router.get("/")
def get_job_list():
    """
    Returns a list of all jobs and the amount of active workers at each job.
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT jobs.id AS id, jobs.job_name AS name, COUNT(villagers.job_id) AS quantity FROM jobs JOIN villagers ON jobs.id = villagers.job_id GROUP BY jobs.id, job_name"))

    job_list = []
    for row in result:
        job_list.append(
            {
                "job_id": row.id,
                "job_title": row.name,
                "villagers_assigned": row.quantity
            }
        )

    return job_list

@router.post("/plan")
def assign_villager(job_list: list[dict]):
    """
    The call passes in a catalog of each job type and how many villagers are working in each job type. 
    The user would return back new values, if any, of how many villagers they want in each job.
    """

    with db.engine.begin() as connection:
        for job in job_list:
            if job["villagers_assigned"] > 0:
                connection.execute(sqlalchemy.text(f"UPDATE villagers SET job_id = {job['job_id']} WHERE id IN (SELECT id FROM (SELECT id FROM villagers ORDER BY id ASC LIMIT {job['villagers_assigned']}) tmp)"))

    return "OK"
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


@router.get("/get_job_list")
def get_job_list():
    """
    Returns a list of all jobs and the amount of active workers at each job.
    """

    with db.engine.begin() as connection:

        job_list_query = """ 
                            SELECT jobs.id AS id,
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
                "job_id": row.id,
                "job_title": row.name,
                "villagers_assigned": row.quantity
            }
        )
    
    return job_list

@router.put("/assign_villager")
# Shouldn't this be           list[Jobs]?
def assign_villager(job_list: list[dict]):
    """
    The call passes in a catalog of each job type and how many villagers are working in each job type. 
    The user would return back new values, if any, of how many villagers they want in each job.
    """

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("UPDATE villagers SET job_id = 0"))
        for job in job_list:
            if job["villagers_assigned"] > 0:
                update_query =  """
                                    UPDATE villagers
                                    SET job_id = :job_id
                                    WHERE id IN (SELECT id FROM 
                                        (SELECT id 
                                        FROM villagers 
                                        ORDER BY id 
                                        ASC LIMIT :villagers_asn) tmp) 
                                    AND job_id = 0"
                                """
                connection.execute(sqlalchemy.text(update_query),{ "job_id" : job['job_id'],
                                                                    "villagers_asn" : job['villagers_assigned']
                                                                    })

    return "OK"
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/assignments",
    tags=["assignments"],
    dependencies=[Depends(auth.get_api_key)],
)

class Jobs(BaseModel):
    job_id: int
    job_name: str
    building_id: int


@router.get("/")
def get_job_list():
    """
    Returns a list of all jobs and the amount of active workers at each job.
    """
    return "OK"

@router.get("/plan")
def get_user_plan(catalog: list[Jobs]):
    """
    The call passes in a catalog of each job type and how many villagers are working in each job type. 
    The user would return back new values, if any, of how many villagers they want in each job.
    """

    return "OK"

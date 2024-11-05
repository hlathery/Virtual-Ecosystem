from fastapi import APIRouter
from pydantic import BaseModel
from src import database as db

router = APIRouter(
)

class Timestamp(BaseModel):
    year: int
    month: int
    day: int
    
@router.get("/info/current_time")
def post_time(timestamp: Timestamp):
    """
    Get current time.
    """
                            #02/07/1975
    return f"{timestamp.month}/{timestamp.day}/{timestamp.year}"


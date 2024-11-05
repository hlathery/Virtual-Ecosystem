from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/eco",
    tags=["ecological"],
    dependencies=[Depends(auth.get_api_key)],
)

class Entity(BaseModel):
    ent_id: int
    num_ent: int
    nourishment: int
    entity_type: str
    biome_id: int




# @router.post("/")
# def get_eco_overview():
#     """
#     Returns a general overview of the ecosystem and its characteristics such as: 
#     predators and prey and how many there are, the characteristics of each body of water and their id, 
#     plants and how many there are, resources (trees for wood, mine shafts for mining, etc.).
#     """

#     return "OK"

@router.put("/grow_plants")
def grow_plants(plants_to_grow: list[Entity]):
    """
    Takes in a request that contains of list of plant seeds to be planted in the 
    requested biome
    """
    return "OK"

@router.get("/trees/")
def plants_overview():
    """
    Returns a list of all plants and the amount in the entire ecosystem
    """

@router.get("/life/prey/")
def prey_overview():
    """
    Returns a list of all prey and the amount in the entire ecosystem
    """

@router.put("/grab_water")
def collect_water(water_bodies: list[Entity]):
    """
    The call takes in a list of bodies of water that the user will harvest water from 
    """
    return "OK"


@router.post("/spawn_prey")
def spawn_prey():
    """
    Takes in a list of prey to be spawned in the requested biome
    """

@router.get("/prey")
def get_prey():
    """
    Returns a list of prey and their amounts in the requested biome 
    """

@router.post("/spawn_predator/")
def spawn_predator():
    """
    Takes in a list of predators and spawns them in their respective biome
    """

@router.post("/predator/")
def get_predator(biome_id: int):
    """
    Returns a list of predator and their amounts in the requested biome
    """





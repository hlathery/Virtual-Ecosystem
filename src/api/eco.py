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



@router.post("/")
def get_eco_overview():
    """
    Returns a general overview of the ecosystem and its characteristics such as: 
    predators and prey and how many there are, the characteristics of each body of water and their id, 
    plants and how many there are, resources (trees for wood, mine shafts for mining, etc.).
    """

    return "OK"

@router.post("/life/predators")
def get_predators(predators: list[Entity]):
    """
    Returns how many predators there are in the surrounding ecosystem.
    """

    return "OK"

@router.post("/life/prey")
def get_prey(prey: list[Entity]):
    """
    Returns how much prey there is in the surrounding ecosystem.
    """

    return "OK"

@router.post("/life/plants")
def get_plants(plants: list[Entity]):
    """
    Returns how many plants there are in the surrounding ecosystem.
    """

    return "OK"

@router.post("/resources/{body_id}")
def get_water_bodies(body_of_water: list[Entity]):
    """
    Accepts a body id (referring to a specific body of water) and returns the water level and dryness of the area.
    """

    return "OK"

@router.post("/resources/{body_id}")
def get_tree_patches(trees: list[Entity]):
    """
    Accepts a body id (referring to a specific patch of trees) and returns the amount of harvestable wood
    """

    return "OK"









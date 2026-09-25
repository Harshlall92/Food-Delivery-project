from fastapi import FastAPI, APIRouter

router = APIRouter(prefix = "/restaurants")

@router.get("")
def get_restaurants():
    pass
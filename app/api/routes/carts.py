from fastapi import APIRouter


router = APIRouter(
    prefix="/api/carts",
    tags=["carts"],
)
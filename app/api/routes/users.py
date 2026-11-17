from fastapi import APIRouter, HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemas.user import Customer, UserCreate
import app.services.user_service as uService

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/customers", status_code=status.HTTP_201_CREATED, response_model=Customer)
async def create_customer(user: UserCreate):
    try:
        customer = await uService.create_customer(UserRepository(), user)
        return customer
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
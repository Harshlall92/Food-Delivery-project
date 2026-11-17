from fastapi import APIRouter, HTTPException, status

from app.services.exceptions import DuplicateItemError, UserNotFoundError
from app.repositories.user_repository import UserRepository
from app.schemas.user import Customer, UserCreate, UserUpdate
import app.services.user_service as uService

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post(
        "/c",
        responses={
            400: {"description": "Invalid input data"},
            409: {"description": "Customer with this email already exists"},
            201: {"description": "Customer created successfully"},
        },
        response_model=Customer
)
async def create_customer(user: UserCreate):
    try:
        customer = await uService.create_customer(UserRepository(), user)
        return customer
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DuplicateItemError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.patch(
        "/c/{customer_id}", 
        responses={
            400: {"description": "Invalid input data"},
            404: {"description": "Customer not found"},
            409: {"description": "Customer with this email already exists"},
            200: {"description": "Customer updated successfully"},
        },
        response_model=Customer)
async def update_customer(customer_id: str, user: UserUpdate):
    try:
        updated_customer = await uService.update_customer(UserRepository(), customer_id, user)
        return updated_customer
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateItemError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

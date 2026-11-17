from fastapi import APIRouter, HTTPException, status

from app.services.exceptions import DuplicateItemError, UserNotFoundError
from app.repositories.user_repository import UserRepository
from app.schemas.user import Customer, RestaurantOwner, UserCreate, UserUpdate
import app.services.user_service as uService

router = APIRouter(prefix="/api/users", tags=["users"])

customer_router = APIRouter(prefix="/c", tags=["users", "customers"])
restaurant_owner_router = APIRouter(prefix="/r", tags=["users", "restaurant_owners"])

router.include_router(customer_router)
router.include_router(restaurant_owner_router)

@customer_router.post(
        "",
        responses={
            409: {"description": "Customer with this email already exists"},
            422: {"description": "Invalid input data"},
            201: {"description": "Customer created successfully"},
        },
        status_code=status.HTTP_201_CREATED,
        response_model=Customer
)
async def create_customer(user: UserCreate):
    try:
        customer = await uService.create_customer(UserRepository(), user)
        return customer
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
    except DuplicateItemError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@customer_router.patch(
        "/{customer_id}", 
        responses={
            404: {"description": "Customer not found"},
            409: {"description": "Customer with this email already exists"},
            422: {"description": "Invalid input data"},
            200: {"description": "Customer updated successfully"},
        },
        response_model=Customer)
async def update_customer(customer_id: str, user: UserUpdate):
    try:
        updated_customer = await uService.update_customer(UserRepository(), customer_id, user)
        return updated_customer
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateItemError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@restaurant_owner_router.post(
    "",
    description="Create a new restaurant owner account",
    responses={
        409: {"description": "Restaurant owner with this email already exists"},
        422: {"description": "Invalid input data"},
        201: {"description": "Restaurant owner created successfully"},
    },
    status_code=status.HTTP_201_CREATED,
    response_model=RestaurantOwner
)
async def create_restaurant_owner(user: UserCreate):
    try:
        owner = await uService.create_restaurant_owner(UserRepository(), user)
        return owner
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
    except DuplicateItemError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
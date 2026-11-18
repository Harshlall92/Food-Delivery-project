from fastapi import APIRouter, HTTPException, status

from app.repositories.restaurant_repository import RestaurantRepository
from app.services.exceptions import DuplicateItemError, ItemNotFoundError, UserNotFoundError
from app.repositories.user_repository import UserRepository
from app.schemas.user import Customer, CustomerAddress, RestaurantOwner, RestaurantOwnerUpdate, UserCreate, UserUpdate
import app.services.user_service as uService

router = APIRouter(prefix="/api/users", tags=["users"])

customer_router = APIRouter(prefix="/c", tags=["users", "customers"])
restaurant_owner_router = APIRouter(prefix="/r", tags=["users", "restaurant_owners"])

router.include_router(customer_router)
router.include_router(restaurant_owner_router)

@customer_router.post(
        "",
        description="Create a new customer account",
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
        description="Update customer account information excluding addresses",
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

@customer_router.post(
        "/{customer_id}",
        responses={
            404: {"description": "Customer not found"},
            409: {"description": "Address with this label already exists for this customer"},
            422: {"description": "Invalid input data"},
            201: {"description": "Address added successfully"},
        }
    )
async def add_address(customer_id: str, address: CustomerAddress):
    try:
        updated_customer = await uService.add_customer_address(UserRepository(), customer_id, address)
        return updated_customer
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
    except DuplicateItemError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@customer_router.patch(
        "/{customer_id}/{address_label}",
        description="Update an existing address for a customer",
        responses={
            404: {"description": "Customer or address label not found"},
            422: {"description": "Invalid input data"},
            200: {"description": "Address updated successfully"},
        },
        response_model=Customer
    )
async def update_address(customer_id: str, address_label: str, new_address: CustomerAddress):
    try:
        updated_customer = await uService.update_customer_address(UserRepository(), customer_id, address_label, new_address)
        return updated_customer
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

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

@restaurant_owner_router.patch(
    "/{owner_id}",
    description="Update an existing restaurant owner account",
    responses={
        404: {"description": "Restaurant owner not found, or associated restaurant does not exist"},
        409: {"description": "Restaurant owner with this email already exists"},
        422: {"description": "Invalid input data"},
        200: {"description": "Restaurant owner updated successfully"},
    },
    response_model=RestaurantOwner
)
async def update_restaurant_owner(owner_id: str, user: RestaurantOwnerUpdate):
    try:
        updated_owner = await uService.update_restaurant_owner(UserRepository(), RestaurantRepository(), owner_id, user)
        return updated_owner
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateItemError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import os
from dotenv import load_dotenv
import jwt
from fastapi import HTTPException, status
from fastapi.params import Depends
from typing_extensions import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.repositories.exceptions import RecordNotFoundError
from app.repositories.user_repository import UserRepository
from app.schemas.user import Admin, AnyUser, Customer, RestaurantOwner, User
from app.services.exceptions import InvalidCredentialsError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "INSECURE_KEY")  # Default key for development; would be overridden in production
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Default algorithm for development; would be overridden in production
TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)  # Default token expiration for development; would be overridden in production

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that the provided plain password matches the hashed password.
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str | None:
    """
    Decodes the provided JWT token and returns the user ID if valid.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: str = str(payload.get("sub"))
    return user_id

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> AnyUser:
    """
    Returns the current user based on the provided JWT token. 
    Raises an HTTPException if the token is invalid or the user does not exist.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = decode_token(token)
    except jwt.InvalidTokenError:
        raise credentials_exception
    if not user_id:
        raise credentials_exception
    user = await UserRepository().get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[AnyUser, Depends(get_current_user)]) -> AnyUser:
    """
    Returns the current active user. Raises an HTTPException if the user is inactive.
    """
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

CurrentUser = Annotated[AnyUser, Depends(get_current_active_user)]

async def create_access_token(user: AnyUser) -> str:
    """
    Creates a JWT access token for the given user. The token includes the user's ID and an expiration time.
    """
    to_encode: dict[str, Any] = {"sub": user.id}

    expires = datetime.now(UTC) + timedelta(minutes=int(TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expires})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(repository: UserRepository, form_data: OAuth2PasswordRequestForm) -> str:
    """
    Authenticates a user based on the provided form data. Raises an InvalidCredentialsError if authentication fails.
    Returns the user's JWT access token if authentication is successful.
    """
    try:
        user =  await repository.get_by_email(form_data.username)
    except RecordNotFoundError:
        raise InvalidCredentialsError("Incorrect username or password.")

    if not verify_password(form_data.password, user.password):
        raise InvalidCredentialsError("Incorrect username or password.")
    return await create_access_token(user)

async def get_current_active_customer(current_user: CurrentUser) -> Customer:
    """
    Returns the current active customer. Raises an HTTPException if the user is not a customer.
    """
    if current_user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a customer"
        )
    return current_user

CurrentCustomer = Annotated[Customer, Depends(get_current_active_customer)]

async def get_current_active_restaurant_owner(current_user: CurrentUser) -> RestaurantOwner:
    """
    Returns the current active restaurant owner. Raises an HTTPException if the user is not a restaurant owner.
    """
    if current_user.role != "restaurant_owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a restaurant owner"
        )
    return current_user

CurrentRestaurantOwner = Annotated[RestaurantOwner, Depends(get_current_active_restaurant_owner)]

async def get_current_active_admin(current_user: CurrentUser) -> Admin:
    """
    Returns the current active admin. Raises an HTTPException if the user is not an admin.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an admin"
        )
    return current_user

CurrentAdmin = Annotated[Admin, Depends(get_current_active_admin)]
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

Token = Annotated[str, Depends(oauth2_scheme)]

def decode_token(token: Token) -> User:
    # Placeholder for token decoding logic
    return User(email="test@example.ca", password="password", first_name="Test", last_name="User")

async def get_current_user(token: Token = Depends(oauth2_scheme)) -> User:
    # Placeholder for user retrieval logic based on the token
    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

CurrentUser = Annotated[User, Depends(get_current_active_user)]
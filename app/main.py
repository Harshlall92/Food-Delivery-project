from pathlib import Path
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from app.api.routes import restaurants, menu_items, users, carts, orders
from app.repositories.user_repository import UserRepository
from app.services.authentication import CurrentAdmin
from app.services.exceptions import InvalidCredentialsError, ItemNotFoundError
from app.services import authentication

app = FastAPI()

FRONTEND_PATH = Path(__file__).parent.parent / "frontend"
print(f"Serving static files from: {FRONTEND_PATH}")

app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")

app.include_router(restaurants.router)
app.include_router(menu_items.router)
app.include_router(users.router)
app.include_router(carts.router)
app.include_router(orders.router)


@app.post("/token", description="Authenticate a user and return an access token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user_id = await authentication.authenticate_user(UserRepository(), form_data)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    except ItemNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect email or password"
        )
    return {"access_token": user_id, "token_type": "bearer"}
    
@app.get("/health")
def health():
    return {"status" : "ok"}

@app.get("/")
def index():
    return FileResponse(FRONTEND_PATH / "index.html", media_type="text/html")

@app.get("/restaurants")
def restaurants_page():
    return FileResponse(FRONTEND_PATH / "restaurants.html", media_type="text/html")

@app.get("/restaurants/new")
def new_restaurant_page():
    return FileResponse(FRONTEND_PATH / "create-restaurant.html", media_type="text/html")

# Must come before /restaurants/{restaurant_id}, or "search" would be read as a restaurant id
@app.get("/restaurants/search")
def search_restaurants_page():
    return FileResponse(FRONTEND_PATH / "search-restaurants.html", media_type="text/html")

@app.get("/restaurants/{restaurant_id}")
def restaurant_detail_page(restaurant_id: str):
    return FileResponse(FRONTEND_PATH / "restaurant-detail.html", media_type="text/html")

@app.get("/update-restaurant/{restaurant_id}")
def update_restaurant_page(restaurant_id: str):
    return FileResponse(FRONTEND_PATH / "update-restaurant.html", media_type="text/html")

@app.get("/accounts/new")
def create_account_page():
    return FileResponse(FRONTEND_PATH / "create-account.html", media_type="text/html")

@app.get("/accounts/{user_id}")
def update_account_page(user_id: str):
    return FileResponse(FRONTEND_PATH / "update-account.html", media_type="text/html")

@app.get("/carts")
def carts_page():
    return FileResponse(FRONTEND_PATH / "carts.html", media_type="text/html")

@app.get("/carts/{customer_id}")
def cart_detail_page(customer_id: str):
    return FileResponse(FRONTEND_PATH / "cart-detail.html", media_type="text/html")

@app.get("/orders")
def orders_page():
    return FileResponse(FRONTEND_PATH / "orders.html", media_type="text/html")

@app.get("/orders/{order_id}")
def order_detail_page(order_id: str):
    return FileResponse(FRONTEND_PATH / "order-detail.html", media_type="text/html")

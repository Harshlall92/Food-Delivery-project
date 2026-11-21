from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes import restaurants, menu_items, users, carts

app = FastAPI()

FRONTEND_PATH = Path(__file__).parent.parent / "frontend"
print(f"Serving static files from: {FRONTEND_PATH}")

app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")

app.include_router(restaurants.router)
app.include_router(menu_items.router)
app.include_router(users.router)
app.include_router(carts.router)

@app.get("/health")
def health():
    return {"status" : "ok"}
@app.get("/website")
def log_in_page():
    return FileResponse(FRONTEND_PATH/"login.html", media_type="text/html")
@app.get("/website/home")
def index():
    return FileResponse(FRONTEND_PATH / "index.html", media_type="text/html")

@app.get("/website/restaurants")
def restaurants_page():
    return FileResponse(FRONTEND_PATH / "restaurants.html", media_type="text/html")

@app.get("/website/restaurants/new")
def new_restaurant_page():
    return FileResponse(FRONTEND_PATH / "create-restaurant.html", media_type="text/html")

@app.get("/restaurants/{restaurant_id}")
def restaurant_detail_page(restaurant_id: str):
    return FileResponse(FRONTEND_PATH / "restaurant-detail.html", media_type="text/html")

@app.get("/website/update-restaurant/{restaurant_id}")
def update_restaurant_page(restaurant_id: str):
    return FileResponse(FRONTEND_PATH / "update-restaurant.html", media_type="text/html")

@app.get("/website/restaurants/{restaurant_id}/cart")
def new_cart_page(restaurant_id: str, customer_id: str):
    return FileResponse(FRONTEND_PATH / "create-cart.html",media_type="text/html")

@app.get("/website/restaurants/{restaurant_id}/cart/update")
def update_cart_page(restaurant_id: str, customer_id: str):
    return FileResponse(FRONTEND_PATH/"update-cart.html", media_type = "text/html")

@app.get("/website/restaurants/{restaurant_id}/order")
def create_order_page(restaurant_id: str, customer_id: str):
    return FileResponse(FRONTEND_PATH/"create-order.html", media_type= "text/html")


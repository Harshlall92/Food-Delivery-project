from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes import restaurants, menu_items

app = FastAPI()

FRONTEND_PATH = Path(__file__).parent.parent / "frontend"
print(f"Serving static files from: {FRONTEND_PATH}")

app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")

app.include_router(restaurants.router)
app.include_router(menu_items.router)

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

@app.get("/restaurants/{restaurant_id}")
def restaurant_detail_page(restaurant_id: str):
    return FileResponse(FRONTEND_PATH / "restaurant-detail.html", media_type="text/html")
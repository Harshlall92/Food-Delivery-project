from fastapi import FastAPI
from app.api.routes import restaurants, menu_items

app = FastAPI()

app.include_router(restaurants.router)
app.include_router(menu_items.router)

@app.get("/")
def index():
    return {"message": "Welcome to the Pilates Princesses Food Delivery Appication!"}

@app.get("/health")
def health():
    return {"status" : "ok"}

from fastapi import FastAPI
from app.api.routes import restaurants

app = FastAPI()

app.include_router(restaurants.router)

@app.get("/health")
def health():
    return {"status" : "ok"}

from fastapi import FastAPI

from app.models import State
from app.routes import router

app = FastAPI(
    title="Taxi Booking System",
    version="0.0.1",
    contact={"name": "Denys Volokh", "email": "denis.volokh@gmail.com"},
)
app.include_router(router, prefix="/api")

setattr(app, "state", State())

import os
from fastapi import FastAPI
from .models import *
from .database import engine
from .routers import router
from .dbseed import init_seed
# Create the FastAPI app and include the router
app = FastAPI()
app.include_router(router)

# Import the models to create the tables in the database
# Base.metadata.create_all(engine)
#
# # Check if DB was already seed, and if not will seed with datas
# init_seed()


# Create tables (souvent OK de le garder, mais je le rends aussi optionnel)
CREATE_TABLES = os.getenv("CREATE_TABLES", "true").lower() == "true"
SEED_DB = os.getenv("SEED_DB", "false").lower() == "true"

if CREATE_TABLES:
    Base.metadata.create_all(engine)

if SEED_DB:
    init_seed()

# Define a simple root endpoint to check the connection
@app.get("/")
def read_root():
    return {"message": "Connected to the database!"}

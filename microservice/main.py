import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import dotenv

dotenv.load_dotenv()

from microservice.database.engine import create_db_and_tables

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from microservice.routers import users, status

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    logging.warning("Starting up")
    create_db_and_tables()
    yield
    logging.warning("Shutting down")

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(status.router)
add_pagination(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
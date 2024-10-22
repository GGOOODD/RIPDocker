from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router
from contextlib import asynccontextmanager
from database import create_tables
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.isfile("./site.db"):
        await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

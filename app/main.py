from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, visitors, incidents, ai, emergencies
from app.database.mongodb import connect_to_mongo, close_mongo_connection
import os
from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager
from app.services.rag_service import init_rag

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    init_rag()
    yield
    await close_mongo_connection()

app = FastAPI(title="School Security Administration System", version="1.0.0", lifespan=lifespan)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(visitors.router, prefix="/api/visitors", tags=["Visitor Management"])
app.include_router(incidents.router, prefix="/api/incidents", tags=["Incident Management"])
app.include_router(emergencies.router, prefix="/api/emergencies", tags=["Emergency Management"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI Services"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the School Security Administration System API"}

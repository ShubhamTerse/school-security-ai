from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.incident import IncidentCreate, IncidentResponse
from app.database.mongodb import get_database
from app.api.auth import get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=IncidentResponse)
async def create_incident(incident: IncidentCreate, current_user: dict = Depends(get_current_user)):
    db = get_database()
    incident_dict = incident.model_dump()
    incident_dict["date_time"] = datetime.utcnow()
    incident_dict["status"] = "Reported"
    incident_dict["ai_analysis"] = None
    
    result = await db.incidents.insert_one(incident_dict)
    incident_dict["_id"] = str(result.inserted_id)
    return incident_dict

@router.get("/", response_model=List[IncidentResponse])
async def get_incidents(current_user: dict = Depends(get_current_user)):
    db = get_database()
    incidents = []
    async for incident in db.incidents.find():
        incident["_id"] = str(incident["_id"])
        incidents.append(incident)
    return incidents

@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(incident_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    incident = await db.incidents.find_one({"_id": ObjectId(incident_id)})
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    incident["_id"] = str(incident["_id"])
    return incident

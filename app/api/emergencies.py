from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.emergency import EmergencyCreate, EmergencyResponse
from app.database.mongodb import get_database
from app.api.auth import get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=EmergencyResponse)
async def report_emergency(emergency: EmergencyCreate, current_user: dict = Depends(get_current_user)):
    db = get_database()
    emergency_dict = emergency.model_dump()
    emergency_dict["date_time"] = datetime.utcnow()
    emergency_dict["status"] = "ACTIVE"
    
    result = await db.emergencies.insert_one(emergency_dict)
    emergency_dict["_id"] = str(result.inserted_id)
    return emergency_dict

@router.get("/", response_model=List[EmergencyResponse])
async def get_emergencies(current_user: dict = Depends(get_current_user)):
    db = get_database()
    emergencies = []
    async for emergency in db.emergencies.find():
        emergency["_id"] = str(emergency["_id"])
        emergencies.append(emergency)
    return emergencies

@router.put("/{emergency_id}/resolve", response_model=EmergencyResponse)
async def resolve_emergency(emergency_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    result = await db.emergencies.update_one(
        {"_id": ObjectId(emergency_id)},
        {"$set": {"status": "RESOLVED"}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Emergency not found")
    
    emergency = await db.emergencies.find_one({"_id": ObjectId(emergency_id)})
    emergency["_id"] = str(emergency["_id"])
    return emergency

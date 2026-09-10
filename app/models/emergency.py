from pydantic import BaseModel, Field
from datetime import datetime

class EmergencyCreate(BaseModel):
    emergency_type: str # Fire, Medical Emergency, Unauthorized Access, etc.
    location: str
    description: str

class EmergencyResponse(EmergencyCreate):
    id: str = Field(alias="_id")
    date_time: datetime
    status: str = "ACTIVE" # ACTIVE, RESOLVED

    class Config:
        populate_by_name = True

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class IncidentCreate(BaseModel):
    title: str
    location: str
    description: str
    reported_by: str

class IncidentAIReport(BaseModel):
    summary: str
    risk_level: str
    risk_reason: str
    recommended_actions: List[str]
    urgency: str
    category: str

class IncidentResponse(IncidentCreate):
    id: str = Field(alias="_id")
    date_time: datetime
    status: str
    ai_analysis: Optional[IncidentAIReport] = None

    class Config:
        populate_by_name = True

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class VisitorBase(BaseModel):
    name: str
    phone: str
    purpose: str
    person_to_visit: str
    status: str = "Inside" # Inside, Completed, Flagged

class VisitorCreate(VisitorBase):
    pass

class VisitorResponse(VisitorBase):
    id: str = Field(alias="_id")
    entry_time: datetime
    exit_time: Optional[datetime] = None

    class Config:
        populate_by_name = True

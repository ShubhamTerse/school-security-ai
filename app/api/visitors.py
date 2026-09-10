from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.visitor import VisitorCreate, VisitorResponse
from app.database.mongodb import get_database
from app.api.auth import get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=VisitorResponse)
async def create_visitor(visitor: VisitorCreate, current_user: dict = Depends(get_current_user)):
    db = get_database()
    visitor_dict = visitor.model_dump()
    visitor_dict["entry_time"] = datetime.utcnow()
    visitor_dict["exit_time"] = None
    
    result = await db.visitors.insert_one(visitor_dict)
    visitor_dict["_id"] = str(result.inserted_id)
    return visitor_dict

@router.get("/", response_model=List[VisitorResponse])
async def get_visitors(current_user: dict = Depends(get_current_user)):
    db = get_database()
    visitors = []
    async for visitor in db.visitors.find():
        visitor["_id"] = str(visitor["_id"])
        visitors.append(visitor)
    return visitors

@router.put("/{visitor_id}/checkout", response_model=VisitorResponse)
async def checkout_visitor(visitor_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    result = await db.visitors.update_one(
        {"_id": ObjectId(visitor_id)},
        {"$set": {"status": "Completed", "exit_time": datetime.utcnow()}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Visitor not found")
    
    visitor = await db.visitors.find_one({"_id": ObjectId(visitor_id)})
    visitor["_id"] = str(visitor["_id"])
    return visitor

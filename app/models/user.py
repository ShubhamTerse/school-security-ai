from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "Teacher" # Admin, Security, Teacher

class UserInDB(UserCreate):
    hashed_password: str

class UserResponse(BaseModel):
    username: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

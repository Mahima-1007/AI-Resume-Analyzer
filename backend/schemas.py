from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: str          # MongoDB _id is a string, not int
    email: str
    full_name: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class JobMatch(BaseModel):
    job_id: str
    title: str
    company: str
    score: float

class ChatMessage(BaseModel):
    role: str
    content: str

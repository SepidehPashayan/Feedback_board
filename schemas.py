from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FeedbackCreate(BaseModel):
    title: str
    message: str

class FeedbackUpdate(BaseModel):
    status: str

class FeedbackResponse(BaseModel):
    id: int
    title: str
    message: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
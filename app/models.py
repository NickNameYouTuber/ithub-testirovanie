from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    created_at: datetime

    class Config:
        from_attributes = True


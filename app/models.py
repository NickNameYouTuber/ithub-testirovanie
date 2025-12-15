from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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

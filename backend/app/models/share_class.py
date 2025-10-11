from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShareClassBase(BaseModel):
    name: str
    type: Optional[str] = None
    status: Optional[str] = "ACTIVE"
    currency: Optional[str] = None
    isin: Optional[str] = None

class ShareClassCreate(ShareClassBase):
    fund_id: str

class ShareClassUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    currency: Optional[str] = None
    isin: Optional[str] = None

class ShareClass(ShareClassBase):
    id: str
    fund_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
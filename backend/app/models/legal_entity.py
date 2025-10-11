from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LegalEntityBase(BaseModel):
    name: str
    type: Optional[str] = None
    status: Optional[str] = "ACTIVE"
    country: Optional[str] = None
    registration_number: Optional[str] = None

class LegalEntityCreate(LegalEntityBase):
    pass

class LegalEntityUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    country: Optional[str] = None
    registration_number: Optional[str] = None

class LegalEntity(LegalEntityBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
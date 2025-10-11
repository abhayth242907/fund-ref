from pydantic import BaseModel
from typing import Optional, List
from .fund import Fund

class ManagementEntityBase(BaseModel):
    name: str
    registration_number: str
    type: Optional[str] = None
    country: Optional[str] = None
    status: Optional[str] = "ACTIVE"

class ManagementEntityCreate(ManagementEntityBase):
    pass

class ManagementEntityUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    country: Optional[str] = None
    status: Optional[str] = None

class ManagementEntity(ManagementEntityBase):
    id: str
    funds: List[Fund] = []

    class Config:
        from_attributes = True

class ManagementEntityResponse(ManagementEntity):
    total_funds: int = 0
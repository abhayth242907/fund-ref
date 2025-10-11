from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class FundBase(BaseModel):
    name: str
    type: str = Field(description="Type of fund (e.g., UCITS, AIF)")
    domicile: str
    currency: str
    launch_date: datetime
    status: str = Field(description="Active, Liquidated, etc.")
    management_entity_id: str

class FundCreate(FundBase):
    pass

class FundUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    domicile: Optional[str] = None
    currency: Optional[str] = None
    launch_date: Optional[datetime] = None
    status: Optional[str] = None

class Fund(FundBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class FundHierarchy(Fund):
    sub_funds: List['Fund']
    share_classes: List['ShareClass']
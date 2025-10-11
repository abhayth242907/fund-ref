from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SubFundBase(BaseModel):
    name: str
    type: Optional[str] = None
    status: Optional[str] = "ACTIVE"
    currency: Optional[str] = None
    master_fund_id: str

class SubFundCreate(SubFundBase):
    pass

class SubFundUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    currency: Optional[str] = None

class SubFund(SubFundBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]
    share_classes: List['ShareClass'] = []  # Forward reference

    class Config:
        from_attributes = True

class SubFundDetail(SubFund):
    master_fund_name: str
    total_share_classes: int = 0
from pydantic import BaseModel
from typing import Optional, List

class ManagementEntity(BaseModel):
    id: str
    name: str
    type: Optional[str]
    country: Optional[str]
    status: Optional[str]

class FundMaster(BaseModel):
    id: str
    name: str
    type: Optional[str]
    management_entity_id: str
    status: Optional[str]
    inception_date: Optional[str]
    currency: Optional[str]

class SubFund(BaseModel):
    id: str
    name: str
    master_fund_id: str
    type: Optional[str]
    status: Optional[str]
    inception_date: Optional[str]
    currency: Optional[str]

class LegalEntity(BaseModel):
    id: str
    name: str
    type: Optional[str]
    status: Optional[str]
    country: Optional[str]
    registration_number: Optional[str]

class ShareClass(BaseModel):
    id: str
    name: str
    fund_id: str
    type: Optional[str]
    status: Optional[str]
    currency: Optional[str]
    isin: Optional[str]
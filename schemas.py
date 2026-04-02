from typing import Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

StatusEnum = Literal["applied", "interview", "selected", "rejected"]

class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    skill: str
    status: StatusEnum

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    status: StatusEnum

class CandidateResponse(CandidateBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

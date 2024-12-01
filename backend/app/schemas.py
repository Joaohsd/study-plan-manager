from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime, date

class Plan(BaseModel):
    id: Optional[int] = None
    goal: str
    deadline: date
    daily_hours: float
    created_at: Optional[datetime] = None
    progress: Optional[float] = None

# Model for creating a new plan
class CreatePlan(BaseModel):
    goal: str
    deadline: date
    daily_hours: float

    @field_validator("daily_hours")
    def daily_hours_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("daily_hours must be a positive float")
        return v

# Model for updating an existing plan
class UpdatePlan(BaseModel):
    goal: Optional[str] = None
    deadline: Optional[date] = None
    daily_hours: Optional[float] = None
    progress: Optional[float] = None

    @field_validator("daily_hours")
    def daily_hours_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("daily_hours must be a positive float")
        return v

    @field_validator("progress")
    def progress_must_be_between_zero_and_one(cls, v):
        if v is not None and not (0 <= v <= 1):
            raise ValueError("progress must be between 0 and 1")
        return v


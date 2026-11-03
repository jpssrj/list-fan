from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, StringConstraints

TitleStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]

class TaskBase(BaseModel):
    title: TitleStr

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[TitleStr] = None
    is_completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

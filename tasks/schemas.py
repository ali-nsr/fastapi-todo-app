from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=150, min_length=5, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Task description")
    is_completed: bool = Field(..., description="Task completed")


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., description="Task id")
    created_at: datetime = Field(..., description="Task creation datetime")
    updated_at: datetime = Field(..., description="Task update datetime")

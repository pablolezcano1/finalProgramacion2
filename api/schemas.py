from pydantic import BaseModel
from typing import List, Optional
from .models import User

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    user_id: Optional[int] = None  # Agrega este campo para permitir la actualización del usuario asignado


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class User(UserBase):
    id: int
    tasks: List[Task] = []

    class Config:
        orm_mode = True
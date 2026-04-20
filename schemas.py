from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str


class TaskCreate(BaseModel):
    title: str


class Task(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True   # ✅ IMPORTANT (Pydantic v2)
from pydantic import BaseModel


class GetTask(BaseModel):
    id: int
    user_id: int
    description: str
    complete: bool


class TaskInfo(BaseModel):
    description: str

from pydantic import BaseModel


class GetTask(BaseModel):
    id: int
    description: str
    complete: bool

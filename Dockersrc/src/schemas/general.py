from pydantic import BaseModel


class Inform(BaseModel):
    detail: str

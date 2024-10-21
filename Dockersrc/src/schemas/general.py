from pydantic import BaseModel


class Inform(BaseModel):
    message: str

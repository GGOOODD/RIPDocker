from pydantic import BaseModel


class RegInfo(BaseModel):
    email: str
    password: str
    repeat_password: str


class LogInfo(BaseModel):
    email: str
    password: str


class GetUser(BaseModel):
    email: str

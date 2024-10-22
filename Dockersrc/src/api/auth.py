from typing import Optional

from fastapi import APIRouter, status, Response, Request
from schemas import *
from services import Auth


router = APIRouter(tags=["Authentication"], prefix="/auth")


@router.post("/register", response_model=GetUser, status_code=status.HTTP_201_CREATED)
async def register(data: RegInfo):
    return await Auth.register(data)


@router.put("/login", response_model=GetUser, status_code=status.HTTP_200_OK)
async def login(data: LogInfo):
    return await Auth.login(data)


@router.put("/logout", response_model=Inform, status_code=status.HTTP_200_OK)
async def logout(request: Request, response: Response):
    return await Auth.logout(request, response)

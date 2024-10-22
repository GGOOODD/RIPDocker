from fastapi import APIRouter, status, Request
from schemas import *
from services import Task

router = APIRouter(tags=["Task"], prefix="/task")


@router.post("/create", response_model=GetTask, status_code=status.HTTP_201_CREATED)
async def create(data: TaskInfo, request: Request):
    return await Task.create(data, request)


@router.get("/get_all", response_model=list[GetTask], status_code=status.HTTP_200_OK)
async def get_all(request: Request):
    return await Task.get_all(request)


@router.get("/get/{task_id}", response_model=GetTask, status_code=status.HTTP_200_OK)
async def get(task_id: int, request: Request):
    return await Task.get(task_id, request)


@router.put("/update_complete/{task_id}", response_model=GetTask, status_code=status.HTTP_200_OK)
async def update_complete(task_id: int, complete: bool, request: Request):
    return await Task.update_complete(task_id, complete, request)


@router.put("/update_description/{task_id}", response_model=GetTask, status_code=status.HTTP_200_OK)
async def update_description(task_id: int, data: TaskInfo, request: Request):
    return await Task.update_description(task_id, data, request)


@router.delete("/delete/{task_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete(task_id: int, request: Request):
    return await Task.delete(task_id, request)

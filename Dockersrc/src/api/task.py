from fastapi import APIRouter, status
from schemas import GetTask, Inform
from services import Task

router = APIRouter(tags=["Task"], prefix="/task")


@router.post("/create", response_model=GetTask, status_code=status.HTTP_200_OK)
async def create(description: str):
    return await Task.create(description)


@router.get("/get_all", response_model=list[GetTask], status_code=status.HTTP_200_OK)
async def get_all():
    return await Task.get_all()


@router.get("/get/{task_id}", response_model=GetTask, status_code=status.HTTP_200_OK)
async def get(task_id: int):
    return await Task.get(task_id)


@router.put("/update_complete/{task_id}", response_model=GetTask, status_code=status.HTTP_200_OK)
async def update_complete(task_id: int, complete: bool):
    return await Task.update_complete(task_id, complete)


@router.put("/update_description/{task_id}", response_model=GetTask, status_code=status.HTTP_200_OK)
async def update_description(task_id: int, description: str):
    return await Task.update_description(task_id, description)


@router.delete("/delete/{task_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete(task_id: int):
    return await Task.delete(task_id)

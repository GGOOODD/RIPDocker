from fastapi import HTTPException, status, Request
from database import new_session, TaskModel, UserModel
from schemas import *
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from functions import Functions


class Task:
    @classmethod
    async def create(cls, data: TaskInfo, request: Request):
        user_id = await Functions.get_user_id(request)
        task_field = TaskModel(
            user_id=user_id,
            description=data.description,
            complete=False
        )
        async with new_session() as session:
            session.add(task_field)
            await session.flush()
            await session.commit()
        return task_field

    @classmethod
    async def get(cls, task_id: int, request: Request):
        user_id = await Functions.get_user_id(request)
        query = select(TaskModel).filter_by(id=task_id)
        async with new_session() as session:
            result = await session.execute(query)
        task = result.scalars().first()
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This task does not exist",
            )
        if task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This task does not connect to you",
            )
        return task

    @classmethod
    async def get_all(cls, request: Request):
        user_id = await Functions.get_user_id(request)
        query = select(UserModel).filter_by(id=user_id).options(joinedload(UserModel.tasks))
        async with new_session() as session:
            result = await session.execute(query)
        user_field = result.scalars().first()

        return user_field.tasks

    @classmethod
    async def update_complete(cls, task_id: int, complete: bool, request: Request):
        user_id = await Functions.get_user_id(request)
        query = select(TaskModel).filter_by(id=task_id)
        async with new_session() as session:
            result = await session.execute(query)
            task = result.unique().scalars().first()
            if task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This task does not exist",
                )
            if task.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This task does not connect to you",
                )
            task.complete = complete
            await session.flush()
            await session.commit()
        return task

    @classmethod
    async def update_description(cls, task_id: int, data: TaskInfo, request: Request):
        user_id = await Functions.get_user_id(request)
        query = select(TaskModel).filter_by(id=task_id)
        async with new_session() as session:
            result = await session.execute(query)
            task = result.scalars().first()
            if task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This task does not exist",
                )
            if task.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This task does not connect to you",
                )
            task.description = data.description
            await session.flush()
            await session.commit()
        return task

    @classmethod
    async def delete(cls, task_id: int, request: Request):
        user_id = await Functions.get_user_id(request)
        query = select(TaskModel).filter_by(id=task_id)
        async with new_session() as session:
            result = await session.execute(query)
            task = result.scalars().first()
            if task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This task does not exist",
                )
            if task.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This task does not connect to you",
                )
            query = delete(TaskModel).filter_by(id=task_id)
            await session.execute(query)
            await session.flush()
            await session.commit()
        return Inform(detail="task deleted")

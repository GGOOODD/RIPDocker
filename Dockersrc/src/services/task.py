from fastapi import HTTPException, status
from database import new_session, TaskModel
from schemas import Inform
from sqlalchemy import select, delete


class Task:
    @classmethod
    async def create(cls, description: str):
        task_field = TaskModel(
            description=description,
            complete=False
        )
        async with new_session() as session:
            session.add(task_field)
            await session.flush()
            await session.commit()
        return task_field

    @classmethod
    async def get(cls, task_id: int):
        query = select(TaskModel).filter_by(id=task_id)
        async with new_session() as session:
            result = await session.execute(query)
        task = result.scalars().first()
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This task does not exist",
            )
        return task

    @classmethod
    async def get_all(cls):
        query = select(TaskModel)
        async with new_session() as session:
            result = await session.execute(query)
        tasks = result.scalars().all()
        return tasks

    @classmethod
    async def update_complete(cls, task_id: int, complete: bool):
        query = select(TaskModel).filter_by(id=task_id)
        async with new_session() as session:
            result = await session.execute(query)
            task = result.scalars().first()
            if task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This task does not exist",
                )
            task.complete = complete
            await session.flush()
            await session.commit()
        return task

    @classmethod
    async def update_description(cls, task_id: int, description: str):
        query = select(TaskModel).filter_by(id=task_id)
        async with new_session() as session:
            result = await session.execute(query)
            task = result.scalars().first()
            if task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This task does not exist",
                )
            task.description = description
            await session.flush()
            await session.commit()
        return task

    @classmethod
    async def delete(cls, task_id: int):
        query = select(TaskModel).filter_by(id=task_id)
        async with new_session() as session:
            result = await session.execute(query)
            task = result.scalars().first()
            if task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This task does not exist",
                )
            query = delete(TaskModel).filter_by(id=task_id)
            await session.execute(query)
            await session.flush()
            await session.commit()
        return Inform(message="task deleted")

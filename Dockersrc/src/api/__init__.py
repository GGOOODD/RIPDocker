from fastapi import APIRouter

from api.task import router as task_router


router = APIRouter(prefix="/api")


router.include_router(task_router)

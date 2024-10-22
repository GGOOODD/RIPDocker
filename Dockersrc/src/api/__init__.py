from fastapi import APIRouter

from api.task import router as task_router
from api.auth import router as auth_router


router = APIRouter(prefix="/api")


router.include_router(task_router)
router.include_router(auth_router)

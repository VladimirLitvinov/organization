from fastapi import APIRouter
from .department import router as department_router
from .position import router as position_router
from .employee import router as employee_router

router = APIRouter(prefix="/api")
router.include_router(department_router)
router.include_router(position_router)
router.include_router(employee_router)
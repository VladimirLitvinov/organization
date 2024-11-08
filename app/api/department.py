from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_async_session
from database.crud import get_department_by_id, create_department_crud, \
    delete_department_crud, get_department_employee, add_department_position, \
    delete_department_position
from schemas.department import DepartmentOutSchema, DepartmentInSchema, \
    DepartmentPositionSchema
from schemas.employee import EmployeeOutSchema

router = APIRouter(tags=['Department'])


@router.get('/departments/{department_id}', response_model=DepartmentOutSchema,
            status_code=200)
async def get_department(department_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    department = await get_department_by_id(department_id, session)
    return department


@router.post('/departments', response_model=DepartmentOutSchema,
             status_code=201)
async def create_department(department: DepartmentInSchema,
                            session: AsyncSession = Depends(
                                get_async_session)):
    department = await create_department_crud(department, session)
    return department


@router.delete('/departments/{department_id}', status_code=204)
async def delete_department(department_id: int,
                            session: AsyncSession = Depends(
                                get_async_session)):
    await delete_department_crud(department_id, session)


@router.get('/departments/{department_id}/employees',
            response_model=list[EmployeeOutSchema], status_code=200)
async def get_department_employees(department_id: int,
                                   session: AsyncSession = Depends(
                                       get_async_session)):
    employees = await get_department_employee(department_id, session)
    return employees


@router.post('/departments/add_position', status_code=201)
async def add_position(data: DepartmentPositionSchema,
                       session: AsyncSession = Depends(get_async_session)):
    add = await add_department_position(data, session)
    return True


@router.delete('/departments/delete_position', status_code=204)
async def delete_position(data: DepartmentPositionSchema,
                          session: AsyncSession = Depends(get_async_session)):
    await delete_department_position(data, session)

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_async_session
from schemas.employee import EmployeeOutSchema, EmployeeInSchema
from database.crud import get_employee_crud, create_employee_crud, \
    update_employee_crud, delete_employee_crud

router = APIRouter(tags=['Employee'])


@router.get("/employees/{employee_id}", response_model=EmployeeOutSchema,
            status_code=200)
async def read_employee(employee_id: int,
                        session: AsyncSession = Depends(get_async_session)):
    employee = await get_employee_crud(employee_id, session)
    return employee


@router.post("/employee", response_model=EmployeeOutSchema, status_code=201)
async def create_employee(employee: EmployeeInSchema,
                          session: AsyncSession = Depends(get_async_session)):
    new_employee = await create_employee_crud(employee, session)
    return new_employee


@router.put("/employee/{employee_id}", response_model=EmployeeOutSchema,
            status_code=202)
async def update_employee(employee_id: int, new_data: EmployeeInSchema,
                          session: AsyncSession = Depends(get_async_session)):
    employee = await update_employee_crud(employee_id, new_data, session)
    return employee


@router.delete("/employee/{employee_id}", status_code=204)
async def delete_employee(employee_id: int,
                          session: AsyncSession = Depends(get_async_session)):
    delete = await delete_employee_crud(employee_id, session)

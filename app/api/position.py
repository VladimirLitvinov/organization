from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_async_session
from database.crud import get_position, create_position_crud, \
    delete_position_crud, update_position_crud, add_employee_crud, \
    delete_position_employee
from schemas.position import PositionOutSchema, PositionInSchema, \
    PositionEmployeeSchema

router = APIRouter(tags=["Position"])


@router.get("/positions/{position_id}", response_model=PositionOutSchema,
            status_code=200)
async def read_position(position_id: int,
                        session: AsyncSession = Depends(get_async_session)):
    position = await get_position(position_id, session)
    return position


@router.post("/positions", response_model=PositionOutSchema, status_code=201)
async def create_position(position: PositionInSchema,
                          session: AsyncSession = Depends(get_async_session)):
    position = await create_position_crud(position, session)
    return position


@router.delete("/positions/{position_id}", status_code=204)
async def delete_position(position_id: int,
                          session: AsyncSession = Depends(get_async_session)):
    await delete_position_crud(position_id, session)


@router.put("/positions/{position_id}", response_model=PositionOutSchema,
            status_code=202)
async def update_position(position_id: int, new_position: PositionInSchema,
                          session: AsyncSession = Depends(get_async_session)):
    update = await update_position_crud(position_id, new_position, session)
    return update


@router.post("/positions/add_employee", status_code=201)
async def add_employee(data: PositionEmployeeSchema,
                       session: AsyncSession = Depends(get_async_session)):
    add = await add_employee_crud(data, session)
    return True


@router.delete("/positions/delete_employee", status_code=204)
async def delete_employee(data: PositionEmployeeSchema,
                          session: AsyncSession = Depends(get_async_session)):
    await delete_position_employee(data, session)

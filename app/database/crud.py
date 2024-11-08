from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from database import Department, Position, Employee, employee_position, departament_position
from schemas.department import DepartmentInSchema, DepartmentPositionSchema
from schemas.employee import EmployeeInSchema
from schemas.position import PositionInSchema, PositionEmployeeSchema


# Department CRUD
async def get_department_by_id(department_id: int,
                               session: AsyncSession) -> Department:
    query = select(Department).where(Department.id == department_id)
    department = await session.execute(query)
    result = department.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return result


async def create_department_crud(data: DepartmentInSchema,
                                 session: AsyncSession) -> Department:
    department = Department(name=data.name, parent_id=data.parent_id)
    session.add(department)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400,
                            detail="Department already exists or parent is not found")

    await session.refresh(department)
    return department


async def delete_department_crud(department_id: int, session: AsyncSession):
    query = select(Department).where(Department.id == department_id)
    department = await session.execute(query)
    result = department.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Department not found")
    delete = await session.delete(result)
    await session.commit()
    return delete


async def get_department_employee(department_id: int, session: AsyncSession) -> \
        list[Employee]:
    query = select(Employee).where(Employee.department_id == department_id)
    employees = await session.execute(query)
    result = employees.all()
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    result = [employee[0] for employee in result]
    return result


async def add_department_position(data: DepartmentPositionSchema,
                                  session: AsyncSession):
    query_departament = select(Department).options(
        joinedload(Department.positions)).where(
        Department.id == data.department_id)
    query_position = select(Position).where(Position.id == data.position_id)
    _department = await session.execute(query_departament)
    _position = await session.execute(query_position)
    department = _department.unique().scalar_one_or_none()
    position = _position.scalar_one_or_none()
    if position is None or department is None:
        raise HTTPException(status_code=404,
                            detail="Position or department not found")
    department.positions.append(position)
    await session.commit()
    await session.refresh(department)


async def delete_department_position(data: DepartmentPositionSchema, session: AsyncSession):
    query = departament_position.delete().where(departament_position.c.departament_id == data.department_id,
                                                departament_position.c.position_id == data.position_id)
    result = await session.execute(query)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Position not found")
    await session.commit()


# Position CRUD

async def get_position(position_id: int, session: AsyncSession) -> Position:
    query = select(Position).where(Position.id == position_id)
    position = await session.execute(query)
    result = position.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return result


async def create_position_crud(data: PositionInSchema,
                               session: AsyncSession) -> Position:
    position = Position(title=data.title, rights=data.rights)
    session.add(position)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Position already exists")

    await session.refresh(position)
    return position


async def delete_position_crud(position_id: int, session: AsyncSession):
    query = select(Position).where(Position.id == position_id)
    position = await session.execute(query)
    result = position.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Position not found")
    await session.delete(result)
    await session.commit()


async def update_position_crud(position_id: int, data: PositionInSchema,
                               session: AsyncSession) -> Position:
    query = select(Position).where(Position.id == position_id)
    position = await session.execute(query)
    result = position.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Position not found")
    result.title = data.title
    result.rights = data.rights
    await session.commit()
    await session.refresh(result)
    return result


async def add_employee_crud(data: PositionEmployeeSchema,
                            session: AsyncSession):
    query_position = select(Position).options(
        joinedload(Position.employees)).where(Position.id == data.position_id)
    query_employee = select(Employee).where(
        Employee.id == data.employee_id)
    _employee = await session.execute(query_employee)
    _position = await session.execute(query_position)
    employee = _employee.scalar_one_or_none()
    position = _position.unique().scalar_one_or_none()
    if position is None or employee is None:
        raise HTTPException(status_code=404,
                            detail="Position or employee not found")
    position.employees.append(employee)
    await session.commit()
    await session.refresh(position)


async def delete_position_employee(data: PositionEmployeeSchema,
                                   session: AsyncSession):
    query = employee_position.delete().where(
        (employee_position.c.employee_id == data.employee_id) &
        (employee_position.c.position_id == data.position_id)
    )
    result = await session.execute(query)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Position not found")

    await session.commit()


# Employee CRUD

async def get_employee_crud(employee_id: int,
                            session: AsyncSession) -> Employee:
    query = select(Employee).where(Employee.id == employee_id)
    employee = await session.execute(query)
    result = employee.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return result


async def create_employee_crud(data: EmployeeInSchema,
                               session: AsyncSession) -> Employee:
    employee = Employee(name=data.name, department_id=data.department_id)
    session.add(employee)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400,
                            detail="Employee already exists or department not exists")
    await session.refresh(employee)
    return employee


async def update_employee_crud(employee_id: int, data: EmployeeInSchema,
                               session: AsyncSession) -> Employee:
    query = select(Employee).where(Employee.id == employee_id)
    employee = await session.execute(query)
    result = employee.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    result.name = data.name
    result.department_id = data.department_id
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400,
                            detail="Employee name or department id error")
    await session.refresh(result)
    return result


async def delete_employee_crud(employee_id: int, session: AsyncSession):
    query = select(Employee).where(Employee.id == employee_id)
    employee = await session.execute(query)
    result = employee.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    await session.delete(result)
    await session.commit()

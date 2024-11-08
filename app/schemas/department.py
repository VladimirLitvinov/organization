from typing import Optional

from pydantic import BaseModel


class DepartmentOutSchema(BaseModel):
    id: int
    name: str


class DepartmentInSchema(BaseModel):
    name: str
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True


class DepartmentPositionSchema(BaseModel):
    department_id: int
    position_id: int

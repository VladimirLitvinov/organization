from typing import Optional

from pydantic import BaseModel


class EmployeeBaseSchema(BaseModel):
    name: str
    department_id: Optional[int] = None


class EmployeeOutSchema(EmployeeBaseSchema):
    id: int


class EmployeeInSchema(EmployeeBaseSchema):
    pass

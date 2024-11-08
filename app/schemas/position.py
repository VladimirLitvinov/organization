from pydantic import BaseModel


class PositionBaseSchema(BaseModel):
    title: str
    rights: str


class PositionOutSchema(PositionBaseSchema):
    id: int


class PositionInSchema(PositionBaseSchema):
    pass


class PositionEmployeeSchema(BaseModel):
    position_id: int
    employee_id: int

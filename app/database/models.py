from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base

employee_position = Table('employee_position', Base.metadata,
                          Column('employee_id', Integer,
                                 ForeignKey('employees.id')),
                          Column('position_id', Integer,
                                 ForeignKey('positions.id'))
                          )

departament_position = Table('departament_position', Base.metadata,
                             Column('departament_id', Integer,
                                    ForeignKey('departments.id')),
                             Column('position_id', Integer,
                                    ForeignKey('positions.id'))
                             )


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey('departments.id'))

    sub_departments = relationship('Department', backref='parent',
                                   remote_side=[id])
    employees = relationship('Employee', back_populates='department')

    positions = relationship('Position', secondary=departament_position,
                             back_populates='departments')


class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    rights = Column(String)

    employees = relationship('Employee', secondary=employee_position,
                             back_populates='positions')

    departments = relationship('Department', secondary=departament_position, back_populates='positions')


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    department_id = Column(Integer, ForeignKey('departments.id'))

    positions = relationship('Position', secondary=employee_position,
                             back_populates='employees')
    department = relationship('Department', back_populates='employees')

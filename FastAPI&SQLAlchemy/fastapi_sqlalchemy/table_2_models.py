from typing import Optional
import datetime

from sqlalchemy import Date, ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Departments(Base):
    __tablename__ = 'departments'
    __table_args__ = (
        Index('name', 'name', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(100))

    employees: Mapped[list['Employees']] = relationship(
        'Employees',
        back_populates='department',
        lazy='selectin'
    )



class Employees(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='RESTRICT', name='employees_ibfk_1'),
        Index('department_id', 'department_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    department_id: Mapped[int] = mapped_column(Integer, nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    hire_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    department: Mapped['Departments'] = relationship(
        'Departments',
        back_populates='employees',
        lazy='selectin'
    )

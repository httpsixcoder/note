import datetime
from sqlalchemy import Date, ForeignKey, Index, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional


class Base(DeclarativeBase):
    pass


class Departments(Base):
    __tablename__ = 'departments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    location: Mapped[Optional[str]] = mapped_column(String(100))

    employees: Mapped[list['Employees']] = relationship(
        'Employees',
        back_populates='department'
    )

    def __repr__(self) -> str:
        return f"<Departments id={self.id} name={self.name!r}>"


class Employees(Base):
    __tablename__ = 'employees'


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    department_id: Mapped[int] = mapped_column(
        ForeignKey('departments.id', ondelete='RESTRICT')
    )
    age: Mapped[Optional[int]] = mapped_column(Integer)
    hire_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    department: Mapped['Departments'] = relationship(
        'Departments',
        back_populates='employees'
    )

    def __repr__(self) -> str:
        return f"<Employees id={self.id} name={self.name!r} dept={self.department_id}>"
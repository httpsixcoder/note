

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from new_demo.sqlalchemy_demo.base import Base

if TYPE_CHECKING:
    from .department import Departments

class Employees(Base):
    __tablename__ = 'employees'

    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    name:Mapped[str]=mapped_column(String(50))
    department_id:Mapped[int]=mapped_column(
        ForeignKey('departments.id',ondelete='RESTRICT')
    )
    age:Mapped[int|None]=mapped_column(Integer)
    hire_date:Mapped[datetime.date|None]=mapped_column(Date)

    department:Mapped["Departments"]=relationship(
        "Departments",
        back_populates="employees",
        lazy="joined",
    )

    def __repr__(self):
        return f"Employee :{self.id},name:{self.name},department_id:{self.department_id}"
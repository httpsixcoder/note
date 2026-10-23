from __future__ import annotations

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


# 部门模型类
class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    desc: Mapped[str | None] = mapped_column(String(200))

    employees: Mapped[List["Employee"]] = relationship(
        back_populates="department",
        lazy="selectin"
    )

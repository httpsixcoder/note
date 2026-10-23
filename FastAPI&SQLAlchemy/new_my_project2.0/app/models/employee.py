from __future__ import annotations

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


# 员工模型类
class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    role: Mapped[str] = mapped_column(String(50))
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="RESTRICT")
    )

    department: Mapped["Department"] = relationship(
        back_populates="employees",
        lazy="joined"
    )

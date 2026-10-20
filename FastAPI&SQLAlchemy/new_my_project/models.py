from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# 1. 定义基类（代替旧的 declarative_base()）
class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"
    # 2. 使用 Mapped 和 mapped_column（强类型）
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    # 3. 一对多关系：lazy="selectin" 是异步 FastAPI 解决 N+1 问题的标配
    employees: Mapped[List["Employee"]] = relationship(
        back_populates="department",
        lazy="selectin",
    )


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int | None] = mapped_column(default=None)
    # 外键
    department_id: Mapped[int] = mapped_column(
        ForeignKey(
            "departments.id",
            ondelete="CASCADE"
        )
    )

    department: Mapped["Department"] = relationship(
        back_populates="employees",
        lazy="joined",
    )

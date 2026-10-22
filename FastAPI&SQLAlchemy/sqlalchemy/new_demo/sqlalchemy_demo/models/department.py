from __future__ import annotations

from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from new_demo.sqlalchemy_demo.base import Base

# 只在类型检查时导入，运行时完全不执行，杜绝循环导入
# `TYPE_CHECKING` 是 `typing` 内置的布尔常量：
# - ✅ **静态阶段（IDE/PyCharm、mypy、pyright 做类型检查的时候）：值 = True**
# - ✅ **真实运行阶段（python main.py 跑业务代码）：值 = False**
if TYPE_CHECKING:
    from .employee import Employees

class Departments(Base):
    __tablename__ = "departments"

    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    name:Mapped[str]=mapped_column(String(20),unique=True)
    location: Mapped[str | None] = mapped_column(String(50))

    employees:Mapped[List[Employees]]=relationship(
        "Employees",           # 找Employees模型类
        back_populates="department",    # 配对另一边模型里的 relationship
        lazy="selectin",                # 加载策略：`lazy="select"`（默认：1对多，1端）|lazy="joined"（1对多，多端）
    )
    def __repr__(self):
        return f"Department: {self.id}, Name: {self.name}"
# from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Employee
from app.schemas.employee_schema import EmployeeCreate, EmployeeUpdate


async def employee_get_by_id(db: AsyncSession, emp_id: int) -> Employee | None:
    return await db.get(Employee, emp_id)


# Sequence[Employee]，**不是严格的 list**
async def employee_by_dept_id(db: AsyncSession, dept_id: int) -> Sequence[Employee]:
    stmt = select(Employee).where(Employee.department_id == dept_id)
    res = await db.execute(stmt)
    return res.scalars().all()


async def employee_create(db: AsyncSession, emp_in: EmployeeCreate) -> Employee:
    # emp_in.model_dump():将 Pydantic 对象变成一个纯 Python 字典。
    emp_obj = Employee(**emp_in.model_dump())
    # 把刚刚创建的 emp_obj 放入 SQLAlchemy 的 Session 缓存中。
    db.add(emp_obj)
    # db.flush()：发送执行，但不是提交事务，用于id回填
    await db.flush()
    return emp_obj


async def employee_update(db: AsyncSession, emp_obj: Employee, emp_in: EmployeeUpdate) -> Employee:
    # exclude_unset=True：只会输出用户实际传过来的字段，没传的不会显示值为None，而是不显示，只显示传入的字段值
    update_data = emp_in.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(emp_obj, k, v)
    await db.flush()
    return emp_obj


async def employee_delete(db: AsyncSession, emp_obj: Employee) -> None:
    await db.delete(emp_obj)

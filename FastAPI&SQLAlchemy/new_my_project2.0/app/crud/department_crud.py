# from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Department
from schemas import DepartmentCreate, DepartmentUpdate


async def department_get_by_id(db: AsyncSession, dept_id: int) -> Department | None:
    return await db.get(Department, dept_id)  ## 2.0 简写：通过主键查【db.get()只能根据主键查询！】


async def department_get_by_name(db: AsyncSession, name: str) -> Department | None:
    stmt = select(Department).where(Department.name == name)
    result = await db.execute(stmt)
    return result.scalars().first()


async def department_create(db: AsyncSession, dept_obj: Department) -> Department:
    db.add(dept_obj)
    await db.flush()  # flush 拿 ID，不 commit，由外层统一 commit
    return dept_obj


async def department_delete(db: AsyncSession, dept_obj: Department) -> None:
    await db.delete(dept_obj)


async def department_update(db: AsyncSession, dept_obj: Department, dept_in: DepartmentUpdate) -> Department:
    update_data = dept_in.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(dept_obj, k, v)
    await db.flush()
    return dept_obj

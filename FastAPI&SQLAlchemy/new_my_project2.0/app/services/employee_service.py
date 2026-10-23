from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException
from app.crud import employee_crud as emp_crud
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate


# id 查询
async def service_employee_get_by_id(db: AsyncSession, emp_id: int, ) -> Employee | None:
    emp = await emp_crud.employee_get_by_id(db, emp_id)
    if not emp:
        raise BusinessException(f"没有ID为{emp_id}的员工")
    return emp


# name 查询
async def service_employee_get_by_department_id(db: AsyncSession, dept_id: int) -> Sequence[Employee]:
    emp_list = await emp_crud.employee_by_dept_id(db, dept_id)
    if not emp_list:
        raise BusinessException(f"ID为{dept_id}的部门没有员工")
    return emp_list


# ✅ 事务边界：【增、改、删】才加 async with db.begin()
# 块内无异常 → 自动commit；块内抛异常 → 自动rollback
# 创建
async def service_employee_create(db: AsyncSession, emp_in: EmployeeCreate) -> Employee:
    async with db.begin():
        return await emp_crud.employee_create(db, emp_in)


# 删除
async def service_employee_delete_by_id(db: AsyncSession, emp_id: int) -> None:
    # 仅演示，物理删除
    async with db.begin():
        emp = await emp_crud.employee_get_by_id(db, emp_id)
        if not emp:
            raise BusinessException(f"ID为{emp_id}的员工不存在，无法删除")

        await emp_crud.employee_delete(db, emp)


# 更新修改
async def service_employee_update(db: AsyncSession, emp_id: int, emp_in: EmployeeUpdate) -> Employee:
    async with db.begin():
        emp_obj = await emp_crud.employee_get_by_id(db, emp_id)
        if not emp_obj:
            raise BusinessException(f"无法修改，ID为{emp_id}的员工不存在，无法删除")
        return await emp_crud.employee_update(db, emp_obj, emp_in)

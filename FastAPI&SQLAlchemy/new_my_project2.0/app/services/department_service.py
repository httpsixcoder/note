from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException
from app.crud import department_crud as dept_crud
from app.models import Department, Employee
from app.schemas import DepartmentCreate, DepartmentUpdate


# id 查询
async def service_department_get_by_id(db: AsyncSession, dept_id: int, ) -> Department | None:
    dept = await dept_crud.department_get_by_id(db, dept_id)
    if not dept:
        raise BusinessException(f"没有ID为{dept_id}的部门")
    return dept


# name 查询
async def service_department_get_by_name(db: AsyncSession, dept_name: str) -> Department | None:
    dept = await dept_crud.department_get_by_name(db, dept_name)
    if not dept:
        raise BusinessException(f"没有名字为{dept_name}的部门")
    return dept


# 创建
async def service_department_create(db: AsyncSession, dept_in: DepartmentCreate) -> Department:
    # 🌟 整个创建流程是一个原子操作，要么全成功，要么全失败
    async with db.begin():
        # 1. 业务校验（查重）
        existing = await dept_crud.department_get_by_name(db, dept_in.name)
        if existing:
            raise BusinessException(f"部门 '{dept_in.name}' 已存在！")

        # 2. 组装并保存（CRUD 内部依然只 flush）
        dept_obj = Department(**dept_in.model_dump(exclude={"employees"}))
        if dept_in.employees:
            dept_obj.employees = [Employee(name=emp.name, role=emp.role) for emp in dept_in.employees]
        await dept_crud.department_create(db, dept_obj)

        # 3. 返回前，手动刷新一下，避免 MissingGreenlet
        # 在异步 session 事务结束之后，去访问 ORM 对象的【延迟加载关联属性】，直接抛 MissingGreenlet。
        # 本质：这个 ORM 对象绑定的 greenlet 协程环境已经结束、销毁了，没法再发起新的数据库查询去懒加载关联数据。
        await db.refresh(dept_obj, ["employees"])
        return dept_obj


# 删除
async def service_department_delete_by_id(db: AsyncSession, dept_id: int) -> None:
    async with db.begin():
        dept = await dept_crud.department_get_by_id(db, dept_id)
        if not dept:
            raise BusinessException(f"ID为{dept_id}的部门不存在，无法删除")
        # 仅演示，物理删除

        await dept_crud.department_delete(db, dept)


# 更新修改
async def service_department_update(db: AsyncSession, dept_id: int, dept_in: DepartmentUpdate) -> Department:
    async with db.begin():
        dept_obj = await dept_crud.department_get_by_id(db, dept_id)
        if not dept_obj:
            raise BusinessException(f"无法修改，ID为{dept_id}的部门不存在，无法删除")
        if dept_in.name and dept_in.name != dept_obj.name:
            existing = await dept_crud.department_get_by_name(db, dept_in.name)
            if existing:
                raise BusinessException(f"无法修改，部门 '{dept_in.name}' 已存在，请勿重复创建！")

        return await dept_crud.department_update(db, dept_obj, dept_in)

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db, verify_token
from app.schemas import EmployeeResponse, EmployeeCreate, EmployeeUpdate
from app.services import employee_service as emp_service

router = APIRouter(
    prefix="/employees",
    tags=["员工管理"],
    dependencies=[Depends(verify_token)]
)


# 1. 根据部门 ID 查询员工列表 (注意：列表查询返回 List，并且固定路径要放在 /{emp_id} 前面)
@router.get(
    "/department/{dept_id}",
    response_model=List[EmployeeResponse],  # 🌟 注意这里返回的是一个列表
    status_code=status.HTTP_200_OK,
    summary="根据部门 ID 查询员工列表"
)
async def get_employees_by_dept(dept_id: int, db: AsyncSession = Depends(get_db)):
    return await emp_service.service_employee_get_by_department_id(db, dept_id)


# 2. 根据员工 ID 查询
@router.get(
    "/{emp_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="根据 ID 查询员工"
)
async def get_employee_by_id(emp_id: int, db: AsyncSession = Depends(get_db)):
    return await emp_service.service_employee_get_by_id(db, emp_id)


# 3. 创建员工
@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="创建员工"
)
async def create_employee(emp_in: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    return await emp_service.service_employee_create(db, emp_in)


# 4. 更新员工
@router.put(
    "/{emp_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="更新指定 ID 员工信息"
)
async def update_employee(
        emp_id: int,
        emp_in: EmployeeUpdate,
        db: AsyncSession = Depends(get_db)
):
    return await emp_service.service_employee_update(db, emp_id, emp_in)


# 5. 删除员工
@router.delete(
    "/{emp_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除指定 ID 员工"
)
async def delete_employee(emp_id: int, db: AsyncSession = Depends(get_db)):
    # 204 状态码无响应体，直接 await
    await emp_service.service_employee_delete_by_id(db, emp_id)

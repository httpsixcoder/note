from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db, verify_token
from app.schemas import DepartmentResponse, DepartmentCreate, DepartmentUpdate
from app.services import department_service as dept_service


router = APIRouter(
    prefix="/departments",
    tags=["部门管理"],
    # 给所有加，或者给单独router加
    dependencies=[Depends(verify_token)]
)


@router.get(
    "/{dept_id}",
    # dependencies=[Depends(verify_admin)], # 方式2
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK,
    summary="根据 ID 查询部门")
async def get_dept_by_id(dept_id: int, db: AsyncSession = Depends(get_db)):
    return await dept_service.service_department_get_by_id(db, dept_id)


@router.get(
    "/name/{dept_name}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK,
    summary="根据 name 查询部门")
async def get_dept_by_name(dept_name: str, db: AsyncSession = Depends(get_db)):
    return await dept_service.service_department_get_by_name(db, dept_name)


@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="创建部门")
async def create_dept(dept_in: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    return await dept_service.service_department_create(db, dept_in)


@router.delete(
    "/{dept_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除指定id部门")
async def delete_dept(dept_id: int, db: AsyncSession = Depends(get_db)):
    return await dept_service.service_department_delete_by_id(db, dept_id)


@router.put(
    "/{dept_id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK,
    summary="更新指定id部门信息")
async def update_dept(
        dept_id: int,
        dept_in: DepartmentUpdate,
        db: AsyncSession = Depends(get_db),
        # current_user: dict = Depends(verify_token)# 🌟 如果需要在业务里记录“谁改的”，可以在这里再注入一次
):
    # 注：如果 Router 层已经挂载了，这里其实不需要再写 Depends(verify_token)，
    # 除非你需要在函数体里用到 current_user 的信息。
    return await dept_service.service_department_update(db, dept_id, dept_in)


"""
以下是你这 5 个接口的推荐写法对比：

推荐 URL	                HTTP 方法	说明
/{dept_id}	            GET	        用 GET 方法本身就代表“查询”
/name/{dept_name}	    GET	        避免和纯数字的 ID 冲突，保留 /name/
/	                    POST	    用 POST 方法本身就代表“新建”
/{dept_id}	            DELETE	    用 DELETE 方法本身就代表“删除”
/{dept_id}	            PUT	        用 PUT 方法本身就代表“更新”
"""

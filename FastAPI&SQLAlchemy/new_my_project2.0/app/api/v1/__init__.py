"""
    API v1 路由聚合
"""
from fastapi import APIRouter

from . import department, employee

# 创建 v1 版本的全局路由
api_router = APIRouter()

# 将子路由挂载进来
api_router.include_router(department.router)
api_router.include_router(employee.router)

__all__ = ["api_router"]

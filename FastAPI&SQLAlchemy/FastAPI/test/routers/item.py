"""
    测试：处理用商品功能模块的请求
"""
from fastapi import APIRouter
from pydantic import BaseModel

# 创建对象
router = APIRouter(
    prefix="/item",
    tags=["商品管理"],
)


# 查询所有用的信息
@router.get("/")
def get_item():
    return {"username": "亚瑟士", "price": 100}


@router.post("/add")
def add_item(name: str, price: int):
    return {"name": name, "price": price}

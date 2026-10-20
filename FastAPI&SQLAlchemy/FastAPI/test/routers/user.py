"""
    测试：处理用户功能模块的请求
"""
from fastapi import APIRouter
from pydantic import BaseModel

# 创建对象
router = APIRouter(
    prefix="/user", # 设置当前当前文件中所处理的所有的请求的请求路径以/user为前缀
    tags=["用户管理"],
)


class User(BaseModel):
    username: str
    password: str
    age: int


# 查询所有用的信息
@router.get("/")
def get_user():
    return {"username": "admin", "password": "123456"}


@router.post("/add")
def add_user(user: User):
    return {"username": user.username, "password": user.password, "age": user.age}

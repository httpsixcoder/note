from typing import Optional, List

from pydantic import BaseModel, ConfigDict


# ================= 输入模型 (Request Body) =================
class EmployeeCreate(BaseModel):
    name: str
    age: Optional[int] = None


class DepartmentCreate(BaseModel):
    name: str
    employees: List[EmployeeCreate] = []  # 支持创建部门时一并创建员工


# ================= 输出模型 (Response Body) =================
class EmployeeResponse(BaseModel):
    id: int
    name: str
    age: Optional[int]

    # Pydantic v2 新语法：允许从 ORM 对象属性中读取数据
    model_config = ConfigDict(from_attributes=True)


class DepartmentResponse(BaseModel):
    id: int
    name: str
    # 嵌套员工响应（⚠️ 注意不要在 EmployeeResponse 里嵌 Department，否则会无限递归报错）
    department: List[DepartmentCreate] = []
    model_config = ConfigDict(from_attributes=True)

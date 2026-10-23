"""
    解耦方式解决循环引用：
"""

"""
# schemas/common.py
from pydantic import BaseModel, ConfigDict

class DepartmentSimple(BaseModel):
    # 只放员工详情页需要看到的部门信息
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
# schemas/department.py
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from .employee import EmployeeResponse

class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="部门名称必须唯一")
    desc: str | None = Field(None, max_length=200, description="部门描述信息")

class DepartmentCreate(DepartmentBase):
    employees: List[EmployeeCreate] = Field(default_factory=list)

# 完整响应：带员工列表，用于部门详情
class DepartmentResponse(DepartmentBase):
    id: int
    desc: str | None
    employees: List[EmployeeResponse] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
# schemas/employee.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from .common import DepartmentSimple  # 只引入这个轻量版，不碰DepartmentResponse

class EmployeeResponse(EmployeeBase):
    id: int
    department_id: int
    # 员工里面只放简单部门信息，不会带上一长串员工列表！
    department: Optional[DepartmentSimple] = None
    model_config = ConfigDict(from_attributes=True)
"""

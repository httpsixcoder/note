from typing import List

from pydantic import BaseModel, Field, ConfigDict

from .employee_schema import EmployeeCreate, EmployeeResponse


# ========== Department ==========
class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="部门名称必须唯一")
    desc: str | None = Field(None, max_length=200, description="部门描述信息")


class DepartmentCreate(DepartmentBase):
    # 专门给 list/dict 这种可变类型用：**每次创建这个模型实例，都会生成一个全新的空列表**
    # ❌ 禁止直接写 `= []`：直接写 [] 会所有请求共享同一个列表，并发场景数据错乱
    employees: List[EmployeeCreate] | None = Field(default_factory=list, description="下属员工列表，可选")


class DepartmentUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=50, description="部门名称，修改时保证唯一")
    desc: str | None = Field(None, max_length=200, description="部门描述信息")
    # 注意：嵌套更新员工一般不建议直接在部门update里面带上employees，容易混乱
    # 员工修改单独走员工接口，这是主流做法，这里就不加employees了

class DepartmentResponse(DepartmentBase):
    id: int = Field(..., description="部门主键ID")
    employees: List[EmployeeResponse] = Field(default_factory=list, description="部门下属员工列表")
    model_config = ConfigDict(from_attributes=True)

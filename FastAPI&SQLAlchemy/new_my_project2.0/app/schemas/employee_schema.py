from pydantic import BaseModel, Field, ConfigDict


# ========== Employee ==========
# 抽取出共用字段，遵循「Base / Create / Response」分层规范
# 分层思想：Base 放共用字段；Create 继承 Base，用于接收前端提交；Response 继承 Base，用于返回给前端
# - Base：存放【新增、返回都会用到的公共字段】，避免重复写代码
#       Field(..., xxx) → 必填字段，前端必须传，不能省略
#       Field(None, xxx) → 可选字段，默认值是 None，不传就是 `None`
# - Create继承BaseModel：POST 新增接口，接收前端传过来的数据（一般不含数据库自动生成的 id）
# - Response继承BaseModel：查询接口，返回给前端的数据（包含 id、外键这类后端生成字段）
class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="员工姓名")  # 第一个参数 `...` 代表**必填，不允许为空**
    role: str = Field(..., min_length=2, max_length=50, description="员工职位")


class EmployeeCreate(EmployeeBase):
    department_id: int = Field(..., description="所属部门ID")

class EmployeeUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=30, description="员工姓名")
    role: str | None = Field(None, min_length=2, max_length=50, description="员工职位")
    department_id: int | None = Field(None, description="所属部门ID")


class EmployeeResponse(EmployeeBase):
    id: int = Field(..., description="员工主键ID")
    department_id: int = Field(..., description="所属部门ID")
    # 可以直接把 SQLAlchemy 查出来的 ORM 模型对象，转换成这个 Pydantic 响应模型
    model_config = ConfigDict(from_attributes=True)

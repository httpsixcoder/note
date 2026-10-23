"""
    数据校验层
"""
from .department_schema import DepartmentBase, DepartmentCreate, DepartmentUpdate, DepartmentResponse
from .employee_schema import EmployeeBase, EmployeeCreate, EmployeeUpdate, EmployeeResponse

__all__ = [
    "EmployeeBase", "EmployeeCreate", "EmployeeUpdate", "EmployeeResponse",
    "DepartmentBase", "DepartmentCreate", "DepartmentUpdate", "DepartmentResponse"
]

"""
    出现循环引入的时候，解决方法：
    1.局部导入（函数内部导入，推荐学习阶段用，好理解）
        from __future__ import annotations 结合 字符串向前引用
        Pydantic V2 支持字符串注解 + __future__ annotations，序列化、校验、文档都能正常识别，FastAPI /docs 文档也正常渲染。
    2.【推荐】架构层面【解耦，根治循环依赖，企业规范首选⭐⭐⭐⭐⭐】
        依赖关系：
            department → employee
            employee → common
        没有双向互相引用，彻底杜绝循环导入，可读性最好，大型项目都这么写！
            from pydantic import BaseModel, ConfigDict
            class DepartmentSimple(BaseModel):
                # 极简部门模型，给员工详情里嵌套使用，只有少量字段
                id: int
                name: str
                model_config = ConfigDict(from_attributes=True)

"""

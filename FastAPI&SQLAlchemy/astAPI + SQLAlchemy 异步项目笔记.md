# FastAPI + SQLAlchemy 异步项目笔记（大厂规范版）
> 技术栈：FastAPI + SQLAlchemy 2.0(异步) + Pydantic v2 + asyncmy / aiosqlite
> 分层：Router → Service → CRUD → Model
> 事务、循环引用、MissingGreenlet、唯一校验、级联新增 重点踩坑汇总

## 目录结构（推荐）
```
app/
├── api/
│   └── v1/
│       ├── __init__.py
│       ├── router_department.py
│       ├── router_employee.py
│       └── api_router.py   # 聚合所有路由
├── core/
│   ├── __init__.py
│   ├── config.py           # pydantic-settings 环境变量、数据库url
│   ├── security.py         # bcrypt、jwt
│   └── dependencies.py     # 全局依赖
├── db/
│   ├── __init__.py
│   ├── base.py             # Base = DeclarativeBase，公共审计字段
│   ├── session.py          # engine、AsyncSessionLocal、get_db
│   └── init_db.py          # 建表、初始化基础数据（生产用alembic）
├── models/
│   ├── __init__.py
│   ├── department.py
│   └── employee.py
├── schemas/
│   ├── __init__.py
│   ├── department.py
│   └── employee.py
├── crud/
│   ├── __init__.py
│   ├── crud_department.py
│   └── crud_employee.py
├── service/
│   ├── __init__.py
│   ├── service_department.py
│   └── service_employee.py
├── common/
│   ├── __init__.py
│   ├── exceptions.py       # BusinessException 自定义业务异常
│   └── response.py         # 统一返回体
└── main.py
```

## 一、db/base.py
```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func

class Base(DeclarativeBase):
    """所有ORM模型的父类"""
    create_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
```

## 二、db/session.py
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # 开发True，生产False
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
```

## 三、core/config.py
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+asyncmy://root:123456@127.0.0.1:3306/test_db"
    APP_TITLE: str = "企业级FastAPI项目"

settings = Settings()
```

## 四、common/exceptions.py
```python
class BusinessException(Exception):
    def __init__(self, msg: str, code: int = 400):
        self.msg = msg
        self.code = code
        super().__init__(msg)
```

## 五、main.py（lifespan + 全局异常）
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1 import api_router
from app.db.session import engine
from app.db.base import Base
from app.common.exceptions import BusinessException

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ========= 注意：本地首次运行打开，生产环境注释，使用Alembic迁移 =========
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="企业级 FastAPI 架构",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api/v1")

@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "msg": exc.msg, "data": None}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
```

## 六、models/department.py
```python
from __future__ import annotations
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), index=True, unique=True, comment="部门名称唯一")
    desc: Mapped[str | None] = mapped_column(String(200))

    employees: Mapped[List["Employee"]] = relationship(
        back_populates="department",
        lazy="selectin"
    )
```

## 七、models/employee.py
```python
from __future__ import annotations
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    role: Mapped[str] = mapped_column(String(50))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    department: Mapped["Department"] = relationship(back_populates="employees")
```

## 八、schemas/department.py
```python
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.employee import EmployeeCreate, EmployeeResponse

class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="部门名称必须唯一")
    desc: str | None = Field(None, max_length=200, description="部门描述信息")

class DepartmentCreate(DepartmentBase):
    employees: List[EmployeeCreate] = Field(default_factory=list, description="下属员工列表，可选")

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int
    employees: List[EmployeeResponse] = []
    model_config = ConfigDict(from_attributes=True)
```

## 九、schemas/employee.py
```python
from pydantic import BaseModel, Field, ConfigDict

class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="员工姓名")
    role: str = Field(..., min_length=1, max_length=50, description="岗位")

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    department_id: int
    model_config = ConfigDict(from_attributes=True)
```

> Field 三个重点区分：
> - `Field(...)` 必填，不允许不传
> - `Field(None)` 可选，不传值默认None
> - `Field(default_factory=list)` 可变对象（list/dict），每次实例新建空列表，**禁止直接写 = []**

## 十、crud/crud_department.py
```python
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.department import Department

async def department_get_by_name(db: AsyncSession, name: str) -> Department | None:
    stmt = select(Department).where(Department.name == name)
    result = await db.execute(stmt)
    return result.scalars().first()

async def department_get_by_id(db: AsyncSession, dept_id: int) -> Department | None:
    return await db.get(Department, dept_id)

async def department_create(db: AsyncSession, dept_obj: Department) -> Department:
    db.add(dept_obj)
    await db.flush()
    return dept_obj

async def department_delete(db: AsyncSession, dept_obj: Department):
    await db.delete(dept_obj)
    await db.flush()
```

## 十一、service/service_department.py（重点！事务规范版本）
```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.department import Department
from app.models.employee import Employee
from app.schemas.department import DepartmentCreate
from app.crud.crud_department import department_get_by_name, department_create
from app.common.exceptions import BusinessException

async def service_department_create(db: AsyncSession, dept_in: DepartmentCreate) -> Department:
    """
    ✅ 校验 + 创建放在同一个事务内，防止并发重复插入
    适合有唯一键校验场景（部门名称唯一）
    """
    async with db.begin():
        # 事务内校验，锁住判断-新增流程
        existing = await department_get_by_name(db, dept_in.name)
        if existing:
            raise BusinessException(f"部门 '{dept_in.name}' 已存在，请勿重复创建！")

        dept_data = dept_in.model_dump(exclude={"employees"})
        dept_obj = Department(**dept_data)

        if dept_in.employees:
            dept_obj.employees = [
                Employee(name=emp.name, role=emp.role)
                for emp in dept_in.employees
            ]
        return await department_create(db, dept_obj)
```
> 两种事务方案取舍
> 1. 上面版本：校验+新增在同一个事务，防并发重复，**推荐唯一字段场景**；事务时间略长
> 2. 校验放外面，事务只做新增：速度更快，但有极小概率并发冲突，需要数据库唯一兜底索引

## 十二、api/v1/router_department.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.department import DepartmentCreate, DepartmentResponse
from app.service.service_department import service_department_create

router = APIRouter(tags=["部门管理"])

@router.post("/departments", response_model=DepartmentResponse)
async def create_department(
    dept_in: DepartmentCreate,
    db: AsyncSession = Depends(get_db)
):
    return await service_department_create(db, dept_in)
```

## 十三、api/v1/api_router.py
```python
from fastapi import APIRouter
from app.api.v1.router_department import router as dept_router
from app.api.v1.router_employee import router as emp_router

api_router = APIRouter()
api_router.include_router(dept_router)
api_router.include_router(emp_router)
```

## ✅ 重点踩坑清单
1. **MissingGreenlet**
   异步session对象不能跨协程、不能在session关闭后访问关系字段；不要把ORM对象传到session外面去用，返回前端优先转Pydantic Schema。
2. **循环导入**
   Model层：`from __future__ import annotations` + 字符串前向引用；
   Schema层优先拆简单Simple模型解耦，不建议大量字符串注解。
3. **JSON尾逗号报错 `Illegal trailing comma before end of object`**
   请求体json最后一个key后面不能加逗号，docs调试经常踩。
4. **建表说明**
   - 本地第一次跑：打开lifespan里面`create_all`
   - 第二次、测试、生产：**注释掉！**，改用Alembic做迁移脚本
5. **commit / flush**
   - flush：刷到数据库、拿到自增ID，不提交事务，外层`async with db.begin()`自动commit/rollback
   - begin()上下文：正常退出自动commit，抛出异常自动rollback
6. 分层职责
   - Router：接收参数、返回响应、注入db会话
   - Service：业务校验、业务规则、事务控制
   - CRUD：纯数据库读写，**不写业务判断**
   - Schema：Pydantic参数校验、序列化
   - Model：数据库表映射

## ✅ 版本管理补充（Node/NPM）
Windows 推荐 nvm-windows 管理node版本，可以任意切换多个node版本
```bash
# 查看可安装版本
nvm list available
# 安装指定LTS
nvm install 20.17.0
# 切换版本
nvm use 20.17.0
# 查看当前
nvm current
# 更新npm
npm install -g npm
```

---

你可以直接全选复制上面内容，保存为 `fastapi_async_notes.md`。
要不要我再单独追加一份 **Alembic迁移完整配置** 追加到这个md末尾？
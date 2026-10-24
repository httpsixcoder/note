# FastAPI_SQLAlchemy大厂项目避坑与最佳实践笔记（合并完整版）

> 
> 整合三份文档，以我最初版本为基准，吸收两份补充文档全部新增知识点、报错案例、面试要点、代码模板、工程规范，结构重排统一，消除重复冲突，补充交叉知识点，全文Markdown，适合复习、备查、面试背诵，总字数超1.6w。
> 版本说明：
> 基准：第一轮给你的大厂避坑笔记
> 增补素材1：文档1（同步模型层原理、PyCharm IDE排错、scalar/scalars区分、**init**.py规范、外键参数、循环导入TYPE_CHECKING方案）
> 增补素材2：文档2（异步架构、Alembic迁移、MissingGreenlet深度复盘、422、事务流派对比、RESTful规范、update局部更新逻辑、BusinessException全局异常、可变默认值坑、连接池参数、lifespan废弃on_event说明）

---

## 📌 序言

这份笔记完整记录我们从零搭建**FastAPI + SQLAlchemy 2.0 异步项目**全过程，不是简单代码demo，是实战踩坑实录、排错流程、大厂标准架构、分层职责、事务控制、ORM关系映射、Pydantic校验、IDE调试、上线规范、面试八股合集。
适用场景：

1. 后续新项目直接复制架构、模板、配置
2. 线上报错快速检索定位根因
3. 面试后端岗位，背诵FastAPI+异步SQLAlchemy相关问题
4. 毕业设计、后端业务开发自查清单

核心技术栈清单：

- FastAPI（ASGI异步框架，依赖注入、自动OpenAPI文档、Pydantic深度集成）
- SQLAlchemy 2.0（异步模式 asyncmy + AsyncSession，Mapped声明式注解、select语法、relationship关系映射）
- Pydantic v2（数据校验、DTO分层、序列化/反序列化、from_attributes）
- Alembic（数据库版本迁移，生产环境禁用create_all自动建表）
- uvicorn ASGI服务、PyCharm开发环境
- 分层架构：Router（api）→ Service（业务）→ CRUD（DAO）→ Model（ORM）→ DB会话层

> 
> 核心架构铁律：单向依赖，禁止反向导入，API→Service→CRUD→Model，杜绝循环导入。

---

# 第一章 大厂标准目录结构 & 分层职责详解

## 1.1 最终推荐目录（异步版本，企业通用）

```
my_fastapi_project/
├── .venv/                      # 虚拟环境，.gitignore必须忽略
├── .gitignore                  # 忽略venv、.env、缓存、日志
├── .env                        # 环境变量：数据库url、密钥、DEBUG开关，禁止提交git
├── requirements.txt            # 锁定依赖版本，生产环境统一安装
├── README.md                   # 项目说明、启动命令、接口文档地址
├── alembic/                    # 数据库迁移目录，Alembic生成（生产必用）
├── main.py                     # 项目入口：lifespan、app实例、全局异常、挂载路由
└── app/
    ├── __init__.py
    ├── core/                   # 核心基建层【几乎很少改动】
    │   ├── __init__.py
    │   ├── config.py           # pydantic-settings读取.env环境变量
    │   ├── database.py         # async引擎、async_sessionmaker、get_db依赖
    │   ├── base.py             # ✅ 全局唯一 Base = DeclarativeBase，所有model继承它
    │   ├── security.py         # JWT、bcrypt密码加密、token校验依赖
    │   └── exceptions.py       # 自定义业务异常BusinessException、全局异常handler
    ├── models/                 # ORM模型层：一对一/一对多/外键、relationship
    │   ├── __init__.py
    │   ├── department.py
    │   └── employee.py
    ├── schemas/                # Pydantic校验层（DTO）：Base / Create / Update / Response
    │   ├── __init__.py
    │   ├── department_schema.py
    │   └── employee_schema.py
    ├── crud/                   # DAO数据访问层：纯数据库操作，无业务判断、无事务commit
    │   ├── __init__.py
    │   ├── department_crud.py
    │   └── employee_crud.py
    ├── services/               # Service业务编排层：业务校验、事务边界、组装ORM对象
    │   ├── __init__.py
    │   ├── department_service.py
    │   └── employee_service.py
    └── api/
        ├── __init__.py         # 聚合路由，导入v1路由，统一导出api_router
        ├── deps.py             # 路由公共依赖：权限、登录用户解析
        └── v1/                 # 接口版本管理，方便后续v2迭代，不破坏旧接口
            ├── __init__.py
            ├── departments.py
            └── employees.py
```

## 1.2 每一层职责、能干什么、绝对不能干什么（面试高频）

| 分层 | 职责 | ✅允许 | ❌禁止 |
| --- | --- | --- | --- |
| api/router | 接收http请求、参数解析、返回response、http状态码控制 | Depends注入db、权限依赖；调用service；返回schema响应 | 写sql、写业务校验、直接db.add/commit |
| service | 业务逻辑编排、业务规则校验、事务边界控制、组装ORM对象 | 调用crud、抛出BusinessException、控制事务范围 | 直接写select语句、底层db操作、http返回 |
| crud | 纯粹数据访问层DAO，封装sqlalchemy语句 | select、add、flush、delete；返回ORM对象/序列 | 业务判断（查重、权限）、commit、抛业务异常 |
| models | 映射数据库表结构、字段类型、外键、relationship关联关系 | Mapped字段、索引、唯一约束、级联规则 | 业务逻辑、校验、查询逻辑 |
| schemas | 入参校验、出参序列化、嵌套结构 | 字段长度、必填、描述、默认值、嵌套DTO | 数据库映射、写sql、业务逻辑 |
| core | 全局配置、数据库连接池、安全工具、基础异常 | 引擎初始化、会话工厂、jwt工具 | 业务代码、接口路由 |

> 
> 分层好处：解耦、单元测试友好、数据库迁移切换成本低、多人协作互不干扰；如果未来MySQL换成PostgreSQL，只改core/database.py、少量model字段类型，业务代码几乎不动。

## 1.3 补充：同步版本目录区别

同步项目用`sessionmaker`、`Session`，驱动`pymysql`；异步是`async_sessionmaker`、`AsyncSession`、`asyncmy`，新项目优先异步，高并发场景优势明显。

## 1.4 目录工程规范坑

1. PyCharm一定要把项目根目录（包含main.py）**Mark Directory as -> Sources Root**，解决`ModuleNotFoundError`、IDE红波浪线、导入找不到模块。
2. `__init__.py` **不要用来批量中转导出业务函数**（`from .xx import *`、批量import导出），极易引发循环导入、IDE跳转失效。需要哪个文件直接精准导入。
3. `.env`、数据库密码、密钥严禁提交git，必须加入`.gitignore`。

---

# 第二章 数据库基建：database.py、Base、session、lifespan生命周期

## 2.1 base.py：全局唯一DeclarativeBase（高频踩坑点）

> 
> 致命坑：项目里不能定义多个`class Base(DeclarativeBase)`，每个Base独立metadata，A的metadata注册模型，B的metadata执行create_all找不到表，建表失败！

```
# app/core/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """全局ORM基类，所有模型统一继承这个Base"""
    pass
```

所有model第一行：`class Department(Base):`

## 2.2 database.py 异步引擎、连接池、AsyncSessionLocal、get_db依赖（生产标准模板）

```
# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # 开发=True打印SQL，生产环境False，防止日志泄露、性能损耗
    pool_size=10,         # 常驻连接数
    max_overflow=20,      # 峰值额外临时连接
    pool_recycle=3600,    # 1小时主动回收，规避MySQL 8小时自动断开连接报错
    pool_pre_ping=True,   # 取出连接前ping数据库，剔除失效连接
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # 超级重要！commit之后，ORM对象不会过期，防止异步场景MissingGreenlet
    autoflush=False,
    autocommit=False
)

# FastAPI依赖注入，每个请求独立session
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### 参数详解

1. `expire_on_commit=False`：默认True，commit后对象标记过期，再次访问关联字段会触发懒加载查询，异步环境直接MissingGreenlet，**异步项目强制写False**
2. `autoflush=False`：关闭自动flush，防止未提交数据意外刷入数据库，控制权交给开发者，避免莫名其妙的唯一索引冲突
3. `autocommit=False`：强制手动控制提交，不自动事务，数据安全
4. `pool_pre_ping + pool_recycle` 解决经典报错：`MySQL server has gone away`

## 2.3 lifespan 生命周期（替换废弃的 @app.on_event）

> 
> 旧写法`@app.on_event("startup")`、`@app.on_event("shutdown")`官方已经废弃，新项目统一使用`asynccontextmanager`的lifespan

```
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import engine
from app.core.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ========= 启动阶段 =========
    # ⚠️ 警告：create_all仅本地开发测试使用！生产环境必须删除，使用alembic迁移
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # ========= 关闭阶段 =========
    await engine.dispose() # 释放连接池，关闭数据库连接
app = FastAPI(title="企业级FastAPI异步项目", lifespan=lifespan)
```

> 
> 实操建议：
> 第一次本地跑：保留`create_all`自动建表；
> 表结构稳定之后、准备上线前：注释掉`create_all`，全部交给Alembic管理版本；后续新增字段、修改字段全部生成迁移脚本。
> create_all只能新建不存在的表，**不能修改已有表结构**，新增字段之后执行create_all不会同步，只会报字段不存在。

## 2.4 异步驱动安装

```
pip install sqlalchemy[asyncio] asyncmy
```

连接串格式（mysql异步）：
`mysql+asyncmy://账号:密码@ip:端口/库名`

---

# 第三章 SQLAlchemy 2.0 ORM模型层（models）深度讲解、踩坑大全

## 3.1 现代Mapped + mapped_column语法（替代1.x Column）

```
from __future__ import annotations
from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.base import Base

class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), index=True, unique=True)
    desc: Mapped[str | None] = mapped_column(String(200))

    employees: Mapped[List["Employee"]] = relationship(
        back_populates="department",
        lazy="selectin",
        cascade="all, delete-orphan" # 删除部门，级联删除下属员工，谨慎使用
    )

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    role: Mapped[str] = mapped_column(String(50))
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    department: Mapped["Department"] = relationship(
        back_populates="employees",
        lazy="joined"
    )
```

### 语法说明

1. `Mapped[str]`：非空字段，自动NOT NULL；`Mapped[str | None]`允许NULL，**不需要手写nullable=False**
2. `from __future__ import annotations`：文件头部必加，所有类型注解当做字符串处理，解决前向引用、循环导入
3. `back_populates`双向绑定，两边名字严格对应，写错直接关联失效
4. 外键ondelete/onupdate合法取值：`CASCADE` / `SET NULL` / `RESTRICT` / `NO ACTION`，**不能自己写Replace等非法值，直接CompileError**> 
> 坑：ondelete必须写在ForeignKey()内部，不能写在mapped_column参数里，否则TypeError

## 3.2 Lazy加载策略（异步项目重中之重，MissingGreenlet根源）

- `lazy="select"`：默认，懒加载。访问关联属性才单独发SQL，异步项目禁用！极易MissingGreenlet、N+1查询
- `lazy="joined"`：LEFT JOIN一次性加载关联数据，适合【多对一】（员工查所属部门）
- `lazy="selectin"`：IN子查询批量加载，适合【一对多】（部门查员工列表），解决N+1，异步首选
- `lazy="dynamic"`：返回可继续拼接的查询对象，适合超大数量关联数据，分页场景

> 
> 异步黄金规则：**异步环境禁止依赖隐式懒加载**，要么模型设置正确lazy，要么查询时options(selectinload())主动预加载

## 3.3 循环导入两种标准解决方案（模型互相引用）

方案1：`from __future__ import annotations` + 字符串前向引用（简单场景首选，你当前项目在用）

```
# employee.py
from __future__ import annotations
department: Mapped["Department"] = relationship(back_populates="employees")
```

方案2：`TYPE_CHECKING`（大厂更推荐，IDE识别更好，运行时完全不导入）

```
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.department import Department

class Employee(Base):
    department: Mapped[Department] = relationship(back_populates="employees")
```

> 
> TYPE_CHECKING只在类型检查、PyCharm索引时生效，Python运行时if分支不会执行import，彻底规避循环导入

## 3.4 N+1查询问题复盘

举例：10个部门，每个部门10员工
lazy=select：1次查部门 + 10次循环查员工，11条SQL，N+1
lazy=selectin：1次查部门，1次IN批量查全部员工，总共2条SQL，性能提升巨大

## 3.5 补充：多对多带附加字段（高级）

普通secondary中间表适合单纯多对多；中间表有额外业务字段（成绩、时间），不能用secondary，要用Association Object关联对象，搭配association_proxy。本项目暂时用不到，后续扩展查阅。

---

# 第四章 Pydantic v2 Schemas DTO分层规范、422报错全套避坑

## 4.1 分层范式 Base / Create / Update / Response（固定套路）

- Base：存放新增、返回都需要的公共字段，消除重复代码
- Create：POST新增接口入参，不含id（id数据库自增），校验必填
- Update：PUT/PATCH修改接口入参，全部字段可选，支持局部更新，搭配`exclude_unset=True`
- Response：返回给前端的模型，包含id、外键等后端生成字段，开启`model_config = ConfigDict(from_attributes=True)`，支持ORM对象直接转schema

```
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.employee_schema import EmployeeCreate

# ========== Department ==========
class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="部门名称，唯一")
    desc: Optional[str] = Field(None, max_length=200, description="部门描述")

class DepartmentCreate(DepartmentBase):
    # ❌ 禁止 employees: List[EmployeeCreate] = []
    employees: List[EmployeeCreate] = Field(default_factory=list, description="可选嵌套员工")

class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    desc: Optional[str] = None

class DepartmentResponse(DepartmentBase):
    id: int
    employees: Optional[List["EmployeeResponse"]] = None
    model_config = ConfigDict(from_attributes=True)
```

## 4.2 Field三个高频写法区别（你之前重点问的）

1. `Field(...)`：`...`代表必填，不允许不传，缺失直接422
2. `Field(None)`：可选字段，不传默认值是None
3. `Field(default_factory=list)`：可变对象（list/dict）专用！> 
> 致命大坑：**绝对不要直接写employees: List = []**
> Python类定义时，[]只会创建一次，所有请求共享同一个列表实例，并发场景数据错乱、串数据，可变默认值必须default_factory。

## 4.3 422 Unprocessable Content 报错完整排查手册

422本质：**请求体不符合Pydantic校验规则，请求还没进入service层**
看报错返回的`loc`数组，精准定位错误字段：

- loc:["name"]：name字段缺失、长度不满足min_length、类型不对
- loc:["employees",0,"role"]：嵌套数组里面第一个员工的role字段异常
- JSON语法错误：`Illegal trailing comma before end of object` → json末尾多了逗号，前端传参写错，JSON不允许尾逗号

422常见根因清单：

1. 缺少必填字段、传空字符串，min_length限制不满足
2. 字段类型不匹配（数字传字符串）
3. 嵌套结构的子schema校验失败
4. 请求json存在语法错误（尾逗号、引号错误）
5. 忘记from_attributes=True，返回ORM对象序列化失败（部分版本也报422）

## 4.4 Update局部更新经典写法（只更新前端传入的字段，不覆盖原有数据）

```
# service更新逻辑
update_data = dept_in.model_dump(exclude_unset=True)
for k, v in update_data.items():
    setattr(dept_obj, k, v)
```

`exclude_unset=True`：只拿到前端本次**实际传过来**的字段，没传的字段不进入字典，不会把原有数据覆盖成None。

## 4.5 嵌套转换坑：不能直接把Pydantic对象丢给ORM relationship

错误写法：

```
# dept_in是DepartmentCreate，model_dump之后是dict，直接赋值会报错
dept_obj.employees = dept_in.employees
```

正确写法：循环手动实例化ORM模型

```
if dept_in.employees:
    dept_obj.employees = [
        Employee(name=emp.name, role=emp.role)
        for emp in dept_in.employees
    ]
```

报错：`'dict' object has no attribute '_sa_instance_state'`，就是这个原因！ORM的relationship接收的是ORM实例，不是pydantic字典。

---

# 第五章 CRUD层规范、查询语法、scalar/scalars、first/one_or_none/all

> 
> 核心原则：CRUD只做数据访问，**不写业务判断、不commit**，flush拿id，commit交给外层（get_db统一提交 / service显式事务）

## 5.1 SQLAlchemy2.0 必须用select()，废弃旧query()写法

```
# ✅ 新标准
from sqlalchemy import select
stmt = select(Department).where(Department.name == name)
# ❌ 旧版本写法，2.0不推荐：db.query(Department).filter(...)
```

## 5.2 scalar / scalars 区分（极易混淆）

- `db.scalar(stmt)`：取第一行第一列，适合count、查单列；查到多条会静默丢弃多余数据，ORM实体查询慎用，风险极高
- `db.scalars(stmt)`：返回ScalarResult，取出全部ORM实体对象，查表实体首选

## 5.3 .first() / .one_or_none() / .all()

| 方法 | 返回值 | 行为 | 适用场景 |
| --- | --- | --- | --- |
| .all() | Sequence[Model] | 永远返回序列，无数据返回空列表，不抛异常 | 批量查询、列表接口 |
| .first() | Model | 拿到第一条，多余数据静默丢弃，无数据返回None | 已知有多条，只要第一条（谨慎使用） |
| .one_or_none() | Model | 0条返回None，≥2条直接抛异常 | 根据唯一键/主键查询，数据必须唯一（查重、查主键，大厂推荐） |

> 
> 面试重点：主键/唯一索引查询优先one_or_none，发现多条直接抛异常，提前发现脏数据，而不是first静默掩盖问题。

## 5.4 db.get() 主键快捷查询

`await db.get(Department, dept_id)`，专门按主键查询，底层优先走identity map缓存，性能优于select查询，简洁。

## 5.5 CRUD模板示例

```
# crud/department_crud.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.department import Department

async def department_get_by_id(db: AsyncSession, dept_id: int) -> Department | None:
    return await db.get(Department, dept_id)

async def department_get_by_name(db: AsyncSession, name: str) -> Department | None:
    stmt = select(Department).where(Department.name == name)
    result = await db.execute(stmt)
    return result.scalars().one_or_none()

async def department_create(db: AsyncSession, dept_obj: Department) -> Department:
    db.add(dept_obj)
    await db.flush() # 发送sql，回填自增id，不commit
    return dept_obj

async def department_delete(db: AsyncSession, dept_obj: Department):
    await db.delete(dept_obj)
    # 不commit，交给外层统一提交
```

> 
> crud里只用flush，不commit！

---

# 第六章 Service业务层、事务两大流派、事务冲突报错深度解析

> 
> 这是我们讨论最多、踩坑最多的地方：`A transaction is already begun on this Session.`

## 6.1 两大主流事务流派（大厂两种方案，没有绝对好坏，按需选择）

### 流派一：get_db依赖自动管理（95%业务接口首选，推荐你当前项目）

get_db代码：yield之后自动commit，异常自动rollback

- service层不需要写`async with db.begin():`
- 所有查询、组装、crud.add都在同一个session，请求结束统一提交
- 优点：代码简洁，不容易事务嵌套冲突，绝大多数CRUD业务够用
- 缺点：无法在一个接口内拆分成多段独立事务（一个接口需要多次独立提交场景不适合）

```
# service示例（流派一）
async def service_department_create(db: AsyncSession, dept_in: DepartmentCreate) -> Department:
    # 业务前置校验
    existing = await department_crud.department_get_by_name(db, dept_in.name)
    if existing:
        raise BusinessException(f"部门 {dept_in.name} 已存在")
    
    dept_data = dept_in.model_dump(exclude={"employees"})
    dept_obj = Department(**dept_data)
    if dept_in.employees:
        dept_obj.employees = [
            Employee(name=e.name, role=e.role) for e in dept_in.employees
        ]
    await department_crud.department_create(db, dept_obj)

    # 预加载关联员工，防止MissingGreenlet
    stmt = select(Department).options(selectinload(Department.employees)).where(Department.id == dept_obj.id)
    res = await db.execute(stmt)
    return res.scalars().first()
```

### 流派二：service内部显式`async with db.begin():`手动事务

适用场景：复杂业务、需要原子操作、跨多表强一致性；
⚠️ 致命限制：**begin块里面的所有查询、新增必须全部写在with内部**

> 
> 报错根因：如果begin()之前先执行了一次await查询，sqlalchemy自动开启隐式事务，再写async with db.begin()，直接抛出：
> `InvalidRequestError: A transaction is already begun on this Session.`

错误示范（你之前踩的坑）：

```
# ❌ 错误：校验查询在begin外面，提前开启隐式事务
existing = await crud.get_by_name(db, name)
async with db.begin():
    ...
```

正确写法（流派二）：全部逻辑放进begin内部

```
async def service_department_create(db: AsyncSession, dept_in: DepartmentCreate) -> Department:
    async with db.begin():
        existing = await department_crud.department_get_by_name(db, dept_in.name)
        if existing:
            raise BusinessException(f"部门 {dept_in.name} 已存在")
        dept_data = dept_in.model_dump(exclude={"employees"})
        dept_obj = Department(**dept_data)
        if dept_in.employees:
            dept_obj.employees = [Employee(name=e.name, role=e.role) for e in dept_in.employees]
        await department_crud.department_create(db, dept_obj)
        stmt = select(Department).options(selectinload(Department.employees)).where(Department.id == dept_obj.id)
        res = await db.execute(stmt)
        return res.scalars().first()
```

> 
> 补充大厂优化思路：唯一性校验放事务内 + 数据库加unique唯一索引兜底！
> 校验在事务内防止并发同时请求绕过业务校验（竞态条件，超并发下重复插入），唯一索引是最后一道防线。

## 6.2 事务核心概念区分

- flush：把sql发送到数据库缓冲，拿到自增id，但是没有提交，其他会话看不到数据，可rollback
- commit：提交事务，持久化数据，其他会话可见
- rollback：回滚当前事务，撤销所有未提交修改

---

# 第七章 Router路由层、RESTful规范、全局异常拦截

## 7.1 RESTful规范（面试高频）

URL只用名词，动作交给HTTP Method
✅ 标准写法

- GET /api/v1/departments  查询部门列表
- GET /api/v1/departments/{id} 查询单个部门
- POST /api/v1/departments 新增部门（201 Created）
- PUT /api/v1/departments/{id} 修改部门
- DELETE /api/v1/departments/{id} 删除部门（204 No Content，无返回体）
❌ 禁止：/departments/create /departments/delete/1

> 
> 路由顺序坑：带路径参数`/{dept_id}`的路由，必须放在固定路由（如/name）后面，否则会拦截固定路由。

## 7.2 路由模板

```
# api/v1/departments.py
from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.schemas.department_schema import DepartmentCreate, DepartmentResponse
from app.services.department_service import service_department_create
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/departments", tags=["部门管理"])

@router.post("/", response_model=DepartmentResponse, status_code=201)
async def create_department(
    dept_in: DepartmentCreate,
    db: AsyncSession = Depends(get_db)
):
    return await service_department_create(db, dept_in)
```

## 7.3 全局自定义异常BusinessException + 拦截器

> 
> 目的：统一返回前端可识别的json格式，不要返回原生堆栈给前端

```
# app/core/exceptions.py
from fastapi import Request
from fastapi.responses import JSONResponse

class BusinessException(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code

async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=exc.code,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": None
        }
    )
```

main.py注册：

```
from app.core.exceptions import BusinessException, business_exception_handler
app.add_exception_handler(BusinessException, business_exception_handler)
```

业务层抛异常：`raise BusinessException("部门名称重复")`

---

# 第八章 终极大坑：MissingGreenlet 完整复盘、根因、全套解法

> 
> 你踩过的最难排查报错：`MissingGreenlet: greenlet_spawn has not been called`

## 根因一句话

AsyncSession是绑定在greenlet协程上下文的，当ORM对象离开原有session上下文之后，访问未提前加载的relationship关联字段，尝试懒加载，异步环境没有greenlet，直接报错。
触发场景：

1. expire_on_commit=True，commit之后对象过期，返回给路由序列化时访问关联字段
2. 查询没有预加载关联字段，schema里面又需要返回关联嵌套数据
3. session已经关闭，还在使用ORM对象

## 四层解决方案（优先级从高到低）

1. database设置`expire_on_commit=False`（基础兜底，必加）
2. model的relationship设置正确lazy策略（一对多selectin，多对一joined）
3. 查询时显式预加载：`options(selectinload(Department.employees))`（最稳妥，生产首选）

```
stmt = select(Department).options(selectinload(Department.employees)).where(Department.id == dept_id)
```

4. 不要把session关闭后的ORM对象传递出去，尽量在同一个session内完成查询+序列化需要的所有关联加载

> 
> 排错口诀：只要返回嵌套关联schema，查询必须带上selectinload预加载！

---

# 第九章 全量报错汇总速查表（直接检索排查）

| 报错信息 | 根因 | 解决方案 |
| --- | --- | --- |
| `ImportError: cannot import name 'X' from partially initialized module` | 循环导入A导入B、B导入A | from **future** + 字符串注解 / TYPE_CHECKING |
| `ModuleNotFoundError: No module named 'app'` | 源码根目录未标记，sys.path不对 | PyCharm Mark Sources Root，使用绝对导入 |
| `A transaction is already begun on this Session` | 查询提前触发隐式事务，外层又写async with db.begin() | 全部逻辑放进begin内部；或者改用get_db自动事务 |
| `MissingGreenlet` | 关联字段懒加载、commit后对象过期、session销毁后访问关系 | expire_on_commit=False + selectinload预加载 |
| `Illegal trailing comma before end of object` | JSON末尾多余逗号 | 前端删除json尾逗号 |
| 422 Unprocessable Content | Pydantic校验失败 | 看loc字段，核对字段类型、必填、长度、嵌套 |
| `MySQL server has gone away` | 连接长时间空闲被MySQL断开 | pool_recycle + pool_pre_ping |
| `Unknown database xxx` | MySQL库不存在 | 手动创建数据库，create_all不会自动建库 |
| `Unknown column 'xxx' in 'field list'` | 代码新增字段，数据库表没有更新 | 开发删表重建；生产alembic迁移 |
| `'dict' object has no attribute '_sa_instance_state'` | 直接把pydantic字典赋值给relationship | 循环实例化ORM模型 |
| `CompileError: Unexpected SQL phrase: 'Replace'` | ForeignKey ondelete参数写错 | 改为CASCADE/SET NULL/RESTRICT |
| `IntegrityError Duplicate entry` | 唯一索引重复插入 | service层前置查重 + 数据库unique索引兜底 |
| `AttributeError: 'NoneType' object has no attribute xxx` | 查询返回None，直接取属性 | 判断if obj is None，抛404/BusinessException |

---

# 第十章 工程规范、Alembic迁移、Git、依赖管理

## 10.1 Alembic（生产环境强制）

create_all只适合本地快速开发；上线、迭代表结构必须alembic

- 初始化：`alembic init alembic`
- 修改env.py，导入我们的Base，target_metadata = Base.metadata
- 生成迁移脚本：`alembic revision --autogenerate -m "add employee role"`
- 执行升级：`alembic upgrade head`

> 
> 禁止线上代码依靠lifespan里面create_all自动建表！

## 10.2 requirements.txt

锁定版本，示例：

```
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
sqlalchemy>=2.0.30
asyncmy>=0.2.9
pydantic-settings>=2.0.0
pydantic>=2.0.0
alembic>=1.12.0
bcrypt
python-jose[cryptography]
```

## 10.3 Git规范

.gitignore至少包含：

```
.venv/
.env
__pycache__/
*.pyc
alembic/versions/*.pyc
logs/
```

提交规范Conventional Commits

- feat: 新增功能
- fix: 修复bug（事务、MissingGreenlet、422等）
- refactor: 重构代码，无功能变更
- docs: 更新文档注释
- chore: 依赖、配置调整

## 10.4 PyCharm开发避坑

1. 信任项目目录，加速索引
2. 导入报错红波浪线优先检查Sources Root
3. 自动生成__init__参数：Alt+Insert → Constructor
4. 调试时print ORM对象看不到内容：在model增加__repr__

```
def __repr__(self):
    return f"<Department id={self.id}, name={self.name}>"
```

---

# 第十一章 面试背诵清单（高频问答）

1. 问：FastAPI异步SQLAlchemy为什么设置expire_on_commit=False？
答：默认True，commit后ORM对象过期，访问关联字段触发懒加载，异步环境直接MissingGreenlet；关闭之后commit后对象属性保留，适合接口返回序列化。
2. 问：selectin和joined区别，什么时候用？
答：joined是left join，多对一；selectin是in子查询，一对多，解决N+1。
3. 问：为什么不能直接在pydantic写List = []？
答：可变默认参数，类定义时只实例化一次，所有请求共享同一个list，并发错乱，必须default_factory。
4. 问：service、crud职责怎么划分？
答：crud只封装数据库语句，flush拿id，不做业务校验、不commit；service做业务校验、组装对象、事务编排。
5. 问：怎么防止并发场景重复插入同名部门？
答：service事务内查重 + 数据库字段unique唯一索引双重兜底。
6. 问：create_all和alembic区别？
答：create_all只能新建不存在的表，不能变更表结构，仅本地开发；alembic管理版本迁移，生产环境标准方案。
7. 问：async with db.begin()报错事务已开启是什么原因？
答：begin之前执行查询触发隐式事务，查询必须放进begin代码块内部。

---

# 第十二章 新项目自检清单（新建项目逐项打勾）

- 目录结构按照标准分层，core/base.py全局唯一Base
- database引擎配置pool_pre_ping、pool_recycle、expire_on_commit=False
- 全部model头部加`from __future__ import annotations`
- relationship back_populates双向对应、lazy策略选对
- schema分层Base/Create/Update/Response，可变列表default_factory
- 嵌套ORM关系手动循环实例化，不直接传dict
- 事务方案选定，统一风格，不要混用两种事务写法
- 返回嵌套关联数据，查询增加selectinload预加载
- 全局BusinessException异常拦截器注册完成
- 上线前注释lifespan中的create_all，接入Alembic
- .env、密码、venv加入gitignore

---

# 后记

这份笔记整合了你从0搭建项目所有踩坑，从目录、基建、ORM、校验、事务、报错、面试全部覆盖。以后新项目，直接复制这套架构，遇到报错优先检索第九章报错速查表。

> 
> 后续扩展方向：权限RBAC、分页封装、统一分页Response Schema、redis缓存、单元测试pytest。

如果你需要，我可以再单独抽一份【极简可直接复制的整套代码包】（main + database + base + model + schema + crud + service + router + exception），直接新建项目粘贴运行。
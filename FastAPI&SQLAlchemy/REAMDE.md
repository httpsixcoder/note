# 🚀 FastAPI & SQLAlchemy 核心学习笔记

> 📢 **学习声明**：本笔记的知识体系与案例源于尚硅谷 (Atguigu) 课程。重点提炼了 Web 异步编程、FastAPI 路由机制以及 SQLAlchemy ORM 的核心操作与避坑指南。

---

## 第一部分：协程与 ASGI 基础（FastAPI 的地基）

FastAPI 之所以“快”，是因为它完全基于异步编程（协程）和 ASGI 规范。

### 1. 线程 vs 协程
*   **线程**：由操作系统调度，切换开销大。遇到 I/O 阻塞时，整个线程挂起。
*   **协程**：由程序自身（Event Loop）调度，切换开销极小（函数调用级别）。遇到 I/O 时通过 `await` 主动让出 CPU，去执行其他任务。
*   **⚠️ 核心大坑（阻塞 I/O）**：**绝对不要在 `async def` 函数中使用同步阻塞代码**（如 `time.sleep()`、`requests.get()`）。这会卡死整个事件循环，导致并发彻底失效！必须使用 `asyncio.sleep()`、`aiohttp` 等异步库。

### 2. 协程的并发执行
*   只定义 `async def` 不会自动并发，必须将其包装成 `Task` 或使用 `asyncio.gather()` 统一调度。
*   `asyncio.create_task()`：立即将协程扔进**事件循环**后台跑。
*   `await asyncio.gather(*tasks)`：等待所有并发任务完成，收集结果。
*   使用async def关键字定义的函数就是协程函数，它返回一个协程对象。
*   就绪 -> 挂起 -> 就绪

### 3. WSGI 与 ASGI
*   **WSGI**（旧规范）：同步阻塞，如 Flask、Django 早期版本，配 Gunicorn。
*   **ASGI**（新规范）：支持异步，如 FastAPI，配 **Uvicorn**。

### 4.线程、进程和协程的对比⭐

| **机制** | **调度者**                      | **切换开销**     | **资源共享**        | **适用场景**          | **核心优势**          | **局限性**                                |
| -------- | ------------------------------- | ---------------- | ------------------- | --------------------- | --------------------- | ----------------------------------------- |
| 进程     | 操作系统                        | 极大(内核级)     | 完全隔离            | CPU密集型             | 利用多核              | 资源消耗大，数量有限。                    |
| 线程     | 操作系统                        | 较大(内核级)     | 共享内存 (需加锁)   | I/O 密集型 (低并发)   | 共享地址空间          | 受GIL限制，且数量过多时调度和同步开销大。 |
| 协程     | 程序自身 Event Loop【事件循环】 | 极小(函数调用级) | 共享内存 (无需加锁) | I/O 密集型 (极高并发) | 极高并发，高性能I/O。 | 需要与其配套的异步库或者线程池处理阻塞    |

### 5.常用方法：

async.create_task()：   # 将写成对象创建成为事件循环中的一个任务
asyncio.gether(task1,task2,...)：# 异步执行多个任务
asyncio.run()：# 启动协程

注册为任务:

​	a-> asyncio.create_task(fun())
​	b-> asyncio.gather(fun(),fun(),):隐式将协程对象注册为任务

一般执行协程函数时，都需要设置一个入口函数（顶级协程对象），统一管理其他协程函数的执行,若执行协程函数时，入口函数（顶级协程对象）提前退出，则整个事件循环结束

```python
import asyncio
import time
from unittest import result
# 创建协程函数
async def run(name, delay):
    print(f"任务{name}开始")
    await asyncio.sleep(delay)
    print(f"任务{name}完成")
    return f"任务{name}结果"

# 程序的入口函数（顶级协程对象）
async def main():
    result=await asyncio.gather(run("A",1),run("B",2))
    print(result)
if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"耗时{end_time - start_time:.2f}s")# 耗时2.01s
```



---

## 第二部分：FastAPI 核心操作

### 1. 同步 (def) vs 异步 (async def) 函数
*   **`async def`**：遇到 `await` 会切换。**只有内部调用的是异步库（如异步数据库、aiohttp）时，才用这个。**
*   **`def`**：普通同步函数。FastAPI 会**自动把它扔进线程池**执行，避免阻塞主事件循环。如果内部是纯 CPU 计算，或用的是同步库（如旧版 PyMySQL），用 `def` 即可。
*   **总结**：涉及 I/O 优先异步；纯计算或无异步库时用 `def`。
*   json是javascript中的数据类型，包括两种格式：对象和数组

### 2. 路径参数与查询参数
*   **路径参数**：定义在 URL 路径中，如 `@app.get("/items/{item_id}")`。传入的字符串会自动根据 Python 类型提示（如 `item_id: int`）进行转换和校验。如果传个 `"foo"` 进来，FastAPI 会自动返回 422 校验错误。

```python
@app.get("/param/path/{username}/{password}/{age}")
	def test_param_path(username:str,password:str,age:int):
		return {"username":username,"password":password,"age":age}
```

*   **查询参数**：URL 中 `?` 后面的键值对，如 `?q=xxx&limit=10`。不在路径中声明的参数，默认就是查询参数。可以设默认值使其变成可选参数。

```python
@app.get("/param/query")，路径中？前面是路径，后面是参数
	def test_param_query(name: str, age: str):
		return {"name=": name, "age": age}
```

**注意：查询参数中，默认情况下，每个查询参数都必须传输，也可以设置参数可选，对应的形参设置默认值。**

*   **⚠️ 路由顺序坑**：FastAPI 按代码顺序匹配路由。必须把写死的路径放在前面！例如：`/users/me` **必须**写在 `/users/{user_id}` 之前，否则 `me` 会被当成 `user_id` 匹配掉。

### 3. 请求体 (Pydantic)
*   POST/PUT 请求的数据通过继承 `BaseModel` 来定义，FastAPI 会自动解析 JSON，并做数据验证。

```python
# 模型类
class UserInFo(BaseModel):
    username: str
    password: str = None
@app.post("/param/body")
def test_param_body(user_info: UserInFo):
    return {"username": user_info.username, "password": user_info.password}
```

**注意：模型类继承BaseModel，而BaseMOdel对属性有检验功能，创建对象时，属性必须有值;因此模型类中的属性应该和请求体参数中键保持一致，也可以为模型类的属性设置默认值，此时请求体参数中键可选**

### 4. 路由分发 (APIRouter)
*   项目变大时，不要把所有代码塞进 `main.py`。
*   使用 `APIRouter` 将不同模块拆分为 `routers/user.py`、`routers/item.py`，在主 `main.py` 中使用 `app.include_router(user.router)` 挂载。

### 5.启动uvicorn服务器

- 命令启动：uvicorn python文件名：FastAPI核心对象名 --prot 端口号 --reload

- 代码启动

```python
uvicorn.run(
            app="fastapi_test:app",
            # host="0.0.0.0", # 任何人都可以访问
            host="127.0.0.1",
            port=8000,
            reload=True,
        )
```

---

## 第三部分：SQLAlchemy (ORM) 核心操作

ORM（对象关系映射）让你用“操作类”代替“写 SQL”。

### 1. 核心组件架构
*   **Engine（引擎）**：管理数据库连接池的入口。
*   **Base（基类）**：所有模型类继承它，管理表结构。
*   **Session（会话）**：执行增删改查的操作台。

### 2. 快速起步
1. **连接**：`create_engine("mysql+pymysql://user:pwd@host:port/db")`
2. **基类**：`Base = declarative_base()`
3. **会话工厂**：`SessionLocal = sessionmaker(bind=engine, autoflush=False)`
4. **模型类**：
    ```python
    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        name = Column(String(50))
    ```
5. **建表**：`Base.metadata.create_all(bind=engine)`（⚠️ 只创建不存在的表，不会自动修改已有表结构）。

### 3. 增删改查 (CRUD) 速查
*   **增**：`db.add(obj)` / `db.add_all([obj1, obj2])` 然后 `db.commit()`，需 `db.refresh(obj)` 获取自增 ID。
*   **查**：`db.query(User).filter(User.age > 18).all()`，或按主键查 `db.get(User, 1)`。
*   **改**：查出对象 -> 直接改属性（`user.age = 20`） -> `db.commit()`。
*   **删**：查出对象 -> `db.delete(user)` -> `db.commit()`。

---

## 第四部分：SQLAlchemy 关联关系与高级查询

### 1. 表关联关系 (Relationship)
*   **一对多**：如 部门(Department) -> 员工(Employee)。
    *   子表（员工）用 `ForeignKey("departments.id")` 绑定外键。
    *   父表用 `relationship("Employee", back_populates="department")`。
*   **多对多**：需要一张中间表（`Table` 对象），两边都用 `relationship(..., secondary=中间表)`。
*   **⚠️ 级联与加载（性能核心）**：
    *   `cascade="all, delete-orphan"`：删主表自动删子表。
    *   `lazy="selectin"`：**极力推荐**。查询主表时，一次性用 `IN` 语句把子表全查出来，解决 **N+1 查询问题**。
    *   `lazy="joined"`：用 JOIN 语句一并查出，适合一对一。

### 2. 高级查询技巧
*   **逻辑组合**：`from sqlalchemy import and_, or_`。
*   **连表查询**：`session.query(Employee).join(Department).all()`。
*   **预加载**：`from sqlalchemy.orm import joinedload`。在 query 后面加 `.options(joinedload(Employee.department))`。
*   **子查询**：利用 `subquery()` 和 `func.count()` 做聚合统计。

---

## 第五部分：FastAPI + SQLAlchemy 完美整合

在 FastAPI 中，必须使用**依赖注入（Depends）**来管理数据库 Session 的生命周期，确保每个请求用完数据库后自动关闭。

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine

app = FastAPI()

# 1. 定义依赖项：获取数据库会话，用完自动关闭
def get_db():
    db = SessionLocal()
    try:
        yield db  # 返回给接口函数使用
    finally:
        db.close()  # 无论接口是否报错，必定执行关闭

# 2. 在接口中注入
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    # 直接使用 db 进行 ORM 查询
    return db.query(User).all()
```

---

## 第六部分：新手必看的 6 大天坑

1.  **假异步卡死**：写了 `async def`，里面却用了 `time.sleep(5)`。整个服务器瞬间假死，必须换成 `await asyncio.sleep(5)`。
2.  **路由顺序覆盖**：`/{item_id}` 放在前面，导致后面写死的 `/latest` 永远访问不到。
3.  **忘记关闭 Session**：手动 `SessionLocal()` 却没有 `db.close()`，导致连接池被耗尽，系统直接崩溃。（严格按照上面的 `get_db` 依赖注入写法即可避免）。
4.  **N+1 查询问题**：用 for 循环遍历查询出来的主表对象，并在循环内访问它的关联属性（如 `user.items`）。如果有 100 个用户，就会额外发 100 次 SQL。**解决办法**：模型配置 `lazy="selectin"` 或查询时 `joinedload()`。
5.  **忘记 commit**：ORM 新增或修改数据后，不写 `db.commit()`，只存在内存里，数据库毫无反应。
6.  **多表关联报错**：定义 `relationship` 时，若外键写错，或者双向绑定没写对（如 `back_populates` 两边名字对不上），初始化时会报错说找不到相关类。

# ⭐新技术：

### 1. 数据库驱动与引擎：从“同步驱动”升级为“异步全栈”

- **旧写法（过时）**：使用同步驱动 `pymysql` 搭配 `create_engine`，在接口中写 `async def` 却进行阻塞查询。
- **现主流技术**：**异步驱动（asyncmy / aiomysql）搭配 create_async_engine**。现代高并发 FastAPI 服务统一采用非阻塞的 `await` 数据库 I/O，避免线程池瓶颈。

```python
# 旧代码（同步引擎）
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/fastapi_db", pool_pre_ping=True)

# 新代码（SQLAlchemy 2.0 异步引擎）
from sqlalchemy.ext.asyncio import create_async_engine
# 驱动换为 asyncmy（或 aiomysql）
async_engine = create_async_engine(
    "mysql+asyncmy://root:123456@localhost:3306/fastapi_db",
    pool_size=10,          # 连接池大小
    max_overflow=20,       # 最大溢出连接
    pool_pre_ping=True
)
```

------

### 2. 会话工厂：从 `sessionmaker` 升级为 `async_sessionmaker`

- **旧写法（过时）**：使用 `sessionmaker` 配合同步 `Session`。
- **现主流技术**：SQLAlchemy 2.x 的同步与异步体系彻底分离。异步环境必须使用 **async_sessionmaker** 配合 **AsyncSession**，强行混用会导致 `__aenter__` 等协程属性缺失报错。

```python
# 旧代码（同步会话）
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 新代码（SQLAlchemy 2.0 异步会话）
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False  # 异步必需项，防止提交后访问属性触发隐式 IO 报错
)
```

------

### 3. ORM 模型声明：从 `declarative_base` 升级为 `DeclarativeBase` 与 `Mapped`

- **旧写法（过时）**：`declarative_base()` 配合 `Column(Integer)` 来定义字段。在 SQLAlchemy 2.0 中，这种 1.x 模式已被标记为**弃用（Deprecated）**。
- **现主流技术**：使用 **class Base(DeclarativeBase)**，字段一律使用 **Mapped[类型]** 搭配 **mapped_column()**。这样既能获得 IDE 的强类型代码补全，也与 Pydantic v2 的数据校验完美对接。

```python
# 旧代码（1.x 风格）
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer)

# 新代码（2.0 声明式风格）
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int | None] = mapped_column(default=None)  # 类型即约束，直接由类型注解推导
```

------

### 4. CRUD 查询方式：从 `db.query()` 升级为 `await db.execute(select(...))`

- **旧写法（过时）**：`db.query(Model).filter(...)`。这是旧版 `Query` 接口，不支持异步，且会在同步模式下触发 N+1 查询隐患。
- **现主流技术**：全面使用 SQLAlchemy 2.0 的 **select() 表达式**配合 **await execute()**。

```python
# 旧代码（同步 Query 接口）
def get_employee(db: Session, emp_id: int):
    return db.query(Employee).filter(Employee.id == emp_id).first()

# 新代码（2.0 异步 Execute 风格）
from sqlalchemy import select

async def get_employee(db: AsyncSession, emp_id: int):
    stmt = select(Employee).where(Employee.id == emp_id)
    result = await db.execute(stmt)
    return result.scalars().first()  # 获取单个标量对象
```

------

### 5. 依赖注入管理 Session：从 `yield + close` 升级为 `async with`

- **旧写法（过时）**：在同步 `def get_db()` 里 `try/finally` 手动调用 `db.close()`。
- **现主流技术**：结合 FastAPI 的依赖注入，在 `async def get_db()` 中使用 **async with AsyncSessionLocal() as session**，利用异步上下文管理器自动处理关闭。

```python
# 旧代码
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 新代码
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

------

### 💡 核心变动的底层原因

旧版笔记混用了“普通 `def` 配合线程池”与“`async def` 配合事件循环”两套体系。当前的主流方案是**全链路异步（Full Async）**——从 FastAPI 路由、SQLAlchemy Session 到数据库驱动，全程保持协程状态。这样不仅彻底绕开了 Python 的全局解释器锁（GIL）和线程池上限限制，还能在处理海量并发请求时显著降低内存开销与上下文切换成本。如果项目正在起步，建议直接按照上述新范式来搭建脚手架。






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

查看自动文档：http://127.0.0.1:8000/docs，可看到路由按 tags 分类（用户管理、商品管理）。

```python
from fastapi import APIRouter  # 实例化一个 APIRouter，可指定前缀（所有路由自动加上 /users）
router = APIRouter(
    prefix="/users",
    tags=["用户管理"]  # 文档中归类为「用户管理」
)
@router.get("/")
def get_all_users():
    return {"message": "获取所有用户列表"}
@router.get("/{user_id}")
def get_user(user_id: int):
    return {"message": f"获取 ID 为 {user_id} 的用户信息"}

from fastapi import APIRouter
router = APIRouter(
    prefix="/items",
    tags=["商品管理"]
)
@router.get("/")
def get_all_items():
    return {"message": "获取所有商品列表"}
@router.get("/{item_id}")
def get_item(item_id: int):
    return {"message": f"获取 ID 为 {item_id} 的商品信息"}

from fastapi import FastAPI
from routers import user, item  # 导入子模块路由
import uvicorn

app = FastAPI(title="路由分发示例")
# 挂载用户路由：所有 /users 开头的请求由 user.router 处理
app.include_router(user.router)
# 挂载商品路由：所有 /items 开头的请求由 item.router 处理
app.include_router(item.router)
# 主应用自身也可以定义路由
@app.get("/")
def root():
    return {"message": "欢迎访问主页面"}
if __name__ == "__main__":
    # 直接在代码中启动uvicorn服务器
    uvicorn.run(
        app="main:app",       # 指定要运行的FastAPI应用实例
        host="0.0.0.0",  # 允许外部访问（本地可通过127.0.0.1或localhost访问）
        port=8000,     # 端口号
        reload=True    # 开发模式：代码修改后自动重启（生产环境需去掉）
    )
```

### 5.启动uvicorn服务器

- 命令启动：uvicorn python文件名：FastAPI核心对象名 --prot 端口号 --reload

- 代码启动

```python
uvicorn.run(
	"fastapi_test:app",
	# host="0.0.0.0", # 任何人都可以访问
	host="127.0.0.1",
	port=8000,
    use_colors=True,    # 控制台彩色日志
    # 开发环境
	reload=True,
    log_level="debug",  # 开发打开debug，看详细请求日志
    # 生产环境
    reload=False,
	log_level="info",
    # log_level控制控制台输出日志的最低等级(从啰嗦 → 安静排序)
    # trace → debug → info → warning → error → critical
)
```

- 命令行启动

```bash
# 方式 1：uvicorn 命令行
	# 本地开发，自动热更
uvicorn fastapi_test:app --host 127.0.0.1 --port 8000 --reload
	# 简单单进程生产（不适合高并发，仅临时测试）
uvicorn fastapi_test:app --host 0.0.0.0 --port 8000 --worker 2
	# `workers N`：多进程，充分利用多核 CPU；⚠️ workers 和 reload 不能同时开启
# 方式 2：FastAPI 官方自带 `fastapi run`
	# 开发（热重载）	`fastapi dev` = 开发模式（带 reload）；
fastapi dev fastapi_test.py --host 127.0.0.1 --port 8000
	# 生产			`fastapi run` = 生产模式（无 reload）
fastapi run fastapi_test.py --host 0.0.0.0 --port 8000 --workers 4
```



---

## 第三部分：SQLAlchemy (ORM) 核心操作

ORM（对象关系映射）让你用“操作类”代替“写 SQL”。

### 1. 基本架构

#### 	1.DBAPI（数据库通信层）

DBAPI（Database API）是Python数据库接口规范，是SQLAlchemy与底层数据库通信的 “桥梁”。SQLAlchemy 通过适配这些 DBAPI，实现对多种数据库的兼容。

#### 	2.SQLAlchemy Core（核心层）

Core是SQLAlchemy的 “基础工具集”，提供了SQL表达式语言、数据库连接管理等核心能力，即使不使用 ORM，也能通过 Core 操作数据库。

- Schema / Types：定义数据库的模式（Schema）和数据类型（Types）。

- SQL Expression Language：用Python代码生成SQL语句的 “表达式语言”。

- Engine：管理数据库连接的 “引擎”，是与数据库交互的 “入口”。

- Connection Pooling：管理数据库连接池，提升数据库操作性能。

- Dialect：处理 “方言” 差异，适配不同数据库的 SQL 语法和特性。

    #### 3.SQLAlchemy ORM（对象关系映射层）

本质是对Core的 “封装”，自动转换为Core能理解的 SQL 表达式通过，最终 Engine 执行

#### 	4.核心组件

- 引擎（Engine）：Engine 是与数据库的连接入口，负责管理连接池和执行 SQL 语句。
- 基类（Base）：所有 ORM 模型的父类，用于统一管理数据库表结构。
- 会话（Session）：用于执行数据库操作的会话对象，负责暂存、提交、回滚数据操作。

### 2. 快速起步

​	环境准备：

```bash
# 安装 SQLAlchemy 核心库
pip install sqlalchemy
# 安装 MySQL 驱动（推荐 pymysql，兼容 Python 3.x）
pip install pymysql
```

​	基本案例：

#### 1.**在base.py中定义Base基类**

```python
from sqlalchemy.ext.declarative import declarative_base
# 生成基类，所有模型需继承该类
Base = declarative_base()
```

#### 2.在models.py中定义ORM模型类（映射MySQL表）

```python
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from demo.base import Base

class Department(Base):
    """部门模型（一对多：一个部门包含多个员工）"""
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)  # 部门名称
    location = Column(String(100))  # 部门位置（如"北京总部"）
    # 一对多关联员工：返回员工列表，显式指定外键（可选，但更清晰）
    employees = relationship(
        "Employee",
        back_populates="department",
        # 可选：级联删除（删除部门时自动删除下属员工，根据业务选择）
        # cascade="all, delete-orphan",
        # 可选：懒加载策略，优化查询性能
        lazy="selectin"
    )
class Employee(Base):
    """员工模型（多对一：多个员工属于一个部门）"""
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)  # 姓名
    age = Column(Integer)  # 年龄
    hire_date = Column(Date)  # 入职日期
    #添加外键约束，绑定到departments.id
    department_id = Column(
        Integer,
        ForeignKey("departments.id", ondelete="RESTRICT"),  # 禁止删除有员工的部门
        nullable=False  # 员工必须归属一个部门（根据业务可改为True，允许无部门）
    )
    # 核心修正：多对一关联，指定uselist=False（返回单个部门对象）
    department = relationship(
        "Department",
        back_populates="employees",
        lazy="joined"  # 可选：立即加载部门数据，减少查询次数
    )
```

#### 3.在database.py创建引擎以及会话

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL 连接格式：mysql+pymysql://用户名:密码@主机地址:端口/数据库名
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/fastapi_db"

# 创建引擎（echo=True 会打印执行的 SQL，方便调试）
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 是否启用日志输出 开发环境启用，生产环境关闭
    pool_pre_ping=True  # 连接前检查有效性，避免连接失效
)

# 创建会话工厂（绑定引擎）
SessionLocal = sessionmaker(
    autocommit=False,  # 关闭自动提交，需手动 commit()
    bind=engine
)
```

模型类对应MySQL中的表，类属性对应表字段，通过 Column 定义字段类型和约束。

from sqlalchemy import Column, Integer, String, ForeignKey, Date

from sqlalchemy.orm import relationship

from demo.base import Base

 

class Department(Base):

​    """部门模型（一对多：一个部门包含多个员工）"""

​    __tablename__ = "departments"

 

​    id = Column(Integer, primary_key=True, autoincrement=True)

​    name = Column(String(50), nullable=False, unique=True)  # 部门名称

​    location = Column(String(100))  # 部门位置（如"北京总部"）

 

​    \# 一对多关联员工：返回员工列表，显式指定外键（可选，但更清晰）

​    employees = relationship(

​        "Employee",

​        back_populates="department",

​        \# 可选：级联删除（删除部门时自动删除下属员工，根据业务选择）

​        \# cascade="all, delete-orphan",

​        \# 可选：懒加载策略，优化查询性能

​        lazy="selectin"

​    )

 

class Employee(Base):

​    """员工模型（多对一：多个员工属于一个部门）"""

​    __tablename__ = "employees"

 

​    id = Column(Integer, primary_key=True, autoincrement=True)

​    name = Column(String(50), nullable=False)  # 姓名

​    age = Column(Integer)  # 年龄

​    hire_date = Column(Date)  # 入职日期

 

​    \#添加外键约束，绑定到departments.id

​    department_id = Column(

​        Integer,

​        ForeignKey("departments.id", ondelete="RESTRICT"),  # 禁止删除有员工的部门

​        nullable=False  # 员工必须归属一个部门（根据业务可改为True，允许无部门）

​    )

 

​    \# 核心修正：多对一关联，指定uselist=False（返回单个部门对象）

​    department = relationship(

​        "Department",

​        back_populates="employees",

​        lazy="joined"  # 可选：立即加载部门数据，减少查询次数

​    )

字段约束说明：

Ø primary_key=True：设为主键。

Ø autoincrement=True：MySQL 自增（仅整数类型可用）。

Ø unique=True：唯一索引，避免重复值。

Ø nullable=False：非空约束（字段必须有值）。

#### 4.在main.py中提供建表方法

```python
from demo.base import Base
from demo.database import engine
from demo.models import Employee,Department #必须要加

# 创建表
def create_table():
    print("注册的表名:", Base.metadata.tables.keys())
    # 创建所有模型对应的表
    Base.metadata.create_all(bind=engine)
    print("表创建成功")

if __name__ == '__main__':
    create_table()
```

### 整体代码流程解析:

- 调用 `declarative_base()` 创建了一个基类 `Base`。

- 继承 `Base` 定义了 `Department`（部门）和 `Employee`（员工）两个类。
- 使用 `create_engine` 根据 `DATABASE_URL` 创建了数据库引擎（管理连接池）。
- 建表：`Base.metadata.create_all(bind=engine)`（⚠️ 只创建不存在的表，不会自动修改已有表结构）。
- 导入所有的模型类（后续使用）。

| 方法                                                         | 参数                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `declarative_base()`：生成一个 ORM 基类。                    | ⭐新版本：class Base(DeclarativeBase): pass                   |
| `Column()`：定义表中的一列（字段）。                         | `default`：默认值。                                          |
|                                                              | `primary_key`：是否为主键。                                  |
|                                                              | `autoincrement`：是否自增。                                  |
|                                                              | `nullable`：是否允许为空（默认 True）。                      |
|                                                              | `unique`：是否唯一。                                         |
| `ForeignKey()`：声明外键。                                   | `目标列`（如 `"departments.id"`）：必须用 `表名.列名` 的字符串格式。 |
|                                                              | `ondelete`：级联删除策略。`"RESTRICT"` 表示如果部门下有员工，数据库将拒绝删除该部门（防误删神器）。 |
| `relationship()`:不改变数据库物理结构，只在 Python 代码层面建立对象之间的引用。 | `目标类`（如 `"Employee"`）：用字符串防止类加载顺序报错。    |
|                                                              | `back_populates`：双向绑定的属性名（比如 `Employee` 里的 `department` 属性）。 |
|                                                              | `lazy`：懒加载策略。`selectin`（一对多最优）、`joined`（多对一最优）。 |
|                                                              | `cascade`：ORM 层的级联（例如 `"all, delete-orphan"` 删主表时自动删子表，慎用）。 |
| `create_engine()`：创建一个数据库引擎实例。                  | `DATABASE_URL`：数据库连接字符串。                           |
|                                                              | `echo=True`：是否打印底层执行的 SQL，开发环境强烈建议开启，生产环境关闭。 |
|                                                              | `pool_pre_ping=True`：每次从池里拿连接前，检查是否存活（防止 MySQL 8小时断开导致程序崩溃）。 |
|                                                              | `pool_size`：连接池常驻连接数（默认5）。                     |
|                                                              | `max_overflow`：连接池满了之后允许额外创建的连接数（默认10）。 |
| `sessionmaker()`：生成一个会话工厂（Class），而不是一个具体的会话（Instance）。 | `bind=engine`：把工厂绑定到具体的数据库引擎上。              |
|                                                              | `autocommit=False`：关闭自动提交（极其重要，必须由开发者手动调用 `session.commit()`，防止数据写乱）。 |
|                                                              | `autoflush=False`：关闭自动刷新，通常在 FastAPI 中设为 False 以便更好地控制事务。 |
| `Base.metadata.create_all()`：读取基类 `Base` 中注册的所有表，并生成 SQL 语句在数据库中创建。 | `bind=engine`：指定在哪个数据库里建表。                      |
|                                                              | `checkfirst=True`（默认值）：建表前先检查，如果表已存在则跳过。 |

### 3. 增删改查 (CRUD) 速查

*   **增**：`db.add(obj)` / `db.add_all([obj1, obj2])` 然后 `db.commit()`，需 `db.refresh(obj)` 获取自增 ID。
*   **查**：`db.query(User).filter(User.age > 18).all()`，或按主键查 `db.get(User, 1)`。
*   **改**：查出对象 -> 直接改属性（`user.age = 20`） -> `db.commit()`。
*   **删**：查出对象 -> `db.delete(user)` -> `db.commit()`。

```python
#---------------新增数据（Create）
def insert_data():
    # 获取数据库会话
    db = SessionLocal()
    try:
        # =========== 第一步：新增部门 =============
        new_dept = Department(
            name="研发部",  # 部门名称（唯一）
            location="北京总部"  # 部门位置
        )
        db.add(new_dept)  # 将部门对象加入会话
        db.commit()  # 提交到数据库（执行 INSERT 语句）
        db.refresh(new_dept)  # 刷新对象，获取自增的 id 等字段
        # =========== 第二步：新增关联的员工 ===========
        # 员工1：关联上面创建的研发部
        emp1 = Employee(
            name="张三",
            age=30,
            hire_date=date(2023, 1, 1),  # 入职日期（datetime.date 类型）
            department_id=new_dept.id  # 关联部门 ID（外键）
        )
        # 员工2：同部门的另一个员工
        emp2 = Employee(
            name="李四",
            age=28,
            hire_date=date(2023, 3, 15),
            department_id=new_dept.id
        )
        # 批量添加员工（也可逐个 add）
        db.add_all([emp1, emp2])
        db.commit()  # 提交员工数据
        # 刷新员工对象，获取自增 ID
        db.refresh(emp1)
        db.refresh(emp2)
        # ===================== 输出结果 =====================
        print(f"新增部门：ID={new_dept.id}，名称={new_dept.name}，位置={new_dept.location}")
        print(f"新增员工1：ID={emp1.id}，姓名={emp1.name}，所属部门={new_dept.name}")
        print(f"新增员工2：ID={emp2.id}，姓名={emp2.name}，所属部门={new_dept.name}")
        # 验证关联关系（通过 ORM 关联查询）
        print("\n【验证关联关系】")
        # 从员工查部门
        print(f"员工{emp1.name}的部门名称：{emp1.department.name}")
        # 从部门查员工
        dept_employees = new_dept.employees
        print(f"部门{new_dept.name}的员工列表：{[emp.name for emp in dept_employees]}")
    except Exception as e:
        db.rollback()  # 出错时回滚
        print(f"新增失败：{e}")
    finally:
        db.close()  # 关闭会话
#---------------删除数据（Delete）
def delete_data():
    # 获取会话
    session = SessionLocal()
    try:
        # 删除单个员工
        emp = session.query(Employee).filter(Employee.name == "李四").first()
        if emp:
            session.delete(emp)
            session.commit()
            print(f"已删除员工：{emp.name}")
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"刪除失败：{e}")
    finally:
        session.close()  # 关闭会话
#---------------修改数据（Update）
def update_data():
    # 获取会话
    session = SessionLocal()
    try:
        # 修改员工年龄
        emp = session.query(Employee).filter(Employee.name == "张三").first()
        if emp:
            emp.age = 31  # 直接修改属性
            session.commit()  # 提交更新
            print(f"修改后 {emp.name} 的年龄：{emp.age}")
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"修改失败：{e}")
    finally:
        session.close()  # 关闭会话
#---------------查询数据（Read）
def read_data():
    # 获取会话
    session = SessionLocal()
    try:
        # ======按主键查询 get========
        #  查询id=1的部门
        dept = session.get(Department,1) 
        print(f"部门 ID=1：{dept.name}（{dept.location}）")
        # ======过滤（filter）查询========
        # 查询研发部的所有员工
        rd_employees = session.query(Employee).filter(
            Employee.department_id == 1  # 按部门ID过滤
        ).all()
        print("研发部员工：", [emp.name for emp in rd_employees])  # 输出：['张三']
        # 查询年龄>30的员工
        old_employees = session.query(Employee).filter(Employee.age > 30).all()
        print("年龄>30的员工：", [emp.name for emp in old_employees]) # 输出：['张三', '王五']
        # ======逻辑运算（and_/or_）查询========
        from sqlalchemy import and_, or_
        # 年龄30-40且属于研发部的员工（and_）
        emp = session.query(Employee).filter(
            and_(Employee.age.between(30, 40), Employee.department_id == 1)
        ).first()
        print("符合条件的员工：", emp.name)  # 输出：张三
        # 属于市场部或年龄>32的员工（or_）
        emps = session.query(Employee).filter(
            or_(Employee.department_id == 2, Employee.age > 32)
        ).all()
        print("符合条件的员工：", [emp.name for emp in emps])  # 输出：['张三', '王五']
        # ======表连接（join）查询========
        # 内连接：查询员工及其所属部门名称
        # 语法：query(主表, 关联表).join(关联表, 连接条件)
        result = session.query(Employee, Department).join(
            Department, Employee.department_id == Department.id
        ).all()
        for emp, dept in result:
            print(f"员工 {emp.name} 属于 {dept.name}")
        # 输出：
        # 员工 张三 属于 研发部
        # 员工 王五 属于 市场部
        # ======预加载关联数据（joinedload）查询========
        from sqlalchemy.orm import joinedload
        # 加载员工时同时加载部门信息（避免多次查询）
        employees = session.query(Employee).options(
            joinedload(Employee.department)  # 预加载关联的 department
        ).all()
        # 直接访问关联数据，不会触发新查询
        for emp in employees:
            print(f"{emp.name} 的部门：{emp.department.name}")
        # 输出：
        # 张三 的部门：研发部
        # 王五 的部门：市场部
        # ======子查询（subquery）========
        from sqlalchemy import func
        #子查询：统计每个部门的员工数，再查询员工数>0的部门
        # 步骤1：创建子查询（统计部门员工数）
        dept_emp_count = session.query(
            Employee.department_id,
            func.count(Employee.id).label("count")  # 别名 count
        ).group_by(Employee.department_id).subquery()  # 转为子查询
        # 步骤2：主查询（关联子查询结果）
        depts = session.query(Department).join(
            dept_emp_count, Department.id == dept_emp_count.c.department_id
        ).filter(dept_emp_count.c.count > 0).all()  # 筛选员工数>0的部门
        print("有员工的部门：", [dept.name for dept in depts])  # 输出：['研发部', '市场部']
        # ======去重（distinct）========
        # 查询所有有员工的部门位置（去重）
        locations = session.query(Department.location).join(
            Employee
        ).distinct().all()  # distinct() 去重
        print("部门位置：", [loc[0] for loc in locations])  # 输出：['北京', '广州']
        # ======结果获取（first/all）========
        # first()：返回第一条结果（适合唯一查询）
        first_emp = session.query(Employee).first()
        print("第一个员工：", first_emp.name)  # 输出：张三
        # all()：返回所有结果（列表）
        all_depts = session.query(Department).all()
        print("所有部门：", [dept.name for dept in all_depts])  # 输出：['研发部', '市场部']
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话
```

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

### 参考目录

```plaintxet
project/
├── main.py
├── config.py          # 配置（pydantic-settings，读取环境变量）
├── schemas/           # 入参、出参模型
│   ├── __init__.py
│   ├── user.py
│   └── item.py
├── routers/
│   ├── __init__.py
│   ├── user.py
│   └── item.py
├── common/            # 公共工具：异常、响应、日志
│   ├── __init__.py
│   ├── exceptions.py
│   ├── response.py
│   └── logger.py
├── services/          # 业务层（路由只调用service，不写业务）
│   ├── __init__.py
│   ├── user_service.py
│   └── item_service.py
└── requirements.txt

```

# ⭐新版案例

## 技术栈:(FastAPI + SQLAlchemy 2.0 + Pydantic v2 + 全异步)

### 1.database.py

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from MySQL.test import AsyncSessionLocal

# 1. 数据库连接 URL
# 如果要用你本地的 MySQL，请取消下面这行的注释（注意需要 pip install asyncmy）
DATABASE_URL = "mysql+asyncmy://root:admin@localhost:3306/new_fastapi_db"

# 2. 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)
# 3. 创建异步会话工厂
# expire_on_commit=False 极其重要！异步环境下如果不加，commit后访问对象属性会触发隐式I/O报错
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSessionLocal,
    expire_on_commit=False
)


# 4. FastAPI 依赖注入函数（获取数据库会话）
async def get_db():
    # async with 自动处理会话的关闭，即使接口内部报错也会安全释放
    async with AsyncSessionLocal() as session:
        yield session

```

### 2.models.py

```python
from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# 1. 定义基类（代替旧的 declarative_base()）
class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"
    # 2. 使用 Mapped 和 mapped_column（强类型）
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    # 3. 一对多关系：lazy="selectin" 是异步 FastAPI 解决 N+1 问题的标配
    employees: Mapped[List["Employee"]] = relationship(
        back_populates="department",
        lazy="selectin",
    )


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int | None] = mapped_column(default=None)
    # 外键
    department_id: Mapped[int] = mapped_column(
        ForeignKey(
            "departments.id",
            ondelete="CASCADE"
        )
    )

    department: Mapped["Department"] = relationship(
        back_populates="employees",
        lazy="joined",
    )

```

### 3.schemas.py

```python
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

```

### 4.main.py

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uvicorn

from database import engine, get_db
from models import Base, Department, Employee
from app import DepartmentCreate, DepartmentResponse


# ================= 应用生命周期管理 =================
# 在应用启动时自动创建表（仅限开发环境，生产环境推荐用 Alembic）
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # 运行同步的 create_all
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 应用关闭时可在此处释放连接池
    await engine.dispose()


app = FastAPI(title="现代化 FastAPI + SQLAlchemy 2.0", lifespan=lifespan)


# ================= 接口 1：新增部门（级联新增员工） =================
@app.post("/departments/", response_model=DepartmentResponse)
async def create_department(dept_in: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    # 1. 构造 ORM 对象
    # 因为模型中配置了双向关系，Pydantic 传入的员工列表可以直接赋给 employees 属性
    new_dept = Department(
        name=dept_in.name,
        employees=[Employee(name=emp.name, age=emp.age) for emp in dept_in.employees]
    )

    # 2. 写入数据库
    db.add(new_dept)
    await db.commit()  # 异步提交
    await db.refresh(new_dept)  # 获取生成的自增 ID

    return new_dept


# ================= 接口 2：根据 ID 查询部门（包含员工列表） =================
@app.get("/departments/{dept_id}", response_model=DepartmentResponse)
async def get_department(dept_id: int, db: AsyncSession = Depends(get_db)):
    # 现代查询语法：select() + await execute()
    stmt = select(Department).where(Department.id == dept_id)
    result = await db.execute(stmt)

    # .scalars().first() 提取单个对象
    department = result.scalars().first()

    if not department:
        raise HTTPException(status_code=404, detail="部门不存在")

    # 由于模型中配置了 lazy="selectin"，这里访问 department.employees 不会报错，且不会产生 N+1 查询
    return department


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

测试数据：

```jso
{
  "name": "测试部门",
  "employees": [
    {
      "name": "张三",
      "age": 25
    },
    {
      "name": "李四",
      "age": 28
    }
  ]
}
```



## 2.FastAPI 【anyio 版本（FastAPI 首选替代，推荐）】

```python
from asyncio import CancelledError
import anyio
# 用来控制最大并发数量
sem = anyio.Semaphore(10)
async def fetch_data(name, delay):
    print(f"任务 {name} 开始")
    await anyio.sleep(delay)
    print(f"任务 {name} 完成")
    return f"任务 {name} 结果"
# 带并发限流 + 异常捕获的包装层
async def run_limited(name, delay):
    try:
        # `async with` 是异步上下文管理器。进入的时候申请信号量许可，退出的时候自动释放许可。
        async with sem:
            return {"ok": True, "name": name, "data": await fetch_data(name, delay)}
    except CancelledError:
        # 单独捕获取消异常（超时、外部取消都会抛这个）
        return {"ok": False, "name": name, "err": "任务被取消/全局超时"}
    except Exception as e:
        return {"ok": False, "name": name, "err": str(e)}
# 顶级函数
async def main():
    results = []
    # （任务组），结构化并发核心。主协程一定会等待所有子任务全部完成
    async with anyio.create_task_group() as tg:
        #  tg.start_soon
        for i in range(20):
            # 👉 经典闭包陷阱修复！
            async def wrapper(idx=i):
                r = await run_limited(f"Task-{idx}", 1)
                results.append(r)
            # 一次性把 20 个任务全部交给 TaskGroup 调度
            tg.start_soon(wrapper)
        # 正确写法：当前时间往后5.5秒截止
        tg.cancel_scope.deadline = anyio.current_time() + 2.0
    for mes in results:
        print(mes)
if __name__ == '__main__':
    anyio.run(main)

```

## 3.路由分发

```python
#-----------------------------------------------------routers/user.py
from fastapi import APIRouter, HTTPException
router = APIRouter(
    prefix="/users",
    tags=["用户管理"],
    # 这两个是进阶可选：这个路由组统一的响应、依赖
    # responses={404: {"description": "Not found"}},
    # dependencies=[...]
)
@router.get(
    "/",
    summary="获取全部用户",		# swagger文档（/docs）接口列表
    description="返回用户列表",	# 接口详情里
    # response_model=UserOut 
    # `UserOut` 就是我们在 `schemas/user.py` 定义的 Pydantic BaseMode
    # 作用：约束接口返回的数据结构，自动生成接口文档，自动序列化，过滤敏感字段
)
async def get_all_users():
    # 这里后续可以放你的anyio并发、异步数据库查询
    return {"message": "获取所有用户列表"}
@router.get(
    "/{user_id}",
    summary="获取单个用户",
)
async def get_user(user_id: int):
    # 业务示例：找不到抛404，这是规范写法，而不是只返回message
    if user_id <= 0:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": f"获取 ID 为 {user_id} 的用户信息"}
#-----------------------------------------------------routers/item.py
from fastapi import APIRouter, HTTPException
router = APIRouter(
    prefix="/items",
    tags=["商品管理"],
)
@router.get("/", summary="获取全部商品")
async def get_all_items():
    return {"message": "获取所有商品列表"}
@router.get("/{item_id}", summary="获取单个商品")
async def get_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(status_code=404, detail="商品不存在")
    return {"message": f"获取 ID 为 {item_id} 的商品信息"}
#-----------------------------------------------------routers/__init__.py
from .user import router as user_router
from .item import router as item_router
__all__ = ["user_router", "item_router"]
#-----------------------------------------------------main.py
from fastapi import FastAPI
from routers import user_router, item_router

app = FastAPI(
    title="路由分发示例",
    description="APIRouter模块化路由演示",
    version="1.0.0"
)
# 挂载路由
app.include_router(user_router)
app.include_router(item_router)
@app.get("/", summary="首页")
async def root():
    return {"message": "欢迎访问主页面"}
#-----------------------------------------------------bash命令行启动
# 开发
fastapi dev main.py --host 127.0.0.1 --port 8000
# 或者 uvicorn main:app --reload
# 生产
fastapi run main.py --host 0.0.0.0 --port 8000 --workers 2
```






# 🚀 企业级高并发异步 Web 后端架构技术文档

## 一、 技术栈选型 (Tech Stack)

本项目采用全链路异步方案，旨在应对高并发、I/O 密集型的 API 场景（如大模型应用、高频读写服务）。

- **Web 框架**：FastAPI (基于 Starlette，性能极高，自动生成 OpenAPI 文档)
- **ORM 框架**：SQLAlchemy 2.0 (采用最新 `select()` 语法、强类型 `Mapped` 映射)
- **数据校验**：Pydantic v2 (极速校验，支持嵌套模型)
- **数据库驱动**：asyncmy (纯异步 MySQL 驱动，替代同步的 pymysql)
- **ASGI 服务器**：Uvicorn (支持热更新、多进程)
- **数据库**：MySQL 8.0+

------

## 二、 核心架构分层 (Layered Architecture)

遵循“**瘦路由、胖服务、纯数据**”的原则，各层职责彻底解耦，严格单向依赖。

text

```
Client (前端请求)
   ↓
[1] Router (api/v1/)        # 接口层：解析 HTTP 参数，处理状态码，调用 Service
   ↓
[2] Schema (schemas/)       # 校验层：DTO (Data Transfer Object)，定义 I/O 结构
   ↓
[3] Service (services/)     # 业务层：编排业务逻辑，控制事务边界 (begin/commit)
   ↓
[4] CRUD (crud/)            # 数据层：纯粹的 SQL 执行 (select/add/flush)
   ↓
[5] Model (models/)         # 模型层：定义表结构、外键、关联关系
   ↓
Database (MySQL)
```

------

## 三、 核心技术亮点与最佳实践

### 1. 依赖注入与生命周期管理 (Dependency Injection)

通过 `Depends(get_db)` 自动管理数据库会话。使用 `yield` 机制，确保请求结束后连接必定被回收。

- **亮点**：路由函数无需关心数据库的开关，代码极简。
- **事务边界**：支持两种流派（`get_db` 统一提交 或 `Service` 层显式 `begin`），杜绝了数据半写入（脏数据）问题。

### 2. 全链路异步与防坑机制 (Async & MissingGreenlet)

在异步 `AsyncSession` 中，绝对禁止隐式懒加载。

- **解决方案**：所有关系（`relationship`）必须配置 `lazy="selectin"`，或在查询时强制使用 `selectinload()` 预加载。彻底消灭了 `MissingGreenlet` 报错，同时解决了经典 N+1 查询性能问题。

### 3. 严谨的 Schema 分层设计 (Pydantic DTO)

严格遵守 `Base -> Create / Update / Response` 继承体系：

- **Base**：存放基础公共字段。
- **Create**：用于 POST 请求，强制校验前端必填项。
- **Update**：用于 PUT/PATCH 请求，字段全部设为 `Optional` 支持局部更新。
- **Response**：用于返回前端，包含自增 ID 等，开启 `from_attributes=True`。
- **防坑**：列表字段使用 `default_factory=list` 杜绝 Python 经典的可变默认值共享坑。

### 4. RESTful API 规范

- 彻底摒弃 `/create`、`/delete` 等动词，用 HTTP 方法表达动作。
- `GET` 查（200 OK），`POST` 增（201 CREATED），`PUT` 改（200 OK），`DELETE` 删（204 NO CONTENT）。

### 5. 全局异常拦截与标准化响应

通过 `@app.exception_handler(BusinessException)` 统一拦截业务异常，转化为标准 JSON 格式 `{"code": 400, "message": "xxx", "data": null}`。前端能够清晰区分系统崩溃（500）与业务校验失败（400）。

------

## 四、 一条完整的请求生命周期 (Request Lifecycle)

以 `POST /api/v1/departments/`（创建部门并级联创建员工）为例：

1. **请求接入**：Uvicorn 接收 HTTP 请求，交由 FastAPI 路由匹配。
2. **依赖激活**：`Depends(get_db)` 从连接池拿出 Session；`Depends(verify_token)` 进行权限拦截。
3. **数据校验**：Pydantic 将 JSON Body 转化为 `DepartmentCreate` 对象，校验失败直接返回 422。
4. **路由分发**：Router 将校验好的 `dept_in` 和 `db` 传给 `service_department_create`。
5. **开启事务**：Service 层开启显式事务 `async with db.begin():`。
6. **业务校验**：Service 查重（`SELECT`）。
7. **组装对象**：提取普通字段实例化 `Department`，提取嵌套员工数据实例化 `Employee` 列表并绑定级联关系。
8. **入库执行**：CRUD 层执行 `db.add()` 和 `db.flush()`（生成 INSERT SQL，拿回自增 ID，但不 commit）。
9. **提交事务**：离开 `with` 块，自动执行 `COMMIT`。
10. **序列化**：离开事务后，重新用 `selectinload` 查一次完整对象，FastAPI 按照 `DepartmentResponse` 将其转成 JSON 返回前端。





my_project/
├── app/
│   ├── api/                 # 路由层：只负责接收 HTTP 请求，返回响应
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── department.py
│   │       └── employee.py
│   ├── core/                # 核心配置层
│   │   ├── __init__.py
│   │   ├── database.py      # 数据库引擎与会话管理
│   │   └── exceptions.py    # 自定义业务异常
│   ├── crud/                # 数据访问层：纯粹的 SQL 操作，不包含业务逻辑
│   │   ├── __init__.py
│   │   ├── department.py
│   │   └── employee.py
│   ├── models/              # 数据库模型层：SQLAlchemy 2.0 强类型映射
│   │   ├── __init__.py
│   │   └── models.py
│   ├── schemas/             # 数据校验层：Pydantic v2 DTO
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services/            # 业务逻辑层：编排业务规则、调用 CRUD
│   │   ├── __init__.py
│   │   ├── department.py
│   │   └── employee.py
│   └── main.py              # 应用入口：挂载路由、注册全局异常、lifespan
└── requirements.txt
Router (路由) -> Service (业务) -> CRUD (数据) -> Model (模型)。

**core：项目业务无关的「全局基础能力、配置、通用工具」，是整个应用的基础设施；偏向应用层面。**
**db：专门和数据库打交道的全套代码，只关心数据库连接、ORM 基类、数据库初始化；偏向数据存储层面。**

1.问题：get_db 只负责提供 session，事务 commit /rollback 交给路由接口自己控制！**
依赖层不替业务提交事务！


{
  "name": "研发部",
  "desc": "负责核心技术开发",
  "employees": [
    {"name": "张三", "role": "后端工程师"},
    {"name": "李四", "role": "架构师"}
  ]
}
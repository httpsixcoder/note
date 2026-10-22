from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uvicorn

from database import engine, get_db
from models import Base, Department, Employee
from schemas import DepartmentCreate, DepartmentResponse


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
import os
import subprocess
import sys
from datetime import date
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session

from table_2_models import Base, Departments, Employees

# ========== 1. 数据库连接配置 ==========
# 创建数据库引擎
db_host = "localhost"
db_port = 3306
db_name = "test_orm_new"
db_user_name = "root"
db_password = "admin"
url = (
    f"mysql+pymysql://{db_user_name}:{db_password}"
    f"@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
)
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# 只创建一次 engine，echo 按环境控制，加连接池健壮性参数
engine = create_engine(
    url,
    echo=DEBUG,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# 配置会话工厂
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# ========== 2. FastAPI 用的 get_db 依赖（先记住，后面直接抄） ==========
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========== 3. 建表（如果你还没建过） ==========

def create_tables():
    """用 ORM 元数据建表；已存在则跳过"""
    Base.metadata.create_all(engine)
    print("建表完成（已存在则跳过）")


# ========== 4. 反向生成模型（开发辅助，不要放进业务流程） ==========
def table_2_model(run=False):
    """将数据库表映射为Python类"""
    if not run:
        return
    output_path = "table_2_models.py" # 定义输出文件名字

    venv_python = sys.executable  # 获取当前正在运行这个脚本的 Python 解释器完整路径
    # print("当前使用的Python路径：", venv_python)  # 确认输出是.venv/Scripts/python.exe

    # 1. `venv_python`：用上面拿到的虚拟环境 python
    # 2. `-m sqlacodegen`：把 sqlacodegen 当作模块运行（推荐方式）
    # 3. `--generator sqlmodels`：生成器参数【sqlmodels：生成 SQLModel 风格模型，可选换成 `tables`：原生 SQLAlchemy 2.0 Mapped 风格】
    cmd = [
        venv_python, "-m", "sqlacodegen",
        "--generator", "tables",  # SQLAlchemy 2.0 原生
        url
    ]
    # 在子进程执行上面 cmd 命令，等待命令执行完成
    # capture_output=True：捕获标准输出 stdout 和标准错误 stderr
    # text=True：输出返回字符串
    # result 是一个 CompletedProcess 对象，里面包含：returncode、stdout、stderr
    result = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8"
    )

    # 打印执行结果（定位问题核心）
    print("=== 命令执行结果 ===")
    print(f"返回码（0=成功，非0=失败）：{result.returncode}")
    print(f"标准输出：\n{result.stdout}")
    print(f"错误输出：\n{result.stderr}")  # 重点看这里，会显示失败原因

    # 0 → 命令正常执行，非 0异常退出 报错【连接数据库失败、参数错误、包缺失、账号密码错等等】
    if result.returncode != 0:
        # RuntimeError 是 Python 内置的运行时异常（属于通用业务异常）
        raise RuntimeError(f"sqlacodegen 失败：\n{result.stderr}")

    # `.strip()` 去掉空白、换行；如果输出是空字符串【库里没有任何表】
    if not result.stdout.strip():
        raise RuntimeError("sqlacodegen 输出为空，未写入文件")
    # 更新 ORM
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.stdout)
    print(f"模型已写入：{output_path}")

# ========== 5. 插入数据 ==========
def insert_dept_emp():
    # 1. 创建员工对象（用关键字参数，日期转换为date类型）
    emp = Employees(
        id=100,  # 显式指定参数名
        name='zs',
        age=20,
        hire_date=date(2025, 10, 10)  # 字符串转date对象
    )

    # 2. 创建部门对象（关键字参数，日期转换为datetime类型）
    dept = Departments(
        id=10,
        name='研发部',
        location='北京',
        employees=[emp]  # 关联员工
    )

    # 3. 插入数据库
    with Session(engine) as session:
        session.add(dept)
        try:
            session.commit()
            print(f"插入成功！部门ID：{dept.id}，员工ID：{emp.id}")
        except Exception as e:
            session.rollback()
            print(f"插入失败：{e}")

# ========== 6. 查询验证 ==========
def query_check():
    with SessionLocal() as session:
        stmt = select(Departments).where(Departments.id == 10)
        dept = session.scalars(stmt).first()
        if not dept:
            print("没查到部门 10，先跑 insert_dept_emp()")
            return
        print(f"部门：{dept.id} / {dept.name} / {dept.location}")
        for e in dept.employees:
            print(f"  员工：{e.id} / {e.name} / {e.age} / {e.hire_date} ({type(e.hire_date).__name__})")

if __name__ == "__main__":


    create_tables()  # 首次跑，确保表存在
    # table_2_model(True)  # 需要反向生成时再打开，生成到 *_generated.py
    insert_dept_emp()
    query_check()

import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# 数据库配置
db_host="localhost"
db_port=3306
db_name="test_orm_new"
db_user_name="root"
db_user_pwd="admin"

url=(
    f"mysql+asyncmy://{db_user_name}:{db_user_pwd}"
    f"@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
)
DEBUG=os.getenv("DEBUG","true").lower() == "true"

engine=create_async_engine(
    url,
    echo=DEBUG,  #echo=False（默认）：不打印 SQL 日志。echo=True：打印所有执行的 SQL 语句 + 参数，输出到控制
    pool_pre_ping=True, # 每次从池子取出连接前，先发一条轻量 `SELECT 1` 探测连接是否存活。
    pool_recycle=3600,  # 主动提前回收连接,连接使用满 3600 秒（1 小时）之后，连接池会主动把这个连接扔掉，新建连接替代它
    pool_size=10,       # 连接池里面，常驻保持的最大连接数量。
    max_overflow = 5,   # 溢出临时连接上限
    pool_timeout = 30,  # 拿连接的等待超时时间

)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # 异步必须加
    autocommit=False,
    autoflush=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session



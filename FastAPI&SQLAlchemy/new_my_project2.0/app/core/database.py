"""
    数据库连接
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "mysql+asyncmy://root:admin@localhost:3306/test_fastapi_sqlalchemy_new"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=5,
    pool_recycle=3600,
    pool_timeout=30,
    pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,  # 定会话的类是异步会话 `AsyncSession`
    expire_on_commit=False,  # commit 之后，不会标记过期
    autoflush=False,
    autocommit=False,
)


# ✅ 依赖注入：只提供session，【完全不管理提交、回滚】
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

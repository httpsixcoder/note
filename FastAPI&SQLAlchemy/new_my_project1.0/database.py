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

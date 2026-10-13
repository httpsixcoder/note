"""
    该案例演示了python操作MySQL数据库
"""
"""
import pymysql
# 获取连接
def get_connection():
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='admin',
            database='atguigu',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except:
        print("获取连接的时候发生了异常")
# 从数据库表中查询数据
def select_data(conn):
    # 创建游标对象
    my_cursor = conn.cursor()
    # 执行sql语句
    sql = "select * from t_department"
    my_cursor.execute(sql)
    # 获取查询结果
    results = my_cursor.fetchall()
    for row in results:
        print(row)
    my_cursor.close()
def insert_data(conn):
    my_c = conn.cursor()
    sql = "insert into t_department values (10,'test','testtest')"
    my_c.execute(sql)
    # 提交事务
    conn.commit()
    my_c.close()
def delete_data(conn):
    my_c = conn.cursor()
    sql = "delete from t_department where did=10"
    my_c.execute(sql)
    # 提交事务
    conn.commit()
    my_c.close()
def update_data(conn):
    my_c = conn.cursor()
    sql = "update t_department set dname='dev' where did=10"
    my_c.execute(sql)
    # 提交事务
    conn.commit()
    my_c.close()
if __name__ == '__main__':
    conn = get_connection()
    # insert_data(conn)
    # update_data(conn)
    # delete_data(conn)
    select_data(conn)
    conn.close()
"""

"""
SQLAlchemy ORM 异步版：CRUD 完整示例
@author: Gao
@date: 2026-10-13
"""
import asyncio
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# mysql+asyncmy://root:admin@localhost:3306/atguigu
# └─┬─┘ └──┬──┘   └┬─┘ └─┬─┘ └───┬───┘ └─┬─┘ └──┬──┘
#   │      │       │     │       │       │      │
#  数据库  驱动    用户名 密码      主机     端口    库名
# asyncmy	性能最强，Cython 实现，推荐
# ========== 1. 创建异步引擎 ==========
async_engine = create_async_engine(
    "mysql+asyncmy://root:admin@localhost:3306/atguigu",
    pool_size=5,  # 异步池可以设大一点
    max_overflow=10,  # 溢出连接数
    pool_recycle=3600,  # 连接回收时间
    pool_pre_ping=True,  # 连接预检，每次从池里取连接前，先 ping 一下，确保连接是活的。
    echo=False  # SQL 日志开关，是否把执行的 SQL 打印到控制台。
)
# ========== 2. 定义基类 ==========
Base = declarative_base()


# ========== 3. 定义模型 ==========
# 表 → 类（t_department → Department）
# 行 → 对象（一行记录 → 一个 Department 实例）
# 列 → 属性（did、dname、note）
class Department(Base):
    # 对应的数据库名字【不写的话默认对应数据库名为类名：即department】
    __tablename__ = 't_department'
    # did           属性名（对应表的字段名）
    # Column(...)   声明这是一个表字段
    did = Column(Integer, primary_key=True)
    dname = Column(String(50))
    note = Column(String(100))

    def __repr__(self):
        return f"<Department(did={self.did}, dname={self.dname}, note={self.note})>"


# ========== 4. 创建异步 Session 工厂 ==========
# async_sessionmaker 预绑定 engine 和参数，之后直接调用生成 Session。
# 用法
# 创建工厂
#     AsyncSessionLocal = async_sessionmaker(async_engine, ...)
# 用工厂生成 Session
#     async with AsyncSessionLocal() as session:
AsyncSessionLocal = async_sessionmaker(
    async_engine,  # 用哪个引擎连数据库 bind=async_engine
    class_=AsyncSession,  # 指定生成哪种 Session 类，默认生成同步 Session
    expire_on_commit=False  # commit后对象是否过期，方便继续用对象
)


async def get_session():
    """获取一个异步会话（上下文管理器）"""
    async with AsyncSessionLocal() as session:  # 异步上下文管理器，确保 Session 用完自动关闭。
        yield session  # 把 Session 交给调用方，用完后自动关闭。


# ========== 5. 查询（Read） ==========
async def select_all():
    """查询所有部门"""
    async with AsyncSessionLocal() as session:
        # 查询语句
        stmt = select(Department)
        # 异步执行 SQL，返回一个 Result 对象。
        result = await session.execute(stmt)
        # result	原始结果集（类似元组的集合）
        # .scalars()	取第一列（对于 select(Department)，就是 Department 对象）
        # .all()	转成列表，返回所有行
        return result.scalars().all()


async def select_by_id(did):
    """按 ID 查询"""
    async with AsyncSessionLocal() as session:
        # 按主键查询单条记录。
        return await session.get(Department, did)


# ========== 6. 新增（Create） ==========
async def insert(did, dname, note):
    """新增部门"""
    async with AsyncSessionLocal() as session:
        try:
            # 创建一个 ORM 对象（内存里，还没进库）
            dept = Department(did=did, dname=dname, note=note)
            session.add(dept)
            await session.commit()
            print(f"✅ 新增成功：did={did}")
        except Exception as e:
            await session.rollback()
            print(f"❌ 新增失败：{e}")


# ========== 7. 修改（Update） ==========
async def update(did, dname):
    """修改部门名"""
    async with AsyncSessionLocal() as session:
        try:
            dept = await session.get(Department, did)
            if dept:
                dept.dname = dname
                await session.commit()
                print(f"✅ 修改成功：did={did}")
            else:
                print(f"⚠️ 部门 {did} 不存在")
        except Exception as e:
            await session.rollback()
            print(f"❌ 修改失败：{e}")


# ========== 8. 删除（Delete） ==========
async def delete(did):
    """删除部门"""
    async with AsyncSessionLocal() as session:
        try:
            dept = await session.get(Department, did)
            if dept:
                await session.delete(dept)
                await session.commit()
                print(f"✅ 删除成功：did={did}")
            else:
                print(f"⚠️ 部门 {did} 不存在")
        except Exception as e:
            await session.rollback()
            print(f"❌ 删除失败：{e}")


# ========== 9. 主流程 ==========
async def main():
    # 增
    await insert(10, 'test', 'testtest')
    await insert(11, 'dev', 'devteam')
    # 查
    print("\n--- 查询全部 ---")
    for dept in await select_all():
        print(dept)
    # 改
    await update(10, 'test-v2')
    # 查单个
    print("\n--- 查询 did=10 ---")
    print(await select_by_id(10))
    # 删
    await delete(10)
    await delete(11)
    # 再查
    print("\n--- 删除后全部 ---")
    for dept in await select_all():
        print(dept)


if __name__ == '__main__':
    asyncio.run(main())
    # 启动异步事件循环，执行 main() 协程。
    # 作用：创建事件循环、运行协程、关闭事件循环，一站式搞定。
    # 执行步骤：
    # 创建一个新的事件循环（EventLoop）。
    # 把main()协程注册到事件循环。
    # 运行main()，直到它返回。
    # 关闭事件循环。

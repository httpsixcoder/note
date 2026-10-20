from base import Base
from database import engine
from database import SessionLocal
from demo.models import Employee, Department  # 必须要加


# 创建表
def create_table():
    print("注册的表名:", Base.metadata.tables.keys())
    # 创建所有模型对应的表
    Base.metadata.create_all(bind=engine)
    print("表创建成功")


def insert_data():
    db = SessionLocal()
    new_dept = Department(
        name="研发部",  # 部门名称（唯一）
        location="北京总部"  # 部门位置
    )
    db.add(new_dept)
    db.commit()
    # 回填id
    db.refresh(new_dept)
    print(new_dept.id)

def select_data():
    db = SessionLocal()

    # dept=db.get(Department,1)
    # print(dept.id,dept.name,dept.location)

    dept=db.query(Department).filter(Department.id == 1).one()
    print(dept.id, dept.name, dept.location)



if __name__ == '__main__':
    # create_table()
    # insert_data()
    select_data()

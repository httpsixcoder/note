from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from new_demo.sqlalchemy_demo.models.department import Departments


def create_department(db:Session,name:str,location:str|None =None)->Departments:
    dept=Departments(name=name,location=location)
    db.add(dept)
    try:
        db.commit()
        db.refresh(dept)
        print(f"创建部门成功 id={dept.id} name={dept.name} ")
        return dept
    except Exception as e:
        db.rollback()
        raise e


def get_department_by_id(db:Session,dept_id:int)->Departments|None:
    # statement
    stmt=select(Departments).where(Departments.id==dept_id)
    # scalars(stmt)执行查询，返回一个 ORM 对象的结果集。
    # scalar(stmt)执行查询，返回单个值 (str, int, 或单个对象)。
    return db.scalars(stmt).one_or_none()

def get_department_by_name(db:Session,dept_name:str) -> Departments|None:
    stmt=select(Departments).where(Departments.name==dept_name)
    return db.scalars(stmt).one_or_none()
    # 多个同名
    # return db.scalars(stmt).all()

def list_departments(db: Session) -> List[Departments]:
    """查询全部部门"""
    stmt = select(Departments)
    return list(db.scalars(stmt).all())

def update_department(
    db: Session,
    dept_id: int,
    name: str|None = None,
    location: str|None = None
) -> Departments|None:
    """更新部门信息"""
    dept = get_department_by_id(db, dept_id)
    if not dept:
        return None
    if name is not None:
        dept.name = name
    if location is not None:
        dept.location = location
    try:
        db.commit()
        db.refresh(dept)
        print(f"✅ 更新部门成功 id={dept.id}")
        return dept
    except Exception as e:
        db.rollback()
        raise e

def delete_department(db: Session, dept_id: int) -> bool:
    """删除部门（有员工存在会触发外键RESTRICT，删不掉）"""
    dept = get_department_by_id(db, dept_id)
    if not dept:
        return False
    db.delete(dept)
    try:
        db.commit()
        print(f"✅ 删除部门成功 id={dept_id}")
        return True
    except Exception as e:
        db.rollback()
        raise e
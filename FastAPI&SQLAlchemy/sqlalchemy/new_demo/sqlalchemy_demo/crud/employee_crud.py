from datetime import date
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from new_demo.sqlalchemy_demo.models.employee import Employees


def create_employee(
        db: Session,
        name: str,
        department_id: int,
        age: int | None = None,
        hire_date: date | None = None,
) -> Employees:
    emp = Employees(
        name=name,
        department_id=department_id,
        age=age,
        hire_date=hire_date,
    )
    db.add(emp)
    try:
        db.commit()
        db.refresh(emp)
        print(f"创建员工成功 id={emp.id}")
        return emp
    except Exception:
        db.rollback()
        raise

def get_employee_by_id(db: Session, emp_id: int) -> Employees|None:
    """id查询员工（自动带出所属部门）"""
    stmt = select(Employees).where(Employees.id == emp_id)
    return db.scalar(stmt)

def list_employees_by_dept(db: Session, dept_id: int) -> List[Employees]:
    """查询某个部门下所有员工"""
    stmt = select(Employees).where(Employees.department_id == dept_id)
    return list(db.scalars(stmt).all())

def list_all_employees(db: Session) -> List[Employees]:
    """查询全部员工"""
    stmt = select(Employees)
    return list(db.scalars(stmt).all())

def update_employee(
        db: Session,
        emp_id: int,
        name: str|None = None,
        age: str|None = None,
        department_id: str|None = None
) -> Employees|None:
    """修改员工信息、调动部门"""
    emp = get_employee_by_id(db, emp_id)
    if not emp:
        return None
    if name is not None:
        emp.name = name
    if age is not None:
        emp.age = age
    if department_id is not None:
        emp.department_id = department_id
    try:
        db.commit()
        db.refresh(emp)
        print(f"✅ 更新员工成功 id={emp.id}")
        return emp
    except Exception as e:
        db.rollback()
        raise e

def delete_employee(db: Session, emp_id: int) -> bool:
    """删除员工"""
    emp = get_employee_by_id(db, emp_id)
    if not emp:
        return False
    db.delete(emp)
    try:
        db.commit()
        print(f"✅ 删除员工成功 id={emp_id}")
        return True
    except Exception as e:
        db.rollback()
        raise e

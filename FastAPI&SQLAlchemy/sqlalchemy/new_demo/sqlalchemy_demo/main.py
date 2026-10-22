from datetime import date

from crud import (
    create_department,
    get_department_by_name,
    list_departments,
    update_department,
    create_employee,
    get_employee_by_id,
    list_employees_by_dept,
    update_employee,
    delete_employee,
    delete_department
)
from new_demo.sqlalchemy_demo.base import Base
from new_demo.sqlalchemy_demo.database import engine, SessionLocal


def create_tables():
    """建表"""
    Base.metadata.create_all(engine)
    print("建表完成（已存在则跳过）")

if  __name__=="__main__":
    create_tables()

    with SessionLocal() as session:
        # 1. 新增部门（先判断是否存在，避免唯一键冲突）
        dept = get_department_by_name(session, "研发部")
        if not dept:
            dept = create_department(session, "研发部", "北京海淀")

        # 2. 新增员工，绑定上面部门id
        emp1 = create_employee(session, "张三", dept.id, 22, date(2025, 10, 1))
        emp2 = create_employee(session, "李四", dept.id, 25, date(2025, 10, 5))

        # 3. 查询单个员工
        find_emp = get_employee_by_id(session, emp1.id)
        print(f"\n查询员工详情：{find_emp}，所属部门：{find_emp.department.name}")

        # 4. 查询该部门下全部员工
        emp_list = list_employees_by_dept(session, dept.id)
        print(f"\n部门【{dept.name}】下员工列表：")
        for emp in emp_list:
            print(emp)
        # 5. 更新员工（改名、改年龄）
        update_employee(session, emp1.id, "张三三", 23)

        # 6. 更新部门
        update_department(session, dept.id, "北京朝阳")

        # 7. 查询全部部门
        all_dept = list_departments(session)
        print(f"\n所有部门：{all_dept}")

        # 8. 删除员工
        delete_employee(session, emp1.id)
        delete_employee(session, emp2.id)

        # 9. 删除部门
        delete_department(session, dept.id)


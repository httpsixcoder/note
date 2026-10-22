from .department_crud import  (
    create_department,
    get_department_by_id,
    get_department_by_name,
    list_departments,
    update_department,
    delete_department
)
from .employee_crud import (
    create_employee,
    get_employee_by_id,
    list_employees_by_dept,
    list_all_employees,
    update_employee,
    delete_employee
)

__all__ = [
    "create_department",
    "get_department_by_id",
    "get_department_by_name",
    "list_departments",
    "update_department",
    "delete_department",

    "create_employee",
    "get_employee_by_id",
    "list_employees_by_dept",
    "list_all_employees",
    "update_employee",
    "delete_employee",
]

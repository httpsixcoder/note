"""
    数据库模型层
"""
from .department import Department
from .employee import Employee

__all__ = [
    "Department",
    "Employee"
]

"""
    relationship()
        一对一 / 多对一（Many-to-One）：推荐 lazy="joined" 或 lazy="selectin"
        一对多（One-to-Many）：绝对不能用 joined，必用 lazy="selectin"
        多对多：
代码：
from __future__ import annotations

import datetime
from typing import List
from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from db.base import Base

# =====================================================================
# 🌟 核心 1：把中间表升级为完整的模型类 (Association Object)
# =====================================================================
class Enrollment(Base):
    ""选课记录表（多对多关系的中间实体）""
    __tablename__ = "enrollments"

    # 复合主键：学生ID + 课程ID
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), primary_key=True
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True
    )
    
    # 🌟 额外的业务字段
    score: Mapped[int | None] = mapped_column(Integer, default=None) # 成绩
    enroll_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today) # 报名时间

    # 关联回学生和课程（多对一）
    student: Mapped["Student"] = relationship(back_populates="enrollments", lazy="joined")
    course: Mapped["Course"] = relationship(back_populates="enrollments", lazy="joined")


# =====================================================================
# 🌟 核心 2：Student 模型
# =====================================================================
class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))

    # 1. 与中间表的 1 对多关系
    enrollments: Mapped[List["Enrollment"]] = relationship(
        back_populates="student",
        lazy="selectin",
        cascade="all, delete-orphan" # 删除学生时，自动删除其选课记录【 级联删除,清理孤儿数据】
    )

    # 2. 🌟 关联代理：让你依然可以使用 student.courses 直接获取课程列表
    courses: AssociationProxy[List["Course"]] = association_proxy(  
        target_collection="enrollments",
        attr="course",
        creator=lambda course: Enrollment(course=course) # 快捷创建中间表记录的方法
    )


# =====================================================================
# 🌟 核心 3：Course 模型
# =====================================================================
class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))

    # 1. 与中间表的 1 对多关系
    enrollments: Mapped[List["Enrollment"]] = relationship(
        back_populates="course",
        lazy="selectin",
        cascade="all, delete-orphan" # 级联删除,清理孤儿数据
    )

    # 2. 关联代理：让你依然可以使用 course.students 直接获取学生列表
    # 告诉 IDE，course.students 返回的是一个包含 Student 对象的列表。
    students: AssociationProxy[List["Student"]] = association_proxy(   
        # 告诉代理，你要操作的数据源头是本类中的 enrollments 列表。
        target_collection="enrollments",
        # 提取属性：告诉代理，当你读取数据时，请从 enrollments 列表里的每一个 Enrollment 对象中，把 .student 属性拿出来。
        # 即print(course.students) 时，代理会自动把 enrollments 里的每一个学生提取出来，拼成一个列表给你。
        attr="student",
        # 写入拦截器：当你试图用 course.students.append(new_student) 添加学生时，因为 students 只是个代理，不能直接 append
        # 这个时候，代理会自动调用 creator 这个 lambda 函数。
        # 它会把你要添加的 new_student 包装成一个 Enrollment 对象（Enrollment(student=new_student)），
        # 然后再悄悄塞进 enrollments 列表中。
        creator=lambda student: Enrollment(student=student)
    )
"""

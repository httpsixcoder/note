"""
    测试：fFastAPI和SQLAlchemy集合而案例
"""

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from table_2_models import Departments, Employees
from database import SessionLocal, engine

app = FastAPI()


# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 部门相关接口
@app.post("/departments/")
def create_department(name: str, location: str, db: Session = Depends(get_db)):
    db_department = Departments(name=name, location=location)
    db.add(db_department)
    db.commit()
    # 回填ID
    db.refresh(db_department)
    return db_department


@app.get("/departments/")
def read_departments(db: Session = Depends(get_db)):
    return db.query(Departments).all()


@app.get("/departments/get/{department_id}")
def read_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(Departments).filter(Departments.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@app.delete("/departments/delete/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    dept=db.get(Departments,department_id)
    db.delete(dept)
    db.commit()
    return {"message":"Department deleted"}


@app.put("/departments/update")
def update_department(id:int,name:str,location:str,db: Session = Depends(get_db)):
    dept=db.get(Departments,id)
    dept.name = name
    dept.location = location
    db.commit()
    return {"message":"Department updated"}

if __name__ == "__main__":
    # 直接在代码中启动uvicorn服务器
    uvicorn.run(
        app="main:app",  # 指定要运行的FastAPI应用实例
        host="0.0.0.0",  # 允许外部访问（本地可通过127.0.0.1或localhost访问）
        port=8000,  # 端口号
        reload=True  # 开发模式：代码修改后自动重启（生产环境需去掉）
    )

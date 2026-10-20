"""
    路由分发功能的核心文件
"""
import uvicorn
from fastapi import FastAPI

from routers import user, item

# 创建FastAPI的核心对象

app=FastAPI()

# 引入两个路由对象
app.include_router(user.router)
app.include_router(item.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
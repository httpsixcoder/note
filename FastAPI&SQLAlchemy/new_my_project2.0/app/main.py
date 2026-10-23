from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1 import api_router # 使用聚合路由
from app.core.database import engine
from app.core.exceptions import BusinessException
from db.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ===================== 重要分割线 =====================
    # 👉【仅第一次本地初始化项目时打开】
    # 👉【第二次启动、测试、生产环境：必须注释下面这一段！！】
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    # =====================================================

    yield  # 服务运行阶段，接收请求
    # 服务关闭后，优雅销毁数据库连接池（永久保留，不用注释）
    await engine.dispose()


app = FastAPI(
    title="企业级 FastAPI 架构",
    lifespan=lifespan
)


# ================= 全局异常拦截器 =================
@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=400,
        content={"code": 400, "message": exc.message, "data": None}
    )
# ================= 全局兜底未知异常 =================（生产必备，不返回原始堆栈给前端）
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 真实项目这里要写日志：logger.error
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部异常",
            "data": None
        }
    )

# 挂载路由
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True,log_level="info")

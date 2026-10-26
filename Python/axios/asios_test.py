from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ⚠️ 必须在挂载路由之前添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    # 学习阶段允许所有来源，生产环境这里要写死你的前端域名（如 "https://www.mywebsite.com"）
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HelloReq(BaseModel):
    content: str  # 接收叫 content 的字段


@app.get("/hello")
def hello():
    return {"code": 1000, "content": "hello111"}


@app.post("/hello")
def hello(req: HelloReq):
    print(req.content)
    print("123")
    return {"code": 666, "content": "hello666"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

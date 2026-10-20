"""
    测试：FastAPI的使用
"""
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# 创建FastAPI的核心对象
app = FastAPI()


# 路径处理装饰器，所装饰的函数处理的请求必须满足以下条件：请求方式-》get，请求路径-》/helloworld
@app.get("/helloworld")
# 路径处理函数
def start():
    # return的数据先转换为json，在座位响应体相应到浏览器
    return {"message": "hello world"}
    # # 前端返回null
    # return {"message":None}
    # # 前端返回true
    # return {"message":True}


# 测试响应体
@app.get("/test/response")
def test_response():
    # return "helloworld" # helloworld
    # return 100 # 100
    # return True # True -> true False -> false
    # return {"name":"张三","age":23,"gender":"male" #{"name":"张三","age":23,"gender":"male"}
    return ["zs", "ls", "ww"]  # ["zs","ls","ww"]


# 测试路径参数
# param/path/admin/123456
@app.get("/param/param/{username}/{password}/{age}")
def test_param_path(username: str, password: str, age: int = None):
    return {"username": username, "password": password, "age": age}


# 测试查询参数
# param/query?name=admin&&age=123456
@app.get("/param/query")
def test_param_query(name: str = "小明", age: int = None):
    return {"name=": name, "age": age}


# 测试请求体参数
# 路径：/param/body，请求体参数：{username:admin,password:123456}

# 模型类
class UserInFo(BaseModel):
    username: str
    password: str = None


@app.post("/param/body")
def test_param_body(user_info: UserInFo):
    return {"username": user_info.username, "password": user_info.password}


@app.post("/param/{name}/{age}")
async def test_param(name: str, age: int,gender:str,user_info: UserInFo):
    return {"name": name, "age": age, "gender": gender, "username": user_info.username, "password": user_info.password}

if __name__ == "__main__":
    uvicorn.run(
        app="fastapi_test:app",
        # host="0.0.0.0", # 任何人都可以访问
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

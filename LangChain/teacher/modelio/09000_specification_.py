"""

"""
import asyncio
# 标准库，用来把异步生成器装饰成异步上下文管理器。这是实现资源“用时开启，用完释放”的核心工具。
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


def create_llm() -> BaseChatModel:
    return init_chat_model(
        "openai:qwen-flash",
        temperature=0.2,  # 抽取/分类用 0~0.3；创意写作才调高
        timeout=30,  # 秒，必须有，否则挂死
        max_retries=2,  # 网络层重试（≠ Agent 中间件的模型重试）
    )


async def get_master_intro(llm: BaseChatModel) -> None:
    try:
        resp = await llm.ainvoke([
            SystemMessage("你是哲学家"),
            HumanMessage("简单介绍你自己，少于50字"),
        ])
    except Exception as e:
        print(e)
        return
    print(resp.content)  # 纯文本（最常用）


@asynccontextmanager
async def lifespan():
    llm = create_llm()
    yield llm


async def main():
    async with lifespan() as llm:
        await get_master_intro(llm)


if __name__ == "__main__":
    asyncio.run(main())

"""
FastAPI ：
    
    # 定义 FastAPI 的生命周期（启动时创建 llm）
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.llm = create_llm() # 把模型挂载到 app 实例上
    yield
    # 释放资源

app = FastAPI(lifespan=lifespan)

# 写一个依赖项，让路由可以拿到 llm
def get_llm(request: Request) -> BaseChatModel:
    return request.app.state.llm

@app.get("/ask")
async def ask_philosopher(question: str, llm: BaseChatModel = Depends(get_llm)):
    resp = await llm.ainvoke([HumanMessage(question)])
    return {"answer": resp.content}
"""

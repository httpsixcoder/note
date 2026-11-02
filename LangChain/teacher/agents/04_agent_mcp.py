"""

"""
import asyncio

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient


load_dotenv()
# 创建MCP的客户端对象
client = MultiServerMCPClient(
    {
        "12306-mcp": {
            "transport": "streamable_http",
            "url": "https://mcp.api-inference.modelscope.net/40c030f21d2a43/mcp"
        }
    }
)


# 调用MCP工具
async def agent_invoke_mcp():
    # 获取MCP服务器中提供的工具
    tools = await client.get_tools()

    llm = init_chat_model("openai:qwen-flash")

    # 创建智能体
    agent = create_agent(
        model=llm,
        tools=tools,
    )
    # 异步调用智能体
    result = await agent.ainvoke({
        "messages": [
            ("user", "今天从北京到海城的车票有哪些，以表格的方式输出")
        ]
    })
    print(result)
    print(result["messages"][-1].content)


if __name__ == '__main__':
    asyncio.run(agent_invoke_mcp())

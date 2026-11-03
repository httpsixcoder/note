"""
    测试：流式执行图对象
"""
import operator
import time
from typing import TypedDict, List, Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime

load_dotenv()


class MyState(TypedDict):
    message: Annotated[List[BaseMessage], operator.add]
    current_step: str


def input_node(state: MyState):
    return {
        "message": [HumanMessage("请帮我写一段Python")],
        "current_step": "input_step"
    }


def processing_node(state: MyState, runtime: Runtime):
    # def processing_node(state: MyState):
    writer = runtime.stream_writer
    steps = ["正在分析意图...", "正在检索知识库...", "正在构建Prompt..."]
    for i, step in enumerate(steps, start=1):
        writer({
            "step_index": i,
            "description": step,
            "timestamp": time.time()
        })
    return {
        "current_step": "processing_step"
    }


def generation_node(state: MyState):
    llm = init_chat_model("openai:qwen-flash")
    response = llm.invoke(state["message"])
    return {
        # "message": [response.content],
        "current_step": "generation_step"
    }
    # # message
    # for chunk in llm.stream(state["message"]):
    #     print(chunk.content, end="", flush=True)
    # return {
    #     "message": list(llm.stream(state["message"])),  # 它会捕获每一个 chunk
    #     "current_step": "generation_step"
    # }


builder = StateGraph(MyState)
builder.add_node(input_node)
builder.add_node(processing_node)
builder.add_node(generation_node)

builder.set_entry_point("input_node")
builder.add_edge("input_node", "processing_node")
builder.add_edge("processing_node", "generation_node")

graph = builder.compile()
# 流式执行图对象
# values：每一个节点执行后，流式输出完整的状态
# updates（默认）：每一个节点执行后，流式输出状态中更新的属性
# custom：流式输出节点内部的自定义数据
# message：在任何调用了LLM的节点中，流式输出两元数组：（LLM Token，metadata）
# debug：流式输出图对象节点执行的步骤
# 混合模式：使用以上五种模式的一种或者多种随意组合。
# for token in graph.stream({}):
for token in graph.stream({}, stream_mode="message"):
    # for token in graph.stream({},stream_mode=["custom","update"]):
    print(token)

"""
values:
{'message': [HumanMessage(content='请帮我写一段Python', additional_kwargs={}, response_metadata={})], 'current_step': 'input_step'}
{'message': [HumanMessage(content='请帮我写一段Python', additional_kwargs={}, response_metadata={})], 'current_step': 'processing_step'}
{'message': [HumanMessage(content='请帮我写一段Python', additional_kwargs={}, response_metadata={}), '当然可以！请告诉我您需要什么样的 Python 代码？例如：\n\n- 一个简单的计算器\n- 读取和处理文件（如 CSV、JSON）\n- 爬虫（网页数据抓取）\n- 数据分析或绘图（使用 pandas、matplotlib）\n- 函数或类的定义\n- 命令行工具\n- 或其他特定需求\n\n请描述一下您的具体需求，我会为您编写一段清晰、可运行的 Python 代码。'], 'current_step': 'generation_step'}
updates：
{'input_node': {'message': [HumanMessage(content='请帮我写一段Python', additional_kwargs={}, response_metadata={})], 'current_step': 'input_step'}}
{'processing_node': {'current_step': 'processing_step'}}
{'generation_node': {'message': ['当然可以！请告诉我您需要什么样的 Python 代码？例如：\n\n- 您想要实现什么功能？（如：文件操作、数据处理、网络请求、图形界面等）\n- 是否有特定的库或语法要求？\n- 需要处理的数据类型或格式？\n\n举个例子，如果您想要一个简单的程序来读取文本文件并统计单词数量，我可以这样写：\n\n```python\ndef count_words(filename):\n    try:\n        with open(filename, \'r\', encoding=\'utf-8\') as file:\n            text = file.read().lower()\n            # 去除标点符号并分割成单词\n            words = \'\'.join(c if c.isalpha() or c.isspace() else \' \' for c in text).split()\n            word_count = len(words)\n            print(f"文件中总共有 {word_count} 个单词。")\n            return word_count\n    except FileNotFoundError:\n        print(f"文件 {filename} 未找到。")\n        return 0\n\n# 调用函数\ncount_words("example.txt")\n```\n\n请告诉我您的具体需求，我会为您量身定制一段实用的 Python 代码！'], 'current_step': 'generation_step'}}
custom：
{'step_index': 1, 'description': '正在分析意图...', 'timestamp': 1793691062.2666342}
{'step_index': 2, 'description': '正在检索知识库...', 'timestamp': 1793691062.2666342}
{'step_index': 3, 'description': '正在构建Prompt...', 'timestamp': 1793691062.2666342}
message：
当然可以！请告诉我您需要什么样的 Python 代码？例如：

- 一个简单的计算器？
- 读取和处理文件？
- 数据分析或绘图？
- 爬虫程序？
- 函数或类的定义？
- 其他特定功能？

请提供具体需求，我会为您编写一段清晰、可运行的 Python 代码。
debug：
{'step': 1, 'timestamp': '2026-11-03T07:33:13.890425+00:00', 'type': 'task', 'payload': {'id': '59c245f3-286f-2e93-8ebb-afbbc7d2128a', 'name': 'input_node', 'input': {'message': []}, 'triggers': ('branch:to:input_node',)}}
{'step': 1, 'timestamp': '2026-11-03T07:33:13.891426+00:00', 'type': 'task_result', 'payload': {'id': '59c245f3-286f-2e93-8ebb-afbbc7d2128a', 'name': 'input_node', 'error': None, 'result': {'message': [HumanMessage(content='请帮我写一段Python', additional_kwargs={}, response_metadata={})], 'current_step': 'input_step'}, 'interrupts': []}}
{'step': 2, 'timestamp': '2026-11-03T07:33:13.891426+00:00', 'type': 'task', 'payload': {'id': 'd31b34df-0da6-80da-1a59-b71d7fdbe749', 'name': 'processing_node', 'input': {'message': [HumanMessage(content='请帮我写一段Python', additional_kwargs={}, response_metadata={})], 'current_step': 'input_step'}, 'triggers': ('branch:to:processing_node',)}}
{'step': 2, 'timestamp': '2026-11-03T07:33:13.892425+00:00', 'type': 'task_result', 'payload': {'id': 'd31b34df-0da6-80da-1a59-b71d7fdbe749', 'name': 'processing_node', 'error': None, 'result': {'current_step': 'processing_step'}, 'interrupts': []}}
{'step': 3, 'timestamp': '2026-11-03T07:33:13.892425+00:00', 'type': 'task', 'payload': {'id': 'bf64ec6b-c3d9-ebc9-214c-9c57235261ec', 'name': 'generation_node', 'input': {'message': [HumanMessage(content='请帮我写一段Python', additional_kwargs={}, response_metadata={})], 'current_step': 'processing_step'}, 'triggers': ('branch:to:generation_node',)}}
{'step': 3, 'timestamp': '2026-11-03T07:33:18.016010+00:00', 'type': 'task_result', 'payload': {'id': 'bf64ec6b-c3d9-ebc9-214c-9c57235261ec', 'name': 'generation_node', 'error': None, 'result': {'message': ['当然可以！请告诉我您需要什么样的 Python 代码？例如：\n\n- 一个简单的计算器？\n- 读取和处理文件？\n- 数据分析（如使用 pandas）？\n- 网络爬虫？\n- 图形界面（GUI）？\n- 或者其他特定功能？\n\n请提供具体需求，我会为您编写一段清晰、可运行的 Python 代码。'], 'current_step': 'generation_step'}, 'interrupts': []}}
"""

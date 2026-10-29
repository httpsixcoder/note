"""
    提示词模板
"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = init_chat_model("openai:qwen-flash")
#
# prompt_template1 = ChatPromptTemplate.from_template("请评价 {product}的优缺点，包括{aspect1}和{aspect2}.")
# prompt_template2 = ChatPromptTemplate.from_messages([
#     {"role": "system", "content": "你是一个专业的评论员"},
#     {"role": "user", "content": "请评价{product}的优缺点, 包括{aspect1}和{aspect2}. "}
# ])
prompt_template3 = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的评论员"),
    # 放在 human 后，会破坏多轮结构
    # MessagesPlaceholder("history", optional=True),   # 放历史消息
    ("user", "请评价{product}的优缺点, 包括{aspect1}和{aspect2}. ")
])
# 不行，无法解析字符串
# prompt_template4 = ChatPromptTemplate.from_messages([
#     SystemMessage(content="你是一个专业的评论员"),
#     HumanMessage(content="请评价{product}的优缺点, 包括{aspect1}和{aspect2}. ")
# ])
#
# prompt1 = prompt_template1.invoke({
#     "product": "拯救者Y90000",
#     "aspect1": "性能",
#     "aspect2": "性价比"
# })
# prompt2 = prompt_template2.invoke({
#     "product": "拯救者Y90000",
#     "aspect1": "性能",
#     "aspect2": "性价比"
# })
prompt3 = prompt_template3.invoke({
    "product": "拯救者Y90000",
    "aspect1": "性能",
    "aspect2": "性价比"
})
# prompt4 = prompt_template4.invoke({
#     "product": "拯救者Y90000",
#     "aspect1": "性能",
#     "aspect2": "性价比"
# })
# print("=======================1=====================================")
# result = llm.invoke(prompt1)
# print(result.content)
# print("=======================2=====================================")
# result = llm.invoke(prompt2)
# print(result.content)
print("=======================3=====================================")
# 推荐
result = llm.invoke(prompt3)
# result = prompt_template3.invoke({
#     "product": "拯救者Y90000",
#     "aspect1": "性能",
#     "aspect2": "性价比"
# })
print(result.content)
# print("=======================4=====================================")
# 无法解析字符串
# result = llm.invoke(prompt4)
# print(result.content)
print("============================================================")

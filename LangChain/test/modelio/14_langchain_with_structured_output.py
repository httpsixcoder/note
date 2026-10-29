from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

load_dotenv()

llm = init_chat_model("openai:qwen-flash")


class JieRiItem(BaseModel):
    name: str = Field(description="节日名称")
    description: str = Field(description="该节日的描述")


class JieRi(BaseModel):
    festivals: list[JieRiItem] = Field(description="节日和描述的结构化列表")


# llm = llm.with_structured_output(schema=JieRi)
# resp = llm.invoke([
#     HumanMessage("查询一年中的重要节日，以及节日描述")
# ])
# 返回一个JieRi对象而非Json
resp = llm.with_structured_output(schema=JieRi).invoke([
    HumanMessage("查询一年中的重要节日，以及节日描述")
])
# 3. 此时 resp 已经是 JieRi 对象了，不需要 .content！
# print(type(resp)) #<class '__main__.JieRi'>
# print(resp)  # 直接打印对象
# print(resp.festivals)  # 可以像对象一样直接调用属性
# print(resp.festivals[0].name)  # 可以像对象一样直接调用属性
# print(resp.festivals[0].description)# 可以像对象一样直接调用属性
print("----------------------------")
# print(resp.festivals[1].name)  # 可以像对象一样直接调用属性
# print(resp.festivals[1].description)# 可以像对象一样直接调用属性
for item in resp.festivals:
    print(item.name)
    print(item.description)
    print("=================")

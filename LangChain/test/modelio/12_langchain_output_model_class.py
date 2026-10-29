from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from pydantic import Field, BaseModel

load_dotenv()


llm=init_chat_model("openai:qwen-flash")

class Prime(BaseModel):
    prime: list[int] = Field(description="存储所有的素数")
    count: int = Field(description="素数的个数")


parser = JsonOutputParser(pydantic_object=Prime)

# print(parser.get_format_instructions())

result=llm.invoke([
    SystemMessage(parser.get_format_instructions()),
    HumanMessage("帮我查询1-500之间所有的素数以及素数的数量")
])
print(result.content)
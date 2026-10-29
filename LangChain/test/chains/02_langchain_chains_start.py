from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
# llm
llm = init_chat_model("openai:qwen-flash")
# template
prompt_template = ChatPromptTemplate.from_messages([("user", "将{text}翻译为英文")])
# parser
parser = StrOutputParser()
# data
data = {
    "text": "你好"
}
# chains
chains = prompt_template | llm | parser
result = chains.invoke(data)
print(result)



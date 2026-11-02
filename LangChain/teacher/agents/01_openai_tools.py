"""
    测试：调用原生openai，调用tool
"""
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
client = OpenAI()

# 1. 通过JSON结构定义工具，包括工具名称，描述，参数等
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get today's weather for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称, e.g. San Francisco",
                    },
                    "date": {
                        "type": "string",
                        "description": "想要查询的天气的日期, e.g. 2023-12-25"
                    }
                },
                "required": ["city", "date"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]


def get_weather(city, date):
    return f"{city} on {date} is cloudy with a chance of rain."


messages = [
    {"role": "user", "content": "What is the weather like in 北京 on 2024-12-25?"}
]

# 2. Prompt the model with tools defined
response = client.chat.completions.create(
    model="qwen-flash",
    messages=messages,
    tools=tools,
)

messages.append(response.choices[0].message)

for tool_call in response.choices[0].message.tool_calls or []:
    if tool_call.function.name == "get_weather":
        # 3. 执行工具函数的逻辑
        args = json.loads(tool_call.function.arguments)
        weather = get_weather(args["city"], args["date"])

        # 4. 将工具函数的执行结果添加到消息列表中
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps({"weather": weather}),
            }
        )

response = client.chat.completions.create(
    model="qwen-flash",
    messages=messages,
    tools=tools,
)

# 5. 模型会根据工具函数的执行结果，生成最终的回复
print(response.choices[0].message.content)

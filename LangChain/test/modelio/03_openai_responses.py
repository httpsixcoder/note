"""
    测试：使用OpenAI原生API（Responses）调用模型
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(verbose=True)

# 获取模型对象
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASH_URL"),
)
result = client.responses.create(
    model="qwen-flash",
    input=[
        {"role": "system", "content": "你是一个专业的笑话专家"},
        {"role": "user", "content": "给我讲个笑话"}
    ]
)

print(result.output[0].content[0].text)
"""
Response(
    id="resp_d6e513d7-28f4-93e1-bcfb-bd942bc84b9c",
    access_programs=None,
    created_at=1793101330.0,
    error=None,
    incomplete_details=None,
    instructions=None,
    metadata={},
    model="qwen-flash",
    object="response",
    output=[
        ResponseOutputMessage(
            id="msg_6237716a-78f6-4b9e-9e62-de1cba21d2db",
            content=[
                ResponseOutputText(
                    annotations=[],
                    text="（推了推眼镜，清了清嗓子）  \n\n今天我遇到个特别搞笑的事——  \n\n我朋友去应聘程序员，面试官问他：“你有什么特长？”  \n\n他自信满满地说：“我会预测未来！”  \n\n面试官一愣：“哦？那你说说，明天会下雨吗？”  \n\n他说：“不会。”  \n\n面试官笑了：“那你预测错了，明天下雨。”  \n\n朋友淡定地掏出手机：“你看，我刚查了天气预报，明天确实不下雨。”  \n\n面试官：……（沉默三秒）“那你刚才说‘不会’的时候，怎么不直接说‘查了天气预报’？”  \n\n朋友耸耸肩：“因为那样就不是‘预测’了，是‘查表’。”  \n\n（停顿两秒，突然凑近）  \n所以……你觉得我这笑话，是预测对了，还是查表成功了？ 😏",
                    type="output_text",
                    logprobs=None,
                )
            ],
            role="assistant",
            status="completed",
            type="message",
            phase=None,
        )
    ],
    parallel_tool_calls=True,
    temperature=1.0,
    tool_choice="auto",
    tools=[],
    top_p=1.0,
    background=False,
    completed_at=1793101331.0,
    conversation=None,
    max_output_tokens=None,
    max_tool_calls=None,
    moderation=None,
    previous_response_id=None,
    prompt=None,
    prompt_cache_diagnostics=None,
    prompt_cache_key=None,
    prompt_cache_options=None,
    prompt_cache_retention=None,
    reasoning=None,
    safety_identifier=None,
    service_tier="default",
    status="completed",
    text=None,
    top_logprobs=0,
    truncation=None,
    usage=ResponseUsage(
        input_tokens=53,
        input_tokens_details=InputTokensDetails(
            cache_write_tokens=None, cached_tokens=0
        ),
        output_tokens=184,
        output_tokens_details=OutputTokensDetails(reasoning_tokens=0),
        total_tokens=237,
        x_details=[
            {
                "input_tokens": 53,
                "output_tokens": 184,
                "total_tokens": 237,
                "prompt_tokens_details": {"cached_tokens": 0},
                "x_billing_type": "response_api",
            }
        ],
    ),
    user=None,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    store=True,
    billing=None,
)

"""




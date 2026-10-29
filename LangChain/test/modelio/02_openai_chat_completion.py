"""
    测试：使用OpenAI原生API（ChatCompletions）调用模型
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(verbose=True)

# 获取模型对象
client =OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASH_URL"),
)
result=client.chat.completions.create(
    model="qwen-flash",
    messages=[
        {"role":"user","content":"给我讲个笑话"}
    ]
)

print(result.choices[0].message.content)


"""
ChatCompletion(
    id="chatcmpl-65089372-c3bf-97f6-8cd3-6190a48918ee",
    choices=[
        Choice(
            finish_reason="stop",
            index=0,
            logprobs=None,
            message=ChatCompletionMessage(
                content="当然可以！来一个轻松的：\n\n有一天，小明去面试，面试官问他：“你有什么特长？”\n\n小明想了想，认真地说：“我会预测未来。”\n\n面试官笑了笑：“哦？那你预测一下，你什么时候能被录用？”\n\n小明淡定地回答：“这个嘛……我预测我不会被录用。”\n\n面试官一愣，随即笑着说：“你被录用了！我们正需要一个有自知之明的人。”\n\n😂\n\n（温馨提示：笑完记得工作别太“预测”啊～）",
                refusal=None,
                role="assistant",
                annotations=None,
                audio=None,
                function_call=None,
                tool_calls=None,
            ),
        )
    ],
    created=1793100355,
    model="qwen-flash",
    object="chat.completion",
    metadata=None,
    moderation=None,
    service_tier=None,
    system_fingerprint=None,
    usage=CompletionUsage(
        completion_tokens=109,
        prompt_tokens=12,
        total_tokens=121,
        completion_tokens_details=None,
        prompt_tokens_details=PromptTokensDetails(
            audio_tokens=None,
            cache_write_tokens=None,
            cached_tokens=0,
            image_tokens=None,
            text_tokens=None,
        ),
    ),
)
"""
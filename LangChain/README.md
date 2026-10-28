# LangChain 1.x 学习笔记（2026 版 · 面向 AI 应用开发岗）

> 基线：`langchain` 1.x（Python 3.12）｜对照官方文档 <https://docs.langchain.com/oss/python/langchain/overview>
> 本笔记定位：**课程文档讲"怎么用"，本笔记补"为什么这么用、什么时候别用、上生产会踩什么坑"**。
> 标注约定：✅ 已按官方文档核对过 API ｜ ⚠️ 版本敏感，动手前先 `pip show` 看版本 ｜ 🔍 需核实

---

## 0. 先看差异：这份笔记和课程文档的 8 个不同

| # | 课程文档 | 本笔记的做法 | 为什么 |
|---|---|---|---|
| 1 | 工具/中间件写得很透 | 补充**结构化输出的 3 种策略**（`ToolStrategy`/`ProviderStrategy`/`with_structured_output`） | Agent 里 `response_format` 才是 v1 的正解，用法和裸模型不同 |
| 2 | 中间件只讲 2 个（Summarization、HITL） | 补齐**重试/降级/调用上限/PII/工具错误**等 14 个内建中间件 | 生产环境的可靠性全靠这一层 |
| 3 | 记忆只讲 `InMemorySaver` | 补 `SqliteSaver`/`PostgresSaver` 与**多租户 thread_id 设计** | `InMemorySaver` 重启即丢，上线必换 |
| 4 | 未讲流式细节 | 补 `stream_mode` 的 4 种取值与 SSE 落地 | 面试高频，"流式怎么做"几乎必问 |
| 5 | RAG 讲链路，未讲**评估** | 补 gold set + recall@k + 失败归因 | 决定你能不能算出"提升了多少" |
| 6 | 未讲成本与延迟 | 补 token 统计、缓存、模型路由 | 简历上唯一能写的数字来源 |
| 7 | 未讲安全边界 | 补 PII、工具白名单、prompt injection、HITL | 2026 年 Agent 岗必问 |
| 8 | 未提 Deep Agents | 补 `create_deep_agent` 与"何时别用多 Agent" | 少走弯路：多 Agent 不是默认架构 |

---

## 1. LangChain 到底解决什么问题

### 1.1 一句话
**它把「模型 + 提示词 + 工具 + 检索 + 状态 + 重试」抽象成可组合对象（Runnable）**，让你换模型、加工具、加记忆时不重写业务代码。

### 1.2 与竞品的关系（选型表）

| 方案 | 适合 | 不适合 | 一句话 |
|---|---|---|---|
| 原生 SDK（openai / anthropic） | 单轮调用、只用一个厂商、追求最小依赖 | 多工具、多轮、要换厂商 | 最轻，但每加一个能力都要自己写循环 |
| **LangChain 1.x** | 应用层：RAG、工具调用、结构化输出、快速迭代 | 复杂分支流程、强状态机 | **Agent = Model + Harness**，harness 就是它 |
| LangGraph | 有环、有分支、要人工审核、要持久化恢复 | 简单线性流程（杀鸡用牛刀） | 底层运行时，`create_agent` 就建在它上面 |
| LlamaIndex | 文档密集 RAG、索引策略多 | 通用 Agent 编排 | RAG 特化，LangChain 更通用 |
| Dify / Coze | 业务同学自助搭 | 要写自定义逻辑、要控成本与延迟 | 演示快，深水区要落代码 |

> ⚠️ 面试陷阱：说"我用 LangChain 做 RAG"会被追问"那 LangChain 帮你做了什么"。答：**统一模型接口、Runnable 组合、工具 schema 生成与调用循环、检索器抽象、checkpoint 持久化**。答不出就是"调包"。

### 1.3 v1 的三个关键变化（必须知道，否则看旧教程会乱）

1. **`create_agent` 成为标准入口**，取代 `langgraph.prebuilt.create_react_agent`。
2. **`content_blocks` 统一多厂商消息内容**（text / reasoning / tool_call / image…），不再各自解析 `response_metadata`。
3. **命名空间精简**：`langchain` 只留核心；旧的 chains、retrievers、hub、indexing API 全部搬到 **`langchain-classic`**。

```python
# v1 命名空间（推荐记这一套）
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
from langchain.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage, trim_messages
from langchain.tools import tool
```

```python
# 旧代码迁移：import 只改包名，逻辑不变
from langchain.chains import RetrievalQA          # 旧
from langchain_classic.chains import ...          # 新（需 pip install langchain-classic）
```

### 1.4 安装（最小集 → 生产集）

```bash
# 最小可跑
pip install -U langchain langchain-openai python-dotenv

# RAG
pip install -U langchain-text-splitters langchain-milvus langchain-community

# Agent 生态
pip install -U langgraph langchain-mcp-adapters deepagents

# 可观测
pip install -U langsmith
```
⚠️ `langchain`、`langchain-core`、`langchain-openai` 三者版本必须兼容，别手动 pin 单个包；用 `uv pip sync requirements.txt` 或 `uv add` 让解析器决定。

---

## 2. Model I/O

### 2.1 建模型：`init_chat_model` vs 厂商类

```python
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    "openai:gpt-4.1-mini",     # "provider:model" 写法最省事
    temperature=0.2,           # 抽取/分类用 0~0.3；创意写作才调高
    timeout=30,                # 秒，必须有，否则挂死
    max_retries=2,             # 网络层重试（≠ Agent 中间件的模型重试）
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)
```

**注意：base_url和api_key会自动获取环境变量中的OPENAI_API_KEY和OPENAI_BASE_URL（可省略）**

| 方式 | 优点 | 缺点 | 用在哪 |
|---|---|---|---|
| `init_chat_model("openai:gpt-4.1")` | 改字符串即换厂商，配置化 | 个别厂商私有参数不支持 | **默认选它** |
| `ChatOpenAI(...)` 等具体类 | 参数最全、类型提示最好 | 换厂商要改代码 | 需要厂商私有能力时 |

⚠️ 常见坑：`temperature` 不是所有模型都支持（部分推理模型直接报错）；`max_tokens` 是**输出上限**，不是输入。

### 2.2 消息类型（这是 LangChain 的"HTTP 协议"）

| 类 | 作用 | 关键字段 |
|---|---|---|
| `SystemMessage` | 角色设定、规则 | `content` |
| `HumanMessage` | 用户输入 | `content`（可多模态块） |
| `AIMessage` | 模型输出 | `content`、`tool_calls`、`usage_metadata`、`content_blocks` |
| `ToolMessage` | 工具执行结果 | `content`、`tool_call_id`（**必须与请求配对**） |

```python
resp = llm.invoke([
    SystemMessage("你是严谨的技术文档助手，不确定就说不确定。"),
    HumanMessage("LangChain 的 checkpoint 是什么？"),
])
print(resp.content)                 # 纯文本（最常用）
print(resp.usage_metadata)          # {'input_tokens':..,'output_tokens':..,'total_tokens':..}
print(resp.tool_calls)              # [{'name':'..','args':{..},'id':'..'}] 仅当调工具
```

```python
# v1 新姿势：content_blocks 统一解析多厂商内容（推理、引用、内置工具）
for block in resp.content_blocks:
    if block["type"] == "text":
        print(block["text"])
    elif block["type"] == "reasoning":
        print("思考：", block["reasoning"])
```
⚠️ `content_blocks` 支持范围：Anthropic / AWS / OpenAI / Google GenAI / Ollama 已支持，其余厂商逐步跟进。**别在国产模型上假设它有 reasoning 块**。

### 2.3 四种调用方式

| 方法 | 语义 | 典型场景 | 坑 |
|---|---|---|---|
| `.invoke(x)` | 同步、阻塞、返回完整结果 | 脚本、后台批处理 | 在 async 函数里调用会阻塞事件循环 |
| `.batch([x1,x2,...])` | 并发批处理 | 跑评测集、离线生成 | 注意 rate limit，需 `config={"max_concurrency": 5}` |
| `.stream(x)` | 逐 token 返回 | 交互式 UI | 只流"文本"，工具调用要等整轮 |
| `.ainvoke/.astream/.abatch` | 异步版 | **FastAPI / 高并发服务** | 全链路都要 async，混用同步库会退化 |

**invoke和ainvoke返回的是AIMessage对象**

**stream和astream返回的是一个生成器（Generator）or 异步生成器（AsyncGenerator）**

**batch和abatch返回的是List[AIMessage]对象**

```python
for chunk in llm.stream("用三句话解释 RAG"):
    print(chunk.content, end="", flush=True)
```

### 2.4调用本地模型

**隐式调用：`base_url="http://localhost:11434"`【ollama本地服务，默认接口11434】**

```python
"""
    测试：调用本地模型，通过ollama调用的n3:8b
"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from openai import base_url

load_dotenv()

llm = init_chat_model(
    # 需要配置本地ollama的设置
    # "ollama:qwen3:8b",
    "ollama:deepseek-r1:7b",
    # 默认可以不写隐式获取，，如果端口号改变则需要显式写出【ollama端口号11434】
    # base_url="http://localhost:11434",

)
result = llm.invoke([
    HumanMessage("你好")
])
print(result.content)
```

---

## 3. Prompt 与输出解析

### 3.1 `ChatPromptTemplate`

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，回答不超过{limit}字，必须引用原文编号。"),
    MessagesPlaceholder("history", optional=True),   # 放历史消息
    ("human", "{question}"),
])

msgs = prompt.invoke({"role": "法律顾问", "limit": 120, "question": ".."})
```
⚠️ 三个高频坑：
1. 变量名写错不报错，运行时才炸 → 用 `prompt.input_variables` 自检。
2. `MessagesPlaceholder` 放错位置（放在 human 后）会破坏多轮结构。
3. 中文提示词里混用 `{}`（如 JSON 示例）会被当变量 → 用 `{{}}` 转义。

### 3.2 结构化输出：三种方式，别混用

| 方式 | 用法 | 优点 | 缺点 / 坑 |
|---|---|---|---|
| `llm.with_structured_output(Schema)` | 裸模型 / 链 | 一次调用、自动校验 | 部分厂商走 tool-calling 实现，参数不同 |
| `JsonOutputParser` + prompt 约束 | 无 function calling 的模型 | 兼容性最好 | 要自己处理解析失败与重试 |
| `create_agent(response_format=ToolStrategy(Schema))` | **Agent 场景** | 在主循环内完成，不额外加一次调用 | 只有 Agent 有这个参数 |

```python
from pydantic import BaseModel, Field

class Ticket(BaseModel):
    """工单分类结果"""
    category: str = Field(description="退款/物流/质量/其他 之一")
    urgency: int = Field(ge=1, le=5, description="1=不急，5=紧急")
    reason: str = Field(description="判断依据，30 字以内")

structured = llm.with_structured_output(Ticket)
t = structured.invoke("我买的鞋三天没发货，客服也不回")
print(t.category, t.urgency)   # 拿到的是 Ticket 实例，不是字符串
```

```python
# Agent 场景（v1 特色：结构化输出在主循环内完成，省一次 LLM 调用）
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

agent = create_agent(
    "openai:gpt-4.1-mini",
    tools=[search_tool],
    response_format=ToolStrategy(Ticket),
)
r = agent.invoke({"messages": [{"role": "user", "content": "帮我判断这个投诉"}]})
print(r["structured_response"])   # Ticket(...)
```
⚠️ `ToolStrategy` 有 `handle_errors` 参数，默认遇到解析错误/多个 tool call 会重试；**生产必须显式配置**，否则会静默重试烧 token。

---

## 4. LCEL / Runnable：LangChain 的"函数式管道"

### 4.1 本质
`a | b` 调用的是 `Runnable.__or__`，返回 `RunnableSequence`。每个环节都是 `Runnable`，所以都自动拥有 `.invoke/.batch/.stream/.ainvoke/.with_retry/.with_fallbacks`。

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | StrOutputParser()
chain.invoke({"role": "顾问", "limit": 80, "question": "什么是向量检索？"})
# 等价于 StrOutputParser().invoke(llm.invoke(prompt.invoke({...})))
```

### 4.2 常用 Runnable（背这张表就够了）

| 组件 | 作用 | 一句话示例 |
|---|---|---|
| `RunnableSequence` | 串行 | `a \| b` |
| `RunnableParallel` | 并行，输出 dict | `{"ctx": retriever, "q": RunnablePassthrough()}` |
| `RunnablePassthrough` | 原样透传 | 把用户问题同时送进检索和提示词 |
| `RunnableLambda` | 把普通函数变成 Runnable | 格式化、清洗 |
| `.bind(...)` | 预绑参数 | `llm.bind(temperature=0)` |
| `.with_retry(...)` | 节点级重试 | 外部 API 抖动 |
| `.with_fallbacks([...])` | 主备模型切换 | 主力模型 429 时降级 |

```python
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

format_docs = RunnableLambda(lambda docs: "\n\n".join(d.page_content for d in docs))

rag = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | ChatPromptTemplate.from_messages([
        ("system", "只依据 context 回答，找不到就说不知道。\n\n{context}"),
        ("human", "{question}"),
      ])
    | llm
    | StrOutputParser()
)
```

### 4.3 避坑
1. **LCEL 不是必须**。写复杂分支时 LCEL 会变成"括号地狱"，直接写 Python 函数 + `create_agent`/LangGraph 更好。v1 已经把 chains 移出核心，就是在暗示这点。
2. `RunnableParallel` 里若某一路抛异常，整条链失败 → 用 `.with_fallbacks()` 或包 `RunnableLambda` 做 try/except 返回空。
3. 调试别猜：`chain.get_graph().print_ascii()` 看结构，`chain.invoke(..., config={"callbacks":[ConsoleCallbackHandler()]})` 看每步输入输出。

---

## 5. Tools：Agent 的手脚

### 5.1 定义一个"大厂能用"的工具

```python
from pydantic import BaseModel, Field
from langchain.tools import tool

class WeatherArgs(BaseModel):
    city: str = Field(description="城市名，中文，如 杭州")
    date: str = Field(description="日期，格式 YYYY-MM-DD")

@tool(args_schema=WeatherArgs)
def get_weather(city: str, date: str) -> str:
    """查询指定城市某天的天气。数据实时，超时 3 秒，仅支持中国大陆城市。"""
    return f"{city} {date}：多云，22℃，湿度 60%"
```

**工具描述的五条硬标准**（决定模型会不会正确调用）：
1. docstring 第一行写**做什么**，第二行写**边界**（支持范围、超时、是否幂等）。
2. 参数必须有 `description` + 例子，尤其是日期/枚举/单位。
3. 返回**结构化字符串**（推荐 JSON 或 `key: value`），别返回一坨自然语言。
4. 工具内部**自己兜住异常**，返回可读错误（`{"error": "城市不存在"}`），别让异常冒到 Agent。
5. 有副作用的工具（转账/发邮件/删数据）**必须**配 HITL 中间件。

### 5.2 工具是怎么被调用的（面试必考）

```python
llm_with_tools = llm.bind_tools([get_weather])
resp = llm_with_tools.invoke("杭州明天天气？")

if resp.tool_calls:                        # 模型不执行，只是"点了菜"
    call = resp.tool_calls[0]
    result = {"get_weather": get_weather}[call["name"]].invoke(call["args"])
    final = llm_with_tools.invoke([
        HumanMessage("杭州明天天气？"), resp,
        ToolMessage(result, tool_call_id=call["id"]),   # 必须带 id 回填
    ])
```
> 这就是 `create_agent` 内部循环做的事：**model → 有 tool_calls 就执行 → 回填 ToolMessage → 再进 model → 直到没有 tool_calls**。能手写这段，Agent 就不再是黑盒。

---

## 6. Retrieval / RAG（你的主战场）

### 6.1 全链路

```
文档 → 加载 → 切分 → 嵌入 → 向量库
                              ↓
用户问题 → (改写) → 检索(向量/BM25/混合) → 重排(rerank) → 拼上下文 → LLM → 带引用回答
                                                                  ↓
                                                          评估：recall@k / 忠实度 / 延迟 / 成本
```

### 6.2 加载与切分

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,        # 中文建议 300~800
    chunk_overlap=80,      # 约 10~15%
    separators=["\n\n", "\n", "。", "！", "？", " ", ""],   # 中文标点必须加
)
chunks = splitter.split_documents(docs)
```

| 切分策略 | 适用 | 代价 | 备注 |
|---|---|---|---|
| 固定长度 + 重叠 | 通用基线 | 低 | **先跑这个当 baseline** |
| 递归分隔符 | 大部分业务文档 | 低 | 中文要补标点分隔符 |
| 按结构（标题/章节） | 手册、法规、教材 | 中 | 保留元数据，检索后能定位 |
| 语义切分（embedding 相似度断点） | 长文、话题跳转多 | 高（要嵌入） | 提升有限，别一上来就用 |
| Small-to-Big / 父子块 | 需要"小块检索、大块生成" | 中 | 课程重点，生产很实用 |

⚠️ 三个坑：① 表格被切断（先转 Markdown 再切）；② 页码/标题等元数据丢失（检索结果没法溯源）；③ `chunk_overlap` 设 0，跨段答案永远检索不到。

### 6.3 嵌入与向量库

```python
from langchain.embeddings import init_embeddings
from langchain_core.vectorstores import InMemoryVectorStore

emb = init_embeddings("openai:text-embedding-3-small")
store = InMemoryVectorStore(embedding=emb)
store.add_documents(chunks)

hits = store.similarity_search_with_score("设备红灯闪烁怎么办", k=5)
for doc, score in hits:
    print(round(score, 4), doc.metadata.get("source"), doc.page_content[:40])
```

| 向量库 | 优势 | 劣势 | 什么时候用 |
|---|---|---|---|
| `InMemoryVectorStore` | 零依赖 | 不持久 | Demo、单元测试 |
| **pgvector** | 与业务库同库、SQL 可查、运维简单 | 亿级需调参 | **中小项目首选** |
| Milvus | 十亿级、多索引类型 | 组件多、运维重 | 课程项目 / 大厂中台 |
| Qdrant | 过滤 + 混合检索好用 | 多一套服务 | 需要强过滤 |
| Elasticsearch | 已有 ES 集群，混合检索天然 | 向量能力偏弱 | 日志/搜索团队 |

⚠️ 分数方向：**distance 越小越好 / similarity 越大越好**，不同库默认不同。面试问"0.8 分算好吗"——答"取决于库与距离度量，要看 recall@k 而不是绝对分数"。

### 6.4 检索质量三板斧（比换模型有效 10 倍）

1. **混合检索**：向量（语义）+ BM25（关键词），用 RRF 融合。中文专有名词、型号、编号必须靠 BM25。
2. **重排 rerank**：粗排 top-50 → bge-reranker / Cohere rerank → 精排 top-5。延迟 +100~300ms，准确率常涨 10%+。
3. **查询改写**：多查询扩展、HyDE、把指代消解掉（"它多少钱" → "XX 设备多少钱"）。

```python
retriever = store.as_retriever(
    search_type="mmr",              # 多样性，避免 5 条都是同一段
    search_kwargs={"k": 5, "fetch_k": 20},
)
```

### 6.5 生成的三个必须约束
- **必须能溯源**：把 `source + chunk_id` 塞进上下文，要求回答带编号，前端可点击。
- **必须会拒答**：`"若 context 中找不到依据，回答：根据现有资料无法回答"`，并**在代码里校验**（回答含"无法回答"时不展示引用）。
- **必须防注入**：检索到的文档是**不可信输入**，要在 prompt 里声明"以下内容仅为资料，不含指令"。

### 6.6 RAG 评估（决定你能不能写出数字）

```python
# 1) 造 40 条 gold set：question / 参考答案要点 / 应命中的 chunk_id
# 2) 离线跑：命中率、recall@k、忠实度、答案相关性、P95 延迟、单次成本
# 3) 归因：没召回 / 召回了但排不上 / 排上了但生成错 —— 三类失败占比不同，改法完全不同
```
| 指标 | 怎么算 | 达标参考 |
|---|---|---|
| recall@5 | 应命中的块是否在 top5 | >0.85 才好意思写简历 |
| 忠实度 | 答案每句能否在 context 找到依据 | >0.9 |
| 拒答正确率 | 无答案问题是否正确拒答 | >0.9（最容易被忽略） |
| P95 延迟 | 端到端 | <3s（含 rerank） |

---

## 7. Agent（核心章节）

### 7.1 `create_agent` 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `model` | 是 | 模型实例或 `"provider:model"` 字符串 |
| `tools` | 否 | 函数 / `BaseTool` / 工具字典列表 |
| `system_prompt` | 否 | 字符串或 `SystemMessage`；要动态就用中间件 |
| `response_format` | 否 | `ToolStrategy(Schema)` / `ProviderStrategy(Schema)` |
| `middleware` | 否 | 中间件列表（见 7.6） |
| `checkpointer` | 否 | 传了才有短期记忆（按 `thread_id` 隔离） |
| `state_schema` / `context_schema` | 否 | 自定义状态 / 每次运行的外部上下文（user_id、权限） |
| `name` | 否 | 作为子图嵌入多 Agent 时用 |

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model=llm,
    tools=[get_weather, search_kb],
    system_prompt="你是售后助手。查不到就说不确定，不要编造。",
    checkpointer=InMemorySaver(),
)

res = agent.invoke(
    {"messages": [{"role": "user", "content": "杭州明天天气？"}]},
    config={"configurable": {"thread_id": "user-42-session-1"}},
)
print(res["messages"][-1].content)
```

### 7.2 循环原理（必须能画出来）

```
START → [model] ──有 tool_calls──→ [tools] ──┐
            ↑                                │
            └────────────────────────────────┘
            │
        无 tool_calls → END
```
一句话：**Agent 就是一个 while 循环，判断条件是"模型还点不点工具"**。所以：
- 循环不会自己停 → 必须配 **调用次数上限**（`ModelCallLimitMiddleware` / `ToolCallLimitMiddleware`）。
- 工具报错会中断 → 必须配 **工具错误/重试** 中间件。
- 状态靠 checkpointer → 中断后能 `Command(resume=...)` 续跑（HITL 就靠这个）。

### 7.3 记忆与持久化

| Checkpointer | 存储 | 适用 | 坑 |
|---|---|---|---|
| `InMemorySaver` | 进程内存 | 学习、单元测试 | 重启丢；多进程不共享 |
| `SqliteSaver` | 本地文件 | 单机 demo / 桌面应用 | 并发写锁 |
| `PostgresSaver` | PG | **生产标配** | 需建表 `checkpointer.setup()` |

```python
from langgraph.checkpoint.postgres import PostgresSaver   # pip install langgraph-checkpoint-postgres

with PostgresSaver.from_conn_string(DB_URL) as cp:
    cp.setup()
    agent = create_agent(model=llm, tools=tools, checkpointer=cp)
```
**thread_id 设计**（大厂一定会问）：`{tenant_id}:{user_id}:{conversation_id}`。别用自增数字，跨租户串会话是安全事故。

> 长期记忆（跨会话）≠ checkpointer。跨会话要用 `store`（`InMemoryStore`/`PostgresStore`）+ 中间件，别混。

### 7.4 流式（面试必问）

```python
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "查一下杭州天气并总结"}]},
    config={"configurable": {"thread_id": "t1"}},
    stream_mode="messages",          # 逐 token + 工具进度
):
    msg, metadata = chunk
    if msg.content:
        print(msg.content, end="", flush=True)
```

| `stream_mode` | 给什么 | 前端怎么用 |
|---|---|---|
| `"values"` | 每步完整状态 | 调试用，流量大 |
| `"updates"` | 每个节点的增量 | 显示"正在调用工具…" |
| `"messages"` | `(message, metadata)` 元组 | **打字机效果** |
| `"custom"` | 自己 `get_stream_writer()` 写的 | 自定义进度条 |

### 7.5 中间件：v1 最重要的能力

**6 个钩子**（自定义中间件实现其一即可）：

| 钩子 | 时机 | 典型用途 |
|---|---|---|
| `before_agent` | 整轮开始 | 加载用户画像、鉴权 |
| `before_model` | 每次进模型前 | 裁剪历史、注入动态提示词 |
| `wrap_model_call` | 包裹模型调用 | **模型路由**、缓存、mock |
| `wrap_tool_call` | 包裹工具调用 | 权限校验、审计日志、缓存 |
| `after_model` | 每次模型回复后 | 输出校验、护栏 |
| `after_agent` | 整轮结束 | 落库、指标上报 |

**内建中间件（生产常用，按重要性排）**：

| 中间件 | 解决什么 | 不配的后果 |
|---|---|---|
| `HumanInTheLoopMiddleware` | 敏感工具人工审批 | 模型直接给你转账 |
| `ModelRetryMiddleware` / `ToolRetryMiddleware` | 限流/超时指数退避重试 | 一次 429 整轮失败 |
| `ModelFallbackMiddleware` | 主力模型挂了自动切备 | 故障时全站不可用 |
| `ModelCallLimitMiddleware` / `ToolCallLimitMiddleware` | 防死循环、防成本爆炸 | 见过一晚上烧掉几百块的 |
| `SummarizationMiddleware` | 长对话压缩 | 上下文溢出报错 |
| `PIIMiddleware` | 邮箱/手机号脱敏或拦截 | 用户隐私进日志 |
| `ContextEditingMiddleware` | 清旧工具结果 | token 越来越贵 |
| `ToolErrorMiddleware` | 把异常转成模型能读的错误 | 工具一挂整个 run 崩 |
| `TodoListMiddleware` / `FileSearchMiddleware` / `ShellToolMiddleware` | 规划、找文件、跑命令 | 复杂任务能力不足 |
| `LLMToolEmulator` | 用 LLM 假装执行工具 | 测试时没法跑 |

```python
# 生产配置模板（照这个抄）
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware, ModelRetryMiddleware, ToolRetryMiddleware,
    ModelCallLimitMiddleware, SummarizationMiddleware, PIIMiddleware,
)

agent = create_agent(
    model=llm,
    tools=[search_kb, create_ticket, send_email],
    checkpointer=cp,
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        ModelRetryMiddleware(max_retries=3, backoff_factor=2.0),
        ToolRetryMiddleware(max_retries=2, on_failure="continue"),
        ModelCallLimitMiddleware(max_calls=15),          # 参数名以官方为准
        SummarizationMiddleware(model=llm, trigger={"tokens": 6000}),
        HumanInTheLoopMiddleware(interrupt_on={
            "send_email": {"allowed_decisions": ["approve", "edit", "reject"]},
        }),
    ],
)
```
⚠️ 中间件**顺序有意义**：重试放里层（先重试再兜错），HITL 放外层（最后一道门）。

```python
# 自定义中间件：按用户等级路由模型（省钱又保效果）
from dataclasses import dataclass
from langchain.agents.middleware import AgentMiddleware

@dataclass
class Ctx:
    user_tier: str = "free"

class ModelRouter(AgentMiddleware):
    def wrap_model_call(self, request, handler):
        cheap = init_chat_model("openai:gpt-4.1-nano")
        if getattr(request.runtime.context, "user_tier", "free") == "free":
            return handler(request.override(model=cheap))
        return handler(request)

agent = create_agent(model=llm, tools=tools, middleware=[ModelRouter()], context_schema=Ctx)
```

### 7.6 HITL（人在环）—— 2026 年 Agent 岗高频题

```python
from langgraph.types import Command

# 第一次调用会停在中断点
res = agent.invoke({"messages": [{"role": "user", "content": "给 Alice 转 100 元"}]},
                   config={"configurable": {"thread_id": "t1"}})

if "__interrupt__" in res:
    待审 = res["__interrupt__"][0].value          # 含 action_requests
    # 人工决策：approve / edit / reject
    res = agent.invoke(Command(resume={"decisions": [{"type": "approve"}]}),
                       config={"configurable": {"thread_id": "t1"}})
```
⚠️ 三坑：① 不配 checkpointer 会直接报错（中断要存状态）；② `thread_id` 换了就续不上；③ `decisions` 数量必须与 `action_requests` 对齐。

### 7.7 多 Agent：什么时候该用（反直觉）

| 场景 | 该不该用多 Agent |
|---|---|
| 一个模型 + 十几个工具能干完 | ❌ 不用。工具多了用 **工具检索/选择**（`LLMToolSelectorMiddleware`） |
| 需要隔离上下文（读大文件、长搜索） | ✅ 用 **subagent**（`SubAgentMiddleware` / `create_deep_agent`） |
| 明确分工且串行（检索→写作→校对） | ✅ 用 **LangGraph 显式编排**，比多 Agent 自组织可控 |
| 想"让 Agent 自己开会" | ❌ 调试地狱、成本翻倍、效果常不如单 Agent + 好提示词 |

```python
# 预装的"深"Agent：规划 + 文件系统 + 子 Agent + 摘要
from deepagents import create_deep_agent
deep = create_deep_agent(model=llm, tools=[search_kb], system_prompt="...")
```
> 面试金句：**多 Agent 是扩容上下文的手段，不是架构炫技。先证明单 Agent + 工具不行，再上多 Agent。**

---

## 8. 工程化（课程没讲、面试必问的部分）

### 8.1 FastAPI + 流式（可直接当项目骨架）

```python
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/chat")
async def chat(q: str, thread_id: str = "default"):
    async def gen():
        async for msg, meta in agent.astream(
            {"messages": [{"role": "user", "content": q}]},
            config={"configurable": {"thread_id": thread_id}, "recursion_limit": 30},
            stream_mode="messages",
        ):
            if msg.content:
                yield f"data: {json.dumps({'t': msg.content}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream")
```
四个必加：`timeout`、`recursion_limit`、`thread_id` 鉴权、请求级 trace_id。

### 8.2 可靠性三件套

| 问题 | 手段 |
|---|---|
| 网络抖动 / 429 | `ModelRetryMiddleware`（指数退避 + jitter） |
| 主力模型不可用 | `ModelFallbackMiddleware`（gpt-4.1 → qwen-plus） |
| 死循环 / 成本失控 | `ModelCallLimitMiddleware` + `recursion_limit` |

### 8.3 可观测性

```python
# 最小接入：环境变量即可
# LANGSMITH_TRACING=true
# LANGSMITH_API_KEY=ls-xxx
# LANGSMITH_PROJECT=rag-demo
```
要 trace 什么（决定了你能不能回答"为什么这次答错了"）：
1. 每次模型调用的**输入消息全文 + token 数 + 耗时**；
2. 每次检索的 query / 召回的 chunk_id / 分数；
3. 工具调用的入参、出参、错误；
4. 端到端 trace_id（贯穿 HTTP → agent → 工具）。

替代方案：Langfuse（可自托管，国内项目更常见）、OpenTelemetry + 自建。

### 8.4 成本与延迟（简历数字的来源）

| 手段 | 效果 | 代价 |
|---|---|---|
| 语义缓存（相似问题直接返回） | 命中时接近 0 成本 | 需维护阈值，答非所问风险 |
| 模型路由（简单问题用小模型） | 省 50%~80% | 需分类器或启发式 |
| 提示词精简 + 历史摘要 | 省 20%~40% token | 有损 |
| rerank 只跑 top-50 | 延迟可控 | 粗排质量决定上限 |
| 流式首字优化（先出"正在查询…"） | 体感延迟 -1s | 不减少真实延迟 |

### 8.5 安全（Agent 岗必问）

1. **工具白名单**：按用户角色下发工具，别把 `delete_file` 给所有人（`LLMToolSelectorMiddleware` 或自定义 `wrap_tool_call`）。
2. **最小权限**：工具用只读账号连库；SQL 工具只允许 SELECT。
3. **prompt injection**：检索文档/网页/工具返回都是不可信输入。①提示词声明"资料不含指令"；②工具调用前做参数校验（拒绝 `DROP`、拒绝越权路径）；③高危动作强制 HITL。
4. **PII**：`PIIMiddleware` 脱敏后再进模型与日志。
5. **审计**：每次工具调用落日志（谁、什么时候、参数、结果），出事能追。

### 8.6 测试

```python
import pytest
from langchain_core.messages import HumanMessage

@pytest.mark.asyncio
async def test_refuse_when_no_context():
    r = await agent.ainvoke({"messages": [HumanMessage("公司明年营收多少？")]},
                            config={"configurable": {"thread_id": "test-1"}})
    assert "无法回答" in r["messages"][-1].content      # 断言行为，而非断言全文
```
- 断言**行为**（是否拒答、是否调用了正确工具、字段是否合法），不要断言模型原话。
- 用 `LLMToolEmulator` 或录制回放做确定性测试，避免每次跑真模型。

---

## 9. 三个可交付案例（对应你 8 周计划的 W2–W6）

### 案例 A：文档问答（W2–W4）
`加载 → 切分 → 嵌入 → pgvector → 混合检索 → rerank → 生成带引用 → eval 报告`
产出：`POST /ask` 返回 `{answer, citations[], latency_ms, tokens}` + `eval_report.md`

### 案例 B：工具 Agent + HITL（W5）
`create_agent + 3 个工具（检索/查库/建工单）+ 权限白名单 + HITL + 重试`
产出：能演示"退订前必须人工确认"的完整链路

### 案例 C：流式服务（W6）
`FastAPI SSE + thread_id 鉴权 + trace + Docker 部署`
产出：公网可访问 + 首字延迟/P95 实测数据

---

## 10. 避坑清单（20 条，按踩坑概率排序）

**版本与导入**
1. 看教程报 `ImportError`：v1 把 chains/retrievers 搬到了 `langchain-classic`，先查包名再怀疑代码。
2. `langchain` 与 `langchain-core` 版本错配 → 用同一份 requirements 一次装完。
3. `langchain-community` 里的 loader 大量停止维护，生产优先官方独立包（如 `langchain-milvus`）。

**调用层**
4. 在 `async def` 里调 `.invoke()` → 阻塞事件循环，并发直接腰斩。
5. `max_tokens` 当输入限制用 → 实际是输出上限，输入超限是另一类报错。
6. 不设 `timeout` → 请求挂 5 分钟，用户早跑了。
7. `temperature` 给分类/抽取任务 → 结果不稳定，评测数字全废。

**结构化输出**
8. `with_structured_output` 失败不重试 → 偶发解析错误直接 500。
9. Agent 里用 `with_structured_output` → 应该用 `response_format=ToolStrategy(...)`。
10. Pydantic 字段没写 `description` → 模型瞎填，`Field(description=...)` 是提示词的一部分。

**RAG**
11. `chunk_overlap=0` → 跨段答案永远检索不到。
12. 用相似度分数绝对值判断好坏 → 不同库/度量不可比，只看 recall@k。
13. 检索结果直接拼进 prompt 不做长度控制 → 上下文爆炸，成本飙。
14. 不保留元数据 → 回答无法溯源，业务不敢用。

**Agent**
15. 不配 `checkpointer` 就用 `thread_id` → 记忆不生效（也不报错，最坑）。
16. 不设调用上限 → 死循环烧钱。
17. 工具里抛异常 → 整轮崩，应返回结构化错误。
18. 工具数量 >15 还全量塞给模型 → 选择准确率下降，用工具检索/选择中间件。

**流式与部署**
19. `stream_mode` 用错 → 拿到的是完整状态不是 token，前端没打字机效果。
20. SSE 不加 `X-Accel-Buffering: no` / Nginx 缓冲没关 → 流式变一次性返回。

---

## 11. 易混淆对照（面试最爱问的区别）

| 容易混的 | 区别一句话 |
|---|---|
| `invoke` vs `batch` vs `stream` | 单次阻塞 / 并发批量 / 逐块返回；async 版是 `ainvoke/astream` |
| `RunnableLambda` vs `RunnablePassthrough` | 前者改变数据，后者原样透传（常用于并行分支） |
| `with_structured_output` vs `ToolStrategy` | 前者给裸模型用，后者给 Agent 用 |
| `retriever` vs `vectorstore` | 前者是"检索策略接口"（可 MMR/混合/多查询），后者只是存储 |
| `similarity_search` vs `as_retriever` | 前者一次性取结果，后者可接入链与 Agent 工具 |
| `checkpointer` vs `store` | 前者存**单会话**状态（thread），后者存**跨会话**长期记忆 |
| `thread_id` vs `context` | 前者划定"哪个会话"，后者携带"本次运行的外部数据"（用户、权限） |
| `middleware` vs `callback` | 前者能**改**执行（拦截/替换），后者只能**看** |
| `before_model` vs `wrap_model_call` | 前者改状态，后者能换模型/换工具（更强） |
| `create_agent` vs `create_deep_agent` | 前者自己配 harness，后者预装文件系统/规划/子 Agent |
| `content` vs `content_blocks` | 前者纯文本（最常用），后者带推理/引用/工具块 |
| `temperature` vs `top_p` | 前者调随机性，一般只调一个 |
| `chunk_size` vs `chunk_overlap` | 块大小 vs 相邻块重叠（跨段语义靠它） |
| `InMemorySaver` vs `PostgresSaver` | 内存（重启丢）vs 生产持久化 |
| `LangChain` vs `LangGraph` | 应用层抽象 vs 状态机运行时；`create_agent` 底层是 LangGraph |

---

## 12. 面试题（20 题 · 考点 + 答法要点）

### 概念类
1. **LangChain 解决了什么问题？不用它行不行？**
   考点：是否理解抽象价值。答：统一多厂商模型接口、Runnable 组合、工具 schema 自动生成与调用循环、检索器抽象、checkpoint。不用也行，但每加一个能力都要重写循环。
2. **`create_agent` 内部是怎么跑的？**
   考点：能不能画循环。答：model → 有 `tool_calls` 就执行并回填 `ToolMessage` → 再进 model → 无 `tool_calls` 结束；状态由 LangGraph 管。
3. **LangChain 1.x 相比 0.x 最大变化？**
   考点：版本敏感度。答：`create_agent` 取代 `create_react_agent`、`content_blocks` 统一内容、chains/retrievers 迁到 `langchain-classic`、中间件成为一等公民。
4. **LCEL 的 `|` 做了什么？**
   考点：`__or__` → `RunnableSequence`；所有 Runnable 共享 invoke/batch/stream/retry 能力。
5. **为什么 Agent 需要中间件？**
   考点：工程思维。答：把重试、限额、脱敏、审批、摘要从业务代码里抽出来，可组合、可复用、不改 model 和 tools。

### 工程类
6. **Agent 死循环怎么防？** `ModelCallLimitMiddleware` + `recursion_limit` + 工具级幂等 + 失败计数。
7. **工具报错怎么办？** 工具内兜异常返回结构化错误 → `ToolErrorMiddleware` 转成模型可读消息 → `ToolRetryMiddleware` 只重试可重试错误（连接/超时），鉴权/参数错误不重试。
8. **流式怎么实现？** `stream_mode="messages"` + SSE；注意 Nginx 关缓冲、首字延迟、中断时的连接清理。
9. **多轮会话怎么存？** checkpointer 按 `thread_id` 隔离 → 生产用 `PostgresSaver`；`thread_id` 要带租户与用户。
10. **怎么控制成本？** 模型路由 + 语义缓存 + 历史摘要 + 限制工具结果长度 + 统计 token（`usage_metadata`）。
11. **怎么排查"这次答错了"？** 看 trace：query 原文 → 召回的 chunk 与分数 → 拼进 prompt 的上下文 → 模型输出。90% 是检索问题不是模型问题。
12. **怎么做 Agent 测试？** 断言行为（是否拒答/是否调对工具/字段是否合法），配合工具仿真或录制回放。

### RAG 类
13. **RAG 效果差，从哪查起？** 先算 recall@k：没召回是切分/嵌入问题；召回了没进 top5 是排序问题；都对了还错是生成/prompt 问题。
14. **为什么用混合检索？** 向量擅长语义，BM25 擅长型号/编号/专有名词；中文业务里关键词命中率差距很大。
15. **rerank 值不值？** 值，前提是粗排能给足候选（top-50）；代价是 +100~300ms。
16. **分块大小怎么定？** 先按文档结构定，再用 3 组参数（300/600/1000）跑 recall@5 选，不要凭感觉。
17. **微调还是 RAG？** 知识类问题用 RAG（可更新、可溯源）；风格/格式/固定任务用微调；两者都解决不了的是"模型能力不足"→ 换模型。

### 深挖类
18. **HITL 怎么实现？中断后状态在哪？** checkpointer 存 checkpoint，`__interrupt__` 返回待审动作，`Command(resume={"decisions":[...]})` 续跑；必须同一 `thread_id`。
19. **多 Agent 什么时候值得？** 只有需要**上下文隔离**或**明确串行分工**时。否则工具选择 + 好提示词更便宜可控。
20. **prompt injection 在 RAG 里怎么防？** 资料声明为不可信、工具参数白名单校验、高危动作 HITL、输出侧校验（不执行文档里的"指令"）。

---

## 13. 和课程进度的配合建议

| 课程讲到 | 你在这份笔记里重点看 | 产出 |
|---|---|---|
| Model I/O + Chains | §2 §3 §4 | 一个把 3 家模型切换的配置化小脚本 |
| Retrieval | §6 | 用课程语料跑出 recall@5 基线数字 |
| Agents | §7 | 3 工具 Agent + HITL 演示 |
| 中间件 | §7.5 §8.2 | 生产配置模板跑通（重试+限额+脱敏） |
| MCP | §7 + §8.5 | 接 1 个 MCP server，写清权限边界 |

⚠️ 课程没讲但你必须自己补的：§8（成本/可观测/安全/测试）+ §6.6（评估）。这四块决定你面试时是"用过 LangChain"还是"做过 LangChain 工程"。

---

## 附：参考来源

- LangChain v1 新特性：<https://docs.langchain.com/oss/python/releases/langchain-v1>
- Agents / `create_agent`：<https://docs.langchain.com/oss/python/langchain/agents>
- 内建中间件清单：<https://docs.langchain.com/oss/python/langchain/middleware/built-in>
- 迁移指南（0.x → 1.x）：<https://docs.langchain.com/oss/python/migrate/langchain-v1>
- GitHub：<https://github.com/langchain-ai/langchain>

> 版本提醒：`ModelCallLimitMiddleware` 等参数签名在小版本间有过调整，动手前用 `help()` 或官方 API reference 核对一次（本文已标注 ⚠️ 处）。

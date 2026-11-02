# LangGraph 学习 · 复习 · 开发查询手册（v1 版）

> 基线：`langgraph` 1.x ｜ 官方文档 <https://docs.langchain.com/oss/python/langgraph/overview>
> 定位：**原文讲"怎么用"，本手册补"为什么、什么时候别用、上生产会踩什么"**。目录沿用原笔记，只做必要扩充。
>
> 三种用法：
> - **学习**：按 一 → 五 顺序读，每节末尾【动手】必须敲一遍。
> - **复习**：只看每节的表格 + §十 面试题 + §十一 错误速查。
> - **开发查询**：直接跳 §十二 API 速查表 + §九 坑清单。
>
> 标记：✅ 已核对官方文档 ｜ ⚠️ 版本敏感，`help()` 确认 ｜ 🔍 需核实

---

## 一、LangGraph 概述

### 1.1 什么是 LangGraph

**一句话**：它是**有状态图的运行时**——把"节点 + 边 + 状态"这套图计算模型用在 LLM 应用上，解决"多步、可中断、可恢复、可循环"的编排问题。

官方定位：*a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents*（[overview](https://docs.langchain.com/oss/python/langgraph/overview)）。

它提供的**四件别人不提供的底层能力**（这才是它存在的理由）：

| 能力 | 解决的问题 | 没有它会怎样 |
|---|---|---|
| **Durable execution（持久化执行）** | 跑到一半崩了/超时/等人工，能接着跑 | 用户重跑一遍，前面白花钱 |
| **Streaming** | token、节点进度、自定义事件逐步推给前端 | 只能等全跑完，体验差 |
| **Human-in-the-loop** | 中途暂停、人工审批、改参数再继续 | 敏感操作无人把关 |
| **Persistence / Memory** | 短期(thread) + 长期(namespace) 记忆 | 多轮对话、个性化做不了 |

> 底层是 **Pregel / BSP（超步）** 模型：一"步"内所有节点并行执行，步之间通过**状态通道**同步。理解了这句，后面"为什么节点能并行""为什么 checkpoint 是按步存的"全都通了。

### 1.2 与 LangChain 的区别（2026 的正确说法）

```text
Managed Deep Agents  ← 托管，开箱即用
      ↑
Deep Agents SDK      ← 预装：文件系统 / 规划 / 子Agent / 摘要
      ↑
LangChain  create_agent  ← 高层：模型 + 工具 + 中间件
      ↑
LangGraph            ← 运行时：状态机、持久化、流式、中断
```

| | LangChain | LangGraph |
|---|---|---|
| 抽象层级 | 应用层（组件 + Agent 循环） | 运行时层（图、状态、检查点） |
| 你写什么 | 提示词、工具、中间件 | 节点函数、边、状态 schema |
| 适合 | 80% 的常规 Agent | 有分支/循环/并行/多 Agent/要精细控制 |
| 关系 | `create_agent` **底层就是一个 LangGraph 图** | 可以完全不用 LangChain，纯手写节点 |

**⚠️ v1 的重要变化**：`langgraph.prebuilt.create_react_agent` **已弃用**，官方迁移到 LangChain 的 `create_agent`（[LangGraph v1 发布说明](https://docs.langchain.com/oss/python/releases/langgraph-v1)）。看见老博客里的 `create_react_agent` 就知道是旧文。

> 与之相对：`create_react_agent` 已弃用，但 LangGraph 的核心图 API（StateGraph/节点/边/检查点）**在 1.0 完全没变**——所以你现在学的这套不会白学，这是它敢叫 1.0 的原因。

### 1.3 什么时候**不要**用 LangGraph（面试最爱问）

| 场景 | 判断 |
|---|---|
| 单轮问答、无工具 | ❌ 直接用 SDK |
| 线性 RAG（检索→生成） | ❌ 一个函数就够，画图是负债 |
| 标准工具调用 Agent | ⚠️ 先用 `create_agent`，别手搓 |
| 多分支 + 人工审核 + 断点恢复 | ✅ 正解 |
| 长任务（跑几十分钟）、要并行子任务 | ✅ 正解（`Send` 扇出） |
| 多 Agent 有明确分工 | ✅ 用图显式编排，比"让 Agent 自己开会"可控 |

**面试金句**：*LangGraph 的价值不是"更高级的 LangChain"，而是把「执行状态」变成一等公民——能存、能查、能改、能重放。*

---

## 二、快速入门

### 2.1 环境安装

```bash
pip install -U langgraph               # 核心
pip install -U langgraph-checkpoint-sqlite   # 本地持久化
pip install -U langgraph-checkpoint-postgres # 生产持久化
pip install -U "langgraph-cli[inmem]"  # 本地起服务 + Studio 可视化
```

### 2.2 简单示例（原文版 + 现代写法）

```python
from langgraph.graph import StateGraph, MessagesState, START, END

def mock_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello world"}]}

g = StateGraph(MessagesState)
g.add_node(mock_llm)
g.add_edge(START, "mock_llm")
g.add_edge("mock_llm", END)
graph = g.compile()

print(graph.invoke({"messages": [{"role": "user", "content": "hi!"}]}))
print(graph.get_graph().draw_mermaid())     # 可视化，粘到 mermaid 就能看图
```

**补：`compile()` 的 5 个参数**（原文没讲全，开发时天天用）

| 参数 | 作用 | 何时必须传 |
|---|---|---|
| `checkpointer` | 保存每步状态，支持记忆/恢复/中断 | 要多轮、要 `interrupt` |
| `store` | 跨会话长期记忆 | 要用户画像/跨对话记忆 |
| `cache` | 节点结果缓存 | 有昂贵且幂等的节点 |
| `interrupt_before/after=["node"]` | **静态**断点（调试、强制审核） | 调试时很好用 |
| `debug=True` | 打印每步执行 | 排查"为什么走了这条边" |

**补：本地起服务 + 可视化**（大厂日常不 print，用 Studio 看图）

```json
// langgraph.json
{
  "dependencies": ["."],
  "graphs": { "agent": "./agent.py:graph" },
  "env": ".env"
}
```
```bash
langgraph dev      # 起本地服务 + 打开 Studio，能看到每一步状态、改状态、重放
```

**【动手】** 把上面 10 行跑通，再用 `langgraph dev` 打开一次 Studio——之后所有调试都在这里看，比 print 高效 10 倍。

---

## 三、状态（State）

> 这一章是 LangGraph 的地基。90% 的"诡异 bug"都出在状态合并语义上。

### 3.1 状态的定义

#### 3.1.1 三种定义方式（原文讲了，这里补选择依据）

| 方式 | 校验 | 性能 | 推荐场景 |
|---|---|---|---|
| `TypedDict` | ❌ 无运行时校验 | 最快 | **默认选它**（官方推荐） |
| `Pydantic BaseModel` | ✅ 有校验 | 慢一些 | 输入来自外部/不可信，需要校验 |
| `@dataclass` | ❌ | 快 | 团队偏好 dataclass 时 |

```python
from typing import Annotated, TypedDict
from operator import add
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class State(TypedDict):
    # 无 Annotated = 覆盖语义（新值直接替换旧值）
    query: str
    # 有 Annotated = 用 reducer 合并
    messages: Annotated[list[AnyMessage], add_messages]
    steps: Annotated[int, add]          # 累加
```

**⚠️ 最重要的一条语义**（原文没强调，但新人必踩）：
> 节点返回的 dict 是**部分更新（partial update）**，不是替换整个 state。
> - 键**没有** reducer → 新值**覆盖**旧值
> - 键**有** reducer → 调用 `reducer(旧值, 新值)`
> - 节点返回 `None` → 视为"不更新任何字段"（不是清空！）

#### 3.1.2 输入输出数据隔离（原文已讲，补一个坑）

`state_schema / input_schema / output_schema` 三级隔离，是为了**不把内部实现暴露给调用方**。

⚠️ 坑：`output_schema` 只影响 `invoke()` 的**返回值**，不影响流式 `stream_mode="values"` 与 checkpointer 里存的内容——**敏感字段照样落盘**。要真隔离，就别把敏感字段放 state，放 `context` 或外部存储。

#### 3.1.3 节点间数据隔离（私有状态）

节点参数标注成**另一个 TypedDict**，它只读到那个子集的键（其余键读不到，但**图里还在**）。适合"某个节点只需要几个字段，不想让它看到全量 state"。

⚠️ 坑：私有状态的字段**必须存在于全局 state**，否则节点返回时按局部 schema 过滤，多余键被静默丢弃（不报错，最难查）。

#### 3.1.4 Reducer 函数（原文讲了，补 4 个常用 + 自定义签名）

```python
from langchain_core.messages import RemoveMessage
from langgraph.graph.message import add_messages

def keep_last_n(left: list, right: list, n: int = 20):
    return (left + right)[-n:]

class State(TypedDict):
    messages: Annotated[list, add_messages]      # 智能：追加/按 id 更新/删除
    counter: Annotated[int, add]                 # 数值累加
    items: Annotated[list[str], add]             # 列表拼接
    last_20: Annotated[list[str], keep_last_n]   # 自定义：只留最近 20 条
```

| Reducer | 语义 | 典型用途 |
|---|---|---|
| `add`（`operator.add`） | 相加/拼接 | 计数、列表累积 |
| `add_messages` | 按消息 id 合并；`RemoveMessage(id=...)` 可删除 | 对话历史 |
| 自定义 `f(left, right)` | 你自己定合并规则 | 去重、限长、求和最大值 |
| 无 reducer | 覆盖 | 90% 的单值字段 |

```python
# 删除历史消息（控制上下文长度的关键手法，原文未讲）
def trim_node(state: State):
    return {"messages": [RemoveMessage(id=m.id) for m in state["messages"][:-6]]}
```

**【面试点】** "state 里 messages 用什么 reducer？"→ `add_messages`，它会按 `id` 做 upsert，所以能"流式追加同一个 AI 消息"，也能用 `RemoveMessage` 删除。这是它比自己写 `operator.add` 强的地方。

### 3.2 状态的存储（Checkpointer）

#### 3.2.1 实际场景中的问题（原文已讲）

两个场景：①多轮上下文；②断点续传。本质都是"别每次从空状态开始"。

#### 3.2.2 状态的存储

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver

# 1) 内存：学习/单测
cp = InMemorySaver()

# 2) SQLite：单机
import sqlite3
cp = SqliteSaver(sqlite3.connect("./lg.db", check_same_thread=False))

# 3) Postgres：生产
with PostgresSaver.from_conn_string(DB_URL) as cp:
    cp.setup()                      # 首次必须建表！
    graph = builder.compile(checkpointer=cp)
```

| 后端 | 持久 | 并发 | 适用 |
|---|---|---|---|
| `InMemorySaver` | ❌ 重启丢 | — | 学习、单元测试 |
| `SqliteSaver` | ✅ | 单写 | 单机 demo、桌面端 |
| `PostgresSaver` | ✅ | 高 | **生产标配** |
| `RedisSaver`（第三方） | ✅ | 高 | 已有 Redis 基础设施 |

**补：`durability` 三档**（1.x 新增，控制"每步落盘的强度"，直接影响吞吐）

```python
graph.invoke(input, config=cfg, durability="async")   # "sync" | "async" | "exit"
```
| 取值 | 行为 | 用在哪 |
|---|---|---|
| `"sync"` | 每步同步落盘，最安全最慢 | 金融、涉及资金 |
| `"async"` | 异步落盘（默认倾向） | 大多数在线服务 |
| `"exit"` | 只在图结束时落盘 | 批处理，崩了重跑整批 |
⚠️ 取值与默认值随版本调整过，`help(graph.invoke)` 确认。

**补：`thread_id` 生产设计（大厂必问）**

```python
thread_id = f"{tenant_id}:{user_id}:{conversation_id}"
```
- 别用自增数字 / 时间戳 → 跨租户串会话 = 安全事故。
- 别用 `user_id` 单层 → 用户开两个窗口就串话。
- 加 `conversation_id` 才能"新建对话"。

#### 3.2.3 从状态中恢复执行（原文已讲，补工程细节）

```python
# 第一次：崩了
try:
    graph.invoke({"key_1": "v"}, config=cfg)
except Exception as e:
    print("崩了，状态已保存：", e)

# 恢复：input 传 None + 同一个 thread_id
graph.invoke(None, config=cfg)
```
⚠️ 三个坑：
1. `input=None` 是"继续"，`input={}` 是"用空输入覆盖"——两者行为不同。
2. 恢复的是**最后一个成功的 checkpoint**，即"出问题节点之前"那步；出问题节点会**重新执行**（所以节点要幂等）。
3. `PostgresSaver` 忘了 `setup()` → 报找不到表，且报错信息不直观。

### 3.3 获取历史状态

#### 3.3.1 LangGraph 底层运行算法（Pregel/BSP）

```
超步 1：START → [A ‖ B] 并行执行 → 汇总写入状态通道 → checkpoint #1
超步 2：[C] → checkpoint #2
...
```
三个直接推论（面试考点）：
1. **同一超步内的并行节点看不到彼此的写入**（下一超步才可见）→ 并行节点之间不能有数据依赖。
2. **checkpoint 是按超步存的**，不是按节点 → 恢复粒度是"步"。
3. 图执行天然是"批量同步"，所以**慢节点会拖慢整步**（并行不等于加速，受最慢者限制）。

#### 3.3.2 获取图执行的历史状态

```python
cfg = {"configurable": {"thread_id": "t1"}}

snap = graph.get_state(cfg)                 # 最新快照
print(snap.values, snap.next, snap.config)  # 当前状态 / 下一步要执行的节点

for s in graph.get_state_history(cfg):      # 从新到旧遍历所有 checkpoint
    print(s.config["configurable"]["checkpoint_id"], s.next, list(s.values))
```

**补：时间旅行三件套（原文没讲，是大厂调试神器）**

| 操作 | 代码 | 用在哪 |
|---|---|---|
| 看历史 | `get_state_history(cfg)` | 定位"哪一步状态错了" |
| 改状态 | `graph.update_state(cfg, {"x": 42}, as_node="node_a")` | 人工修正、跳过失败节点 |
| 回放/分叉 | 用历史 `checkpoint_id` 做新 config 再 invoke | 从某步重跑，探索不同分支 |

```python
# 回到某个历史点，改一个字段，重新往下跑（不影响原分支）
past = list(graph.get_state_history(cfg))[3]
fork_cfg = past.config
graph.update_state(fork_cfg, {"query": "换一种问法"}, as_node="node_a")
graph.invoke(None, config=fork_cfg)
```
⚠️ `as_node` 必传或猜错 → 图的 `next` 会算错，可能直接跑完或卡住。

---

## 四、节点（Node）

### 4.1 节点的输入输出

#### 4.1.1 节点输入（原文已讲，补 1.x 的第二个参数）

```python
from langgraph.runtime import Runtime

def node(state: State, runtime: Runtime[Ctx]):
    user_id = runtime.context.user_id      # 本次调用的外部上下文（不入库）
    store   = runtime.store                # 长期记忆
    writer  = runtime.stream_writer        # 自定义流式输出
    return {"answer": "..."}
```

**`context` vs `state` 的区别（面试高频）**

| | `state` | `context` |
|---|---|---|
| 存哪 | checkpointer（历史快照里） | 只活在本次运行的内存 |
| 用途 | 业务数据 | user_id、权限、feature flag、API key |
| 会出现在历史里吗 | ✅ | ❌（更安全） |
| 怎么传 | `invoke({...})` | `invoke(..., context=Ctx(...))` |

⚠️ 把 `api_key`、`user_token` 放 state → 会被写进 checkpoint 数据库，等于泄露。

#### 4.1.2 节点输出（原文已讲，补规则）

| 返回值 | 语义 |
|---|---|
| `dict` | 部分更新（最常用） |
| `None` | 什么都没改 |
| `Command(goto=..., update=...)` | **同时**改状态 + 决定下一步（替代条件边） |
| 抛异常 | 图的执行失败；配了 `retry_policy` 则重试 |

### 4.2 特殊节点

`START` / `END` 本质就是两个字符串常量（`"__start__"` / `"__end__"`）。补一句：**`START` 执行后也会落一个 checkpoint**，所以"空图"也有历史。多个 `add_edge(START, "x")` 就是**并行入口**。

### 4.3 节点缓存

```python
from langgraph.cache.memory import InMemoryCache
from langgraph.types import CachePolicy

builder.add_node("expensive", expensive_node,
                 cache_policy=CachePolicy(ttl=600))   # 10 分钟
graph = builder.compile(cache=InMemoryCache(), checkpointer=cp)
```

**补：缓存的坑（原文没讲）**
1. **默认 key 是对输入 pickle 后 hash** → 输入里含"当前时间/随机数"就永远命中不了。
2. **有副作用的节点不能缓存**（发邮件、下单）——缓存命中=不执行，业务直接丢单。
3. 缓存是**跨 thread 的**（按输入 key，不看 thread_id）→ 同一输入不同用户会拿到同一个结果，涉及个人数据时必须自定义 `key_func`。
4. TTL 设太长 → 数据更新了还在返回旧答案。

```python
# 自定义 key：把用户与输入一起做键
CachePolicy(ttl=300, key_func=lambda args: hashlib.md5(
    f"{args['state']['user_id']}|{args['state']['query']}".encode()).hexdigest())
```

### 4.4 节点重试

```python
from langgraph.types import RetryPolicy

builder.add_node("call_api", call_api,
                 retry_policy=RetryPolicy(
                     max_attempts=3,
                     initial_interval=0.5,     # 秒
                     backoff_factor=2.0,       # 指数退避
                     retry_on=(TimeoutError, ConnectionError),  # 只重试这些
                 ))
```
**默认不会重试的异常**（原文列了，值得记住）：`ValueError/TypeError/ArithmeticError/ImportError/LookupError/NameError/SyntaxError/RuntimeError/ReferenceError/StopIteration/OSError` —— 这些是"代码写错了"，重试没用。

**补：重试的三条工程原则**
1. **只重试可重试的**：网络/429/5xx 重试；401/403/422（参数错）绝不重试。
2. **节点必须幂等**：重试会重复执行，写库要 `INSERT ... ON CONFLICT`，发消息要带幂等键。
3. **退避 + jitter**：固定间隔重试会把下游打挂。

### 4.5 图内外数据传递（Streaming）

#### 4.5.1 六种 `stream_mode`（原文讲了 5 种，补 `tasks`）

| 模式 | 给什么 | 典型用途 |
|---|---|---|
| `values` | 每步后的**完整状态** | 调试；流量大 |
| `updates` | 每步的**增量**（按节点分组） | 显示"正在调用工具" |
| `messages` | `(token, metadata)` 二元组 | 打字机效果 |
| `custom` | 节点里 `get_stream_writer()` 写的任意数据 | 自定义进度（"已解析 3/10 个文件"） |
| `debug` | 最详细（含任务、检查点） | 深度排查 |
| `tasks` | 任务级开始/结束事件 | 长任务进度条 |

```python
# 混合模式：一次拿到多种，chunk 变成 (mode, payload)
for mode, chunk in graph.stream(inp, config=cfg, stream_mode=["updates", "messages"]):
    if mode == "messages":
        token, meta = chunk
        print(token.content, end="", flush=True)
    elif mode == "updates":
        print("\n[step]", list(chunk.keys()))
```

```python
# 自定义流：节点内部往外推（前端进度条就靠它）
from langgraph.config import get_stream_writer

def ingest(state: State):
    writer = get_stream_writer()
    for i, f in enumerate(state["files"]):
        writer({"progress": f"{i+1}/{len(state['files'])}", "file": f})
    return {"done": True}
```

**补：`astream_events(version="v2")`** —— 需要"所有 LLM/tool 细粒度事件"时用它；只关心图状态就用 `stream`。

```python
async for ev in graph.astream_events(inp, config=cfg, version="v2"):
    if ev["event"] == "on_chat_model_stream":
        print(ev["data"]["chunk"].content, end="")
```

⚠️ 坑：`stream_mode` 传列表时 chunk 是元组；传字符串时不是——**这两行代码长得一样但返回值不同**，最多人在这里解包错。

### 4.6 人工审核节点（interrupt）

```python
from langgraph.types import Command, interrupt

def review(state: State):
    decision = interrupt({                      # 暂停，把 payload 抛给调用方
        "action": "transfer",
        "amount": state["amount"],
    })
    if decision.get("approve"):
        return {"approved": True, "amount": decision.get("amount", state["amount"])}
    return {"approved": False}

# 第一次：会停在 interrupt
res = graph.invoke({"amount": 100}, config=cfg)
print(res["__interrupt__"][0].value)

# 续跑：同一个 thread_id + Command(resume=...)
graph.invoke(Command(resume={"approve": True, "amount": 80}), config=cfg)
```

**⚠️⚠️ 最重要的一条（原文没讲透，面试和线上事故都在这）**：
> **`interrupt` 恢复时会从节点开头重新执行**，不是从 `interrupt()` 那行继续。
> 所以 `interrupt()` **之前**的任何副作用（写库、发消息、扣款）会执行两次。

正确写法：
```python
def node(state):
    # ❌ 错：interrupt 之前发消息 → 恢复后发两次
    # send_notice(state["user"])

    decision = interrupt({"preview": build_preview(state)})

    # ✅ 对：所有副作用都在 interrupt 之后
    send_notice(state["user"], decision)
    return {"done": True}
```
进阶：把副作用做成**幂等**（带 `idempotency_key`），或把"生成预览"这类计算**缓存**在 state 里（用 `interrupt` 返回值写回），避免重复计算。

**补：多中断与并行中断**——一个超步内有多个节点调 `interrupt()`，`__interrupt__` 会返回**列表**，`Command(resume={interrupt_id: value})` 时要用 id 区分。前端要做成"待办列表"，不是一个弹窗。

**补：静态断点 vs 动态中断**

| | 用法 | 场景 |
|---|---|---|
| 静态 `compile(interrupt_before=["x"])` | 编译期写死 | 调试、强制审核 |
| 动态 `interrupt()` | 节点内按条件调 | 业务级审批（金额>1000 才拦） |

---

## 五、边（Edge）

### 5.1 边的本质

Pregel 里，边 = **节点订阅哪些通道 + 执行后更新哪些通道**。理解这一点，就能解释"为什么并行节点不能互相读"。

三种边：普通边 `add_edge`、条件边 `add_conditional_edges`、以及**隐式边**——节点返回 `Command(goto=...)`。

### 5.2 条件边

```python
from typing import Literal

def route(state: State) -> Literal["b", "c"]:
    return "b" if state["value"] % 2 == 0 else "c"

builder.add_conditional_edges("a", route, {"b": "node_b", "c": "node_c"})
```

**补：路由函数的三种返回形式（原文只讲了一种）**

```python
def route(state):
    # 1) 返回节点名（字符串）
    # 2) 返回 END
    # 3) 返回 Command —— 边不用映射表，直接带状态更新
    return Command(goto="node_b", update={"step": "routed"})

    # 4) 返回 Send 列表 —— 动态扇出（见 5.4）
```

⚠️ 坑：`add_conditional_edges` 不传映射表时，路由函数**必须返回真实节点名**；传了映射表，返回的是**映射表的键**（原文示例里 `node_b_alias` 这种别名就是为了这个，很多人写成节点名然后 KeyError）。

### 5.3 可控循环

```python
graph.invoke(inp, config={"recursion_limit": 25})   # 默认 25，超过抛 GraphRecursionError
```
- 一个"超步"= 一次并行执行批次，不是"一个节点"，所以 25 步可能跑了上百个节点。
- **循环必须有确定出口**：靠 state 里的计数/标志位/最大轮数，不要靠"模型应该会停"。
- 生产建议 `recursion_limit` 显式设（10~40），并**捕获 `GraphRecursionError` 返回友好提示**。

**补：循环最容易被忽略的两种死法**
1. 条件边永远返回同一分支（模型输出解析失败 → 一直重试）→ 加失败计数。
2. 循环里每轮都往 `messages` 追加 → 上下文爆炸，第 5 轮就超模型窗口 → 配 `trim` 节点。

### 5.4 【新增】并行、扇出与 `Send`（原笔记缺失，大厂必用）

**场景**：一次要处理 20 个文档/20 个城市/20 个用户的子任务——这是"图"相对"链"最大的优势。

```python
from langgraph.types import Send

def fan_out(state: State):
    # 每个 item 起一个独立的并行分支，每个分支拿到自己的入参
    return [Send("process_one", {"doc_id": d}) for d in state["doc_ids"]]

builder.add_conditional_edges("plan", fan_out, ["process_one"])
builder.add_node("process_one", process_one)      # 结果用 Annotated[list, add] 汇总
```
三个要点：
1. `Send` 的分支**入参就是你给的那个 dict**，不是全局 state（要自己带上下文）。
2. 汇总靠 reducer（`Annotated[list, operator.add]`），**顺序不确定**——需要顺序就带 `index` 字段最后排序。
3. 并行度受 `max_concurrency` 控制：`invoke(..., config={"max_concurrency": 5})`，否则 20 个分支同时打 LLM API → 429。

### 5.5 【新增】子图（Subgraph）：模块化与复用

```python
sub = sub_builder.compile()                 # 先编译成图
main.add_node("research", sub)              # 直接当节点用（共享同名 state 键）

# 或包一层，做 schema 转换（子图 state 与父图不同名时）
def call_sub(state: ParentState):
    out = sub.invoke({"query": state["topic"]}, config=cfg)
    return {"research": out["result"]}
main.add_node("research", call_sub)
```
| 用法 | 好处 | 坑 |
|---|---|---|
| 直接 `add_node(compiled)` | 状态自动共享，代码最少 | 键名必须对得上，否则静默不传 |
| 包一层函数 | 完全解耦，可做 schema 映射 | checkpointer 不共享（子图要单独传） |

⚠️ 子图需要自己的 checkpointer 才能在自己的 `thread_id` 上恢复；父图恢复**不会**自动带上子图历史，除非用 `config` 透传（`sub.invoke(..., config=cfg)`）。

### 5.6 【新增】长期记忆：`Store`（跨会话）

`checkpointer` 管"一次会话内的状态"，`Store` 管"跨会话的用户记忆"。两者别混。

```python
from langgraph.store.memory import InMemoryStore      # 生产用 PostgresStore
store = InMemoryStore()
graph = builder.compile(checkpointer=cp, store=store)

# 节点里读写（namespace 是元组，建议 ("users", user_id)）
def remember(state: State, runtime: Runtime):
    runtime.store.put(("users", state["user_id"]), "profile", {"city": "杭州"})
    hits = runtime.store.search(("users", state["user_id"]), limit=5)
    return {"answer": f"我记得你在{hits[0].value['city']}"}
```
| | Checkpointer | Store |
|---|---|---|
| 粒度 | 每个 thread（会话） | 任意 namespace（如按用户） |
| 内容 | 完整图状态 | 你主动读写的小块数据 |
| 是否自动 | ✅ 自动每步存 | ❌ 手动 put/get |
| 用途 | 恢复、时间旅行、中断 | 用户画像、偏好、长期事实 |

---

## 六、【新增】容错与工程化（原文没有，面试必问）

### 6.1 四层容错，别只做一层

| 层 | 手段 | 配置位置 |
|---|---|---|
| HTTP/客户端 | 超时 + 连接池 | SDK 初始化 |
| 节点 | `RetryPolicy` | `add_node(..., retry_policy=)` |
| 节点 | 幂等 + 失败兜底节点 | 业务代码 |
| 图 | `recursion_limit` + 超时 + 降级分支 | `config` / 条件边 |

```python
# 超时：LangGraph 没有全局 timeout，用 asyncio.wait_for 包住
import asyncio
try:
    res = await asyncio.wait_for(graph.ainvoke(inp, config=cfg), timeout=60)
except asyncio.TimeoutError:
    return {"answer": "处理超时，请稍后重试"}      # 降级，不要把异常抛给用户
```

### 6.2 结构化输出

```python
from pydantic import BaseModel

class Plan(BaseModel):
    steps: list[str]
    risk: str

def planner(state: State):
    out = llm.with_structured_output(Plan).invoke(state["query"])
    return {"plan": out.steps, "risk": out.risk}
```
**做法对比**：图里节点直接 `with_structured_output`（简单、可控）；整个 Agent 要结构化结果用 `create_agent(response_format=ToolStrategy(Plan))`。**别在节点里手写 `json.loads(模型输出)`**——解析失败率会让你怀疑人生。

### 6.3 测试

```python
def test_route_even():
    g = build_graph().compile()           # 不传 checkpointer，纯函数式
    assert g.invoke({"value": 2})["step"] == "B执行完毕"

def test_interrupt_flow():
    g = build_graph().compile(checkpointer=InMemorySaver())
    cfg = {"configurable": {"thread_id": "t"}}
    r = g.invoke({"amount": 100}, cfg)
    assert "__interrupt__" in r                       # 断言"会中断"
    r = g.invoke(Command(resume={"approve": True}), cfg)
    assert r["approved"] is True
```
要断言**图的行为**（走了哪条边、有没有中断、状态对不对），不要断言 LLM 原话。

### 6.4 可观测性

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=ls-xxx
LANGSMITH_PROJECT=lg-demo
```
至少要能看到：节点级耗时、每步 state 快照、LLM token 数、工具入参出参。没有这些，"为什么这次答错了"只能靠猜。

---

## 七、【新增】多 Agent 的四种形态（选型不踩坑）

| 形态 | 怎么做 | 优点 | 缺点 | 什么时候用 |
|---|---|---|---|---|
| **单 Agent + 多工具** | `create_agent` | 简单、便宜、好调 | 工具多于 15 个选不准 | 80% 的场景 |
| **Supervisor（主管）** | 一个路由节点决定调哪个子 Agent | 可控、易调试 | 主管节点易成瓶颈 | 有明确分工（检索/写作/审核） |
| **Handoff（接力）** | 节点返回 `Command(goto="other_agent")` | 上下文传递自然 | 状态命名要统一 | 客服转人工/转专家 |
| **Swarm / 自组织** | 多个 Agent 互相调用 | 灵活 | 调试地狱、成本翻倍 | 研究性场景，生产慎用 |

```python
# Supervisor 最小实现（比"多 Agent"框架更可控）
def supervisor(state: State) -> Command:
    nxt = llm.with_structured_output(Route).invoke(state["messages"]).next
    return Command(goto=nxt)
```
**面试金句**：*多 Agent 的目的是**隔离上下文**和**拆分职责**，不是让模型"开会"。能用工具解决就别上多 Agent。*

---

## 八、【新增】部署（从本地到线上）

| 方式 | 怎么做 | 适合 |
|---|---|---|
| 自己包 FastAPI | `graph.astream` + SSE，Docker 部署 | **绝大多数公司**（可控、便宜） |
| `langgraph dev` | 本地起服务 + Studio | 开发调试 |
| `langgraph build/up` | 打镜像、起容器 | 自建 |
| LangSmith Deployment | 托管，自动扩缩容 | 要 SLA、不想运维 |

```python
# 自己包：SSE 流式（生产最常见形态）
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
app = FastAPI()

@app.post("/chat")
async def chat(q: str, thread_id: str):
    cfg = {"configurable": {"thread_id": thread_id}, "recursion_limit": 25}
    async def gen():
        async for mode, chunk in graph.astream(
            {"messages": [{"role": "user", "content": q}]},
            config=cfg, stream_mode=["messages", "updates"]):
            if mode == "messages":
                tok, _ = chunk
                if tok.content:
                    yield f"data: {tok.content}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream")
```
生产必加：`thread_id` 鉴权（防越权读别人会话）、Nginx `X-Accel-Buffering: no`、连接断开时 `finally` 清理、`recursion_limit` 兜底。

---

## 九、开发中最容易踩的坑（20 条，按出现频率排）

**状态**
1. 忘了 `Annotated[..., reducer]` → 以为是追加，实际每次被覆盖（最经典）。
2. 节点返回 `None` 以为是清空，实际是"不更新"。
3. 私有状态 schema 里有全局 state 没有的键 → 静默丢弃，不报错。
4. 用 Pydantic 做 state 又想放不可序列化对象（连接、锁） → checkpoint 序列化失败。
5. `messages` 用 `operator.add` 而不是 `add_messages` → 无法删除、无法按 id 更新。

**存储与恢复**
6. `PostgresSaver` 忘 `setup()`。
7. `input={}` 当"继续"用 → 实际用空输入覆盖，历史白存。
8. `thread_id` 用单层用户 id → 多窗口串话。
9. 恢复时期待"从出错那行继续" → 实际从**节点开头**重跑，副作用重复。
10. 把 `api_key`/token 放进 state → 落盘泄露。

**流式**
11. `stream_mode` 传列表后按 dict 解包 → 拿到元组报错。
12. 只推 token 不推"正在调用工具" → 长工具调用时前端看起来卡死。
13. Nginx 没关缓冲 → 流式变一次性。

**节点**
14. 给有副作用的节点配缓存 → 命中即不执行，业务丢单。
15. 缓存默认 key 含时间戳 → 永不命中。
16. `RetryPolicy` 重试了 `ValueError` → 重试 3 次还是错，浪费时间与 token。
17. 节点内部吞掉异常返回空字符串 → 图"正常"跑完，输出是错的（比报错更危险）。

**图结构**
18. 条件边返回节点名但传了映射表 → KeyError。
19. 并行分支写同一个非 reducer 字段 → 后写覆盖先写，结果随机。
20. 循环没有计数出口 → `GraphRecursionError`，用户看到 500。

**中断**
21. `interrupt` 之前有副作用 → 恢复后执行两次。
22. 不配 checkpointer 用 `interrupt` → 直接报错。
23. 多个中断用 `Command(resume=value)` 不带 id → 恢复错位置。

---

## 十、面试重点难点（展开版）

> 用法：先自己答，再看"参考要点"；带 🔥 的是 2026 年高频。

### 概念层

**🔥1. LangGraph 和 LangChain 到底什么关系？**
考的是你有没有分清"运行时"和"框架"。参考要点：LangGraph 是低层运行时（状态机 + 持久化 + 流式 + 中断）；LangChain 的 `create_agent` 就建在它上面；两者可独立使用；`create_react_agent` 在 v1 已弃用。
追问：*那什么情况必须下到 LangGraph？*——需要显式分支/并行/人工审核/断点恢复/多 Agent 编排时。

**🔥2. 为什么说 LangGraph 的"状态"是核心？**
参考：状态是节点间唯一的通信通道（Pregel 通道），节点只返回增量，合并规则由 reducer 决定；checkpoint 存的就是每个超步后的状态；所以"状态设计错了，后面全错"。
追问：*部分更新和覆盖怎么区分？*——看有没有 `Annotated[..., reducer]`。

**3. 一个超步（superstep）里发生了什么？**
参考：所有被激活的节点并行执行 → 它们的写入按 reducer 合并 → 生成 checkpoint → 决定下一批节点。
追问：*并行节点能读到彼此的结果吗？*——不能，下一超步才可见。

### 工程层

**🔥4. 图跑到一半崩了怎么恢复？**
参考：`PostgresSaver` + 固定 `thread_id` + `invoke(None, cfg)`；恢复粒度是最后一个成功的 checkpoint（出错节点会重跑，节点要幂等）。
追问：*和"重试节点"有什么区别？*——重试在节点级、同一进程内；恢复是跨进程、从持久化状态继续。

**🔥5. `interrupt` 的实现原理？为什么要求节点幂等？**
参考：中断时保存 checkpoint 并把 payload 抛给调用方；恢复时 LangGraph **重新执行整个节点**，`interrupt()` 这次直接返回 resume 值。所以中断前的副作用会执行两次 → 必须幂等或把副作用移到中断之后。

**6. `stream_mode` 有几种？分别给什么？**
参考：`values/updates/messages/custom/debug/tasks`；`messages` 给 `(token, metadata)`；混合模式传列表，chunk 变 `(mode, payload)`。
追问：*前端要做"进度条 + 打字机"怎么办？*——`["messages","custom"]`，custom 推进度。

**7. 节点缓存什么时候是**危险**的？**
参考：有副作用（写库/发消息）、输入含时间或随机、结果依赖用户身份但 key 没带用户 id、数据会变但 TTL 太长。

**🔥8. 怎么防止死循环？**
参考：`recursion_limit`（默认 25，按超步算）+ 状态里的计数器/最大轮数 + 条件边保证有出口 + 捕获 `GraphRecursionError` 降级。别指望"模型会停"。

**9. 大任务（20 个子任务）怎么并行？**
参考：条件边返回 `[Send("worker", {...}) for ...]` 扇出；结果用 `Annotated[list, operator.add]` 汇总；`max_concurrency` 控并发防 429；顺序不确定要带 index 排。

### 架构层

**🔥10. 什么时候不该用 LangGraph？**
参考：线性 RAG、单轮问答、标准工具 Agent（先用 `create_agent`）。上图的成本是：调试复杂度、多一层抽象、团队学习成本。

**11. 短期记忆和长期记忆怎么分？**
参考：checkpointer（thread 级、自动、含完整状态）vs store（namespace 级、手动、小块事实）。常见错误是把用户画像塞 state 里，导致每次会话都要重建。

**12. 多 Agent 一定要用 LangGraph 吗？**
参考：不用框架也能做（一个 `Command(goto=...)` 就是 handoff）；框架的价值是持久化与可视化。判断标准是"是否需要上下文隔离与独立恢复"。

**13. 生产部署你怎么做？**
参考：FastAPI + `astream` + SSE；`thread_id` 带租户与用户做鉴权；Postgres checkpointer；LangSmith/Langfuse trace；`recursion_limit` 与超时；Nginx 关缓冲；压测看 P95。

**14. 图状态里放不下大对象（10MB 文档）怎么办？**
参考：state 只放引用（id/路径），大对象进对象存储或 store；否则 checkpoint 膨胀、序列化变慢、DB 爆炸。

**15. 怎么调试"这次走错分支了"？**
参考：`get_state_history` 看每步 state 与 `next`；Studio 可视化；在路由函数打日志（输入 state → 返回值）；`update_state` 改字段复现。

### 深挖层

**16. Pregel 模型下"节点并行"和 `asyncio` 并发什么关系？**
参考：图层面并行是超步调度；节点内部若调外部 API，需自己用 async 才能真正并发；同步节点会占线程。

**17. checkpointer 存什么？为什么按超步而不是按节点？**
参考：存超步后的完整状态 + 待执行任务（`next`）+ 元数据；按超步才能保证"恢复时的一致性"（半个超步的状态是不合法的）。

**18. `Command` 和条件边有什么区别？**
参考：条件边只决定去哪，不改状态；`Command` 一次完成"改状态 + 跳转"，还能 `resume` 中断。条件边可测性好，`Command` 代码更短。

**19. 子图的 checkpointer 和父图共享吗？**
参考：不共享；要恢复子图历史得显式传同一 `config`。这是"子图里 interrupt 恢复不了"的常见原因。

**20. 如果让你优化一个 P95 8 秒的 LangGraph 服务，从哪下手？**
参考：先看 trace 找最慢节点（常是 LLM 调用或 rerank）→ 并行化无依赖节点 → 流式返回首字 → 缓存昂贵且幂等的节点 → 换小模型/减少上下文 → 最后才是加机器。

---

## 十一、错误速查（报错 → 原因 → 解法）

| 报错 / 现象 | 原因 | 解法 |
|---|---|---|
| `GraphRecursionError` | 超过 `recursion_limit`（默认 25 超步） | 加出口条件；显式设 `recursion_limit`；捕获后降级 |
| `KeyError: 'xxx'` on conditional edges | 路由返回的是节点名，但传了映射表 | 返回映射表的键 |
| `InvalidUpdateError` | 并行节点写了同一个无 reducer 的键 | 加 reducer 或改用独立字段 |
| `Checkpointer required for interrupt` | 用了 `interrupt` 但没配 checkpointer | `compile(checkpointer=...)` |
| `No checkpointer set` / 状态没恢复 | `config` 里没传 `thread_id`，或后端不一致 | 统一 `thread_id` 与同一 checkpointer 实例 |
| 流式没反应/一次性返回 | `stream_mode` 用错，或 Nginx 缓冲 | 用 `messages`；`X-Accel-Buffering: no` |
| 状态字段"消失" | 节点参数标注了私有 schema，键不在其中 | 检查 annotation 与键名 |
| checkpoint 表不存在 | `PostgresSaver` 没 `setup()` | 首次调用前 `setup()` |
| 副作用执行两次 | `interrupt` 前有副作用 | 移到 `interrupt` 之后 / 幂等化 |
| 序列化失败 | state 里有连接/锁/函数 | 只放可序列化数据 |

---

## 十二、API 速查表（开发时直接抄）

| 想做什么 | 代码 |
|---|---|
| 建图 | `StateGraph(State, context_schema=Ctx)` |
| 加节点 | `g.add_node("name", fn, retry_policy=..., cache_policy=...)` |
| 普通边 | `g.add_edge(START, "a")` / `g.add_edge("a", END)` |
| 条件边 | `g.add_conditional_edges("a", route, {"k": "node"})` |
| 扇出 | `return [Send("worker", {...}) for x in items]` |
| 节点内跳转+改状态 | `return Command(goto="b", update={"x": 1})` |
| 中断 | `interrupt(payload)`；续跑 `invoke(Command(resume=v), cfg)` |
| 编译 | `g.compile(checkpointer=cp, store=st, cache=InMemoryCache())` |
| 调用 | `graph.invoke(inp, config=cfg, context=Ctx(...), durability="async")` |
| 流式 | `graph.stream(inp, cfg, stream_mode=["messages","updates"])` |
| 取状态 | `graph.get_state(cfg)` / `graph.get_state_history(cfg)` |
| 改状态 | `graph.update_state(cfg, {"x": 1}, as_node="a")` |
| 恢复 | `graph.invoke(None, cfg)` |
| 看图 | `graph.get_graph().draw_mermaid()` |
| 自定义流 | `get_stream_writer()({"progress": 1})` |
| 长期记忆 | `runtime.store.put(("users", uid), "k", {...})` |

**导入位置总表**（免得每次都翻文档）

```python
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from langgraph.types import Command, Send, interrupt, RetryPolicy, CachePolicy
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.memory import InMemoryStore
from langgraph.cache.memory import InMemoryCache
from langgraph.runtime import Runtime
from langgraph.config import get_stream_writer
from langgraph.errors import GraphRecursionError
```

---

## 十三、2026 趋势：这一层正在变成什么样

| 趋势 | 现状 | 对你的影响 |
|---|---|---|
| **Harness 化** | 框架不再只给"链"，而是给"运行时 + 中间件 + 权限" | 会写中间件 > 会写链 |
| **Deep Agents 预装** | `create_deep_agent` 自带文件系统/规划/子 Agent/摘要 | 少自己造；但要能讲清"它替你做了什么" |
| **托管化** | LangSmith Deployment 一类托管运行时 | 部署能力在贬值，**编排设计能力在升值** |
| **评估与可观测成刚需** | trace + eval 是标配 | 只会"跑通"的人会被筛掉 |
| **Agent 安全** | 工具权限、沙箱、HITL 成企业准入门槛 | 面试问"怎么防越权"是常规题 |
| **多 Agent 降温** | 从"Agent 开会"回归"单 Agent + 工具 + 好提示词" | 别把多 Agent 写简历第一行 |

---

## 十四、和你的学习进度的配合

| 阶段 | 重点章节 | 产出 |
|---|---|---|
| 本周（入门） | 一、二、三 | 跑通 10 行示例 + 用 Studio 看一次图 |
| 状态吃透 | 三（reducer 语义） | 自己写 3 个 reducer（限长/去重/累加） |
| 节点边 | 四、五 | 手写一个"检索→判断→重试"分支图 |
| 上强度 | 5.4 Send、5.5 子图、5.6 Store | 20 文档并行处理 + 用户记忆 |
| 生产化 | 六、八、九 | FastAPI + SSE + Postgres checkpointer + 压测 |
| 面试冲刺 | 十、十一、十二 | 能 3 分钟讲清"崩了怎么恢复""为什么 interrupt 要幂等" |

> ⚠️ 与你 8 周计划的关系：**LangGraph 是 W5（Agent 工具编排）和 W6（部署）的主技术**。本周只要跑通 一~三，别提前啃 Send/子图——课上讲到再回来看 §5.4–5.6。

---

## 附：参考来源

- LangGraph 概览：<https://docs.langchain.com/oss/python/langgraph/overview>
- LangGraph v1 变化（`create_react_agent` 弃用）：<https://docs.langchain.com/oss/python/releases/langgraph-v1>
- LangChain v1 `create_agent`：<https://docs.langchain.com/oss/python/releases/langchain-v1>
- 迁移指南：<https://docs.langchain.com/oss/python/migrate/langgraph-v1>
- GitHub：<https://github.com/langchain-ai/langgraph>

> 版本提醒：`durability` 取值、`RetryPolicy`/`CachePolicy` 字段、`Runtime` 的导入路径在小版本间有调整，标 ⚠️ 处请用 `help()` 或 API reference 再确认一次。

# TypeScript 学习笔记（基础+高频+高阶+Vue配套）

> 
> 文件名：`typescript-notes.md`
> 适用：Vue3 + TS 开发，从入门到常用实战写法，剔除冷门语法，优先保留业务高频代码

# TypeScript 学习笔记
> 配套 Vue3 + TS 开发，分为：基础语法、高频类型、高阶类型、Vue 实战配套、常见坑

## 目录
1. [基础介绍与环境](#1-基础介绍与环境)
2. [基础类型](#2-基础类型)
3. [类型注解 & 类型推断](#3-类型注解--类型推断)
4. [函数类型（高频）](#4-函数类型高频)
5. [对象、接口 Interface](#5-对象-接口-interface)
6. [类型别名 Type](#6-类型别名-type)
7. [联合类型 | 交叉类型 &](#7-联合类型--交叉类型-)
8. [泛型 Generic（重点）](#8-泛型-generic重点)
9. [工具类型（内置，高频）](#9-工具类型内置高频)
10. [类型断言、非空断言](#10-类型断言非空断言)
11. [枚举 Enum](#11-枚举-enum)
12. [类 Class](#12-类-class)
13. [高级：infer、模板字面量类型](#13-高级infer模板字面量类型)
14. [Vue3 + TS 配套写法（核心）](#14-vue3--ts-配套写法核心)
15. [TS 配置 tsconfig.json 常用项](#15-tsconfigjson-常用项)
16. [常见报错 & 踩坑清单](#16-常见报错--踩坑清单)

## 1. 基础介绍与环境

### 什么是 TS
TypeScript = JavaScript 的超集，**静态类型检查**，编译后输出 JS；浏览器/Node 不直接识别 TS，必须编译。
- 优势：编译期捕获类型错误、代码提示、重构友好、适合大型项目
- 后缀：`.ts` / `.tsx`（React），Vue 中是 `.vue` + `<script setup lang="ts">`

### 安装
```bash
# 全局
npm install -g typescript
# 项目内
npm install -D typescript
# 查看版本
tsc -v
```

### 编译命令

```
tsc demo.ts          # 生成 demo.js
tsc --init           # 生成 tsconfig.json
```

---

## 2. 基础类型

```
// 布尔
let flag: boolean = true
// 数字（不分 int/float）
let num: number = 100
// 字符串
let str: string = "hello"
// 数组 两种写法
let arr1: number[] = [1,2,3]
let arr2: Array<string> = ["a","b"]
// 元组 Tuple：固定长度、固定位置类型
let tuple: [string, number] = ["张三", 18]
// null / undefined
let n: null = null
let u: undefined = undefined
// any：关闭类型校验（尽量少用！逃生舱）
let anyVal: any = "abc"
anyVal = 123
// unknown：安全的 any，不能直接操作，必须先类型收窄
let unk: unknown = "test"
// void：函数无返回值
function fn(): void {}
// never：永远不会返回（抛出异常、死循环）
function err(): never { throw new Error("error") }
```

> 
> ✅ 业务建议：优先 `unknown`，拒绝滥用 `any`

---

## 3. 类型注解 & 类型推断

```
// 类型注解：手动标注 :type
let a: string = "test"

// 类型推断：TS自动识别，省略注解
let b = 20 // TS自动推断 b:number

// 空对象/数组无法推断时，必须注解
let list: string[] = []
```

---

## 4. 函数类型（高频）

```
// 基础：参数类型 + 返回值类型
function add(a: number, b: number): number {
  return a + b
}

// 可选参数 ?
function say(name: string, msg?: string): string {
  return msg ? `${name}:${msg}` : name
}

// 默认参数
function greet(name: string = "guest") {
  return name
}

// 箭头函数类型
const mul = (a: number, b: number): number => a * b

// 函数类型表达式
type FnType = (x: number, y: number) => number
const calc: FnType = (a,b) => a + b

// 剩余参数
function sum(...args: number[]): number {
  return args.reduce((p,c)=>p+c,0)
}
```

---

## 5. 对象、接口 Interface

> 
> Interface：描述**对象结构**，可以继承、合并声明；推荐用来定义实体、后端返回数据结构

```
interface User {
  id: number
  name: string
  age?: number // 可选属性
  readonly avatar: string // 只读，不可修改
}

const u: User = {
  id: 1,
  name: "tom",
  avatar: "xxx.png"
}

// 接口继承
interface Admin extends User {
  permission: string[]
}
```

> 
> 区别：`interface` 适合对象结构、支持extends；`type` 更灵活，可以写联合、交叉

---

## 6. 类型别名 Type

```
type Status = "success" | "fail" | "loading"

type Goods = {
  id: number
  title: string
  price: number
}

// type 交叉
type A = {a:number}
type B = {b:string}
type C = A & B
```

> 
> 简单口诀：
> 
> 
> - 定义对象实体、后端结构 → `interface`
> - 联合类型、工具组合、简单别名 → `type`

---

## 7. 联合类型 | 交叉类型 &

```
// 联合：满足其中一种
type Sex = "man" | "woman"
let s: Sex = "man"

// 类型收窄（联合必用）
function printId(id: number | string) {
  if(typeof id === "string") {
    console.log(id.toUpperCase())
  } else {
    console.log(id.toFixed(2))
  }
}

// 交叉 &：同时满足全部
type Person = {name:string} & {age:number}
const p: Person = {name:"jack", age:20}
```

---

## 8. 泛型 Generic（重点）

> 
> 泛型：类型参数，**组件/函数复用，保留类型信息**，Vue 中表单、列表、请求封装高频

```
// 基础泛型函数
function getArr<T>(val: T): T[] {
  return [val]
}
getArr<number>(10)
getArr("hi") // 自动推断 T=string

// 泛型约束 extends
interface HasLen { length: number }
function getLen<T extends HasLen>(target: T): number {
  return target.length
}
getLen("abc")
getLen([1,2,3])

// 泛型接口（后端分页标准结构）
interface PageRes<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}
// 使用
type UserPage = PageRes<User>
```

✅ 后端分页响应，这个 `PageRes<T>` 在 Vue 项目里几乎必写

---

## 9. 工具类型（内置高频）

> 
> 全部是 TS 内置，不用自己实现

```
interface User {
  id: number
  name: string
  age: number
}

// Partial：全部属性可选
type UserPartial = Partial<User>
// Required：全部属性必填
type UserRequired = Required<UserPartial>
// Readonly：全部只读
type ReadUser = Readonly<User>
// Pick：挑选部分属性
type UserPick = Pick<User, "id" | "name">
// Omit：剔除部分属性
type UserOmit = Omit<User, "age">
// Exclude：从联合类型剔除
type T1 = Exclude<"a"|"b"|"c", "a"> // "b"|"c"
// Extract：提取交集
type T2 = Extract<"a"|"b", "a"|"d"> // "a"
// Record：构造键值对类型 Record<KeyType, ValType>
type Dict = Record<string, number>
const map: Dict = { a:1, b:2 }
```

🔥 高频TOP5：`Partial / Pick / Omit / Record / Required`

---

## 10. 类型断言、非空断言

```
// 类型断言：告诉TS我比它清楚类型
const someVal: unknown = "hello"
const len = (someVal as string).length

// 非空断言 !：确定不是 null / undefined
const dom = document.getElementById("app")!
dom.innerHTML = "hi"
```

> 
> ⚠️ 风险：断言只是告诉编译器，**不会做运行时校验**，不要滥用

---

## 11. 枚举 Enum

适合状态码、字典、固定选项

```
enum OrderStatus {
  PENDING = 0,
  PAID = 1,
  FINISH = 2
}
// 反向映射
console.log(OrderStatus[0]) // PENDING

// 字符串枚举（推荐，无反向映射，更干净）
enum Sex {
  MALE = "M",
  FEMALE = "F"
}
```

> 
> 业务优先字符串枚举，数字枚举容易出现反向映射坑

---

## 12. 类 Class

```
class Animal {
  // 访问修饰符 public / private / protected
  public name: string
  private age: number
  constructor(name: string, age: number) {
    this.name = name
    this.age = age
  }
  say(): void {
    console.log(this.name)
  }
}
```

- `public`：默认，任意访问
- `private`：仅类内部
- `protected`：类内部 + 子类

---

## 13. 高级：infer、模板字面量类型

> 
> 适合封装工具类型，Vue 请求封装、组件提取类型会用到

```
// infer：在条件类型里提取类型
type GetReturnType<T> = T extends (...args: any[]) => infer R ? R : never
type Fn = () => string
type Ret = GetReturnType<Fn> // string

// 模板字面量类型
type EventName = `on${Capitalize<string>}`
type ClickEvt = `onClick`
```

---

## 14. Vue3 + TS 配套写法（核心）

> 
> `<script setup lang="ts">` 组合式语法糖，项目主流

### 1. defineProps 类型

```
<script setup lang="ts">
interface Props {
  title: string
  count?: number
}
const props = defineProps<Props>()

// 需要默认值时，withDefaults
const props = withDefaults(defineProps<Props>(), {
  count: 0
})
</script>
```

### 2. defineEmits

```
const emit = defineEmits<{
  change: [val: number]
  submit: [data: User]
}>()
// 使用 emit("change", 100)
```

### 3. ref / reactive

```
import { ref, reactive } from "vue"

// ref 基础类型会自动推断
const num = ref(0)
// ref 对象，建议显式标注
const user = ref<User>()

// reactive
const form = reactive<User>({
  id:1,
  name:""
})
```

### 4. computed

```
const double = computed<number>(() => num.value * 2)
```

### 5. 泛型组件 defineProps + 泛型（表格分页组件高频）

```
defineProps<{
  list: T[]
}>()
// 泛型组件写法
const props = defineProps<{
  data: T[]
}>() as { data: T[] }
```

### 6. Axios 请求封装搭配 TS（高频模板）

```
// 统一响应结构
interface ApiRes<T> {
  code: number
  data: T
  msg: string
}

// 请求函数
async function getUser(): Promise<ApiRes<User>> {
  return axios.get("/api/user")
}
```

### 7. vue-router 路由类型

```
import type { RouteLocationNormalizedLoaded } from "vue-router"
const route = useRoute() as RouteLocationNormalizedLoaded
```

---

## 15. tsconfig.json 常用项

```
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    /* 模块 */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    /* 严格类型（Vue项目推荐开启！） */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.vue"]
}
```

> 
> `"strict": true` 是 TS 灵魂，强制类型校验，不要关

---

## 16. 常见报错 & 踩坑清单

1. `Object is possibly 'null'`：加非空断言 `!` 或者判断收窄
2. `Property 'xxx' does not exist on type '{}'`：缺少类型注解，补上 interface
3. `any` 泛滥：优先 `unknown` + 类型判断
4. defineProps 默认值：必须搭配 `withDefaults`，直接赋值无效
5. reactive 赋值覆盖丢失响应：优先 ref 或者 Object.assign
6. 泛型组件类型丢失：给 props 手动 as 断言
7. 枚举不要滥用：简单固定字符串优先联合字面量，更轻量
8. ts 识别不了 .vue 文件：需要 `env.d.ts`

```
// env.d.ts
declare module "*.vue" {
  import type { DefineComponent } from "vue"
  const component: DefineComponent<{}, {}, any>
  export default component
}
```

```

---

## 使用方式
1. 复制上面全部内容
2. 在本地新建文件，命名：`typescript-notes.md`
3. 粘贴保存，VSCode 打开直接预览

如果你想要，我可以再额外给你：
- 一份配套 `env.d.ts`
- 一份 axios 请求封装完整版 TS 文件
- 或者单独抽一份 Vue3+TS 高频代码片段小抄版（单独md）
```
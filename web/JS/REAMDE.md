# JavaScript 学习笔记（README.md）

> 面向后端开发者学习前端JS，参考课程讲义，补充参数说明、示例、注意事项、避坑点；包含：JS基础语法、变量、运算符、流程控制、数组、函数、BOM、DOM、事件、JSON、正则表达式。

## 目录

1. JavaScript 基础介绍
2. JS代码引入方式
3. JS输出方式
4. 数据类型与变量(var / let / const)
5. 运算符
6. 流程控制
7. 数组 Array
8. 函数
9. BOM 浏览器对象模型
10. DOM 文档对象模型【重点】
11. JS事件【重点】
12. JSON 数据格式（前后端交换数据）
13. 正则表达式
14. 高频避坑总结

------

# 1 JavaScript 基础介绍

JavaScript 是**浏览器端解释型脚本语言**，不需要编译，逐行解释执行。

> HTML 负责结构，CSS负责美化，**JS负责交互，实现页面动态效果**。

## JS三大组成部分

| 组成       | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| ECMAScript | JS语法规范：变量、数据类型、运算符、循环、函数               |
| BOM        | Browser Object Model 浏览器对象模型：操作浏览器窗口、弹窗、地址栏 |
| DOM        | Document Object Model 文档对象模型：操作页面HTML标签（增删改查标签、属性、文本） |

### JS语言特点

1. **弱类型**：变量不固定类型，可以随时接收数字、字符串、对象；自动隐式类型转换。
2. **事件驱动**：监听用户点击、输入等行为做出响应。
3. **跨平台**：只需要浏览器支持，不依赖操作系统。
4. **基于对象**：可以使用、创建对象；不完全等同于Java面向对象。

## JS注释

```
// 单行注释
/*
多行注释
*/
```

------

# 2 JS代码引入方式

## 方式1：内部脚本

页面中使用 `<script>` 标签写js代码；script标签可以放在html任意位置（head / body末尾）。

> ⚠️建议写在`</body>`标签**前面**，保证html标签先加载完毕，JS才能获取DOM元素。

```
<body>
<script>
console.log("hello js");
</script>
</body>
```

## 方式2：外部js文件（项目推荐）

新建后缀为`.js`文件，html使用`src`引入外部脚本。

> ⚠️ 标签写了`src`，标签内部写的js代码不会执行！

```
<script src="js/demo.js"></script>
```

demo.js

```
console.log("外部js文件执行");
```

------

# 3 JS三种输出方式

| 方法                     | 作用             | 特点                                       |
| ------------------------ | ---------------- | ------------------------------------------ |
| `alert("内容")`          | 浏览器弹窗输出   | **阻塞代码执行**；里面html标签不会解析生效 |
| `document.write("内容")` | 页面输出文本     | 可以解析html标签                           |
| `console.log("内容")`    | 浏览器控制台输出 | 开发调试最常用，不会阻塞                   |

示例

```
alert("提示弹窗");
document.write("<h2>页面输出标题</h2>");
console.log("控制台打印日志");
```

------

# 4 数据类型与变量

## 4.1 JS六种数据类型

使用 `typeof 变量名` 判断数据类型

| 类型        | 说明                                      |
| ----------- | ----------------------------------------- |
| `number`    | 数字（整数、小数）                        |
| `string`    | 字符串；单引号`''`、双引号`""`、反引号``` |
| `boolean`   | 布尔：`true` / `false`                    |
| `object`    | 对象；`null`打印typeof结果也是object      |
| `undefined` | 变量声明，没有赋值                        |
| `function`  | 函数类型                                  |

> null 和 undefined区别

- `null`：变量有值，表示**空对象**，没有想要的数据。
- `undefined`：变量只声明，**从未赋值**。

## 4.2 变量声明 `var / let / const`

```
var a = 10;
let b = 20;
const c = 30; // const常量，不能重新赋值
```

### var vs let 核心区别

1. `var`：函数作用域，存在变量提升；循环结束外面依然可以访问循环变量。
2. `let`：**块级作用域 { }**，推荐现代JS全部使用let；大括号外面访问不到内部变量。
3. `const`：常量，声明时必须赋值，后续**禁止修改**；如果是对象，对象属性可以修改。

示例

```
for(let i=0;i<5;i++){
}
// console.log(i); // let：报错，i只在for循环块内部生效

for(var j=0;j<5;j++){
}
console.log(j); // var：循环外面可以访问j
```

> ✅开发规范：优先用`let`；不变的数据使用`const`；**尽量不要用var**。

------

# 5 运算符

## 算术运算符

```
+ - * / % ++ --
```

## 赋值运算符

```
= += -= *= /= %=
```

## 比较运算符

> `==` 只比较**值**，会自动做类型转换 `===` **全等：同时比较值 + 数据类型，开发优先使用**

```
console.log("10" == 10);  // true，只比较值
console.log("10" === 10); // false，类型不一样
```

同理：`!=`、`!==`（不全等，推荐）

## 逻辑运算符

`&&` 与；`||` 或；`!`非；支持短路运算。

## 三元运算符

```
条件 ? 满足执行 : 不满足执行
let res = 10 > 5 ? "大于5" : "小于等于5";
```

------

# 6 流程控制

`if / else if / else`；`switch`；`for`；`while`；`do‑while` 语法和Java大体一致。

```
if(条件){

}

switch(变量){
    case 值1:
        break;
    default:
}

for(let i=0;i<10;i++){

}
```

------

# 7 数组 Array

JS数组特点：

1. **数组元素可以是任意不同类型**（数字、字符串、对象混合存放）
2. **数组长度可以动态自动变化**，不需要提前固定大小。

## 7.1 创建数组

```
//方式1 字面量【推荐】
let arr = [10,20,30];

//方式2 new Array
let arr1 = new Array(); //空数组
let arr2 = new Array(5); //长度为5空数组
let arr3 = new Array(11,22,33);
```

## 7.2 数组常用API

| 方法           | 功能                               | 返回值              |
| -------------- | ---------------------------------- | ------------------- |
| `push(ele)`    | 向数组**末尾**添加一个/多个元素    | 返回新数组长度      |
| `pop()`        | 删除数组最后一个元素               | 返回被删除的元素    |
| `reverse()`    | 数组反转                           | 返回反转后的数组    |
| `concat(arr2)` | 数组拼接，不修改原数组             | 返回新数组          |
| `join("-")`    | 数组转字符串，按分隔符拼接         | 字符串；和split相反 |
| `sort()`       | 数组排序；注意默认按字符串字典排序 | 排序后数组          |

## 7.3 数组遍历

```
let arr = [10,20,30];
//普通for循环
for(let i=0; i<arr.length; i++){
    console.log(arr[i]);
}

//for‑of 增强遍历（直接拿元素）
for(let item of arr){
    console.log(item);
}
```

------

# 8 函数 function

> JS函数类似Java方法；**没有参数类型、没有返回值类型声明；有没有return决定是否返回数据。**

## 8.1 命名函数

```
//定义
function add(a,b){
    return a + b;
}
//调用
let sum = add(1,2);
```

## 8.2 匿名函数

没有函数名字，一般赋值给变量、绑定事件。

```
let fn = function(){
    console.log("匿名函数执行");
}
fn();
```

> ⚠️ JS**没有函数重载**！函数名相同，后面定义函数直接覆盖前面的。

------

# 9 BOM 浏览器对象模型

`window` 浏览器顶层对象，调用window的属性/方法，`window.`可以省略。

## 9.1 弹窗

```
alert("提示警告框");
confirm("提示确认框")
prompt（“提示输入框）

//确认框，返回布尔 true确认 / false取消
let flag = confirm("确定删除吗？");
if(flag){
    console.log("用户点击确认");
}
```

## 9.2 location地址栏对象

```
//页面跳转，修改浏览器地址
location.href = "[https://www.baidu.com](https://www.baidu.com)";
```

## 9.3 定时器（拓展）

```
//延迟执行：延迟多少毫秒执行一次
setTimeout(function(){}, 1000);

//循环定时器，每隔一段时间重复执行
setInterval(function(){},1000);
```

------

# 10 DOM 文档对象模型【重点】

DOM：把HTML全部标签转为JS对象；JS可以**获取标签、修改属性、修改文本、新增、删除标签**。

## 10.1 获取DOM标签对象

| API                                          | 作用                        | 返回值               |
| -------------------------------------------- | --------------------------- | -------------------- |
| `document.getElementById("id值")`            | 根据id获取标签              | 单个对象；id页面唯一 |
| `document.getElementsByTagName("div")`       | 按标签名字获取              | 伪数组集合           |
| `document.getElementsByName("name值")`       | 按name属性获取              | 伪数组集合           |
| `document.getElementsByClassName("class值")` | 按class类名获取             | 伪数组集合           |
| `document.querySelector("#id / .cls / div")` | CSS选择器获取**第一个匹配** | 单个对象             |
| `document.querySelectorAll("div")`           | CSS选择器获取全部匹配       | 伪数组集合           |

示例

```
<div id="box" class="c1">测试内容</div>
<script>
let box = document.getElementById("box");
console.log(box);
</script>
```

## 10.2 操作标签属性

```
//获取属性
let hrefVal = aEle.href;
//修改属性
aEle.href = "[https://xxx.com](https://xxx.com)";
```

## 10.3 innerHTML vs innerText

| 属性        | 说明                                                     |
| ----------- | -------------------------------------------------------- |
| `innerHTML` | 读写标签里面的内容；**会解析html标签**                   |
| `innerText` | 读写标签文本；**html标签当做普通文本原样显示，不会解析** |

```
ele.innerHTML = "<b>加粗文字</b>"; //页面会加粗显示
ele.innerText = "<b>加粗文字</b>"; //页面原样输出<b>符号
```

## 10.4 DOM节点新增、删除、替换

```
//1.创建标签对象
let li = document.createElement("li");
li.innerHTML = "西安";

//2.追加到父标签末尾
ul.appendChild(li);

//3.插入到某个子元素前面
ul.insertBefore(newNode, targetNode);

//4.替换子节点
ul.replaceChild(newNode, oldNode);

//5.删除标签
ele.remove();
```

------

# 11 JS事件【重点】

> 事件：监听用户页面操作（点击、输入、失去焦点等）；触发之后执行JS函数。

## 两种绑定事件写法

### 方式1：标签内绑定（不推荐，耦合html和js）

```
<input type="button" value="按钮" onclick="fn()">
<script>
function fn(){
    alert("点击了按钮");
}
</script>
```

### 方式2 JS代码绑定（项目推荐，分离结构与逻辑）

```
<input type="button" id="btn" value="按钮">
<script>
let btn = document.getElementById("btn");
//绑定匿名函数
btn.onclick = function(){
    alert("点击按钮");
}
</script>
```

## 常用事件

| 事件名       | 触发时机                                     |
| ------------ | -------------------------------------------- |
| `onclick`    | 单击鼠标                                     |
| `ondblclick` | 双击鼠标                                     |
| `onfocus`    | 输入框获得焦点（光标进入）                   |
| `onblur`     | 输入框失去焦点（光标离开）                   |
| `onchange`   | 内容发生改变，失去焦点触发（下拉框、输入框） |

> 关键字 `this`：**事件回调函数内部，this代表当前触发事件的DOM标签对象。**

```
inputEle.onchange = function(){
    console.log(this.value); // this就是input标签
}
```

------

# 12 JSON 前后端数据交换格式

JSON：JavaScript Object Notation，轻量文本数据格式，**后端和前端最主要数据交换格式**。

> ⚠️JSON只是字符串，不是JS对象；键名必须使用**双引号**，不能写单引号。

## JSON两种格式

1. 对象格式 `{ "key":值 , "key2":值2 }`
2. 数组格式 `[ {}, {}, {} ]` 支持互相嵌套。

## ⭐JSON字符串 <==> JS对象转换

```
// JS对象 → JSON字符串
let jsObj = {"name":"张三","age":18};
let jsonStr = JSON.stringify(jsObj);

// JSON字符串 → JS对象
let parseObj = JSON.parse(jsonStr);
console.log(parseObj.name);
```

> 后端接口返回给前端的数据一般都是JSON字符串，前端使用`JSON.parse()`转成js对象读取属性。

------

# 13 正则表达式 RegExp

> 正则：字符串匹配校验规则；常用于表单校验（账号、密码、邮箱）。

## 常用元字符

| 符号    | 含义                                  |
| ------- | ------------------------------------- |
| `[0‑9]` | 数字；简写`\d`                        |
| `[a‑z]` | 小写字母                              |
| `[A‑Z]` | 大写字母                              |
| `\w`    | 字母数字下划线 `[a‑zA‑Z0‑9_]`         |
| `.`     | 任意字符；匹配普通点需要转义`\.`      |
| `*`     | 0次或多次                             |
| `+`     | 1次或多次                             |
| `?`     | 0次或者1次                            |
| `{m}`   | 正好m次；`{m,n}` m‑n次；`{m,}`至少m次 |
| `^`     | 开头；在`[]`内部代表取反              |
| `$`     | 结尾                                  |

> 精确完整匹配必须加上 `^`开头、`$`结尾，否则是模糊匹配。

## 正则定义与test校验

```
//字面量定义
let reg = /^[1-9][0-9]{4,14}$/;

//test返回布尔，校验字符串是否匹配规则
let ok = reg.test("123456");
console.log(ok);
```

修饰符：`i` 忽略大小写 `/^abc$/i`

## 示例：邮箱正则

```
let emailReg = /^[a-zA-Z0-9_.-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]+$/;
```

------

# 📋高频避坑总结

1. **script标签位置**：获取DOM元素的JS代码，要写在标签后面；写在head里面会获取不到元素返回`null`。
2. `var`尽量不要用；优先`let`块级作用域，常量用`const`。
3. 比较相等：优先使用 `===` 全等，少用`==`避免隐式转换带来bug。
4. `innerHTML`识别html标签；`innerText`全部当普通文本。
5. JS函数**不存在重载**，重名函数后面直接覆盖前面。
6. JSON字符串所有key必须**双引号**，单引号不是合法JSON。
7. 正则不加`^ $`属于模糊匹配，只要包含片段就返回true；表单校验一定要写首尾限定符。
8. BOM弹窗`alert()`会阻塞后面代码执行。
9. DOM获取返回集合（伪数组）不能直接调用数组方法，必须循环遍历或者转为真数组。
10. `this`只在事件函数内部代表触发事件的dom对象；普通全局函数this指向window。
11. 外部js标签写了`src`属性，标签体内写的JS代码不会执行。

> 拓展：JS主要用于浏览器操作DOM、处理表单、接收后端JSON数据渲染页面；是前端和后端(FastAPI)交互必备基础。

---

持续更新中，欢迎指点。⭐
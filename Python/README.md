# 🐍 Python 预习笔记 (Python Study Notes)

> 📢 **学习声明**：本笔记的知识体系、大纲脉络与案例演示，**学习课程源于尚硅谷 (Atguigu) 的 Python 课程**。在此特别感谢尚硅谷老师的悉心教导，本仓库仅为个人学习过程中的知识点梳理、踩坑记录与心得沉淀。

这里记录了我学习 Python 过程中的知识点梳理、踩坑记录与心得。持续更新中，欢迎各位前辈和大神交流指正！

## 📖 目录
- [Day01：环境搭建与基础入门](#day01环境搭建与基础入门)
- [Day02：数据类型与基础语法](#day02数据类型与基础语法)
- [Day03：流程控制与序列](#day03流程控制与序列)
- [Day04：字符串、元组、集合、字典与函数](#day04字符串元组集合字典与函数)
- [Day05：函数进阶（函数、闭包与作用域）](#day05函数进阶函数闭包与作用域)
- [Day06：文件操作与面向对象基础](#day06文件操作与面向对象基础)
- [Day07：面向对象进阶（魔法方法）](#day07面向对象进阶魔法方法)
- [Day08：异常及其异常处理](#day08异常及其异常处理)
- [Day09：模块与包](#day09模块与包)
- [Day10：Python高级语法](#day10Python高级语法)
- [Day11：进程与线程](#day11进程与线程)
- [附录：Pychram快捷键]()

---



# Day01：环境搭建与基础入门

### 1. Python 简介
- **Python 的发展史**：由 Guido van Rossum（龟叔）于 1989 年圣诞节期间开发，1991 年发布第一个版本。
- **Python 的特点**：解释型、面向对象、动态数据类型、开源、跨平台、语法简洁。
- **Python 的应用领域**：Web 开发、数据分析、人工智能、自动化运维、爬虫、科学计算等。
- **Python 的版本**：目前主流为 Python 3.x，Python 2.x 已于 2020 年停止维护。**推荐使用 Python 3.10 或 3.11 版本**（稳定且兼容性好）。

### 2. 环境搭建
- **下载安装包**：去 Python 官网（`python.org`）下载对应操作系统的安装包。
- **Windows 安装注意事项**：
  - 务必勾选 **`Add Python to PATH`**（将 Python 添加到环境变量），否则后续在命令行无法直接使用 `python` 命令。
  - 选择 `Customize installation`（自定义安装），勾选 `pip` 和 `tcl/tk` 等核心组件。
  - 安装路径**不要包含中文和空格**，例如 `D:\Python\Python311`。
- **验证安装**：打开命令行（CMD），输入 `python --version` 或 `python -V`，若显示版本号则安装成功。
- **pip 包管理工具**：Python 自带的包管理器，用于安装第三方库。常用命令：
  - `pip install 库名`：安装库
  - `pip uninstall 库名`：卸载库
  - `pip list`：查看已安装的库
  - `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple 库名`：使用清华镜像加速安装

### 3. PyCharm 安装与配置
- **PyCharm 版本**：社区版（Community，免费）和专业版（Professional，收费）。初学者用社区版足够。
- **下载安装**：去 JetBrains 官网下载，安装路径建议为纯英文路径。
- **基本配置**：
  - 主题设置：`File -> Settings -> Appearance & Behavior -> Appearance -> Theme`（推荐 `Light` 或 `Darcula`）。
  - 字体设置：`Editor -> Font`，推荐字体 `JetBrains Mono`，字号 `16-18`，开启连字（Ligatures）。
  - 解释器配置：`File -> Settings -> Project -> Python Interpreter`，选择你安装的 Python 版本。

### 4. 第一个 Python 程序
```python
# 这是单行注释
print("Hello, World!")
print("Hello, Atguigu!")
```
- **运行方式**：
  - 右键 -> `Run '文件名'`。
  - 快捷键 `Shift + F10`。
  - 在下方 `Run` 窗口查看输出结果。

### 5. 变量与数据类型
- **变量的定义**：变量名 = 值，例如 `name = "张三"`、`age = 18`。
- **变量的命名规范**：
  - 由字母、数字、下划线组成，不能以数字开头。
  - 不能使用 Python 关键字（如 `if`、`for`、`while` 等）。
  - 区分大小写（`Name` 和 `name` 是不同的变量）。
  - 见名知意，推荐使用小写字母加下划线（如 `user_name`）。
- **基本数据类型**：
  - **整数（int）**：`100`、`-20`、`0`
  - **浮点数（float）**：`3.14`、`-0.5`
  - **字符串（str）**：`"Hello"`、`'Python'`
  - **布尔值（bool）**：`True`、`False`
  - **空值（None）**：`None`
- **查看数据类型**：使用 `type()` 函数，如 `print(type(100))` 输出 `<class 'int'>`。

### 6. 输入与输出
- **输出**：`print()` 函数。
  - `print("内容")`
  - `print("内容1", "内容2")`（逗号分隔，默认空格分隔）
  - `print("内容", end="")`（修改结束符，默认换行）
- **输入**：`input()` 函数。
  - `input("提示信息")` 会暂停程序，等待用户输入，返回的是**字符串类型**。
  - 如需转换为整数，需使用 `int(input("请输入数字："))`。

### 7. 注释
- **单行注释**：`# 注释内容`
- **多行注释**：使用三个单引号或三个双引号包裹。
```python
"""
这是多行注释
可以写多行内容
"""
```
- **注意**：Python 中三引号严格来说不是多行注释，而是字符串，只是没有赋值给变量时被解释器忽略，常被当作多行注释使用。

### 8. 基础运算符
- **算术运算符**：`+`、`-`、`*`、`/`、`//`（整除）、`%`（取余）、`**`（幂运算）

- **赋值运算符**：`=`、`+=`、`-=`、`*=`、`/=` 等

- **比较运算符**：`>`、`<`、`==`、`!=`、`>=`、`<=`，返回布尔值

- **逻辑运算符**：`and`、`or`、`not`

- 海象运算符：海象运算符可减少单独一行赋值，精简代码，减少临时变量书写，在循环读取输入的时候很常用

    ```python
    if (x:=int(input()))>0:
        print(x)
   #必须加括号！`(x:=表达式)`    
   ```

### 9. 今日踩坑记录
- **坑1**：安装 Python 时忘记勾选 `Add Python to PATH`，导致命令行输入 `python` 提示“不是内部或外部命令”。解决办法：重新安装或手动配置环境变量。
- **坑2**：PyCharm 没有配置解释器，运行代码时报错 `No Python interpreter configured`。解决办法：在设置里手动添加 Python 解释器路径。
- **坑3**：`input()` 返回的是字符串，直接与整数比较会报错 `TypeError`。解决办法：使用 `int()` 转换。

------

*持续更新中，欢迎指点。*



# Day02：数据类型与基础语法

### 1. 数据类型（6 种）
- **数值**：整数（`int`）、浮点数（`float`）、复数（`complex`）、布尔（`bool`）
- **字符串**：`str`
- **容器**：列表（`list`）、元组（`tuple`）、集合（`set`）、字典（`dict`）
- **特殊**：`None`

*【内置函数round 是 "银行家舍入"，四舍六入五成双，等于 5：看前一位，偶数就舍去，奇数就进1】*

**可变与不可变类型：**
- 不可变类型：数值、字符串、元组。**（指不能在原内存地址上修改数据）**
- 可变类型：列表、集合、字典。
- 小整数池 `[-5~256]` 缓存机制；大整数池看运行环境。浮点数精度丢失需导入 `Decimal` 包。

### 2. 字符串基础
- **引号**：单引号、双引号、三引号（所见即所得，并非多行注释，本质是字符串）。
- **转义字符 `\`**：`\` 在行尾作为续行符；`\b` 退格、`\n` 换行、`\t` 横向制表符、`\r` 回车。
- **intern 机制（滞留机制）**：不夹杂空格或特殊字符的字符串，默认开启 intern 机制，共享内存。单个字母长度为1的 ASCII 字符会被 intern 机制处理（包括空格），靠引用计数决定是否销毁。

### 3. 数据类型转换
- **自动转换（隐式）**：两种不同类型计算，较小类型转换为较大类型。例如两个整型进行除法运算结果是浮点型。
- **强制转换（显式）**：
  - `int(x, base)`：将 x（字符串）转换为整数
  - `float(x)`：转换为浮点数
  - `complex(real[,imag])`：创建复数
  - `str(x)`：转换为字符串
  - `repr(x)`：转换为解释器可读的字符串形式
  - `eval(x)`：执行字符串表达式，并返回表达式的值
  - `bin(x)` / `oct(x)` / `hex(x)`：整型转换为二/八/十六进制字符串
  - `ord(x)`：将字符转换成 Unicode 码点（整数）
  - `chr(x)`：将整型转换为一个 Unicode 字符

### 4. 字符编码与解码
- **编码**：将字符串转换成字节序列 `s.encode(编码方式)`。**（UTF-8 一个汉字占 3 字节，GBK 占 2 字节）**
- **解码**：将字节序列转换成字符串 `s.decode(解码方式)`。

### 5. 输入与解析
```python
# 获取用户输入
变量 = input("提示信息")

# 解析输入：map(函数, 可迭代对象)
str1 = input("请以YYYY,MM,DD的格式输入：")
y, m, d = map(int, str1.split(','))
```

- `map(int, ['2024', '3', '1'])` 的作用是：对可迭代对象中的每个元素，依次应用这个函数，返回一个迭代器。map对象只能遍历一次，遍历完就空了。

    

### 6.格式化输出

- `%` 格式化（C 语言风格）：`%d`，`%f`，`%s`，`%x`（进制），`%e`（科学计数），`%.2f`（控制精度）
- `str.format()` 方法：`print("我叫{name}，今年{age}岁".format(name=name, age=age))`
- **f-string（推荐）**：`print(f"我叫{name}，今年{age}岁")`
- `print` 参数：`sep` 为分隔符，`end` 为结束符。

### 7. 常用内建函数

- `type()`：查看对象类型（不会认为子类是一种父类类型）
- `isinstance()`：判断对象是否是指定类型（会认为子类是一种父类类型）
- `id()`：获取对象的内存地址
- `dis` 模块：查看括号内的底层执行逻辑，如 `dis.dis("""print(b:=30)""")` 对比 `dis.dis("""print(30)""")`。

---

*持续更新中，欢迎指点。*



# Day03：流程控制与序列

### 1. 程序流程控制
- **分支**：单分支（`if`）、双分支（`if...else`）、多分支（`if...elif...else`）。
- **嵌套分支与 match case**：
```python
match 对象:
    case a:
        语句1
    case b:
        语句2
    case _:
        兜底语句
```
- **三目运算符**：`表达式1 if 判断条件 else 表达式2`
- **作用域注意**：`if`、`while`、`for`、`try...` 不会增加新的作用域。

### 2. 循环
- **while 循环**：`while 条件表达式:`
- **while...else**：正常循环结束执行 `else`；使用 `break` 时 `else` 不会被执行。
- **for 循环**：`for 变量 in 可迭代对象:`。可迭代对象包括列表、元组、集合、字符串。
- **range() 函数**：`range([start], stop, [step])`，初始值默认 0，步长默认 1，范围包括初始值，不包含结束值。
- **循环选择**：明确次数使用 `for`，不明确使用 `while`。
- **关键字**：`continue`、`break`、`pass`（占位）。

```python
# 打印进度条【暂停0.5秒】
time.sleep(0.5)
```

### 3. 序列
- 可以存放不同类型的数据，有序（可以通过下标获取数据）。
- 属于序列的容器数据类型：列表、元组、字符串。
- **基本操作**：
  - 索引：`seq[0]`
  - 切片：`seq[1:3]`
  - 相加：`seq1 + seq2`
  - 乘法：`seq * 3`
  - 检查成员：`x in seq`
  - 计算长度：`len(seq)`
  - 计算最值：`max(seq)`、`min(seq)`

### 4. 列表（list）
可变、有序、可重复、可存放不同类型数据。

```python
list1 = [100, 200, 300, 400, 500]
# 内存解析：100、200在小整数池，300、400、500在内存中创建；列表对象存放地址；list1指向列表对象。
# print(list1[2]) 先找到列表地址，访问下标为2的内容，该内容是一个地址，指向300数值。
```

**常用操作：**
- 创建：`[]` 或 `list()` 或列表推导式
- 切片：`list[start:stop:step]`
  - `list1[:]` 复制整个列表（新列表对象）
  - `list1[::-1]` 倒序取出所有元素
- 添加：`append(600)`（末尾）、`insert(2, 700)`（指定位置）
    - list1=list1+[1,2]       id 变了【右边是新列表，list1指向它】
    - list1+=[1,2]		id没变【等价于 nums1.extend([6, 7])】
- 相加：`list1 + list2`（创建新列表）
- 乘法：`list1 * 2`（相当于 `list1 + list1`）
- 修改：`list1[0] = 0` 或切片修改 `list1[2:4] = ["30", "40", "50"]`
- 遍历：直接遍历、下标遍历、`enumerate【获取下标和元素】`
- 删除：`del list[2]`、`del list1`
- 嵌套：`list3 = [[1,2,3], ['a','b','c'], [7,8,9]]`
- 推导式：
  - 基础：`[i**2 for i in range(4)]`
  - 带条件：`[i**2 for i in range(10) if i%2==0]`
  - 使用现有列表：`[i**2 for i in list]`
  - 笛卡尔积：`[f"{i}-->{j}" for i in list1 for j in list2]`
- `zip()` 函数：将多个迭代对象打包成元组，以最少的为标准。

**常用函数总结：**
| 函数                            | 说明                                                         |
| :------------------------------ | :----------------------------------------------------------- |
| `list.insert(index, x)`         | 在指定位置插入 x                                             |
| `list.append(x)`                | 在末尾添加 x                                                 |
| `list.extend(list1)`            | 在列表后面追加一个列表（修改原列表，对比 `list1 + list2` 创建新列表） |
| `del list[index]`               | 删除指定位置数据                                             |
| `list.remove(x)`                | 删除第一次出现的 x                                           |
| `list.pop([index])`             | 删除指定位置的数据，默认末尾                                 |
| `list.clear()`                  | 清空列表                                                     |
| `list[start:end] = list1`       | 修改列表切片的数据                                           |
| `sorted(list[, reverse=True])`  | 返回排序后的新列表                                           |
| `list.sort([reverse=True])`     | 对原列表排序，无返回值                                       |
| `list.reverse()`                | 反转列表中的元素                                             |
| `list.index(x[, start[, end]])` | 返回 x 首次出现的位置                                        |
| `list.count(x)`                 | 返回 x 的数量                                                |
| `len(list)`                     | 返回列表元素个数                                             |
| `max(list)` / `min(list)`       | 返回列表最大/最小值                                          |
| `sum(list)`                     | 返回列表中所有元素的和                                       |
| `list.copy()`                   | 拷贝列表（浅拷贝），等价于 `list1[:]`                        |
| `list(x)`                       | 将序列转换成列表                                             |

---
*持续更新中，欢迎指点。*



# Day04：字符串、元组、集合、字典与函数

### 1. 字符串（str）
不可变、有序、存单个字符。

**常用操作：**
- 原始字符串：在字符串前面加 `r` 或 `R`（不转义）。
- 替换：`str1.replace(old, new[, max])`
- 分割：`str1.split('x'[, max])` / `rsplit`
- 连接：`x.join(seq)` 以 x 为分隔符合并序列。*【容器里面所有元素必须是字符串类型】*

注意：区分 `split()` 和 `join()`（一对互操作）
`"a,b,c".split(',')` → 按逗号切割，得到列表 `["a","b","c"]`
`','.join(["a","b","c"])` → 列表合并为字符串 `"a,b,c"`

- 截掉：
  - `strip(x)`：截掉两边所有的 x 字符（注意：是字符集，不是子串）
  - `lstrip()` / `rstrip()`：截掉左侧/右侧
  - `removeprefix(x)`：截掉指定前缀（精确匹配一次）
  - `removesuffix(x)`：截掉指定后缀（精确匹配一次）
  - *注意：`strip("x")` 是剥离两端所有字符 `x`；而 `removeprefix("xx")` 是精确剥离那一个前缀字符串。*
- 大小写：`upper()`、`lower()`、`swapcase()`（大写变小写，小写变大写）、`capitalize()`、`title()`、`casefold()`（返回适合无大小写比较的字符串版本）
- 寻找：`find(x)`（不存在返回 -1）、`rfind()`、`index(x)`（不存在报错）、`rindex()`
- 计数：`count(x[, start][, end])`
- 检查：
  - `startswith(x)` / `endswith(x)`
  - `isspace()`：非空且只含有空白
  - `isalnum()`：非空且只包含字母和数字
  - `isalpha()`：非空且只包含字母
  - `isascii()`：只包含 ASCII 码（含空格）
  - `isdecimal()`：非空且只包含十进制字符（0-9）
  - `isdigit()`：非空且只包含数字（0-9，上下角标数字）
  - `isnumeric()`：非空且只包含数值字符（0-9，上下角标数字，一二三，罗马数字，分数）
  - `isidentifier()`：是否是有效的标识符

### 2. 元组（tuple）
不可变、有序、可存放不同类型。
- 创建：`tup = (100, 200)`。**当只有一个时，需要在末尾加上逗号：`(100,)`**。
- 推导式：`tup = tuple((i*2 for i in range(10)))`（推导式最外面要加上 `tuple()`）
- 访问：`tup[2]`，`tup[-2]`，`tup[2:4]`
- 相加/乘法：`tup1 + tup2`，`tup1 * 2`
- 检查：`in`，`not in`
- 最值求和：`max()`、`min()`、`sum()`
- 遍历：下标遍历、内容遍历、`enumerate`

### 3. 集合（set）
可变、不重复、无序（没有下标，不能切片）、可存放不同类型。
- 创建：`{100, 200}`、`set()`。**注意：直接定义空的 `{}` 会生成字典**。
- 添加：`set1.add(x)`、`set1.update(x)`（x 可为列表、元组、字符串、字典）、`set1.union(x)`（返回新集合）
- 删除：`set1.pop()`（随机删）、`set1.remove(x)`（不存在报错）、`set1.discard(x)`（不存在不报错）
- 清空：`set1.clear()`
- 集合间运算：
  - 差集：`difference(x)`、`difference_update(x)`、`set1 - set2`
  - 交集：`intersection(x)`、`intersection_update(x)`、`set1 & set2`
  - 并集：`set1 | set2`
  - 对称差集（不重复元素）：`symmetric_difference(set2)`、`symmetric_difference_update(set2)`
- 判断：`isdisjoint()`（无交集）、`issubset()`（子集）、`issuperset()`（超集）
- 拷贝：`set1.copy()`（新集合）

### 4. 字典（dict）
可变、无序（键值对访问）、键不能重复，值可以重复。
- 创建：`{}`、`dict()`、`{"name": "gao"}`、`dict(name="gao")`、字典推导式 `{i: i*2 for i in range(5)}`、`fromkeys(seq[, default])`
- 访问：
  - `dic1["name"]`（不存在报错）
  - `dic1.get("name")`（不存在返回 None，可指定默认值）
  - `dic1.setdefault(key[, default])`（不存在则添加）
- 添加/修改：`dic1["address"] = "earth"`
- 检查：`"name" in dic1`（检查 key 是否存在）
- 遍历：
  - `for i in dic1.keys():`
  - `for i in dic1.values():`
  - `for i in dic1.keys():` 配合 `dic1[k]` 遍历所有 key 和 value
  - `for k, v in dic1.items():`
- 删除：`del dict[key]`、`dic1.pop('name')`、`dic1.popitem()`（取出最后插入的键值对）
- 清空：`dic1.clear()`
- 更新：`dic1.update(dic2)`【批量处理】
- 拷贝：`dic1.copy()`

### 5. 容器对比总结
|              数据结构               | 是否可变 |      是否重复      |          是否有序          |     定义符号     |
| :---------------------------------: | :------: | :----------------: | :------------------------: | :--------------: |
|     列表（list）底层是动态数组      |   可变   |       可重复       |            有序            |  `[]`，`list()`  |
|   元组（tuple）底层是定长只读数组   |  不可变  |       可重复       |            有序            | `(,)`，`tuple()` |
| 集合（set）底层是哈希表（只存 key） |   可变   |       不重复       | 无序（Py3.7+保持插入顺序） |  `{}`，`set()`   |
| 字典（dict）底层是哈希表 + 紧凑数组 |   可变   | key不可，value可以 |            无序            | `{:}`，`dict()`  |

```python
# - 不可变类型（int、str、tuple）都是可哈希的，可以作为 set 的元素和 dict 的 key。
# - 可变类型（list、dict、set）不可哈希，不能放进 set。
# 一个对象如果是“可变”的，它就绝对“不可哈希”；反之，“不可变”是“可哈希”的必要条件
# 哈希容器（set、dict 的 key）之所以能实现“不可重复”，完全依赖于元素的“可哈希性”
```

```python
# set3=set() #创建空的集合
# dict1={} #创建字典
```

------

*持续更新中，欢迎指点。*



# Day05：函数进阶（函数、闭包与作用域）

### 1. 函数基础
带名字的代码块，用于复用。**必须先声明，后调用**。

```python
def 函数名(参数列表):
    函数体
    [return]
```

- **形参与实参**：定义时是形参（占位符），调用时是实参（实际数据）。
- **内存分配**：函数调用时会在**栈区**分配存储空间，然后给形参、局部变量分配存储空间。函数执行结束，栈空间释放，形参和局部变量也会被释放。**（注意：栈是后进先出）**。

### 2. 可变与不可变类型的数据传递
- **不可变类型**（整数、字符串、元组）：传递的是值（`fun(a)`），函数内部修改只是修改复制对象，**不会影响外部变量**。
- **可变类型**（列表、字典）：传递的是引用（`fun(la)`），函数内部修改**会影响外部变量**。
- **特殊情况**：
  - `num = num * 2` 时，地址发生改变。
  - `num *= 2` 时，地址不变（针对可变类型）。

### 3. 函数参数的传递形式
- **必须参数（位置参数）**：按照传参顺序对应。
- **关键字参数（名字参数）**：按参数名对应。
- **默认值参数**：定义时有默认值，可覆盖。**（注意：非默认值参数必须放在默认值参数前面）**。
- **不定长参数**：
  - `*args`：底层封装成元组。如果在末尾正常传参；没在末尾必须用关键字传参。
  - `**kwargs`：底层封装成字典。必须在末尾，传参时以键值对传入。

```python
def func(**c):
func(x=10, y=20, z=30) #c = {'x': 10, 'y': 20, 'z': 30}
```

- **解包传参**：`*tuple`（把元组元素分别取出）/ `**dict`（把字典键值对分别取出）。
- **强制传参类型**：`/` 前必须使用位置传参，`*` 后必须使用关键字传参。

**【在 Python 中，参数顺序必须是：位置参数 → *args → 关键字参数 → kwargs】**

### 4. 防止函数修改外部数据（深浅拷贝）
- **浅拷贝**：`list[:]`、`list.copy()`、`list()`、`copy.copy()`。拷贝父对象，**不会拷贝内部的子对象**，只有第一层独立。
- **深拷贝**：`copy.deepcopy()`。完全拷贝父对象及其子对象，**所有层都独立**。
- *注意：创建新对象依旧不可避免浅拷贝的问题，必须用深拷贝彻底解决。*

### 5. 函数的返回值
- `return` 作用：结束当前函数，返回调用位置；将结果返回给调用者。
- 如果函数体没有 `return`，Python 默认返回 `None`。
- `return` 可以返回多个值，以**元组**形式返回。

### 6. 函数的嵌套调用与闭包
- **函数的嵌套调用**：在一个函数的函数体中调用另一个函数（注意作用域）。
- **闭包**：
  - **作用**：延长外层函数局部变量的生命周期，让内层函数访问外层函数的变量。
  - **前提条件**：
    1. 函数的嵌套定义（在一个函数的函数体中又定义了一个新的函数）。
    2. 内层函数访问外层函数的变量。
    3. 外层函数的返回值是内层函数对象。
  - **闭包的经典应用场景**
      - **装饰器**
      - **延迟执行**（回调函数）
      - **数据封装**（计数器）

### 7. 变量的作用域（LEGB）
- 在程序中访问变量时，按照以下顺序寻找：
  - 局部 Local
  - 嵌套 Enclosing（闭包作用域）
  - 全局 Global
  - 内建 Builtin
  - **优先级：Local > Enclosing > Global > Builtin**。
- **注意**：Python 中只有模块（module）、类（class）、函数（def、lambda）才会引入新的作用域。
- `if`、`elif`、`else`、`for`、`while`、`try`、`except` **不会**引入新的作用域。
- **局部变量和全局变量**：
  - 在函数内部对变量赋值时，Python 默认将其当作局部变量，即使全局作用域已有同名变量。
  - **`global`**：在局部作用域中，声明使用的是全局变量。
  - **`nonlocal`**：在局部作用域中，声明使用的是嵌套变量。

### 8.匿名函数

​	Lambda函数定义匿名函数

​	匿名函数作为内置函数的参数：

​		sorted（）对序列中的元素排序

​		map（）对序列中的元素逐一处理，返回的是一个map对象

​		filter（）对序列中的元素过滤，返回是一个 filter对象

​		reduce（）对序列中的累积，返回的是具体的结果值，归约聚合

### 9.高阶函数

**接收函数作为参数，或者返回一个函数的函数**

#### `1.map(func, iterable, ...)`

**作用**：对可迭代对象中的每个元素，依次应用 `func`，返回一个**迭代器**（Python 3 中不再直接返回列表）。

**参数**：

​	`func`：处理函数（可以是 lambda、普通函数、内置函数）。

​	`iterable`：一个或多个可迭代对象（多个时，`func` 也要接收多个参数）。

```python
nums = [1, 2, 3, 4]
# 单个可迭代对象
result = list(map(lambda x: x ** 2, nums))
print(result)  # [1, 4, 9, 16]
# 多个可迭代对象
a = [1, 2, 3]
b = [10, 20, 30]
result = list(map(lambda x, y: x + y, a, b))
print(result)  # [11, 22, 33]
# 配合内置函数（更简洁）
str_nums = ["1", "2", "3"]
result = list(map(int, str_nums))
print(result)  # [1, 2, 3]
```

#### `2.filter(func, iterable)`

**作用**：用 `func` 判断每个元素是否保留，返回一个**迭代器**，里面只包含使 `func` 返回 `True` 的元素。

**参数**：

​	`func`：返回布尔值的判断函数（返回 None 时等价于过滤假值）。

​	`iterable`：可迭代对象。

```python
nums = [-3, -1, 0, 1, 2, 3]
# 保留正数
result = list(filter(lambda x: x > 0, nums))
print(result)  # [1, 2, 3]
# 传入 None，过滤掉所有假值（0、""、None、[]、{} 等）
mixed = [0, 1, "", "hello", None, [], [1, 2]]
result = list(filter(None, mixed))
print(result)  # [1, 'hello', [1, 2]]
```

#### 3.`reduce(func, iterable, initializer)`

​	**作用**：对序列中的元素进行**累积操作**，把前一次的结果和下一个元素继续传给 `func`。**注意：Python 3 中 reduce 被移到了 functools 模块里。**

​	**参数**：

​		`func`：接收两个参数，返回一个值。

​		`iterable`：可迭代对象。

​		`initializer`（可选）：初始值。有初始值时，从初始值开始计算。

**⚠️ 注意**：`reduce` 的可读性较差，很多公司代码规范里**不推荐过度使用**，除非聚合逻辑特别复杂。

```python
nums = [1, 2, 3, 4, 5]
# 求和
total = reduce(lambda x, y: x + y, nums)
print(total)  # 15
# 求乘积（带初始值）
total = reduce(lambda x, y: x * y, nums, 10)
print(total)  # 1200（从 10 开始乘）
# 找最大值
max_num = reduce(lambda x, y: x if x > y else y, nums)
print(max_num)  # 5
```

#### 4. `sorted(iterable, key=None, reverse=False)`

​	**作用**：对可迭代对象排序，返回**新的列表**（不修改原对象）。

​	**参数**：

​		`iterable`：可迭代对象。

​		`key`：指定比较标准的函数（**核心！**）。

​		`reverse`：`True` 表示降序。

```python
# 基本排序
print(sorted([3, 1, 2]))  # [1, 2, 3]
# 按字符串长度排序
words = ["apple", "a", "banana", "cat"]
print(sorted(words, key=len))  # ['a', 'cat', 'apple', 'banana']
# 按对象属性排序
students = [Student(...), ...]
print(sorted(students, key=lambda s: s.score, reverse=True))
# 多级排序（元组）
print(sorted(students, key=lambda s: (s.grade, -s.score)))
# 先按年级升序，年级相同时按分数降序
```

#### 5. `max(iterable, key=None, default=None)` / `min(...)`

​	**作用**：找最大/最小值。

​	**参数**：

​		`iterable`：可迭代对象。

​		`key`：指定比较标准的函数。

​		`default`：序列为空时的返回值（防止报错）。

```python
students = [Student(...), ...]
# 找分数最高的学生（返回学生对象）
top = max(students, key=lambda s: s.score)
# 找分数最低的
low = min(students, key=lambda s: s.score)
# 空列表防报错
top = max([], key=lambda s: s.score, default=None)
```

#### 6. `functools.partial(func, *args, **kwargs)`

**作用**：**冻结**函数的部分参数，返回一个新的函数。常用于“参数固定”场景。

**推荐场景**：

- 回调和事件处理中，需要固定部分参数。
- 大模型开发中，把 API 的固定参数（如 `model="gpt-4"`）预先绑定。

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

# 固定 exponent=2，创建一个"平方函数"
square = partial(power, exponent=2)
print(square(5))  # 25

# 固定 base=2，创建一个"2的n次方函数"
power_of_two = partial(power, 2)
print(power_of_two(10))  # 1024
```



### 9.函数注释	func.\_\_annotations\_\_ 查看

```python
# 添加了注释的自定义函数
def dog(name:str,age:(1,99),species:'狗的品种') -> tuple:
    return(name,age,species)

# 通过函数.__annotations来查看函数的说明    【函数的注释不具备强制性，可以不按注释传值】
print(dog.__annotations__)
```

### 10.函数说明文档	help(print_info) 查看 “”“内容”“”

```python
def print_info(name,age):
    '''这个函数完成了打印信息的功能'''
    print(name,age)

help(print_info) 
#print_info(name, age)
#    这个函数完成了打印信息的功能
```

---
*持续更新中，欢迎指点。*



# Day06：文件操作

### 文件基本概念

将数据写到磁盘文件的过程成为持久化

二进制文件：图片文件，视频文件

纯文本文件：能用记事本打开，创建编码格式： ASCII,ISO-8859-1、GB2312,GBK,UTF-8,UTF-16 等

### 文件的打开与关闭

#### 1.打开和关闭文件

open()：打开或者创建文件，该方法执行完毕后会返回一个file对象

​	open(文件名，模式)

​		模式：

​			r	只读，不存在报错

​			w	写入，覆盖写入，不存在自动创建

​			a	追加写入，不存在自动创建

​			x	创建新文件并写入，已存在则报错

​			b	编码方式以二进制打开，一般用于非文本文件，如图片

​			t	以文本模式打开，默认

​			+	能读能写 

```python
# 建议用 with open，可以自动关闭文件，遇到异常也不会漏掉 close()：
# with 语句的底层原理
# with open(...) as f 背后的魔法方法是 __enter__ 和 __exit__。上下文管理器会用到。
with open("./output.txt", "w", encoding="utf-8") as f:
	f.write("This is a test.")
with open("./output.txt", "r", encoding="utf-8") as f:
	print(f.read())
```

close（）关闭【资源释放】

​	file.close()

#### 2.读写文件

​	写：file.write("内容")

​		注意：路径地址

```
copy_file("F:\\1.png","E:\\2.png")	转义\\
copy_file("F:/1.png","E:/2.png")	反斜杠 win和linux都可以
copy_file(r"F:\1.png",r"E:\2.png")	r""
```

​	读：file.read()

​		read(size)    读取文件指定大小的内容

​			如果编码方式是t, 那么size表示字符数,

​			如果编码方式是b, 那么size表示读取的是字节数

```python
while content := source_file.read(1024):
    target_file.write(content)
    # 迭代,读取位置会自动向后刷新
```

#### 3.常用函数

- 文件对象（File Object）方法

| 方法                        | 说明与注意事项                                               |
| --------------------------- | ------------------------------------------------------------ |
| `file.seek(offset[, from])` | 移动偏移量并返回新的绝对位置。 • `offset`：移动的字节数，负数表示从倒数第几位开始。 • `from`：0为开头，1为当前位置，2为末尾。 • **注意：from 不为 0 时，必须使用 'b' 二进制模式打开文件。** |
| `file.tell()`               | 返回当前偏移量。                                             |
| `file.truncate([size])`     | 从开头开始截断文件为 `size` 个字符，无 `size` 表示从当前位置截断。 *(注：Windows系统下换行符占2个字符)* |
| `file.writelines(seq)`      | 将序列中字符串写入文件，需要自己加入换行符。                 |
| `file.readable()`           | 如果可以读取文件则返回 `True`。                              |
| `file.writable()`           | 如果可以写入文件则返回 `True`。*(图片中拼写为 writeable，正确拼写应为 writable)* |
| `file.seekable()`           | 如果文件支持随机访问则返回 `True`。                          |

- os 模块：目录与文件操作

| 方法                  | 说明                                                         |
| --------------------- | ------------------------------------------------------------ |
| `os.rename(old, new)` | 重命名文件。                                                 |
| `os.remove(file)`     | 删除文件。                                                   |
| `os.mkdir(dir)`       | 创建目录，**不支持递归创建**。                               |
| `os.makedirs(dir)`    | **递归创建目录**（即可以一次性创建多层不存在的目录）。       |
| `os.getcwd()`         | 获取当前路径。                                               |
| `os.chdir(dir)`       | 进入指定目录。                                               |
| `os.listdir(dir)`     | 获取目录下文件和目录列表。                                   |
| `os.rmdir(dir)`       | 删除**空目录**。                                             |
| `os.removedirs(dir)`  | 递归删除空目录（如果子目录删除后父目录也空了，会一并删除）。 |

- `os.path` 模块：路径操作与判断

| 方法                     | 说明                                             |
| ------------------------ | ------------------------------------------------ |
| `os.path.abspath(path)`  | 将相对路径转换为绝对路径。                       |
| `os.path.basename(path)` | 获取路径中的文件名部分。                         |
| `os.path.dirname(path)`  | 获取路径中的目录部分。                           |
| `os.path.join(*paths)`   | 拼接多个路径，自动处理路径分隔符（跨平台兼容）。 |
| `os.path.split(path)`    | 将路径分割为（目录, 文件名）的元组。             |
| `os.path.splitext(path)` | 将路径分割为（文件名, 扩展名）的元组。           |
| `os.path.exists(path)`   | 判断路径是否存在。                               |
| `os.path.isfile(path)`   | 判断路径是否为文件。                             |
| `os.path.isdir(path)`    | 判断路径是否为目录。                             |
| `os.path.getsize(path)`  | 获取文件的大小，以字节为单位。                   |
| `os.path.getatime(path)` | 获取文件的最后访问时间。                         |
| `os.path.getmtime(path)` | 获取文件的最后修改时间。                         |

- `os.walk()` 递归遍历目录

```python
import os

for root, dirs, files in os.walk(os.getcwd()):
    print("当前路径：", root)
    print("目录：", dirs)
    print("文件：", files)
    print()
```

------

*持续更新中，欢迎指点。*



# Day07：面向对象（OOP）

- POP 面向过程，以步骤/过程为中心 怎么做
- OOP 面向对象，万物皆对象 谁来做
- FP 面向函数编程，函数是第一公民 做什么

#### 1. 基本概念
- **对象**：客观存在都是对象【万物皆对象】。
- **类**：对大量对象共性的抽象。类是创建对象的模板。
  - **有什么**：属性（数据）
  - **做什么**：方法（行为）
- **关系**：类是客观事物在人脑中的主观反应，对象是类的实例化。

#### 2. 类的定义
```python
class 类名:
    """类说明文档"""
    
    # 类属性 | 类变量【类下、方法外定义】
    class_attr = "类属性"
    
    # 实例属性 | 实例变量【一般在 __init__ 方法中定义】
    def __init__(self, name):
        self.name = name  # 实例属性
        
    # 方法定义
    def instance_method(self):  # 实例方法
        pass
    
print(Person.__doc__) #打印类的说明文档
```

#### 3. 属性（Attributes）

- **类属性（类变量）**：
    - 定义在类下、方法外。
    - 通过 `类名.属性名` 或 `实例.属性名` 访问。
    - 通过 `类名.属性名 = 值` 添加或修改。
- **实例属性（实例变量）**：
    - 一般在 `__init__` 方法中定义。
    - 通过 `实例.属性名` 访问和修改。
    - 只能通过实例访问和修改。

#### 4. 方法（Methods）

- **实例方法**：
    - 类中定义。
    - 第一个参数是 `self`，代表实例本身。
    - 通过 `实例名.方法名()` 访问。

- **类方法**：
    - 通过 `@classmethod` 修饰。
    - 第一个参数是 `cls`，代表当前类。
    - 不需要实例化，直接通过 `类名.方法名()` 访问。

- **静态方法**：
    - 通过 `@staticmethod` 修饰。
    - 不需要实例化，直接通过 `类名.方法名()` 访问。无需传递 `self` 或 `cls`。

- **魔法方法**：
    - 格式 `__xxx__`（双前下划线、双后下划线）。这类方法不需要手动调用，执行特定操作时会自动触发。
    - `def __new__(cls, *args, **kwargs)`
        - 建对象时第一个被调用，真正构造
        - 必须返回`return super().__new__(cls)`，否则 `__init__ `不会被触发。
    - `def __init__(self, ...)`
        - `__new__ `返回实例后调用，初始化赋值操作。只能返回 None
    - `def __del__(self)`
        - 对象引用计数归零时（被垃圾回收）。清理资源。
    - `def __getattr__(self, name)`
        - 访问不存在的属性时触发（兜底）。
        - 避坑：内部要 raise AttributeError，否则会无限递归。
        - 区分：`__getattribute__` 是每次访问属性都触发，极易死循环，新手别碰。
    - `def __setattr__(self, name, value)`
        - 每次执行 `self.name = value` 都触发。拦截赋值（可用于数据校验）。
        - 避坑：必须调用 `super().__setattr__(name, value) `完成真正赋值，否则无限递归。
    - `def __eq__(self, other)`
        - 使用 == 比较时触发。定义“相等”的规则。
        - 🔴 面试必考坑：重写 `__eq__` 后，Python 3 会自动把` __hash__` 设为 None，导致实例不可哈希（无法放进 set 或作为 dict 的 key）。
        - 正确做法：重写 `__eq__` 的同时，也要重写 `__hash__`，比如 return hash((self.name, self.age))。
    - `def __lt__(self, other):`【`__eq__（等于）、__lt__（小于）、__gt__（大于）`】
        - 和其它对象比较 运算符的重载，例如`return self.age < other.age`
    - `def __str__(self)`
        - print(obj)、str(obj) 时触发。面向用户的友好展示。
    - `def __repr__(self)`
        - repr(obj)、交互式解释器直接输入对象时触发。面向开发者的精确展示。
    - 三大避坑口诀
        - `__new__` 要 `return super().__new__(cls)`，不然 `__init__ `罢工。
        - `__getattr__` 里要 `raise AttributeError，__setattr__` 里要` super().__setattr`__，不然无限递归。
        - 重写 `__eq__ `必须重写 `__hash__`，不然对象不能进 set 和 dict。
        - **面试：`__str__` 和 `__repr__` 的区别是什么？**

    它们的设计目标不同：

    `__str__` 面向终端用户，追求友好易读，由 `print`、`str` 触发。

    `__repr__` 面向开发者，追求精确无歧义，由 `repr`、交互式环境、以及列表/字典打印时触发。

    工程中如果只允许写一个，我会推荐写 `__repr__`。因为 `print` 在找不到 `__str__` 时会自动回退到 `__repr__`，反之则不成立。而且 `__repr__` 的理想标准是返回能通过 `eval()` 重建对象的字符串

```python
"""
    该案例演示了魔法方法
"""
class Student:
    # 用于演示__new__的单例特性
    _instance=None
    def __new__(cls, *args, **kwargs):
        print("1.__new__被调用：准备创建对象")
        instance=super().__new__(cls) # 调用父类__new__ 真正分配内存【构造】
        return instance # 如果然忘记return，不会执行__init__
    def __init__(self, name, age):
        print("2.__init__ 被调用：填充数据")
        # 注意：下面这行会处罚__setattr__ 。赋值【初始化】
        self.name = name
        self.age = age
    def __setattr__(self, key, value):
        print(f"5.__setattr__ 被调用：设置{key}={value}")
        # 数据校验：年龄不能为负数
        if key=="age" and value<0:
            raise ValueError("年龄不能为负数")
        # 必须调用super()，否则无限递归
        super().__setattr__(key,value)
    # （4）__getattr__：访问不存在属性是兜底
    def __getattr__(self, key):
        print(f"4.__getattr__ 被调用：属性{key} 不存在")
        # 必须抛出异常，否则无限递归
        raise AttributeError(f"Student 对象没有属性：{key}")
    # 6. __eq__：定义相等规则
    def __eq__(self, other):
        print("6. __eq__ 被调用：比较两个对象")
        if not isinstance(other,Student):
            return NotImplemented
        return self.name == other.name and self.age == other.age
    # 6.__hash__：配合__eq__使用，可保证哈希
    def __hash__(self):
        print("6.__hash__ 被调用：计算哈希值")
        return hash((self.name, self.age))
    # 7.__str__：面向用户展示
    def __str__(self):
        print("7.__str__ 被调用：print、str时触发")
        return f"学生：{self.name},年龄{self.age}"
    # 8.__repr__:面向开发者展示
    def __repr__(self):
        print("8.__repr__ 被调用：repr、交互式环境触发")
        return f"Student(name='{self.name},age={self.age})')"
    # 3.__del__：对象销毁
    def __del__(self):
        print(f"3.__del__ 被调用：{self.name}被销毁")
# -----------------测试-------------
print("====创建对象====")
s1=Student("zs",20)
s2=Student("zs",20)
print("print 触发")
print(s1)
print("repr 触发")
print(repr(s1))
print("s1==s2 触发")
print(s1==s2)
print("hash + eq 触发")
print(set([s1,s2]))
print("getattr 触发")
try:
    s1.email
except AttributeError as e:
    print(f"捕获异常：{e}")
print("del 触发")
del s1
del s2
"""
====创建对象====
1.__new__被调用：准备创建对象
2.__init__ 被调用：填充数据
5.__setattr__ 被调用：设置name=zs
5.__setattr__ 被调用：设置age=20
1.__new__被调用：准备创建对象
2.__init__ 被调用：填充数据
5.__setattr__ 被调用：设置name=zs
5.__setattr__ 被调用：设置age=20
print 触发
7.__str__ 被调用：print、str时触发
学生：zs,年龄20
repr 触发
8.__repr__ 被调用：repr、交互式环境触发
Student(name='zs,age=20)')
s1==s2 触发
6. __eq__ 被调用：比较两个对象
True
hash + eq 触发
6.__hash__ 被调用：计算哈希值
6.__hash__ 被调用：计算哈希值
6. __eq__ 被调用：比较两个对象
8.__repr__ 被调用：repr、交互式环境触发
{Student(name='zs,age=20)')}
getattr 触发
4.__getattr__ 被调用：属性email 不存在
捕获异常：Student 对象没有属性：email
del 触发
3.__del__ 被调用：zs被销毁
3.__del__ 被调用：zs被销毁
"""
```

#### 5. 类的操作

- **成员引用（获取类的成员）**：`类名.成员名`
- **实例化（创建类的对象）**：`实例名 = 类名(参数)`
- 动态添加
    - 动态的给实例添加属性【在实例方法中self.新属性=新属性值】
    - 动态的给类添加属性【直接在外面类.新属性=新属性值】
    - 动态给实例添加方法【在类外写函数，实例化的对象.方法名=函数名。对象.方法名()调用】
    - 动态给实例添加方法【实例化的对象.方法名=types.MethodType(函数名，实例)】【最标准、最推荐】
    - 动态给类添加方法【类外定义函数（含装饰器），类.方法名=函数名。类.方法名()调用】
- 动态删除
    - 动态删除属性【del 实例化的对象.属性名】
    - 动态删除方法【del 实例化的对象.方法名】
- 限制添加实例属性于实例方法
    - 类中`__slots__ = ("name", "age","eat")`限制

#### 6. init：对象的创建过程

当执行对象的创建操作时，底层执行流程如下：

1. 首先调用 `__new__()` 方法：**创建当前类的实例出来**。
2. 然后在 `__new__()` 方法中调用 `__init__()` 方法。
3. 调用时，会将 `__new__()` 创造出来的实例作为 `__init__()` 的第一个参数传递过去。
4. 在 `__init__()` 方法中，主要给创造出来的对象**添加实例属性以及对属性赋值**。

【严格讲，\_\_init\_\_不是构造方法，**真正创建对象**的是**\_\_new\_\_**，**\_\_init\_\_**应该叫**初始化方法**】

![1789958331627](C:\Users\win10\AppData\Roaming\Typora\typora-user-images\1789958331627.png)

\_\_init\_\_方法不是必须的，如果没有在定义类的时候显式提供\_\_init\_\_，默认会提供一个只有一个参数self的init方法，但是self这个参数不需要我们传递。*self是一个约定俗成的名字，代表当前创建的对象*

【\_\_init\_\_()方法只能返回None，不返回其他值】

#### 7.self：

​	self代表类的实例自身，p.eat() 相当于 【底层执行】Person.eat(p)

​	通过self访问类的实例的属性和实例方法

---

*持续更新中，欢迎指点。*



## 面向对象的三大特性

#### 封装      *主要指的是成员的私有化*

私有化：只能在类的内部访问成员，在类的外部成员就不能访问了

实现方式：【原理：底层是通过改名实现私有化】

​	_ 名			：只是一个约定，不具备强制性

​	_ _名（或\_ _名\_）：在类的外部无法访问，只能在类中访问私有成员

​	`	__name` 会被 Python 改写成 `_ClassName__name`，外部可以通过 `_ClassName__name` 访问，

​	【这只是**保护机制**，不是**强制安全机制**。】

一般写法：【@property ，@age.setter，一般方法命名： 私有属性去掉前面下划线】

​	`def age(self):`添加修饰器@property，只读，直接age访问即可

​	`def age(self, age):`添加修饰器@age.setter实现`self.__age = age`

​	原本的`self.__age = age`直接`ls.age=20 设置。  print(ls.age)访问`

​	 注意：【@property装饰的方法不要和变量重名，否则可能导致无限递归】

```python
class Person:
    __age=0
@property
def age(self):
    return self.__age
@age.setter
def xxx(self,new_age):
    self.__age=new_age
```

#### 继承	*子类 is a 父类*

​	单继承

​		class 子类（父类）：

​			类体

​	多继承

​		class 子类（父类1，父类2，父类3...）

​			类体

​	复用父类中的方法

​		super（）. 方法（）

​		父类 . 方法（）

​	super()：不是简单的“调用父类”，而是基于方法解析顺序（MRO）调用当前类在MRO链的下一个类

​	方法解析顺序：可使用类名.\_\_mro\_\_访问类的继承链来查看方法解析顺序

```python
MRO以及super结合使用【推荐写法】
class A:
    def __init__(self,a,**args):
        self.a=a
        super().__init__(**args)
class B:
    def __init__(self,b,**args):
        self.b=b
        super().__init__(**args)
class C(A,B):
    def __init__(self,a,b):
        # 方法一：
        # A.__init__(self,a)
        # B.__init__(self,d)
        # 方法二：
        super().__init__(a=a,b=b)
```

​	按照ROM去执行【解决继承的钻石继承问题】

```python
#【解决继承的钻石问题】
class Child(Parent1, Parent2):
    def __init__(self):
        super().__init__()
```

#### 多态

​	同一变量在不同的场景下呈现不同状态

​	使用场景

​		在方法的参数中使用多态【函数/方法的参数不指定具体的类，而是指定一个“抽象类型”或“接口”。】

​			eg：继承同一个类的不同子类，执行重写后的父类方法的效果不一致

​		在返回值中使用多态【一个方法/函数返回的对象，不需要让调用者知道具体是什么类】

​			eg：同一个函数（方法）的返回值，基于不同参数，返回值可能是不同类型（类/实例）

​		在声明变量的时候使用多态【变量本身没有类型（Python 是动态类型语言），变量是一个标签，可以指向任何对象】

​			eg：列表中存放不同的类，for遍历时，同一个引用指向不同的类

#### 重写

*【注意：Java中有重写还有重载，但是Python中只有重写，因为在内存中，如果方法名一致，只对应一个地址，所以指挥按照最后一个执行。Python **不直接支持传统重载**（同名方法参数不同），但可以通过**默认参数**和**可变参数**模拟重载效果。】*

**在Python中实现重载，通过可变参数。**`eg: def eat(self，*args，\*\*args)`

#### 抽象

定义：如果类中存在抽象方法，那么这个类就是抽象类，需要让这个类继承ABC

抽象方法：只需要声明这个方法，但是方法的具体实现不能完成，方法上加注@abstractmethod

注意：抽象类不能被实例化，如果子类继承了抽象父类，必须对抽象类中的父类方法进行实现，如果没有实现，那么子类也属于抽象类，不能被实例化

```python
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    def area(self):
        return self.length * self.width
```

------

*持续更新中，欢迎指点。*



# Day08：异常及其异常处理

### 1. 程序常见的问题

- **语法错误**：程序在语法解析阶段就发现问题，程序不会执行。
- **异常**：程序语法正确，但运行时发生错误。运行期间检测到的错误被称为异常。

**区别**：语法错误在编译/解释阶段就被拦截，异常是在运行时才暴露。

### 2. 异常处理

**目的**：不是规避异常，而是当异常发生时提供处理方法，让程序不终止，继续向下执行。

**如果不处理异常**：默认将异常打印到控制台，程序终止，异常后面的代码不执行。

#### 基本语法

```python
try:
    # 可能发生异常的代码
except:
    # 发生异常时，对异常进行处理的代码
```

**底层原理**：
1. 程序运行时如果发生异常，底层会**创建一个对应的异常类型对象**。
2. 这个异常对象会**向上抛出（raise）**。
3. 当调用者接收到异常后，通过 `except` 代码块对异常对象进行**捕获**并处理。
4. 如果没有被 `except` 捕获，继续向上抛出，直到交给解释器。
5. 解释器默认在控制台打印异常信息，程序终止。

#### 针对不同类型的异常进行处理

```python
try:
    # 可能发生异常的代码块
except 异常类型1 as 别名:
    # 处理方式1
except 异常类型2 as 别名:
    # 处理方式2
except (异常类型3, 异常类型4, 异常类型5) as 别名:
    # 处理方式3
except:
    # 兜底处理【相当于 if-else 中的 else】
```

#### else 语句块【可选】

`try` 中**没有发生异常**时，执行 `else` 中的代码。

```python
try:
    # 可能发生异常的代码
except 异常类型1 as 别名:
    # 处理方式1
else:
    # try 中没发生异常，执行 else 代码
```

**说明**：`else` 中的代码放 `try` 里效果一样，但 `else` 语义更清晰——“只有成功执行才走这里”。

#### finally 语句块【资源释放】

**不管是否发生异常都执行**。通常把资源释放（关闭文件、断开连接）放在里面。

```python
try:
    # 可能发生异常的代码
except 异常类型1 as 别名:
    # 处理方式1
else:
    # try 中没发生异常，执行 else 代码
finally:
    # 不管是否发生异常都执行
```

- 【大部分和else一样，**但是except没有捕获异常，则finally会被执行，而代码块外面的不会被执行**】
- **面试：函数体里面try中执行return后，依旧执行finally里面的代码**

### 3. 抛出异常

**`raise` 抛出异常**：
```python
raise 异常类型("异常信息")
```

**`assert` 抛出异常**（断言）：
```python
assert 表达式, "异常信息"
# 等价于：
if not 表达式:
    raise AssertionError("异常信息")
```

**使用场景**：
- `raise`：主动抛出异常，用于校验参数、中断流程。
- `assert`：用于调试阶段的断言，生产环境会被优化掉（`python -O` 运行时）。

### 4. 自定义异常

```python
class 自定义异常类型(Exception):
    pass
```

### 5. 异常的传递

- try嵌套或者函数的嵌套定义——一层一层向外传递
- 如果存在函数的嵌套调用——沿着函数的调用方向反向传递

### 6. with 语句与上下文管理器

#### 语法

```python
with expression as variable:
    # 代码块
```

#### 说明

- `with`、`as`：关键字。
- `expression`：是一个对象或函数调用，返回的内容类型必须是**上下文管理器对象**。
- **上下文管理器中必须提供两个方法**：`__enter__` 和 `__exit__`。
- `variable`：可选，用于存储 `expression` 对象的 `__enter__` 方法的返回值。

#### 执行原理

1. 执行 `with` 语句时，调用 `expression.__enter__()`。
2. `__enter__` 的返回值被存储在 `variable` 中（如果有），以供 `with` 代码块使用。
3. `__enter__` 的返回值一般是 `self`（当前上下文管理器对象）。
4. 执行 `with` 语句中的内容。
5. 当代码执行完毕后，**不管是否发生异常**，都会执行上下文管理器对象中的 `__exit__` 方法，在 `__exit__` 方法中将资源释放掉。

#### 扩展：

#### `__exit__` 的三个参数

```python
def __exit__(self, exc_type, exc_val, exc_tb):
    # exc_type：异常类型，正常退出为 None
    # exc_val：异常实例，正常退出为 None
    # exc_tb：异常 traceback 对象，正常退出为 None
    # 返回 True：吞掉异常；返回 False 或 None：异常继续抛出
    pass
```

#### 自定义上下文管理器示例

```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        print(f"耗时：{time.time() - self.start:.4f} 秒")
        return False


with Timer() as t:
    total = sum(range(10000000))
```

#### 使用 `contextlib` 简化写法

```python
from contextlib import contextmanager


@contextmanager
def timer():
    import time
    start = time.time()
    try:
        yield    # yield 之前 = __enter__，之后 = __exit__
    finally:
        print(f"耗时：{time.time() - start:.4f} 秒")


with timer():
    total = sum(range(10000000))
```

### 7. 常见异常类型速查

| 异常类型            | 触发场景         |
| :------------------ | :--------------- |
| `SyntaxError`       | 语法错误         |
| `NameError`         | 使用未定义的变量 |
| `TypeError`         | 类型不匹配       |
| `ValueError`        | 值不合法         |
| `IndexError`        | 索引越界         |
| `KeyError`          | 字典键不存在     |
| `AttributeError`    | 属性不存在       |
| `ZeroDivisionError` | 除以零           |
| `FileNotFoundError` | 文件不存在       |
| `ImportError`       | 导入模块失败     |
| `AssertionError`    | assert 断言失败  |

------
*持续更新中，欢迎指点。*



# Day09：模块与包

### 1.模块的导入：一个以 .py 结尾的源文件就是一个模块

- #### 全局导入：导入模块的所有成员

    ​	语法：import 模块名 [as 别名]

    ​	使用方式：模块名.成员名    或者    别名.成员名

- #### 局部导入：

    ​	方式1：导入模块的指定成员

​			语法：from 模块名 import 成员1 as 别名，成员2 as 别名，成员3 as 别名

​			使用方式：直接通过成员名或者别名访问

​		方式2：导入模块所有不以单下划线开头的成员

​			语法：from 模块名 import *

​			使用方式：直接通过成员名访问

​			【在被导入的模块中，通过`__all__`可设置哪些成员可以被导入，仅在form  import *下有作用】

- #### 模块搜索顺序：当导入一个模块时候，按照以下顺序查找

​		1.当前目录

​		2.PYTHONPATH环境变量中的目录

​		3.包含Python模块以及这些模块所依赖的任何extension module 的目录

```python
import sys
print(sys.path) 			   #通过这种方式查看模块搜索顺序
sys.path.append("目标目录")		#通过这种方式添加临时目录
```

- #### **`__name__`是python中内置的特殊变量【常作测试使用】**

​		当文件被直接运行时，`__name__`的值为`__main__`

​		当文件作为模块被导入时，`__name__`的值为该模块的名字

- #### dir(x)函数：打印x所有成员，x为空则打印当前作用域中所有成员【变量，函数，类】

### 2.包的导入【包：文件夹下有一个`__init__.py`文件】

- #### 全局导入：导入包中模块的所有成员

​		语法：import 包名.模块名 [as 别名]

​		使用方式：包名.模块名.成员名 或者 别名.成员名

​		注意：如果import最后一个是包 import 包a.包b ，那么在被导入的包对应的`__init__.py`文件中必须指定导入包下的哪个模块

- #### 局部导入

​		方式一：从包中导入模块

​			语法：from 包名 import 模块名 [as 别名]

​			使用方式：模块名.成员名

​		方式二：从包中模块导入功能

​			语法：from 包名.模块名 import 成员1 [as 别名]，成员2 [as 别名]

​			使用方法：成员名或者别名

​		方式三：从包中导入指定模块

​			语法1：导入模块所有成员--和普通的模块导入一样【from 包名.模块名 import *】

​			语法1：导入包下的模块【from 包名 import *  **注意：必须在`__init__.py`指定导入哪些模块**】

### 3.标准库：下载Python自带

​	`collections` 模块：容器数据类型

​		1.`defaultdict` —— 带默认值的字典

```python
from collections import defaultdict

d = {}

# defaultdict：指定默认值工厂
dd = defaultdict(int)    # 默认值为 0
dd["a"] += 1
print(dd)   				# defaultdict(<class 'int'>, {'a': 1})
dd2 = defaultdict(list)  # 默认值为 []
dd2["b"].append(1)
print(dd2)  				# defaultdict(<class 'list'>, {'b': [1]})
dd3 = defaultdict(set)   # 默认值为 set()
dd3["c"].add(1)
print(dd3)  				# defaultdict(<class 'set'>, {'c': {1}})
```

​		**常用场景**：

​			统计频率：`defaultdict(int)`

​			分组：`defaultdict(list)`

​			去重分组：`defaultdict(set)`

​		2.`Counter` —— 计数器【统计可哈希对象的出现次数。】

```python
from collections import Counter
# 从字符串统计字符频率
char_count = Counter("abracadabra")
print(char_count)
# Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
# 最常见的 1 个
print(char_count.most_common(1))   # [('a', 5)]
# 最常见的 3 个
print(char_count.most_common(3))   # [('a', 5), ('b', 2), ('r', 2)]

# 从列表统计
nums = [1, 2, 2, 3, 3, 3]
num_count = Counter(nums)
print(num_count)   # Counter({3: 3, 2: 2, 1: 1})
# 更新：增加新元素
num_count.update([2, 3, 3, 3])
print(num_count)   # Counter({3: 6, 2: 3, 1: 1})
# 减法
c = Counter(a=3, b=1)
d = Counter(a=1, b=2)
print(c - d)       # Counter({'a': 2})
```

​		常用方法：

​			most_common(n)	返回出现次数最多的 n 个元素 

​			update(iterable)	增加计数 

​			subtract(iterable)	减少计数 

​			elements()	返回元素迭代器（按计数重复）

​			 total()	返回所有计数值之和

### 4.第三方库（pip）

#### 	打包自己的库并安装

​		1.先安装 setuptools 库

​		2.在包外【和包平级】创建一个 setup.py 文件

```python
# 老版本
# from distutils.core import setup
# 新版本
from setuptools import setup
setup(
    name="graphic",  # 需要打包的名字
    version="1.0",  # 版本
    py_modules=["graphic.circle", "graphic.rectangle"],  # 需要打包的模块
)
```

​		3.在 setup.py 同级目录下进行构建【同级cmd】 执行  **`python setup.py build`**【校验能否打包】

​		4.生成压缩包  **`python setup.py sdist`**【真正打包】

​		5.pip命令安装自己打的库

```
【命令行】pip install path_to_your_package/dist/your_package_name-0.1.tar.gz
```

​		6.Pycharm安装自己打的包库

​	**注意：3-5步骤是旧版本，新版本：**

​		1.在 setup.py 同级目录下，pip install build

​		2.python -m build【**一句话替代 build 和 sdist**】

- **vehicle-1.0.tar.gz**：源码分发包（Source Distribution）。里面是 `.py` 代码，别人安装时需要在自己的电脑上重新编译打包。
- **vehicle-1.0-py3-none-any.whl**：轮子包（Wheel）。它已经被预先构建好了（你截图里刚执行的 build 过程），安装速度极快。**推荐以后优先使用 .whl 文件**

3.pip install .\dist\vehicle-1.0-py3-none-any.whl

### 5.Python高级语法

#### 	1.浅拷贝深拷贝：

​		浅拷贝：切片，工厂函数（list()，set()）,copy()函数

​		深拷贝：copy.deepcopy()

​		注意：

​			非容器类（数字，字符串，和其他“原子”类型的对象）无法拷贝

​			元组变量如果只包含原子类型对象，不能对其拷贝

​			元组不光包含不可变数据类型，还包含可变数据类型，不能对其进行浅拷贝

​			元组不光包含不可变数据类型，还包含可变数据类型，能对其进行深拷贝

#### 	2.迭代器：

​		相关概念：

​			遍历：将数据一个一个取出来

​			循环：遍历的一种实现方式

​			迭代：遍历的一种实现方式，for循环底层就是迭代器【调用next函数，将数据一个一个取出来】

- 能用for遍历的都是可迭代器对象：属于Iterable【list，tuple，set，dict，str，generator(range(n)）】 


- 可迭代对象： 有`__iter__()`，调用iter(对象)，底层自动调用`__iter__()`魔法方法，获取当前对象迭代器


- 迭代器：有`__next__()`，调用next(对象)，底层自动调用`__next__()`这个魔法方法，获取下一个值

    ​	手动实现迭代器：

```python
# 手动实现迭代器
class MyIterator:
    def __init__(self,lst):
        self.lst=lst
        self.index=0
    def __iter__(self):
        return self
    def __next__(self):
        if self.index>=len(self.lst):
            raise StopIteration
        res=self.lst[self.index]
        self.index+=1
        return res
it = MyIterator([1, 2, 3])   
for x in it:
    print(x)
```

------

*持续更新中，欢迎指点。*



# Day10：Python高级语法

### 1.生成器：（generator）

是一个用于创建迭代器的简单而又强大的工具

#### 	1.创建生成器对象的方式

​		1.推导式：generator = （x for x in range（5））

​		2.生成器函数：和普通函数的区别是，普通函数返回通过return，生成器函数返回值，通过yield

​		注意：当在生成器函数中使用 yield 语句时，函数的执行将会暂停，并将 yield 后的表达式作为当前迭代的值返回。每次调用生成器的 next() 方法或者使用 for 循环进行迭代时，函数会从上次暂停的地方继续执行（会记住上次执行语句时素有的数据值），知道再次遇到 yield 语句

#### 	2.生成器函数的优势是它们可以按需生成值，避免一次性生成大量数据并占用大量内存 

#### 	3.next和send对比：

##### 		next（）：

​			启动生成器，获取值

​			从上一次暂停的位置恢复执行，获取值

##### 		send（）：

​			启动生成器，获取值

​			从上一次暂停的位置恢复执行，获取值，并向生成器”发生“一个值

​		注意：如果使用send启动生成器，参数必须传None，引因为这个时候还没有yield

```python
def generator_demo():
    print("开始")
    for i in range(3):
        print(f"准备生成 {i}")
        yield i
        print(f"继续执行，准备下一次")
    print("结束")
gen = generator_demo()
for x in gen:
    print(f"收到: {x}")
```

### 2.命名空间（Namespace）

*存放 “变量名-对象” 映射关系的容器【带唯一索引的字典】*

​	三大核心命名空间：

​		1.内置名称的命名空间

​		2.模块的全局命名空间

​		3.函数的局部命名空间

​	其他命名空间：

​		1.类命名空间

​		2.实例命名空间

​		3.嵌套命名空间

​		4.包命名空间

### 3.作用域（Scope）

​	搜索顺序：局部（Local）->嵌套（Enclosing）->全局（Global0->内嵌（Builtin）【LEGB】

- ​	**Local**：当前函数内部。
- ​	**Enclosing**：闭包中外层函数的变量。
- ​	**Global**：当前模块的全局变量。
- ​	**Builtin**：Python 内置命名空间。

### 4.闭包（Closure）

​	目的：**延长外部函数局部变量的生命周期**

​	前提：

​		1. 外部函数内定义一个内部函数

​		2. 内部函数用到外部函数中的变量

​		3. 外部函数将内部函数作为返回值

### 5.装饰器（Decorator）（OCP开闭原则，扩展开放修改关闭）

​	1.本质：【**闭包**实现】

​		装饰器允许在不修改原有代码的基础上，动态地添加或者修改函数

​		装饰器本质是一个接收函数作为输入并返回一个新的包装过后的函数的对象

​	2.**和普通函数调用对比，闭包实现装饰器的好处：**

​		装饰器：

​			只需要装饰一次，就能得到新的装饰后的函数对象

​			可以为每一个被装饰的函数单独维护状态（外层函数中定义变量）

​		普通的函数包装

​			一次性调用，每次执行函数，都要将函数的素有代码执行一遍

​			没有办法为每一个被装饰的函数单独维护状态

​	3.语法糖  **@** ：

​		当在被装饰函数的前面添加@函数名，在执行时候，被装饰函数作为参数传递给@后指定的函数，并执行重新赋值的 func = decerator(func)

```python
from math import sqrt
def decerator(f):
    def inner(x):
        x=abs(x)
        return f(x)
    return inner
@decerator
def func(x):
    return sqrt(x)
print(func(-9))
```

​	4.多层装饰器**【洋葱模型：装饰从下往上包，执行从上往下剥。】**

​		装饰顺序：**装饰顺序是从下往上**离函数最近的装饰器先被应用

​		执行顺序：**执行顺序是从上往下**调用函数时，最外层的装饰器先执行，依次向内

​	5.带参数装饰器【**三层**，1.接收参数列表。2.@装饰器名字。3.内层inner】

​	6.类装饰器：【**init 接收， call 调用**】

​		优势：

​			参数存在实例属性里，不用闭包，更清晰。

​			更容易做状态管理（比如统计调用次数）。

​		语法糖：

​			obj() 是 obj.\_\_call\_\_() 的语法糖。

​			在被装饰函数上面写@类名，是类装饰器的语法糖

------

*持续更新中，欢迎指点。*



# Day11：进程与线程

### 1.并发并行

​	并发：**交替执行**，同一时间段内处理多个任务【单核CPU就可以】**并发是逻辑概念**

​	并行：**同时执行**，同一时刻真正一起运行【必须多核CPU】**并行是物理概念**

​	Python 有个 **GIL（全局解释器锁）**，导致**一个进程内同一时刻只有一个线程在跑**。

​		想并发：用多线程、协程（适合 I/O 密集）。 

​		想并行：必须用多进程（绕过 GIL，适合 CPU 密集）。

​	同步：**按顺序执行******，上一个做完才做下一个

​	异步：**任务不等待**，继续做别的事，**适合 I/O 密集（网络请求、读写文件），尤其是大模型 API 调用**

### 2.进程与线程

#### 		1.进程（分配内存资源）

​		进程是操作系统进行资源分配的基本单位

​		操作系统中一个正在运行的程序或者软件就是一个进程

​		每个进程都有自己独立的一块空间

​		一个进程崩溃后，在保护模式下不会对其他进程产生影响

​		多线程是指在操作系统中同时运行多个程序		

##### 			1.使用`multiprocessing.Process`创建进程

​	Unix/Linux操作系统提供一个 os.fork() 系统调用，调用一次返回两次，系统自动把当前进程（父进程）复制一个进程（子进程），分别在父进程和子进程内返回。

​	windows中没有 fork() 调用，Python提供跨平台多进程模块 multiprocessing。multiprocessing 模块提供一个 Process 类来代表一个进程对象。Windows 用 `spawn` 创建子进程，不加保护会无限递归。

```python
multiprocessing.Process(group=None,target=None,name=None,args=(),kwargs={},*,daemon=None)
```

| 参数     | 作用                                                         |
| -------- | ------------------------------------------------------------ |
| group    | 永远传 `None`，为了和 `threading.Thread`（线程） 兼容。完全不用管 |
| `target` | 核心参数，由run() 方法来发起调用的可调用对象，默认None       |
| `name`   | 进程名字，默认None。不传默认叫 `Process-1`、`Process-2`。    |
| `args`   | 参数元组。传给 `target` 的参数                               |
| `kwargs` | 关键字参数字典。传给 `target` 的参数                         |
| `daemon` | 是否为守护进程`True` 表示主进程结束时子进程强制退出，`False` 表示等子进程执行完 |

​	Process 的属性和方法与其他常用方法

| 属性                | 作用                                                         |
| ------------------- | ------------------------------------------------------------ |
| `p.pid`             | 获取进程ID（号）                                             |
| `p.name`            | 获取进程名称                                                 |
| `p.daemon`          | 判断或者是否守护进程**，必须在 start() 之前设置              |
| `p.exitcode`        | 获取子进程的退出码<br />None`（未结束）、`0`（正常）、负数（被信号终止，如 `-15` 是 SIGTERM） |
| **方法**            | **作用**                                                     |
| `p.start()`         | 启动子进程，传入target对象，只能被调用一次                   |
| `p.join([timeout])` | 阻塞主进程，主进程等待子进程结束，timeout为曹氏多少秒后主进程继续执行 |
| `p.run()`           | 默认调用传入target对象，如果子类化了Process，可以重写方法自定义行为 |
| `p.is_alive()`      | 判断子进程是否存活                                           |
| `p.terminate()`     | **强制终止**子进程                                           |
| `p.kill()`          | **强制杀掉**子进程，更彻底                                   |
| `p.close()`         | 关闭进程对象，释放资源，**必须在 join() 或 terminate() 之后调用** |
| `os.getpid()`       | 获取当前进程编号                                             |
| `os.getppid()`      | 获取当前进程的父进程编号                                     |

```python
import multiprocessing
import time
def write_file():
    print(f"write_file{__name__}")
    with open('./file.txt', 'w') as f:
        while True:
            f.write('hello world\n')
            # 文件写入时，数据先进入内存缓冲区，缓冲区满了才会真正写到硬盘。
            # 如果写进程不调用 f.flush()，读进程可能很长时间读不到新数据（因为数据还在内存里）。
            # f.flush() 强制将缓冲区数据立刻写入硬盘，让读进程能立刻读取到。
            f.flush()
            time.sleep(0.5)
def read_file():
    print(f"read_file{__name__}")
    with open('./file.txt', 'r') as f:
        while True:
            time.sleep(0.5)
            content = f.read()
            print(content)
p1=multiprocessing.Process(target=write_file)
p2=multiprocessing.Process(target=read_file)
# if __name__ == '__main__': 的必要性（重中之重！）
# 在 Windows 下，Python 创建新进程是通过重新导入当前模块来实现的。
# 如果不在 if __name__ == '__main__': 里调用 start()，那么新进程在导入模块时，
# 又会执行到 p1.start()，从而无限递归创建新进程，直接导致系统卡死或报 RuntimeError。
if __name__=='__main__':
    print(f"主进程{__name__}")
    p1.start()
    p2.start()
    print("end")
```

##### 		2.自定义 Process 子类创建进程

```python
import os
from multiprocessing import Process
class Worker(Process):
    # start()做的事：创建子进程 → 在子进程中调用run()
    def run(self): #start->run->target
        print(f"进程号是：{os.getpid()}，父进程号是{os.getppid()}")
if __name__ == '__main__':
    print(f"进程号是：{os.getpid()}，父进程号是{os.getppid()}")
    w1=Worker()
    w2=Worker()
    # 如果你手动调用 w1.run()，它只是在当前进程执行 run() 里的代码，根本不会创建新进程。
    w1.start()
    w2.start()
```

##### 		3.创建进程池

`multiprocessing.Pool([processes[,initializer[,initargs[,maxtasksperchild[,context]]]]])`

###### 			1.进程池的创建

| 参数               | 作用                                                         |
| ------------------ | ------------------------------------------------------------ |
| `processes`        | 要使用的工作进程数量，不传默认等于 `os.cpu_count()`（CPU 核心数）。 |
| `initializer`      | 进程初始化函数，每个工作进程都在启动时调用initializer(*initargs) |
| `initargs`         | 初始化的参数，必须是元组                                     |
| `maxtasksperchild` | 每个子进程最大任务数。**解决内存泄漏神器**。默认是None，工作进程寿与池齐 |
| `context`          | 进程启动方式，一般不用管，Windows 默认是 `spawn`，Linux 默认是 `fork`。 |

​	注意：进程池对象的方法只有创建他的进程能够调用

​	使用时一般只指定prcesser参数

###### 			2.常用方法【进程池的进程默认是守护进程，所以需join()确保主进程等待】

| 方法                                                         | 作用                                                         | 是否阻塞 |
| ------------------------------------------------------------ | ------------------------------------------------------------ | -------- |
| `pool.apply(func[, args[,kwds]])`                            | 提交**单个**任务。用args参数及kwds命名参数调用func，在返回结果前阻塞。func只会在一个进程池中的一个工作进程中执行 | 阻塞     |
| `pool.apply_async(func[, args[,kwds,[,callback[,error_callback]]]])` | 异步调用，返回 `AsyncResult`，callback获取结果，error_callback处理异常 | 非阻塞   |
| `pool.close()`                                               | 阻止后续任务提交到进程池，所有任务执行完毕后工作进程退出     | -        |
| `pool.terminate()`                                           | **强制终止**所有子进程，不必等待未完成的任务                 | -        |
| `pool.join()`                                                | z阻塞主进程等待工作进程结束。调用前必须调用close()或者terminate | 阻塞     |
| `pool.map_async(func, iterable)`                             | 批量提交，返回 `AsyncResult`                                 | 非阻塞   |
| `pool.map(func, iterable)`                                   | 批量提交，**按顺序**返回结果                                 | 阻塞     |
| `pool.imap(func, iterable)`                                  | 迭代器版 map，**边跑边出结果**                               | 非阻塞   |
| `pool.starmap(func, iterable)`                               | 批量提交，自动解包参数                                       | 阻塞     |
| `result.get()`                                               | 从 `AsyncResult` 获取结果                                    | 阻塞     |
| `result.wait()`                                              | 等待任务完成                                                 | 阻塞     |
| `result.ready()`                                             | 判断任务是否完成                                             | 非阻塞   |
| `result.successful()`                                        | 判断任务是否成功                                             | 非阻塞   |
| `pool.__len__()`                                             | 当前活跃进程数                                               | -        |

**注意：用apply_async时，加join()【守护进程需要阻塞】和close()【join前必须使用close或者terminate】**

##### 		4.进程间通信 【进程间不共享全局变量，进程之间内存是完全独立】

​	Queue通信 `mutiprocessing.Queue([maxsize])`返回一个使用一个通道和少量锁和信号量实现的共享队列实例。当一个进程将一个对象放放进队列中时，一个写入线程会启动并将对象从缓冲区写入管道中。默认队列是无限大小，可以通过maxsize参数限制

​	qsize()：返回队列大致长度。由于多线程或者多进程上下文，这个数字不可靠

​	empty()：队列为空返回True。由于多线程或者多进程的环境，这个状态不可靠

​	full()：队列满返回True。由于多线程或者多进程的环境，这个状态不可靠

​	put(obj[,block[,timeout]])：将obj放入队列。如果参数block是True（默认值）而且timeout是None（默认值），将会阻塞当前进程，知道有空的缓冲槽。如果timeout为正数，则阻塞最多timeout秒后还有没可用的缓冲槽是抛出queue.Full异常。反之（block为False），仅当有可用缓冲槽时才放入对象，否则抛出queue.Full异常（此时timeout忽略）【 **put_nowait(obj) 相当于put(obj,False)** 】

​	get([block,[timeout]])：从队列中取出并返回对象。如果block为True（默认值）并且timeout为None时，将会阻塞进程，直到队列中出现可用对象。如果timeout为正数，则阻塞最多timeout秒后还没有可用的对象则抛出queue.Empty 异常。反之（block为False），仅当有可用对象能够取出时返回，否则抛出异常queue.Empty异常（timeout忽略）【**get_nowait() 相当于 get(False)**】

**注意：Pool进程池实现 【multiprocessing.Manager().Queue配合进程池中的apply_async】【兼容性】**

**注意：multiprocessing.Process 与Queue 使用时候需要在最后阻塞【p1.join()】【兼容性】**

#### 2.线程（分配CPU资源）		

​	线程是处理器任务调度和执行的基本单位

​	一个进程至少有一个线程，也可以运行多个线程

​	多个线程之间可共享数据

​	线程出错异常后，如果没有捕获，可能导致整个进程崩溃

​	多线程是指同一个进程中同时执行多个任务

##### 	1.使用 threading.Thread 创建一个线程

Python标准库中提供两个模块：\_thread（低级）和threading（高级模块，对\_thread进行封装）

`threading.Thread(group=None,target=None,name=None,args=(),kwargs={},*,daemon=None)`

| 参数   | 作用                                                         |
| ------ | ------------------------------------------------------------ |
| group  | 应为None，保留给将来实现 ThreadGroup 类的扩展使用            |
| target | 用于run() 方法带哦用的可调用对象。默认是None，表示不需要任何方法 |
| name   | 线程名称。默认以”Thread-N“构架唯一名称。或者”Thread-N(target)“形式，target为target.\_\_name\_\_,如果指定了target参数的情况下 |
| args   | 用于发起调用目标函数的参数列表或者元组。默认（）             |
| kwargs | 用于发起调用目标函数的关键字参数字典。默认{}                 |
| daemon | 是否是守护线程模式，默认None                                 |

​	Thread的属性和方法与其他常用方法

| 属性           | 作用                                                         |
| -------------- | ------------------------------------------------------------ |
| `t.name`       | 线程名，默认 `Thread-N`，可自定义                            |
| `t.ident`      | 线程 ID（类似进程的 PID）                                    |
| `t.daemon`     | 是否守护线程，**必须在 start() 前设置**                      |
| `t.native_id`  | 操作系统级线程 ID（Python 3.8+）此线程的线程id，os（内核）分配 |
| `t.is_alive()` | 线程是否存活                                                 |

| 方法                       | 作用                                     |
| -------------------------- | ---------------------------------------- |
| `t.start()`                | 启动线程，自动调用 `run()                |
| `t.join([timeout])`        | 阻塞线程，直到完成主和超时。             |
| `t.is_alive()`             | 判断线程是否存活                         |
| `t.run()`                  | 自定义线程行为，默认调用传入的target对象 |
| threading.enumerate()      | 查看都有哪些现场                         |
| threading.current_thread() | 返回当前线程实例                         |

##### 	2.自定义 threading.Thread 子类创建一个线程

##### 	3.创建线程池

ThreadPoolExecutor 是 concurrent.futures模块中的线程池实现，它允许我们轻松的提交任务到线程池中

###### 		1.线程池的创建

`concurrent.futures.ThreadPoolExecutor(max_workers=None,thread_name_prefix="",initializer=None,initargs=())`

| 参数               | 作用                                   |
| ------------------ | -------------------------------------- |
| max_workers        | 线程池最大线程数（默认取决于系统资源） |
| thread_name_prefix | 线程名前缀                             |
| initializer        | 每个线程启动时的初始化函数             |
| initargs           | 传给 `initializer` 的参数，必须是元组  |

###### 		2.线程池常用的方法 

| 方法                                            | 作用                                                         |
| ----------------------------------------------- | ------------------------------------------------------------ |
| `submit(fn, *args，**kwargs)`                   | 提交单个任务，返回 `Future`对象，使用Future.result()获取任务结果 |
| `map(fn, *iterables，timeout=None,chunksize=1)` | 类似map批量提交，按顺序返回，可迭代对象传给目标函数，        |
| `shutdown(wait=True,cancel_futures=False)`      | 关闭池，wait是否等待线程中所有线程完成任务，cancel_futures是否取消尚未开始任务 |
| `with` 语句                                     | 自动 `shutdown`                                              |
| `as_completed(futures)`                         | 按完成顺序迭代 `Future`                                      |
| `wait(futures)`                                 | 等待一批任务完成                                             |

##### 	4.互斥锁

线程安全问题：多个线程访问相同独享的时候，如果对对象进行修改操作，那么可能会出现线程问题

【解决】互斥锁概念：保证了每次只有一个线程进行写入操作，从而保证了多线程请胯下的数据正确性

​		1.添加： threading.Lock() 创建互斥锁

​		2.使用：lock.acquire(\[blocking=True][,timeout=1])来获取锁

blocking为True，线程会阻塞直到获取锁。如果为False线程立刻返回。获取锁成功返回True，否则返回False/timeout为等待超时时间。超时未获得锁返回False

​		3.释放锁：lock.release() 释放

#### 3.进程和线程的区分

##### 	资源分配

​	进程拥有独立的内存空间和系统资源，每个进程都有自己的代码段、数据段和堆栈等。而线程共享所属进程的内存空间和资源，同一进程内的线程之间可以直接访问共享内存。

##### 	开销

​		创建进程需要分配独立的内存、打开文件等系统资源，开销较大。

​		创建线程只需在所属进程的内存空间内进行少量资源分配，开销较小。

##### 	并发性

​		在多核心 CPU 环境下，进程和线程都可以异步执行但进程之间的异步是真正的异步（每个进程在不同核心上同时执行），而线程之间的异步在单核心 CPU 上是通过时间片轮转实现的 “伪异步”（在同一时刻只有一个线程执行），在多核心 CPU 上可以实现异步。但是在Cpython中，因为GIL的存在，也不是真正的异步

##### 	独立性

​		进程之间相互独立，一个进程的崩溃通常不会影响其他进程。而同一进程内的线程之间相互影响，一个线程出现问题可能导致整个进程崩溃。

##### 	通信

​		进程间通信相对复杂，需要使用特殊的机制，如管道、消息队列、共享内存等。

​		线程间通信相对简单，因为它们共享内存，可以直接访问共享变量。

#### 4.使用场景

##### 	适合使用多线程的情况：

**I/O 密集型任务：**如网络请求、文件读写等。线程共享内存，切换开销小，在等待 I/O 操作完成的时间内可以切换到其他线程执行，提高整体效率。例如一个程序需要同时从多个网站下载数据，使用多线程可以在等待网络响应时执行其他下载任务。

**对资源共享要求高：**线程间共享内存，方便数据共享和通信。例如在一个图形界面程序中，多个线程需要共享界面数据并进行实时更新。

##### 	适合使用多进程的情况：

**CPU 密集型任务**：多进程可以利用多核心 CPU 实现真正的并行计算，充分发挥硬件性能。例如进行复杂的科学计算、数据处理等任务，每个进程在不同核心上独立计算，提高计算速度。

**需要隔离的任务：**进程相互独立，一个进程崩溃不会影响其他进程。对于一些可能出现异常或不稳定的任务，使用多进程可以保证系统的稳定性。例如运行多个独立的服务，每个服务作为一个进程，避免一个服务出错影响其他服务。

------

*持续更新中，欢迎指点。*



# 📎 附录：Pychram快捷键（仅个人常用）

**Alt + J**：选中下一个和当权选中同名的变量，统一修改

**Ctrl + Shift + Alt + J**：一次性选中所有的和选中同名的变量，统一修改

**按住 alt**：添加光标

**Ctrl + Alt + T**：包围选中代码

**Ctrl + Shift + V**：从剪贴板历史粘贴

------

*持续更新中，欢迎指点。*


# CSS & CSS3 学习笔记

> 适配后端开发者学习，包含：概念、语法、引入方式、选择器、常用属性、盒子模型、浮动、Flex弹性布局、CSS3新增特性；标注参数说明、使用示例、注意事项、避坑点。

## 目录

1. CSS基础概念
2. CSS三种引入方式
3. CSS选择器
4. CSS常用基础属性
5. 盒子模型（Box Model）核心
6. 浮动 float
7. 定位 position
8. CSS3 新增常用特性
9. 高频避坑总结

------

# 1 CSS基础概念

**CSS：Cascading Style Sheets 层叠样式表**

- HTML负责搭建页面**结构**，CSS负责页面**美化样式**。
- 层叠：多个样式作用在同一个标签，同名属性覆盖，不同属性全部叠加生效。

### 语法格式

```
选择器 {
    属性名: 属性值;
    属性名2: 属性值2;
}
```

- **选择器**：指定要设置样式的标签
- **属性名: 属性值** 一对为一条样式，分号结尾。

示例

```
div {
    width: 200px;
    height: 200px;
    border: red 1px solid;
}
```

> CSS注释：`/* 注释内容 */`，不会生效。

------

# 2 CSS三种引入方式

## 2.1 行内样式（内联样式）

写在标签的`style`属性上，**仅对当前标签生效**，优先级最高。

```
<div style="color:red;font-size:20px;">测试文字</div>
```

> 缺点：代码耦合高，复用差；适合临时调试，业务少用。

## 2.2 内部样式

写在html页面`<head>`中的`<style>`标签，**当前整个页面生效**。

```
<head>
    <style>
        div {
            color: green;
        }
    </style>
</head>
```

## 2.3 外部样式【项目生产最常用】

写独立后缀为`.css`的文件；html通过`<link>`标签引入。

```
<head>
    <!-- rel="stylesheet" 不能省略，代表引入样式表 -->
    <link rel="stylesheet" href="css/style.css">
</head>
```

css/style.css

```
div{
    color: blue;
}
```

### 优先级规则

1. **行内样式 > 内部样式 / 外部样式**

2. 内部、外部：

    后加载的同名样式覆盖先加载的

    > 只有同名属性才覆盖；不同属性全部叠加。

------

# 3 CSS选择器

> 选择器：筛选页面中需要添加样式的HTML标签。

## 3.1 基础选择器

### ①标签选择器

直接写标签名，选中页面**全部同名标签**

```
p {
    color: red;
}
```

### ②id选择器

符号 `#`；标签设置`id="xxx"`。

> ⚠️同一个页面id**必须唯一**。JS获取DOM依赖id唯一性。

```
<p id="p1">测试</p>
#p1 {
    color: blue;
}
```

### ③class类选择器【开发最常用】

符号 `.`；标签设置`class="类名"`。

- 多个标签可以复用同一个class；
- 一个标签可以写多个class，空格隔开 `class="text big red"`。

```
<p class="text‑big">测试</p>
.text‑big {
    font‑size: 24px;
}
```

#### 基础选择器优先级

```
id选择器 > class类选择器 > 标签选择器
```

## 3.2 复合选择器

### 后代选择器 空格

父 子 空格隔开，选择父标签**所有后代（子、孙子）**

```
div p {
    color: orange;
}
/* div内部所有p标签 */
```

### 子元素选择器 `>`

只选直接子元素，不包含孙子后代

```
div > p {
    color: orange;
}
```

### 并集选择器 `,`

多个选择器逗号分隔，给多组标签设置相同样式

```
h1,h2,p {
    color: #333;
}
```

### 交集选择器（标签+类）

直接连写，无空格；同时满足标签和class

```
p.text-red {
    color: red;
}
/* 选中 class=text‑red 的p标签 */
```

## 3.3 伪类选择器

以`:`开头，描述标签**特殊状态**，常用于a超链接。

```
/* a链接伪类，顺序不能乱：LVHA */
a:link { /* 未访问 */
    color: black;
}
a:visited { /* 已经访问过 */
    color: purple;
}
a:hover { /* 鼠标悬浮【高频】 */
    color: red;
}
a:active { /* 鼠标点击按下未松开 */
    color: blue;
}
```

> hover也可以用于div等普通元素：`div:hover{}`

## 3.4 CSS3属性选择器（拓展）

```
/* 包含属性name */
input[name] {}
/* name等于username */
input[name="username"] {}
```

------

# 4 CSS常用基础属性

## 4.1 文本字体属性

```
div{
    font‑size: 24px;         /* 字体大小，单位px像素 */
    font‑family: "微软雅黑";  /* 字体 */
    font‑weight: bold;       /* 加粗：bold加粗 normal正常 */
    color: #ff0000;          /* 文字颜色：英文、十六进制#RRGGBB */
    text‑align: center;      /* 文本对齐 left / center / right */
    line‑height: 40px;       /* 行高；行高等于盒子高度可以实现文字垂直居中 */
    text‑decoration: none;   /* 文本修饰：none去掉下划线；underline下划线 */
}
```

> 颜色十六进制简写：`#ff0000` → `#f00`；`#ffffff` → `#fff`。

## 4.2 背景属性

```
div{
    background‑color: #ccc;                     /* 背景颜色 */
    background‑image: url("img/a.jpg");        /* 背景图片 */
    background‑repeat: no‑repeat;              /* 重复：no‑repeat不重复；repeat‑x横向重复 */
    background‑position: center;               /* 背景图位置 center / left top */
    background‑size: cover;                   /* CSS3：背景图铺满盒子 */
}
/* 简写，顺序无强制 */
background: #ccc url("img/a.jpg") no‑repeat center;
```

## 4.3 边框 border

简写语法：`border: 宽度 样式 颜色;`

```
div {
    border: 2px solid red;
}
```

- 样式：`solid`实线；`dashed`虚线；`double`双线；`none`无边框。 分开四边设置

```
border‑top: 1px solid red;
border‑right: 1px solid red;
border‑bottom: 1px solid red;
border‑left: 1px solid red;
```

## 4.4 显示模式 display

| 取值           | 说明                                               |
| -------------- | -------------------------------------------------- |
| `block`        | 块级元素：独占一行，可以设置宽高（div h1‑h6 p）    |
| `inline`       | 行内元素：同一行排列，**宽高设置无效**（span b i） |
| `inline‑block` | 行内块：同一行排列，可以设置宽高（img、input）     |
| `none`         | 隐藏元素，不占页面空间；彻底消失                   |

> 避坑：行内元素不能直接设置width、height；改成`display:inline‑block`。

------

# 5 盒子模型 Box Model【CSS核心】

网页所有元素看做矩形盒子，从内向外四层：

1. **content 内容**：`width`、`height` 设置内容区域宽高
2. **padding 内边距**：内容到边框之间距离
3. **border 边框**
4. **margin 外边距**：盒子与其他盒子之间距离

## 5.1 padding 内边距

简写（顺时针：上、右、下、左）

```
div{
    padding: 10px;                   /* 全部四边10px */
    padding: 10px 20px;              /* 上下10px，左右20px */
    padding: 10px 20px 30px;         /* 上10px，左右20px，下30px */
    padding: 1px 2px 3px 4px;        /* 上 右 下 左 */
}
```

分开写：`padding‑top` / `padding‑right` / `padding‑bottom` / `padding‑left`

> ⚠️**W3C标准盒模型：padding、border会撑大盒子整体实际宽高**。

## 5.2 margin 外边距

语法格式和padding完全一致。

```
div{
    margin: 0 auto; /* 上下0，左右auto；块级盒子水平居中【高频】 */
}
```

> 避坑1：**垂直方向相邻块元素margin会发生外边距合并塌陷，取两者的最大值**。 避坑2：`margin:0 auto` **只对块级元素生效**；行内、行内块无效。

## 5.3 CSS3 盒子模型切换 box‑sizing

```
box‑sizing: border‑box;
```

设置为`border‑box`之后：`width/height`代表**整个盒子总宽高**；padding、border向内挤压内容，不会撑大盒子。开发非常常用。

```
div{
    width:200px;
    height:200px;
    padding:20px;
    border:5px solid red;
    box‑sizing: border‑box;
}
```

------

# 6 浮动 float

> 作用：实现多个块级元素**并排一行显示**；早期网页布局方案。

```
float: left;   /* 向左浮动 */
float: right;  /* 向右浮动 */
float: none;   /* 默认不浮动 */
```

### 浮动特点

1. 浮动元素脱离普通文档流；原来的普通流元素会“流到浮动元素下面”。
2. 多个设置`float:left`的块会从左向右并排。

### ⚠️清除浮动【必学避坑】

父盒子**没有设置高度**，内部全部子元素浮动，父盒子高度会变成0，布局错乱。

清除浮动三种常用方案：

1. **额外标签法**：浮动元素末尾加空div，`clear:both`

```
.clear{
    clear: both;
}
```

1. **伪元素清除浮动（推荐）**

```
.clearfix::after{
    content:"";
    display:block;
    clear:both;
    height:0;
    visibility:hidden;
}
```

给父盒子加上class="clearfix"即可。

1. 父盒子设置 `overflow:hidden`；简单，但部分场景有副作用。

> 现在新项目优先使用Flex布局，尽量少用float。

------

# 7 定位 position

| 取值                   | 说明                                                         | 偏移属性              |
| ---------------------- | ------------------------------------------------------------ | --------------------- |
| `static`               | 默认，普通文档流，定位无效                                   | top/left无效          |
| `relative`**相对定位** | **不脱离文档流**；相对于自己原来的位置偏移                   | top left right bottom |
| `absolute`**绝对定位** | 脱离文档流；相对于**最近一个已经定位的父元素**；父没有定位则相对于浏览器窗口 | top left              |
| `fixed`**固定定位**    | 脱离文档流；相对于浏览器视口，滚动页面位置不动（悬浮回到顶部按钮） | top left              |

> 重点记忆：
>
> - `absolute`父容器需要设置`position:relative`，实现子盒子相对于父盒子定位。
> - `z‑index`：控制定位元素堆叠层级；数值越大越靠上；**只有定位元素z‑index生效**。

```
z‑index: 999;
```

------

# 8 CSS3 新增常用特性

## 8.1 圆角 border‑radius

```
/* 四个角全部圆角 */
border‑radius: 8px;
/* 圆形：正方形盒子 border‑radius:50% */
border‑radius: 50%;
```

## 8.2 盒子阴影 box‑shadow

```
box‑shadow: x偏移 y偏移 模糊大小 颜色;
box‑shadow: 2px 2px 10px #999;
```

## 8.3 文字阴影 text‑shadow

```
text‑shadow: 1px 1px 3px #666;
```

## 8.4 Flex 弹性布局【现代布局，强烈推荐，替代浮动】

> 给父盒子设置 `display:flex`；父容器叫flex容器，子元素叫flex项目。

### 父容器常用属性

```
.box{
    display: flex;
    /* 主轴方向 row水平；column垂直 */
    flex‑direction: row;
    /* 换行 wrap；nowrap不换行 */
    flex‑wrap: wrap;
    /* 主轴对齐 */
    justify‑content: center; /* 居中；flex‑start左对齐；space‑between两边贴边中间均分 */
    /* 侧轴（交叉轴）对齐 */
    align‑items: center; /* 垂直居中 */
}
```

### 子项目属性

```
flex: 1; /* 瓜分剩余空间；多子元素写flex:1，自动平分宽度 */
align‑self: center; /* 单独修改自己侧轴对齐 */
order: 2; /* 排序，数字越小越靠前 */
```

> ✨经典场景：父`display:flex; justify‑content:center; align‑items:center;`实现子元素**水平+垂直居中**。

## 8.5 过渡 transition（简单动画）

实现属性变化平滑动画，不要瞬间突变。

```
/* 哪个属性 过渡时间 运动曲线 */
transition: width 0.5s ease;
/* 全部属性都过渡 */
transition: all 0.3s;
```

配合hover使用，鼠标悬浮平滑变化。

## 8.6 2D变换 transform

```
transform: translate(50px,100px); /* 位移 x,y；百分比是相对于自身大小 */
transform: rotate(45deg); /* 旋转，deg角度 */
transform: scale(1.2); /* 缩放，大于1放大 */
```

## 8.7 @keyframes 关键帧动画

```
/* 定义动画 */
@keyframes move {
    0% {transform:translateX(0px);}
    100% {transform:translateX(200px);}
}
/* 使用动画 */
div{
    animation: move 2s infinite alternate;
}
```

------

# 9 高频避坑总结

1. 行内元素（span、b）**默认不能设置width、height**，改为`display:inline‑block`。
2. `margin:0 auto`只对**块级元素**生效，实现盒子水平居中，不能实现文字垂直居中；文字垂直居中用`line‑height`。
3. 标准盒子模型padding、border会撑大盒子；想要宽高固定，设置`box‑sizing:border‑box`。
4. 浮动元素父盒子不写高度，会出现高度塌陷，记得清除浮动；新项目优先Flex，少用float。
5. `position:absolute`绝对定位，父元素要设置`position:relative`，才会相对于父盒子定位，否则参照浏览器窗口。
6. `z‑index`只对**已经设置定位（relative/absolute/fixed）**的标签生效，普通static元素无效。
7. a标签伪类顺序必须：`link → visited → hover → active`（LVHA），顺序错 hover 会失效。
8. 外部css引入`rel="stylesheet"`不能漏写，否则样式不生效。
9. 垂直方向块元素margin会发生外边距合并塌陷，不要依赖垂直margin做间距。
10. flex布局父盒子写`display:flex`，子元素float会失效。
11. `display:none`彻底隐藏，不占空间；`visibility:hidden`隐藏，但是保留占位。

> 拓展小提示：Flex布局是现在网页主流布局方案，兼容性现代浏览器全部支持；浮动float属于旧时代布局方案，尽量减少使用。

------

持续更新中，欢迎指点。⭐
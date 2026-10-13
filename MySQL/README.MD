# 🐬 MySQL 核心知识速查手册

> 📢 **学习声明**：本笔记的知识体系、大纲脉络与案例演示，**学习课程源于尚硅谷 (Atguigu) 的 MySQL 课程**。在此特别感谢尚硅谷老师的悉心教导，本仓库仅为个人学习过程中的知识点梳理、踩坑记录与心得沉淀。

这里记录了我学习 MySQL 过程中的知识点梳理、踩坑记录与心得。欢迎各位前辈和大神交流指正！

## 📖 目录

- [1. 基础概念](#1-基础概念)
- [2. SQL 分类](#2-sql-分类)
- [3. DDL 数据定义](#3-ddl-数据定义)
- [4. DML 数据操作](#4-dml-数据操作)
- [5. DQL 数据查询](#5-dql-数据查询)
- [6. 运算符](#6-运算符)
- [7. 数据类型](#7-数据类型)
- [8. 系统函数](#8-系统函数)
- [9. 关联查询](#9-关联查询)
- [10. 子查询](#10-子查询)
- [11. 约束](#11-约束)
- [12. 事务](#12-事务)
- [13. 用户与权限](#13-用户与权限)
- [14. 核心定义与范式](#14-核心定义与范式)
- [15.Python连接MySQL](#15-Python连接MySQL)

---

## 1. 基础概念

| 概念                         | 说明                                                         |
| :--------------------------- | :----------------------------------------------------------- |
| DB                           | Database，存储数据的地方                                     |
| DBMS                         | 数据库管理系统（MySQL、Oracle、SqlServer）                   |
| SQL                          | 结构化查询语言，操作数据库的通用语言                         |
| 关系型                       | **二维表** + SQL + 强 ACID（MySQL、PostgreSQL、Oracle）      |
| 非关系型 NoSQL(not only SQL) | **键值**/文档/图 + 高扩展 + 最终一致（Redis、MongoDB、Neo4j） |

**表关系**：一对一、一对多（外键）、多对多（中间表）。

**关系型 = 表格 + SQL + 强事务；**

**非关系型 = 灵活模型 + 高扩展 + 最终一致。**

**关系型和非关系型数据库的区别？**

- 数据模型不同：关系型是二维表，非关系型是键值/文档/图等。

- Schema（图）：关系型严格，非关系型灵活。

- 事务：关系型强 ACID，非关系型 BASE。

- 扩展：关系型垂直扩展，非关系型水平扩展。

- 查询：关系型 SQL + JOIN，非关系型各自 API。

- 适用场景：关系型适合强一致、复杂查询；非关系型适合高并发、海量数据、灵活 schema。

*MySQL5.5之后  InnoDB 是默认的存储引擎。*

---

## 2. SQL 分类

| 类型     | 全称                         | 语句                        |
| :------- | :--------------------------- | :-------------------------- |
| **DDL**  | Data Define Language         | create、alter、drop         |
| **DML**  | Data Manipulation Language   | insert、update、delete      |
| **DQL**  | Data Query Language          | select                      |
| **DCL**  | Data Control Language        | grant                       |
| **TCL**  | Transaction Control Language | COMMIT、ROLLBACK、SAVEPOINT |
| **其他** | 命令                         | use、show、set              |

| 命令                                      | 作用                          |
| ----------------------------------------- | ----------------------------- |
| `mysql -h主机名 -P端口号 -u用户名 -p密码` | **完整的连接命令**            |
| `show index from 表名;`                   | **查看索引**                  |
| `show variables like '%character%';`      | **查看 MySQL 的字符集配置**。 |
| `show variables;`                         | 查看所有系统变量              |
| `show variables like '%xxx%';`            | 模糊匹配变量名                |
| `show status;`                            | 查看服务器状态信息            |
| `show status like '%xxx%';`               | 模糊匹配状态名                |
| `show databases;`                         | 查看所有数据库                |
| `show tables;`                            | 查看当前库的表                |
| `show create table 表名;`                 | 查看建表语句                  |
| `show engines;`                           | 查看存储引擎                  |
| `show charset;`                           | 查看支持的字符集              |
| `show collation;`                         | 查看校对规则                  |

语法规范**：

- SQL 不区分大小写。
- 库名/表名/字段名用字母、数字、下划线，避免关键字。
- 关键字冲突时用反引号 `` ` `` 包裹。

**注释**：`# 注释`、`-- 注释`、`/* 注释 */`

---

## 3. DDL 数据定义

### 3.1 库操作

```sql
-- 创建
create database 库名;
create database if not exists 库名;

-- 查看
show databases;
show create database 库名;

-- 修改编码
alter database 库名 character set 字符集 collate 校对规则;
-- 修改库名
-- MySQL 不支持 ALTER DATABASE ... RENAME 来重命名数据库。
-- alter database xxx

-- 使用
use 库名;

-- 删除
drop database 库名;
drop database if exists 库名;
```

### 3.2 表操作

```sql
-- 创建表
create table [if not exists] 表名(
    字段名 数据类型,
    字段名 数据类型
);

-- 查看
show tables;
show tables from 库名;
show create table 表名;
desc 表名;	【desc只用于查看表结构】

-- 修改表编码
alter table 表名 character set 字符集 collate 校对规则;

-- 添加字段
alter table 表名 add 字段名 数据类型;
alter table 表名 add 字段名 数据类型 first;
alter table 表名 add 字段名 数据类型 after 另一个字段;

-- 删除字段
alter table 表名 drop 字段名;

-- 修改字段数据类型
alter table 表名 modify 字段名 新数据类型;

-- 修改字段名
alter table 表名 change 旧字段名 新字段名 新数据类型;

-- 修改字段位置
alter table 表名 modify 字段名 数据类型 first;
alter table 表名 modify 字段名 数据类型 after 另一个字段;

-- 修改表名
alter table 旧表名 rename 新表名;
rename table 旧表名 to 新表名;

-- 删除表
drop table [if exists] 表名;

-- 复制表结构
create table 新表 like 旧表;

-- 复制表结构 + 数据
create table 新表 as (select * from 旧表);
```

---

## 4. DML 数据操作

### 4.1 插入

```sql
-- 全字段插入（值顺序、类型、个数必须与表结构一一对应）
insert into 表名 values(值1,值2,...),(值1,值2,...);

-- 指定字段插入【批量】
insert into 表名(字段1,字段2) values(值1,值2),(值1,值2);

-- 复制数据
insert into 表名 select * from 旧表 where 条件;
```

### 4.2 删除

```sql
-- 条件删除
delete from 表名 where 条件;

-- 删除所有（表结构保留，可回滚）新数据续用旧的id
delete from 表名;

-- 截断表（表结构保留，不可回滚，效率高）删除整个表，创建一个一摸一样的，id从1开始
【⭐这是DDL，事务只对DML有效，对DDL无效】truncate 表名;
```

**delete vs truncate**：
- `delete`：逐行删除，事务中可回滚。
- `truncate`：drop 后重建，效率高，**不可回滚**。

### 4.3 修改

```sql
-- 修改满足条件的行
update 表名 set 字段1=值1, 字段2=值2 where 条件;

-- 修改所有行
update 表名 set 字段1=值1, 字段2=值2;
```

---

## 5. DQL 数据查询

### 5.1 基本语法

```sql
select 常量;
select 表达式;
select 函数;
select 字段列表 from 表名;
select 字段列表 from 表名 where 条件;
【注意：工程中select 避免写 `*` ，而是把需要的字段都写出来】
```

### 5.2 别名与去重⭐

```sql
select 字段名1 as "别名1", 字段名2 as "别名2" from 表名 as 表别名;

-- 去重
select distinct 字段列表 from 表名;
```

**注意：若别名中存在空格等特殊符号，此时别名必须加单引号或飘号**

### 5.3 七个子句顺序

```sql
select ...
from ...              -- 1. 从哪些表筛选
join ... on ...        -- 2. 多表关联
where ...              -- 3. 行筛选
group by ...           -- 4. 分组
having ...             -- 5. 分组结果筛选
order by ...           -- 6. 排序
limit m, n;            -- 7. 分页
```

### 5.4 group by

```sql
-- 分组统计
select did, avg(salary) from t_employee group by did;

-- 合计
select did, count(*) from t_employee group by did with rollup;

-- 多字段分组
select did, job_id, gender, count(*) from t_employee group by did, job_id, gender;
```

**注意**：select 后只写和分组统计有关的字段，其他字段不要出现。

### 5.5 having

```sql
-- where 筛选原表记录，不能出现分组函数
-- having 筛选统计结果，可以出现分组函数
select did, avg(salary)
from t_employee
where gender='女'
group by did
having avg(salary) > 12000;
```

### 5.6 order by

```sql
select * from t_employee order by salary desc;              -- 降序
select * from t_employee order by salary asc, eid desc;     -- 多字段
```

### 5.7 limit

```sql
-- limit m, n：m 起始行（从 0 开始），n 显示行数
-- m = (page-1) * n

select * from t_employee limit 0, 5;    -- 第1页
select * from t_employee limit 5, 5;    -- 第2页
select * from t_employee limit 10, 5;   -- 第3页
```

---

## 6. 运算符

### 6.1 算术运算符

| 运算符       | 说明                                            |
| :----------- | :---------------------------------------------- |
| `+`          | 求和（**无字符串拼接功能**，非数字则视为0处理） |
| `-`          | 减                                              |
| `*`          | 乘                                              |
| `/`          | 除                                              |
| `div`        | 整除                                            |
| `%` 或 `mod` | 取余                                            |

**NULL与其他数据类型的运算都是NULL**

**日期类型和字符串类型必须加单引号。**

**数值类型可加单引号可不加单引号，所以`select 1+'2'; -- 3` 当作数值2处理 **

### 6.2 比较运算符

| 运算符            | 说明                         |
| :---------------- | :--------------------------- |
| `>` `<` `>=` `<=` | 大小比较                     |
| `=` `!=` `<>`     | 等于/不等于（不能判断 NULL） |

### 6.3 区间与集合

| 运算符                | 说明          |
| :-------------------- | :------------ |
| `between x and y`     | 区间 `[x, y]` |
| `not between x and y` | 不在区间      |
| `in (x,y,z)`          | 在集合中      |
| `not in (x,y,z)`      | 不在集合中    |

### 6.4 模糊匹配

| 运算符 | 说明       |
| :----- | :--------- |
| `%`    | 任意个字符 |
| `_`    | 1 个字符   |

```sql
where ename like '%冰%';    -- 包含"冰"
where ename like '李%';     -- 以"李"开头
where ename like '_红%';    -- 第二个字是"红"
```

### 6.5 逻辑运算符

| 运算符        | 说明 |
| :------------ | :--- |
| `&&` 或 `and` | 与   |
| `||` 或 `or`  | 或   |
| `!` 或 `not`  | 非   |
| `^`或`xor`    | 异或 |

### 6.6 NULL 处理

| 运算符                  | 说明                  |
| :---------------------- | :-------------------- |
| `is null` 或 `<=> null` | 是 NULL               |
| `is not null`           | 不是 NULL             |
| `ifnull(x, y)`          | x 为 NULL 时用 y 代替 |

```sql
where commission_pct is null;
select salary + salary * ifnull(commission_pct, 0) from t_employee;
```

### 6.7⭐ 任何值和 NULL 计算，结果都是 NULL。

**常用函数**：

| 函数                     | 作用                         |
| ------------------------ | ---------------------------- |
| `ifnull(x, y)`           | x 为 NULL 返回 y             |
| `coalesce(x, y, z, ...)` | 返回第一个非 NULL 的值       |
| `nullif(x, y)`           | x == y 返回 NULL，否则返回 x |

### 6.8⭐ is、like、=  使用场景

| 运算符   | 用途              | 推荐场景                            |
| -------- | ----------------- | ----------------------------------- |
| **=**    | **精确相等**判断  | 数值、日期、字符串**完全匹配**      |
| **like** | **模糊匹配**      | 字符串**部分匹配**（配 `%` 和 `_`） |
| **is**   | **只能判断 NULL** | `is null` / `is not null`           |

---

## 7. 数据类型

### 7.1 数值类型

| 类型                       | 说明                                                         |
| :------------------------- | :----------------------------------------------------------- |
| `int`                      | 整数                                                         |
| `int(M) unsigned zerofill` | 显示宽度 M（一般无意义），无符号，零填充（此时**M宽度**就有意义了） |
| `float` / `double` [m,d]   | 浮点数【m：总长度，d：小数点位数】                           |
| `decimal(M,D)`             | 定点数，精度高，适合货币                                     |
| `bit(M)`                   | 位类型，1~64 位，二进制格式显示数据，果需要以整数形式显示，可以使用BIN()或CONV()。 |

**雪花算法**：是 Twitter 开源的一种分布式 ID 生成算法，用于在分布式系统中生成全局唯一且趋势递增的 ID。

雪花算法生成的 ID 是一个 **64 位的整数**。推荐存储`bigint`。

### 7.2 字符串类型

| 类型                         | 说明                            |
| :--------------------------- | :------------------------------ |
| `char(M)`                    | 定长，最多 255 字符，右填充空格 |
| `varchar(M)`                 | 变长，M 必须指定，节省空间      |
| `enum(值1,值2)`              | 枚举，只能取一个                |
| `set(值1,值2)`               | 集合，可取多个组合              |
| `text`                       | 长文本                          |
| `binary(M)` / `varbinary(M)` | 二进制字符串                    |

### 7.3 日期时间类型

| 类型        | 格式                | 说明                                   |
| :---------- | :------------------ | :------------------------------------- |
| `year`      | YYYY                | 1901~2155                              |
| `date`      | YYYY-MM-DD          | 年月日                                 |
| `time`      | HH:MM:SS            | 时分秒                                 |
| `datetime`  | YYYY-MM-DD HH:MM:SS | 年月日时分秒【不受时区影响】           |
| `timestamp` | YYYY-MM-DD HH:MM:SS | 时区转换，范围 1970~2038【受时区影响】 |

select @@time_zone;	【打印时区】

SELECT @@global.time_zone, @@session.time_zone;

set time_zone ='+2:00' 	【修改时区】

### 7.4 其他

| 类型                                            | 说明                      |
| :---------------------------------------------- | :------------------------ |
| `json`                                          | JSON 数据（MySQL 5.7.8+） |
| `geometry` / `point` / `linestring` / `polygon` | 空间类型                  |

---

## 8. 系统函数

### 8.1 数学函数

| 函数                   | 说明                  |
| :--------------------- | :-------------------- |
| `abs(x)`               | 绝对值                |
| `ceil(x)` / `floor(x)` | 向上/向下取整         |
| `mod(x,y)`             | 取余                  |
| `rand()`               | 0~1 随机值            |
| `round(x,y)`           | 四舍五入保留 y 位     |
| `truncate(x,y)`        | 截断为 y 位小数       |
| `format(x,y)`          | 强制保留 y 位，千分位 |
| `sqrt(x)` / `pow(x,y)` | 平方根 / 幂           |

### 8.2 字符串函数

| 函数                                       | 说明              |
| :----------------------------------------- | :---------------- |
| `concat(s1,s2,...)`                        | 拼接              |
| `concat_ws(a,s1,s2,...)`                   | 用 a 拼接         |
| `char_length(s)` / `length(s)`             | 字符数 / 字节数   |
| `locate(s,str)` / `instr(str,s)`           | s 在 str 中的位置 |
| `upper(s)` / `lower(s)`                    | 大写 / 小写       |
| `left(s,n)` / `right(s,n)`                 | 左/右 n 个字符    |
| `lpad/rpad(str,len,pad)`                   | 左/右填充         |
| `ltrim/rtrim/trim(s)`                      | 去左/右/两侧空格  |
| `trim([both/leading/trailing] s from str)` | 去指定字符        |
| `insert(str,index,len,instr)`              | 替换              |
| `replace(str,a,b)`                         | 替换所有 a 为 b   |
| `repeat(s,n)`                              | 重复 n 次         |
| `reverse(s)`                               | 反转              |
| `strcmp(s1,s2)`                            | 比较              |
| `substring(str,index,len)`                 | 截取              |
| `substring_index(str,分隔符,count)`        | 按分隔符截取      |

### 8.3 日期时间函数

| 函数                                           | 说明          |
| :--------------------------------------------- | :------------ |
| `curdate()` / `current_date()`                 | 当前日期      |
| `curtime()` / `current_time()`                 | 当前时间      |
| `now()` / `sysdate()` / `current_timestamp()`  | 当前日期时间  |
| `utc_date()` / `utc_time()`                    | UTC 日期/时间 |
| `unix_timestamp(date)`                         | UNIX 时间戳   |
| `year/month/day/hour/minute/second(date)`      | 取各部分      |
| `extract(type from date)`                      | 提取指定部分  |
| `datediff(date1,date2)`⭐                       | 日期间隔天数  |
| `timediff(time1,time2)`⭐                       | 时间间隔      |
| `date_add/date_sub(date, interval expr type)⭐` | 日期加减      |
| `date_format(datetime, fmt)`                   | 格式化        |
| `str_to_date(str, fmt)`                        | 解析为日期    |
| `get_format(val_type, format_type)`            | 返回显示格式  |

### 8.4 加密函数

| 函数                     | 说明             |
| :----------------------- | :--------------- |
| `md5(str)`               | MD5 值           |
| `sha(str)`               | SHA 加密（40位） |
| `sha2(str, hash_length)` | SHA2 加密        |

### 8.5 系统信息函数

| 函数         | 说明           |
| :----------- | :------------- |
| `database()` | 当前数据库名   |
| `version()`  | 数据库版本     |
| `user()`     | 当前登录用户名 |

### 8.6 条件判断函数

| 函数                                         | 说明                       |
| :------------------------------------------- | :------------------------- |
| `if(a,x,y)`                                  | a 为真返回 x，否则 y       |
| `ifnull(x,y)`                                | x 非空返回 x，否则 y       |
| `case when 条件 then 结果 ... else 结果 end` | 多条件判断【常用于字段中】 |
| `case 表达式 when 值 then 结果 ... end`      | 等值判断【常用于字段中】   |

### 8.7 分组函数（聚合）

⭐**如果没有group by的话则所有数据看作一组【仅一行数据】**

| 函数                        | 说明                                              |
| :-------------------------- | :------------------------------------------------ |
| `avg([DISTINCT],x)`         | 平均值【可以选参数去重】                          |
| `sum(x)`                    | 求和                                              |
| `max(x)` / `min(x)`         | 最大/最小                                         |
| `count(DISTINCT x, [x...])` | 计数【忽略 NULL，可以去重，也可以多字段组合计数】 |

```sql
select count(*) from t_employee;          -- 统计行数
select count(1) from t_employee;          -- 同上
select count(0) from t_employee;          -- 同上
select sum(1) from t_employee;          -- 也可以统计行数
select count(commission_pct) from t_employee;  -- 忽略 NULL
```

### 8.8 窗口函数

#### 1.基本语法

~~~sql
```sql
函数名(参数) over(
    [partition by 字段]
    [order by 字段]
    [rows between <start> and <end>]
)
~~~

| 部分           | 作用                  | 是否必须 |
| -------------- | --------------------- | -------- |
| `over()`       | 声明窗口函数          | ✅ 必须   |
| `partition by` | 分区（类似 group by） | 可选     |
| `order by`     | 分区内排序            | 可选     |
| `rows between` | 窗口范围              | 可选     |

#### 2.常用函数：

| 函数                                       | 说明             |
| :----------------------------------------- | :--------------- |
| `row_number()`【需要over()】               | 顺序编号 1,2,3,4 |
| `rank()【需要over()】`                     | 并列跳过 1,1,3   |
| `dense_rank()`【需要over()】               | 并列不跳过 1,1,2 |
| `lag()/lead()【需要over()】`               | 前/后偏移值      |
| `first_value()/last_value()【需要over()】` | 首/末值          |
| `sum()/avg()/count()/max()/min()`          | 窗口聚合         |

#### 3.窗口范围：

- `unbounded preceding`：分区第一行
- `n preceding`：当前行前 n 行
- `current row`：当前行
- `n following`：当前行后 n 行
- `unbounded following`：分区最后一行

默认窗口范围：`unbounded preceding and current row`

#### 4.排名函数对比

| 数据 | `row_number()` | `rank()` | `dense_rank()` |
| ---- | -------------- | -------- | -------------- |
| 1000 | 1              | 1        | 1              |
| 1000 | 2              | 1        | 1              |
| 2000 | 3              | 3        | 2              |
| 3000 | 4              | 4        | 3              |

#### 5.常用示例

```sql
-- 顺序编号
select row_number() over() as rn, ename, salary from t_employee;

-- 分区排名（按部门分组，薪资降序）
select ename, did, salary,
       dense_rank() over(partition by did order by salary desc) as dr
from t_employee;

-- 三排名对比
select ename, salary,
       row_number() over(order by salary) as rn,
       rank()       over(order by salary) as rk,
       dense_rank() over(order by salary) as dr
from t_employee;

-- 前后值
select ename, salary,
       lag(salary, 1, 0)  over(order by salary) as 上一位薪资,
       lead(salary, 1, 0) over(order by salary) as 下一位薪资
from t_employee;

-- 首末值（last_value 要显式指定范围）
select ename, salary,
       first_value(salary) over(order by salary) as 首位薪资,
       last_value(salary)  over(order by salary
                                rows between unbounded preceding
                                         and unbounded following) as 末位薪资
from t_employee;

-- 累计求和
select ename, salary,
       sum(salary) over(order by salary
                        rows between unbounded preceding
                                 and current row) as 累计薪资
from t_employee;

-- 分区聚合
select ename, did, salary,
       avg(salary) over(partition by did) as 部门平均薪资
from t_employee;

-- 常用套路：Top-N 问题
-- 每个部门薪资前 3
select *
from (
    select ename, did, salary,
           dense_rank() over(partition by did order by salary desc) as dr
    from t_employee
) t
where t.dr <= 3;

-- 每个部门最低 3 个薪资
select *
from (
    select ename, did, salary,
           row_number() over(partition by did order by salary) as rn
    from t_employee
) t
where t.rn <= 3;
```

---

## 9. 关联查询

*七种结果*

| #    | 名称                                       | 集合含义    | SQL 写法                                         |
| ---- | ------------------------------------------ | ----------- | ------------------------------------------------ |
| 1    | **内连接【inner】**                        | A ∩ B       | `A inner join B on ...`                          |
| 2    | **左连接【left join】**                    | A           | `A left join B on ...`                           |
| 3    | **右连接【right join】**                   | B           | `A right join B on ...`                          |
| 4    | **左连接排除交集【left join，B NULL】**    | A - A∩B     | `A left join B on ... where B.关联字段 is null`  |
| 5    | **右连接排除交集【right join，A NULL】**   | B - A∩B     | `A right join B on ... where A.关联字段 is null` |
| 6    | **全外连接【left join union right join】** | A ∪ B       | `A left join B union A right join B`             |
| 7    | **全外连接排除交集【4 union 5】**          | A ∪ B - A∩B | 左边排除 + 右边排除，再 union                    |

### 9.1 内连接

```sql
-- A ∩ B
select ...
from A inner join B on 关联条件;
```

### 9.2 左连接

```sql
-- A（包含 A-A∩B）
select ...
from A left join B on 关联条件;
```

### 9.3 右连接

```sql
-- B（包含 B-A∩B）
select ...
from A right join B on 关联条件;
```

### 9.4 union

```sql
-- 合并去重
select ... from A
union
select ... from B;

-- 合并保留重复
select ... from A
union all
select ... from B;
```

**注意**：两个 select 的列数必须相同。

### 9.5 自连接

```sql
-- 物理一张表，逻辑两张表
select emp.eid, emp.ename, mgr.ename
from t_employee emp
inner join t_employee mgr
on emp.mid = mgr.eid;
```

---

## 10. 子查询

**【书写顺序：from ==> join on ==> where ==> group by ==> having ==> order by ==>  limit】**

**【执行顺序：FROM → ON → JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT】**

order by:

- *order中有一个with rollup 扩展*【作用是再分组的最后一行显示总和】

- *asc代表升序，desc代表降序，默认升序*

```sql
select did, count(*)
from t_employee
group by did with rollup;
```

limit m,n：

- n：表示最多该页显示几行
- m：表示从第几行开始取记录，第一个行的索引是0 
- m = (page-1)*n，page表示第几页

### 10.1 select 中嵌套

```sql
select ename,
       (select avg(salary) from t_employee) as 平均薪资
from t_employee;
```

### 10.2 where/having 中嵌套

```sql
-- 单列单值：用比较运算符
where salary = (select max(salary) from t_employee)

-- 单列多值：用 in / not in
where did in (select did from t_employee where ename='白露')

-- 单列多值 + 比较：用 any / all / in / exists
where salary > all(select salary from t_employee where ename in (...))
【注意：NOT IN 的 NULL 陷阱（重要！）】

-- 如果子查询结果里有 NULL，not in 会返回空结果！
where did not in (select did from t_employee where ...)
原因：not in 等价于 != any，而 任何值 != NULL 结果是 NULL，不是 true。
-- 解决
-- 方法 1：排除 NULL
where did not in (select did from t_employee where did is not null)
-- 方法 2：用 not exists 替代
where not exists(select 1 from t_employee e where e.did = outer.did)
```

### 10.3 exists 型

```sql
-- 子查询返回至少一行，exists 为 true
select * from t_department
where exists(select * from t_employee where t_employee.did = t_department.did);
```

### 10.4 from 中嵌套（临时表）

```sql
select *
from (
    select did, avg(salary) as pingjun
    from t_employee
    group by did
) temp
where temp.pingjun > 10000;
```

### 10.5 update/delete 中嵌套

```sql
-- update
update t_employee
set salary = salary * 1.5
where did = (select did from t_department where dname='测试部');

-- delete
delete from t_employee
where did = (select did from t_department where dname='测试部');
```

**注意**：update/delete 的表和子查询的表是同一张时，需要再套一层临时表。

```sql
-- 嵌套一层结果集。
update t_employee set 
salary=(select salary from (select salary from t_employee where ename = '孙红梅') temp)
where ename ='李冰冰';
```



### 10.6使用子查询复制表结构和数据

#### 	1.复制表结构

```sql
-- 仅复制表结构，可以用create语句
create table department like t_department;
```

#### 	2.复制一条或多条记录

```sql
-- 使用insert语句+子查询，复制数据，此时insert不用写values
insert into department select * from t_department where did<=3;
```

#### 	3.同时复制表结构和记录

```sql
-- 同时复制表结构+数据
create table d_department as (select * from t_department);
-- 如果select后面是部分字段，复制的新表就只有这一部分字段
```

### 10.7 CTE 通用表达式

```sql
with [recursive]
cte_name [(字段名)] as (子查询),
cte_name2 as (子查询)

recursive：表示通用表达式中需要递归引用自己，不写则不递归引用
-- 例
with
emp as (select eid,ename,salary,`mid` from t_employee where salary<9000),
mgr(meid,mename,msalary) as (select eid,ename,salary from t_employee)
```

**递归 CTE**：

```sql
with recursive 
cte as (
    select eid, ename, mid from emp where eid=21
    union all
    select emp.eid, emp.ename, emp.mid
    from emp join cte on emp.eid = cte.mid
)
select * from cte;
```

---

## 11. 约束

*四个主要约束：*

| 约束         | 关键字        | 对应的完整性            | 作用                       |
| ------------ | ------------- | ----------------------- | -------------------------- |
| **主键约束** | `primary key` | 实体完整性              | 唯一且非空，一行一标识     |
| **外键约束** | `foreign key` | 引用完整性              | 子表引用主表，保证关联正确 |
| **唯一约束** | `unique key`  | 实体完整性 / 用户自定义 | 值唯一，允许 NULL          |
| **非空约束** | `not null`    | 域完整性                | 字段不能为 NULL            |

### 11.1 约束类型

| 类型   | 关键字                                                       | 级别       |
| :----- | :----------------------------------------------------------- | :--------- |
| 主键   | `primary key`                                                | 表级       |
| 外键   | `foreign key`                                                | 表级       |
| 唯一键 | `unique key`【允许 NULL：多个 NULL 可以共存（和主键最大区别）】 | 表级       |
| 非空   | `not null`                                                   | 列级       |
| 检查   | `check`   例如：check (age between 18 and 60)                | 表级       |
| 默认值 | `default`                                                    | 列级       |
| 自增   | `auto_increment`                                             | 键字段属性 |

- 表级约束（看其他行）：键约束，检查约束
- 列级约束（只看当前数据）：非空约束，默认值约束

所有的表级约束都可以在“information_schema.table_constraints”表中查看。

```sql
select * from information_schema.table_constraints where table_name = '表名';
```

*键约束会自动创建索引，提高查询效率。约束是逻辑概念，不占用物理空间。索引是物理概念，占用物理空间*

### 11.2 非空约束

```sql
-- 建表时
create table 表名(字段名 数据类型 not null);

-- 建表后添加
alter table 表名 modify 字段名 数据类型 not null;

-- 删除
alter table 表名 modify 字段名 数据类型;
```

### 11.3 唯一键约束

```sql
-- 建表时
create table 表名(
    字段名 数据类型 unique key,
    unique key(字段名1, 字段名2)   -- 复合唯一
);

-- 建表后添加
alter table 表名 add unique (字段名);

-- 删除（通过删除索引）索引名默认是字段名，复合唯一默认是第一个字段名
alter table 表名 drop index 索引名;
-- 查看表的索引信息
show index from 表名; 
```

**特点**：允许 NULL，一个表可有多个唯一键。

### 11.4 主键约束

```sql
-- 建表时
create table 表名(
    字段名 数据类型 primary key,
    primary key(字段名1, 字段名2)   -- 复合主键
);

-- 建表后添加
alter table 表名 add primary key(字段列表);

-- 删除
alter table 表名 drop primary key;
```

**特点**：唯一且非空，一个表只能有一个主键。

InnoDB 的主键是**聚簇索引**，数据行直接存储在 B+ 树叶子节点上

### 11.5 自增约束

```sql
-- 建表时
create table 表名(字段名 数据类型 primary key auto_increment);

-- 建表后添加
alter table 表名 modify 字段名 数据类型 auto_increment;

-- 删除
alter table 表名 modify 字段名 数据类型;

-- 修改自增值
alter table 表名 auto_increment = 8;
```

**特点**：
- 一个表只能有一个自增字段。
- 自增字段必须是 key 字段。
- 自增字段必须是数值类型。
- 赋值 `0` 或 `null` 时自增，赋值具体值时直接使用。

### 11.6 默认值约束

```sql
-- 建表时
create table 表名(字段名 数据类型 default 默认值);

-- 建表后添加
alter table 表名 modify 字段名 数据类型 default 默认值;

-- 删除
alter table 表名 modify 字段名 数据类型;
```

### 11.7 检查约束（MySQL 8.0.16+）

```sql
-- 建表时
create table 表名(
    字段名 数据类型 check(条件),
    check(条件) enforced   -- 表级检查
);

-- 建表后添加
alter table 表名 add check(条件);

-- 删除
alter table 表名 drop check 检查约束名;
```

### 11.8 外键约束

**外键约束会影响性能，效率，所以很多人不愿意加外键约束。**

- 主表（父表）：被引用的表，被参考的表
- 从表（子表）：引用别人的表，参考别人的表

```sql
-- 建表时（先建主表，再建从表）
create table 从表(
    字段名 数据类型,
    foreign key (从表字段) references 主表(被参考字段)
);

-- 建表后添加
alter table 从表 add foreign key (从表字段) references 主表(被引用字段);

-- 删除
alter table 从表 drop foreign key 外键约束名;
alter table 从表 drop index 索引名;
```

**外键等级**：

| 等级                     | 说明                                                        |
| :----------------------- | :---------------------------------------------------------- |
| `cascade`                | 父表 update/delete 时，同步子表                             |
| `set null`               | 父表 update/delete 时，子表字段设为 NULL（不能有 not null） |
| `no action` / `restrict` | 子表有匹配记录时，禁止父表操作（默认）                      |

```sql
foreign key (departmentid) references dept(did)
on update cascade on delete set null
```

**查看约束**：

```sql
select * from information_schema.table_constraints where table_name='表名';
show index from 表名;
```

---

## 12. 事务

### 12.1 ACID

| 属性                   | 说明                                                     |
| :--------------------- | :------------------------------------------------------- |
| **原子性 Atomicity**   | 事务不可再分，最小单元。【要么全做，要么全不做】         |
| **一致性 Consistency** | 数据库从一个“合法状态”变到另一个“合法状态”。【总数守恒】 |
| **隔离性 Isolation**   | 并发的事务之间互相隔离，互不干扰【互不干扰】             |
| **持久性 Durability**  | 一旦 commit 提交，才是永久修改。【提交即永久】           |

### 12.2 事务操作

**【 修改变量影响的是当前整个连接 】**

```sql
-- 开启手动提交模式【下面的SQL都需要手动提交】
set autocommit = false;   -- 或 0
-- ... 操作 ...
commit;                   -- 提交
rollback;                 -- 回滚
set autocommit = true;    -- 或 1 。恢复自动提交

-- 自动提交模式下开启事务
start transaction;        --开始事务
-- ... 操作 ...
commit;   -- 或 rollback;
```

**注意**：DDL（create/drop/alter）和 truncate **不支持事务**，只有 insert/update/delete 支持。

### 12.3 并发问题

| 问题           | 说明                         |
| :------------- | :--------------------------- |
| **脏读**       | 读到其他事务未提交的数据     |
| **不可重复读** | 同一事务两次读同一记录不一致 |
| **幻读**       | 同一事务两次读记录数不一致   |

### 12.4 隔离级别

隔离级别越高, 数据一致性就越好, 但并发性越弱。

| 级别                            | 脏读 | 不可重复读 | 幻读                 |
| :------------------------------ | :--- | :--------- | :------------------- |
| `read-uncommitted`【RU】        | ✅    | ✅          | ✅                    |
| `read-committed`【RC】          | ❌    | ✅          | ✅                    |
| `repeatable-read`（默认）【RR】 | ❌    | ❌          | ❌（MySQL MVCC 避免） |
| `serializable`【串行化】        | ❌    | ❌          | ❌                    |

```sql
-- 修改隔离级别
set transaction_isolation = '隔离级别';
-- 【只读系统变量，修改前提】
-- 方式一：设置当前会话
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- 方式二：设置全局（影响新连接）
SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- 修改当前会话的隔离级别
set session transaction isolation level read committed;
-- 修改全局隔离级别（影响新连接）
set global transaction isolation level read committed;

-- 查看隔离级别
select @@transaction_isolation;
```

### 12.5保存点 SAVEPOINT

```sql
start transaction;
insert into user(name) values('张三');
savepoint sp1;
insert into user(name) values('李四');
rollback to sp1;      -- 只回滚李四，张三保留
commit;               -- 提交张三
```

---

## 13. 用户与权限

 登录验证：用户主机IP地址（客户端主机的IP，而非MySQL服务器的IP） + 用户名 + 密码三重验证。

### 13.1 用户管理

```sql
-- 创建用户
create user '用户名'@'主机' identified by '密码';

-- 修改密码
set password for '用户名'@'主机' = '新密码';

-- 删除用户
drop user '用户名'@'主机';
```

**主机 IP 说明**：
- `192.168.1.25`：指定 IP
- `192.168.1.%`：指定网段
- `%`：任意 IP

### 13.2 权限管理

```sql
-- 授权
grant 权限 on 库.表 to '用户名'@'主机';

-- 撤销权限
revoke 权限 on 库.表 from '用户名'@'主机';

-- 刷新权限
flush privileges;
```

**权限级别**：全局 > 数据库 > 表 > 字段 > 存储过程/函数

#### 常见全局权限

| 权限             | 说明                        |
| ---------------- | --------------------------- |
| `all privileges` | 所有权限                    |
| `select`         | 查询                        |
| `insert`         | 插入                        |
| `update`         | 更新                        |
| `delete`         | 删除                        |
| `create`         | 创建库/表                   |
| `drop`           | 删除库/表                   |
| `grant option`   | **能把自己权限授予别人**    |
| `super`          | 高级管理权限（kill 线程等） |
| `reload`         | 执行 flush 操作             |

```sql
-- 全局
-- 示例：授予所有权限
grant all privileges on *.* to 'admin'@'%';
-- 示例：只授予查询权限
grant select on *.* to 'readonly'@'%';

--数据库
-- 只允许查询 atguigu 库
grant select on atguigu.* to 'reader'@'localhost';
-- 允许操作 shop 库所有表
grant all privileges on shop.* to 'shop_admin'@'%';

-- 表
-- 只能查 t_employee 表
grant select on atguigu.t_employee to 'viewer'@'localhost';
-- 只能改 t_department 表
grant update on atguigu.t_department to 'editor'@'localhost';

-- 字段
-- 只能查员工的姓名和电话，不能查薪资
grant select(ename, tel) on atguigu.t_employee to 'contact'@'%';
-- 只能改员工的地址
grant update(address) on atguigu.t_employee to 'updater'@'%';

--存储过程（procedure）或函数（function）。
-- 允许执行某个存储过程
grant execute on procedure atguigu.p_add_employee to 'hr'@'%';
```

### 13.3 MySQL 8 忘记 root 密码

```bash
# 1. 停止 MySQL
net stop mysql80

# 2. 新建 root_newpasswd.txt，内容：
ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';

# 3. 初始化启动（按 Ctrl+C 结束）
mysqld --defaults-file="C:/ProgramData/MySQL/MySQL Server 8.0/my.ini" --init-file="D:/root_newpasswd.txt"

# 4. 重启 MySQL，用新密码登录
```

### 13.4 可视化工具连接 MySQL 8 报错

```sql
-- Authentication plugin 'caching_sha2_password' cannot be loaded
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';
FLUSH PRIVILEGES;
```

---

## 14. 核心定义与范式

### 14.1 数据完整性

| 类型                 | 说明                               |
| :------------------- | :--------------------------------- |
| **实体完整性**       | 同一表不能有完全相同无法区分的记录 |
| **域完整性**         | 字段值范围限制（如年龄 0-120）     |
| **引用完整性**       | 外键引用必须在主表中存在           |
| **用户自定义完整性** | 用户名唯一、密码非空等             |

### 14.2 键约束 vs 索引

| 概念     | 说明                             |
| :------- | :------------------------------- |
| **约束** | 逻辑概念，不占物理空间           |
| **索引** | 物理概念，占物理空间             |
| 关系     | 键约束自动创建索引，提高查询效率 |

### 14.3 三大范式（面试常考）

| 范式    | 定义                           | 说明           |
| :------ | :----------------------------- | :------------- |
| **1NF** | 字段不可再分                   | 每列都是原子值 |
| **2NF** | 非主键字段完全依赖主键         | 消除部分依赖   |
| **3NF** | 非主键字段不依赖其他非主键字段 | 消除传递依赖   |

**反范式**：为性能考虑，适当冗余字段，减少 JOIN。

### 14.4 存储引擎

| 引擎                     | 特点                     |
| :----------------------- | :----------------------- |
| **InnoDB**（默认，5.5+） | 支持事务、外键、行锁     |
| **MyISAM**               | 不支持事务、表锁、查询快 |
| **MEMORY**               | 内存表，速度快，重启丢失 |
| **ARCHIVE**              | 归档存储，压缩比高       |

### 14.5 MySQL 8 新特性

| 特性                               | 说明                                 |
| :--------------------------------- | :----------------------------------- |
| 系统表全部为 InnoDB                | 数据字典存储在 mysql.ibd             |
| 默认字符集 utf8mb4                 | 支持 emoji                           |
| 默认认证插件 caching_sha2_password | 替代 mysql_native_password           |
| 角色（Role）                       | 权限集合，统一授权                   |
| 密码过期                           | password_expired / password_lifetime |
| 窗口函数                           | row_number / rank / dense_rank 等    |
| CTE 通用表达式                     | with ... as (...)                    |
| 检查约束生效                       | MySQL 8.0.16+                        |

查看系统表类型：

```sql
SELECT DISTINCT(ENGINE) FROM information_schema.tables;
```

使用SHOW语句查看MySQL8.0版本数据库的默认编码：

```sql
SHOW VARIABLES LIKE 'character_set_database';
```

使用SHOW语句查看utf8mb4字符集的部分校对规则如下：

```sql
SHOW COLLATION LIKE 'utf8mb4_0900%';
```

## 15.Python连接MySQL

### 1. **安装依赖包**

```python
conda install pymysql
```

### 2. **代码**

```python
"""
    该案例演示了python操作MySQL数据库
"""
import pymysql
# 获取连接
def get_connection():
    try:
        conn = pymysql.connect(
            host='192.168.10.150',
            port=3306,
            user='root',
            password='123456',
            database='atguigu',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except:
        print("获取连接的时候发生了异常")

# 从数据库表中查询数据
def select_data(conn):
    # 创建游标对象
    my_cursor = conn.cursor()

    # 执行sql语句
    sql = "select * from t_department"
    my_cursor.execute(sql)

    # 获取查询结果
    results = my_cursor.fetchall()

    for row in results:
        print(row)
    my_cursor.close()

def insert_data(conn):
    my_c = conn.cursor()
    sql = "insert into t_department values (10,'test','testtest')"
    my_c.execute(sql)
    # 提交事务
    conn.commit()
    my_c.close()

def delete_data(conn):
    my_c = conn.cursor()
    sql = "delete from t_department where did=10"
    my_c.execute(sql)
    # 提交事务
    conn.commit()
    my_c.close()

def update_data(conn):
    my_c = conn.cursor()
    sql = "update t_department set dname='dev' where did=10"
    my_c.execute(sql)
    # 提交事务
    conn.commit()
    my_c.close()

if __name__ == '__main__':
    conn = get_connection()
    # insert_data(conn)
    # update_data(conn)
    delete_data(conn)
    select_data(conn)
    conn.close()
```

#### 阶段一：简单脚本 / 小工具 / 学习

- **推荐**：`PyMySQL` + `DBUtils` 连接池
- **理由**：保持简单，同时通过连接池解决性能痛点。
- **代码示例**：

```python
"""
PyMySQL + DBUtils 连接池：CRUD 完整示例
"""
import pymysql
from dbutils.pooled_db import PooledDB
# ========== 1. 创建连接池（全局唯一） ==========
POOL = PooledDB(
    creator=pymysql,        # 底层驱动
    maxconnections=10,      # 最大连接数
    mincached=2,            # 初始化时创建的空闲连接数
    maxcached=5,            # 连接池中最多空闲连接数
    blocking=True,          # 连接池满时是否阻塞等待
    host='localhost',
    port=3306,
    user='root',
    password='admin',
    database='atguigu',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
# ========== 2. 获取连接 ==========
def get_conn():
    """从连接池获取连接"""
    return POOL.connection()
# ========== 3. 查询（Read） ==========
def select_all():
    """查询所有部门"""
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select * from t_department")
            return cursor.fetchall()
    finally:
        conn.close()   # 注意：这里是归还给连接池，不是真的关闭

def select_by_id(did):
    """按 ID 查询"""
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "select * from t_department where did = %s",
                (did,)
            )
            return cursor.fetchone()
    finally:
        conn.close()
# ========== 4. 新增（Create） ==========
def insert(did, dname, note):
    """新增部门"""
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "insert into t_department (did, dname, note) values (%s, %s, %s)",
                (did, dname, note)
            )
        conn.commit()
        print(f"✅ 新增成功：did={did}")
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"❌ 新增失败：{e}")
    finally:
        conn.close()
# ========== 5. 修改（Update） ==========
def update(did, dname):
    """修改部门名"""
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "update t_department set dname = %s where did = %s",
                (dname, did)
            )
        conn.commit()
        print(f"✅ 修改成功：did={did}")
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"❌ 修改失败：{e}")
    finally:
        conn.close()
# ========== 6. 删除（Delete） ==========
def delete(did):
    """删除部门"""
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "delete from t_department where did = %s",
                (did,)
            )
        conn.commit()
        print(f"✅ 删除成功：did={did}")
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"❌ 删除失败：{e}")
    finally:
        conn.close()

if __name__ == '__main__':
    # 增
    insert(10, 'test', 'testtest')
    insert(11, 'dev', 'devteam')
    # 查
    print("\n--- 查询全部 ---")
    for row in select_all():
        print(row)
    # 改
    update(10, 'test-v2')
    # 查单个
    print("\n--- 查询 did=10 ---")
    print(select_by_id(10))
    # 删
    delete(10)
    delete(11)
    # 再查
    print("\n--- 删除后全部 ---")
    for row in select_all():
        print(row)
```

- **关键参数建议**：`maxconnections` 建议设为 `10-20`，`mincached` 设为 `2-5`。

#### 阶段二：中型 Web 项目 / 追求开发效率

- **推荐**：`SQLAlchemy` ORM + `mysqlclient` (同步) 或 `asyncmy` (异步)
- **理由**：用 ORM 提升开发效率，用 `mysqlclient`/`asyncmy` 保证性能，用连接池管理连接。
- **代码示例 (同步 SQLAlchemy)**：

```python
# pip install sqlalchemy mysqlclient
# 或者 pip install sqlalchemy pymysql
"""
SQLAlchemy ORM 同步版：CRUD 完整示例
"""
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker
# ========== 1. 创建引擎（自带连接池） ==========
engine = create_engine(
    "mysql+pymysql://root:admin@localhost:3306/atguigu",  # 驱动可以换 mysqlclient
    pool_size=10,          # 连接池大小
    max_overflow=20,       # 池满后允许临时连接数
    pool_recycle=3600,     # 连接回收时间（秒）
    pool_pre_ping=True,    # 取连接前 ping 一次
    echo=False             # True 会打印 SQL，调试用
)
# ========== 2. 定义基类 ==========
Base = declarative_base()
# ========== 3. 定义模型（对应表） ==========
class Department(Base):
    __tablename__ = 't_department'

    did = Column(Integer, primary_key=True)
    dname = Column(String(50))
    note = Column(String(100))

    def __repr__(self):
        return f"<Department(did={self.did}, dname={self.dname}, note={self.note})>"
# ========== 4. 创建 Session 工厂 ==========
Session = sessionmaker(bind=engine)
def get_session():
    """获取一个会话"""
    return Session()
# ========== 5. 查询（Read） ==========
def select_all():
    """查询所有部门"""
    with get_session() as session:
        stmt = select(Department)
        return session.execute(stmt).scalars().all()
def select_by_id(did):
    """按 ID 查询"""
    with get_session() as session:
        return session.get(Department, did)
# ========== 6. 新增（Create） ==========
def insert(did, dname, note):
    """新增部门"""
    session = get_session()
    try:
        dept = Department(did=did, dname=dname, note=note)
        session.add(dept)
        session.commit()
        print(f"✅ 新增成功：did={did}")
    except Exception as e:
        session.rollback()
        print(f"❌ 新增失败：{e}")
    finally:
        session.close()
# ========== 7. 修改（Update） ==========
def update(did, dname):
    """修改部门名"""
    session = get_session()
    try:
        dept = session.get(Department, did)
        if dept:
            dept.dname = dname
            session.commit()
            print(f"✅ 修改成功：did={did}")
        else:
            print(f"⚠️ 部门 {did} 不存在")
    except Exception as e:
        session.rollback()
        print(f"❌ 修改失败：{e}")
    finally:
        session.close()
# ========== 8. 删除（Delete） ==========
def delete(did):
    """删除部门"""
    session = get_session()
    try:
        dept = session.get(Department, did)
        if dept:
            session.delete(dept)
            session.commit()
            print(f"✅ 删除成功：did={did}")
        else:
            print(f"⚠️ 部门 {did} 不存在")
    except Exception as e:
        session.rollback()
        print(f"❌ 删除失败：{e}")
    finally:
        session.close()
if __name__ == '__main__':
    # 增
    insert(10, 'test', 'testtest')
    insert(11, 'dev', 'devteam')
    # 查
    print("\n--- 查询全部 ---")
    for dept in select_all():
        print(dept)
    # 改
    update(10, 'test-v2')
    # 查单个
    print("\n--- 查询 did=10 ---")
    print(select_by_id(10))
    # 删
    delete(10)
    delete(11)
    # 再查
    print("\n--- 删除后全部 ---")
    for dept in select_all():
        print(dept)
```

- `pool_size` 和 `max_overflow` 是最关键的参数，建议根据并发量调整。

#### 阶段三：异步高并发 API / FastAPI 项目

- **推荐**：`SQLAlchemy` (async) + `asyncmy` 或 `aiomysql`
- **理由**：充分利用 `asyncio` 的非阻塞特性，大幅提升 I/O 密集型服务的并发能力。
- **代码示例 (异步 SQLAlchemy)**：

```python
# pip install sqlalchemy asyncmy
# 或者 pip install sqlalchemy aiomysql
"""
SQLAlchemy ORM 异步版：CRUD 完整示例
"""
import asyncio
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# mysql+asyncmy://root:admin@localhost:3306/atguigu
# └─┬─┘ └──┬──┘   └┬─┘ └─┬─┘ └───┬───┘ └─┬─┘ └──┬──┘
#   │      │       │     │       │       │      │
#  数据库  驱动    用户名 密码      主机     端口    库名
# asyncmy	性能最强，Cython 实现，推荐
# ========== 1. 创建异步引擎 ==========
async_engine = create_async_engine(
    "mysql+asyncmy://root:admin@localhost:3306/atguigu",
    pool_size=5,            # 异步池可以设大一点
    max_overflow=10,        # 溢出连接数
    pool_recycle=3600,      # 连接回收时间
    pool_pre_ping=True,     # 连接预检，每次从池里取连接前，先 ping 一下，确保连接是活的。
    echo=False              # SQL 日志开关，是否把执行的 SQL 打印到控制台。
)
# ========== 2. 定义基类 ==========
Base = declarative_base()
# ========== 3. 定义模型 ==========
# 表 → 类（t_department → Department）
# 行 → 对象（一行记录 → 一个 Department 实例）
# 列 → 属性（did、dname、note）
class Department(Base):
    # 对应的数据库名字【不写的话默认对应数据库名为类名：即department】
    __tablename__ = 't_department'
    # did           属性名（对应表的字段名）
    # Column(...)   声明这是一个表字段
    did = Column(Integer, primary_key=True)
    dname = Column(String(50))
    note = Column(String(100))
    def __repr__(self):
        return f"<Department(did={self.did}, dname={self.dname}, note={self.note})>"
# ========== 4. 创建异步 Session 工厂 ==========
# async_sessionmaker 预绑定 engine 和参数，之后直接调用生成 Session。
# 用法
    # 创建工厂
    #     AsyncSessionLocal = async_sessionmaker(async_engine, ...)
    # 用工厂生成 Session
    #     async with AsyncSessionLocal() as session:
AsyncSessionLocal = async_sessionmaker(
    async_engine,  #用哪个引擎连数据库 bind=async_engine
    class_=AsyncSession, #指定生成哪种 Session 类，默认生成同步 Session
    expire_on_commit=False   # commit后对象是否过期，方便继续用对象
)
async def get_session():
    """获取一个异步会话（上下文管理器）"""
    async with AsyncSessionLocal() as session:  #异步上下文管理器，确保 Session 用完自动关闭。
        yield session #把 Session 交给调用方，用完后自动关闭。
# ========== 5. 查询（Read） ==========
async def select_all():
    """查询所有部门"""
    async with AsyncSessionLocal() as session:
        # 查询语句
        stmt = select(Department)
        # 异步执行 SQL，返回一个 Result 对象。
        result = await session.execute(stmt)
        # result	原始结果集（类似元组的集合）
        # .scalars()	取第一列（对于 select(Department)，就是 Department 对象）
        # .all()	转成列表，返回所有行
        return result.scalars().all()
async def select_by_id(did):
    """按 ID 查询"""
    async with AsyncSessionLocal() as session:
        # 按主键查询单条记录。
        return await session.get(Department, did)
# ========== 6. 新增（Create） ==========
async def insert(did, dname, note):
    """新增部门"""
    async with AsyncSessionLocal() as session:
        try:
            # 创建一个 ORM 对象（内存里，还没进库）
            dept = Department(did=did, dname=dname, note=note)
            session.add(dept)
            await session.commit()
            print(f"✅ 新增成功：did={did}")
        except Exception as e:
            await session.rollback()
            print(f"❌ 新增失败：{e}")
# ========== 7. 修改（Update） ==========
async def update(did, dname):
    """修改部门名"""
    async with AsyncSessionLocal() as session:
        try:
            dept = await session.get(Department, did)
            if dept:
                dept.dname = dname
                await session.commit()
                print(f"✅ 修改成功：did={did}")
            else:
                print(f"⚠️ 部门 {did} 不存在")
        except Exception as e:
            await session.rollback()
            print(f"❌ 修改失败：{e}")
# ========== 8. 删除（Delete） ==========
async def delete(did):
    """删除部门"""
    async with AsyncSessionLocal() as session:
        try:
            dept = await session.get(Department, did)
            if dept:
                await session.delete(dept)
                await session.commit()
                print(f"✅ 删除成功：did={did}")
            else:
                print(f"⚠️ 部门 {did} 不存在")
        except Exception as e:
            await session.rollback()
            print(f"❌ 删除失败：{e}")
# ========== 9. 主流程 ==========
async def main():
    # 增
    await insert(10, 'test', 'testtest')
    await insert(11, 'dev', 'devteam')
    # 查
    print("\n--- 查询全部 ---")
    for dept in await select_all():
        print(dept)
    # 改
    await update(10, 'test-v2')
    # 查单个
    print("\n--- 查询 did=10 ---")
    print(await select_by_id(10))
    # 删
    await delete(10)
    await delete(11)
    # 再查
    print("\n--- 删除后全部 ---")
    for dept in await select_all():
        print(dept)
if __name__ == '__main__':
    asyncio.run(main())
    # 启动异步事件循环，执行 main() 协程。
    # 作用：创建事件循环、运行协程、关闭事件循环，一站式搞定。
    # 执行步骤：
        # 创建一个新的事件循环（EventLoop）。
        # 把main()协程注册到事件循环。
        # 运行main()，直到它返回。
        # 关闭事件循环。
```

- 在 FastAPI 中，通常会像上面这样通过依赖注入来管理数据库会话的生命周期。

---

*本文档为速查手册，仅保留核心代码与关键定义。*


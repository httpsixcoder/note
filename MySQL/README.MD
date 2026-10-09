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

---

## 1. 基础概念

| 概念     | 说明                                                      |
| :------- | :-------------------------------------------------------- |
| DB       | Database，存储数据的地方                                  |
| DBMS     | 数据库管理系统（MySQL、Oracle、SqlServer）                |
| SQL      | 结构化查询语言，操作数据库的通用语言                      |
| 关系型   | 二维表 + SQL + 强 ACID（MySQL、PostgreSQL、Oracle）       |
| 非关系型 | 键值/文档/图 + 高扩展 + 最终一致（Redis、MongoDB、Neo4j） |

**表关系**：一对一、一对多（外键）、多对多（中间表）。

---

## 2. SQL 分类

| 类型     | 全称                       | 语句                    |
| :------- | :------------------------- | :---------------------- |
| **DDL**  | Data Define Language       | create、alter、drop     |
| **DML**  | Data Manipulation Language | insert、update、delete  |
| **DQL**  | Data Query Language        | select                  |
| **DCL**  | Data Control Language      | grant、commit、rollback |
| **其他** | 命令                       | use、show、set          |

**语法规范**：
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
desc 表名;

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

-- 指定字段插入
insert into 表名(字段1,字段2) values(值1,值2),(值1,值2);

-- 复制数据
insert into 表名 (select * from 旧表 where 条件);
```

### 4.2 删除

```sql
-- 条件删除
delete from 表名 where 条件;

-- 删除所有（表结构保留，可回滚）
delete from 表名;

-- 截断表（表结构保留，不可回滚，效率高）
truncate 表名;
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
```

### 5.2 别名与去重

```sql
select 字段名1 as "别名1", 字段名2 as "别名2" from 表名 as 表别名;

-- 去重
select distinct 字段列表 from 表名;
```

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

| 运算符       | 说明                     |
| :----------- | :----------------------- |
| `+`          | 求和（无字符串拼接功能） |
| `-`          | 减                       |
| `*`          | 乘                       |
| `/`          | 除                       |
| `div`        | 整除                     |
| `%` 或 `mod` | 取余                     |

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
| `xor`         | 异或 |

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

---

## 7. 数据类型

### 7.1 数值类型

| 类型                       | 说明                       |
| :------------------------- | :------------------------- |
| `int`                      | 整数                       |
| `int(M) unsigned zerofill` | 显示宽度 M，无符号，零填充 |
| `float` / `double`         | 浮点数                     |
| `decimal(M,D)`             | 定点数，精度高，适合货币   |
| `bit(M)`                   | 位类型，1~64 位            |

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

| 类型        | 格式                | 说明                     |
| :---------- | :------------------ | :----------------------- |
| `year`      | YYYY                | 1901~2155                |
| `date`      | YYYY-MM-DD          | 年月日                   |
| `time`      | HH:MM:SS            | 时分秒                   |
| `datetime`  | YYYY-MM-DD HH:MM:SS | 年月日时分秒             |
| `timestamp` | YYYY-MM-DD HH:MM:SS | 时区转换，范围 1970~2038 |

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

| 函数                                          | 说明          |
| :-------------------------------------------- | :------------ |
| `curdate()` / `current_date()`                | 当前日期      |
| `curtime()` / `current_time()`                | 当前时间      |
| `now()` / `sysdate()` / `current_timestamp()` | 当前日期时间  |
| `utc_date()` / `utc_time()`                   | UTC 日期/时间 |
| `unix_timestamp(date)`                        | UNIX 时间戳   |
| `year/month/day/hour/minute/second(date)`     | 取各部分      |
| `extract(type from date)`                     | 提取指定部分  |
| `datediff(date1,date2)`                       | 日期间隔天数  |
| `timediff(time1,time2)`                       | 时间间隔      |
| `date_add/date_sub(date, interval expr type)` | 日期加减      |
| `date_format(datetime, fmt)`                  | 格式化        |
| `str_to_date(str, fmt)`                       | 解析为日期    |
| `get_format(val_type, format_type)`           | 返回显示格式  |

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

| 函数                                         | 说明                 |
| :------------------------------------------- | :------------------- |
| `if(a,x,y)`                                  | a 为真返回 x，否则 y |
| `ifnull(x,y)`                                | x 非空返回 x，否则 y |
| `case when 条件 then 结果 ... else 结果 end` | 多条件判断           |
| `case 表达式 when 值 then 结果 ... end`      | 等值判断             |

### 8.7 分组函数（聚合）

| 函数                | 说明      |
| :------------------ | :-------- |
| `avg(x)`            | 平均值    |
| `sum(x)`            | 求和      |
| `max(x)` / `min(x)` | 最大/最小 |
| `count(x)`          | 计数      |

```sql
select count(*) from t_employee;          -- 统计行数
select count(1) from t_employee;          -- 同上
select count(commission_pct) from t_employee;  -- 忽略 NULL
```

### 8.8 窗口函数

| 函数                              | 说明             |
| :-------------------------------- | :--------------- |
| `row_number()`                    | 顺序编号 1,2,3,4 |
| `rank()`                          | 并列跳过 1,1,3   |
| `dense_rank()`                    | 并列不跳过 1,1,2 |
| `lag()/lead()`                    | 前/后偏移值      |
| `first_value()/last_value()`      | 首/末值          |
| `sum()/avg()/count()/max()/min()` | 窗口聚合         |

```sql
函数名(参数) over(
    [partition by 字段]
    [order by 字段]
    [rows between <start> and <end>]
)
```

**窗口范围**：
- `unbounded preceding`：分区第一行
- `n preceding`：当前行前 n 行
- `current row`：当前行
- `n following`：当前行后 n 行
- `unbounded following`：分区最后一行

---

## 9. 关联查询

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

-- 单列多值 + 比较：用 any / all
where salary > all(select salary from t_employee where ename in (...))
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

### 10.6 CTE 通用表达式

```sql
with [recursive]
cte_name [(字段名)] as (子查询),
cte_name2 as (子查询)
select ... from cte_name;
```

**递归 CTE**：

```sql
with recursive cte as (
    select eid, ename, mid from emp where eid=21
    union all
    select emp.eid, emp.ename, emp.mid
    from emp join cte on emp.eid = cte.mid
)
select * from cte;
```

---

## 11. 约束

### 11.1 约束类型

| 类型   | 关键字           | 级别       |
| :----- | :--------------- | :--------- |
| 主键   | `primary key`    | 表级       |
| 外键   | `foreign key`    | 表级       |
| 唯一键 | `unique key`     | 表级       |
| 非空   | `not null`       | 列级       |
| 检查   | `check`          | 表级       |
| 默认值 | `default`        | 列级       |
| 自增   | `auto_increment` | 键字段属性 |

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

-- 删除（通过删除索引）
alter table 表名 drop index 索引名;
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

| 属性                   | 说明                             |
| :--------------------- | :------------------------------- |
| **原子性 Atomicity**   | 要么都发生，要么都不发生         |
| **一致性 Consistency** | 从一个一致状态变到另一个一致状态 |
| **隔离性 Isolation**   | 事务之间互不干扰                 |
| **持久性 Durability**  | 提交后永久保存                   |

### 12.2 事务操作

```sql
-- 手动提交模式
set autocommit = false;   -- 或 0
-- ... 操作 ...
commit;                   -- 提交
rollback;                 -- 回滚
set autocommit = true;    -- 恢复自动提交

-- 自动提交模式下开启事务
start transaction;
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

| 级别                      | 脏读 | 不可重复读 | 幻读                 |
| :------------------------ | :--- | :--------- | :------------------- |
| `read-uncommitted`        | ✅    | ✅          | ✅                    |
| `read-committed`          | ❌    | ✅          | ✅                    |
| `repeatable-read`（默认） | ❌    | ❌          | ❌（MySQL MVCC 避免） |
| `serializable`            | ❌    | ❌          | ❌                    |

```sql
-- 修改隔离级别
set transaction_isolation = '隔离级别';

-- 查看隔离级别
select @@transaction_isolation;
```

---

## 13. 用户与权限

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

### 13.3 MySQL 8 忘记 root 密码

```bash
# 1. 停止 MySQL
net stop mysql80

# 2. 新建 root_newpasswd.txt，内容：
ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';

# 3. 初始化启动（按 Ctrl+C 结束）
mysqld --defaults-file="MySQL安装路径\my.ini" --init-file="d:\root_newpasswd.txt"

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

---

*本文档为速查手册，仅保留核心代码与关键定义。完整教程请参考尚硅谷 MySQL 教程。*
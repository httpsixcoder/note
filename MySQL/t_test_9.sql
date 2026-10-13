use atguigu;
-- 在t_employee表中查询员工无故旷工一天扣多少钱
-- 分别使用ceil,floor,round,truncate函数
-- 假设本月工作日总天数是22天
-- 旷工一天扣的钱=salary/22
select ename,
  CEIL(salary / 22),
  FLOOR(salary / 22),
  ROUND(salary / 22),
  TRUNCATE(salary / 22, 2),
  salary / 22
from t_employee;
-- 查询公司平均薪资，并对平均薪资分别
-- 分别使用ceil,floor,round,truncate函数
select CEIL(AVG(salary)),
  FLOOR(AVG(salary)),
  ROUND(AVG(salary)),
  TRUNCATE(AVG(salary), 2),
  AVG(salary)
from t_employee;
-- 在t_employee表中查询员工姓名ename和电话tel
-- 并使用concat函数，concat_ws函数
SELECT ename,
  tel,
  CONCAT(ename, tel),
  CONCAT_WS('-', ename, tel)
from t_employee;
-- 在t_employee表中查询薪资高于15000的男员工姓名
-- 并把姓名处理成 张xx 的样式
-- left(s,n)函数表示取字符串s最左边的n个字符
-- 而rpad(str,len,pad)函数表示在字符串str的右边填充pad使得字符串长度达到len
select RPAD(LEFT(ename, 1), 3, 'x'),
  salary
from t_employee
where gender = '男'
  and salary > 15000;
-- 在t_employee表中查询薪资高于10000的男员工姓名，姓名包含的字符数和占用的字节数
-- 【】
select ename,
  char_length(ename) as 字符数,
  length(ename) as 字节数
from t_employee
where salary > 10000
  and gender = '男';
-- 在t_employee表中查询薪资高于10000的男员工姓名和邮箱email
-- 并把邮箱名 @ 字符之前的字符串截取出来
-- MySQL中substring函数截取字符串，位置从1开始
SELECT ename,
  email,
  SUBSTRING(email, 1, INSTR(email, '@') -1)
from t_employee
where gender = '男'
  and salary > 10000;
-- 获取系统日期。curdate()和current_date()函数都可以获取当前系统日期
SELECT CURDATE();
SELECT CURRENT_DATE();
-- 获取系统时间。curtime()和current_time()函数都可以获取当前系统时间
SELECT CURTIME();
SELECT CURRENT_TIME();
-- 获取系统日期时间值。current_timestamp(),localtime(),sysdate(),now()
SELECT CURRENT_TIME(),
  CURRENT_TIMESTAMP(),
  LOCALTIME(),
  SYSDATE(),
  NOW();
-- 获取UNIX时间戳
select UNIX_TIMESTAMP();
-- 获取具体的时间值，比如年、月、日、时、分、秒
-- year(date),month(date),day(date)
-- hour(time),minute(time),second(time)
select YEAR(NOW()),
  month(NOW()),
  day(NOW()),
  hour(NOW()),
  minute(NOW()),
  second(NOW());
-- 获取日期时间的指定值。extract(type from date/time)函数
SELECT EXTRACT(
    year
    FROM NOW()
  );
SELECT EXTRACT(
    month
    FROM NOW()
  );
SELECT EXTRACT(
    day
    FROM NOW()
  );
-- 查询今天距离员工入职的日期间隔天数
select ename,
  datediff(curdate(), hiredate) as '入职天数'
from t_employee;
-- 在t_employee表中查询本月生日的员工姓名、生日
select ename,
  birthday
from t_employee
where MONTH(now()) = MONTH(birthday);
-- 查询入职时间超过5年的
select ename
from t_employee
where hiredate <= date_sub(curdate(), interval 5 year);
-- 如果薪资大于20000，显示高薪，否则显示正常
SELECT ename,
  IF(salary > 20000, '高薪', '正常')
FROM t_employee;
-- 计算实发工资。实发工资 = 薪资 + 薪资 * 奖金比例
select ename,
  salary *(1 + IFNULL(commission_pct, 0))
from t_employee;
-- 查询员工编号，姓名，薪资，等级，等级根据薪资判断
-- 如果薪资大于20000，显示 羡慕级别
-- 如果薪资15000-20000，显示 努力级别
-- 如果薪资10000-15000，显示 平均级别
-- 如果薪资10000以下，显示 保底级别
select eid,
  ename,
  salary,
  CASE
    WHEN salary > 20000 THEN '羡慕级别'
    WHEN salary > 15000 THEN '努力级别'
    WHEN salary > 10000 THEN '平均级别'
    ELSE '保底级别'
  END '级别'
FROM t_employee;
-- 在t_employee表中查询入职7年以上的员工姓名、工作地点、轮岗的工作地点数量情况
-- 计算工作地点的数量可以转换为求work_place中逗号的数量+1
-- work_place中逗号的数量 = work_place的总字符数 - work_place去掉逗号的字符数
-- 使用replace函数去掉work_place中逗号
SELECT ename,
  address,
  CHAR_LENGTH(work_place) - CHAR_LENGTH(REPLACE(work_place, ',', '')) + 1 '工作轮岗地点数'
from t_employee
where hiredate <= DATE_SUB(NOW(), INTERVAL 7 year);
-- 统计t_employee表的员工的数量
SELECT COUNT(1)
from t_employee;
-- 找出t_employee表中最高的薪资值
SELECT max(salary)
from t_employee;
-- 找出t_employee表中最低的薪资值
SELECT min(salary)
from t_employee;
-- 统计t_employee表中平均薪资值
SELECT avg(salary)
from t_employee;
-- 统计所有人的薪资总和
SELECT sum(salary)
from t_employee;
-- 找出年龄最小、最大的员工的出生日期
SELECT MIN(birthday)
from t_employee;
SELECT MAX(birthday)
from t_employee;
-- 查询最新入职的员工的入职日期
select max(hiredate)
from t_employee;
-- 查询每一个部门的平均薪资
SELECT did,
  avg(salary)
from t_employee
group by did;
-- 在t_employee表中查询薪资在[8000,10000]之间的员工姓名和薪资并给每一行记录编序号
select row_number() over(
    order by salary
  ),
  ename,
  salary
from t_employee
WHERE salary BETWEEN 8000 and 10000;
-- 计算每一个部门的平均薪资与全公司的平均薪资的差值
SELECT did,
  avg(salary) -(
    select avg(salary)
    from t_employee
  )
from t_employee
group by did;
-- 在t_employee表中查询女员工姓名，部门编号，薪资
-- 查询结果按照部门编号分组后在按薪资升序排列
-- 并分别使用row_number()、rank()、dense_rank()三个序号函数给每一行记录编序号
select ename,
  did,
  salary,
  row_number() over(
    partition by did
    order by salary
  ) as rn,
  rank() over(
    partition by did
    order by salary
  ) as rk,
  dense_rank() over(
    partition by did
    order by salary
  ) as dr
from t_employee
where gender = '女';
-- 在t_employee表中查询每个部门最低3个薪资值的女员工姓名，部门编号，薪资值
select *
from (
    select ename,
      did,
      salary,
      ROW_NUMBER() over(
        PARTITION by did
        order by salary
      ) as rn
    from t_employee
    where gender = '女'
  ) n
where n.rn <= 3;
-- 在t_employee表中查询每个部门薪资排名前3的员工姓名，部门编号，薪资值
select *
from (
    select ename,
      did,
      salary,
      dense_rank() over(
        PARTITION by did
        order by salary DESC
      ) as dn
    from t_employee
  ) n
where n.dn <= 3;
-- 在t_employee表中查询全公司薪资排名前3的员工姓名，部门编号，薪资值
SELECT ename,
  did,
  salary
from t_employee
ORDER BY salary desc
LIMIT 3;
-- 查找薪资排名的上一位、下一位、首位、末位
-- 【暂未完全理解】
-- 查找薪资排名的上一位、下一位、首位、末位
select ename,
  salary,
  lag(ename, 1, '-') over(
    order by salary
  ) as 上一位姓名,
  lag(salary, 1, 0) over(
    order by salary
  ) as 上一位薪资,
  lead(ename, 1, '-') over(
    order by salary
  ) as 下一位姓名,
  lead(salary, 1, 0) over(
    order by salary
  ) as 下一位薪资,
  first_value(salary) over(
    order by salary
  ) as 首位薪资,
  last_value(ename) over(
    order by salary rows between unbounded preceding and unbounded following
  ) as 末位姓名
from t_employee;
/*
 
 -- 答案
 use atguigu;
 -- 在t_employee表中查询员工无故旷工一天扣多少钱
 -- 分别使用ceil,floor,round,truncate函数
 -- 假设本月工作日总天数是22天
 -- 旷工一天扣的钱=salary/22
 select
     ename,
     salary/22,
     ceil(salary/22),
     floor(salary/22),
     round(salary/22,2),
     truncate(salary/22,2)
 from t_employee;
 -- 查询公司平均薪资，并对平均薪资分别
 -- 分别使用ceil,floor,round,truncate函数
 select
     avg(salary),
     ceil(avg(salary)),
     floor(avg(salary)),
     round(avg(salary),2),
     truncate(avg(salary),2)
 from t_employee;
 use atguigu;
 -- 在t_employee表中查询员工姓名ename和电话tel
 -- 并使用concat函数，concat_ws函数
 select concat(ename,tel),concat_ws('-',ename,tel) from t_employee;
 -- 在t_employee表中查询薪资高于15000的男员工姓名
 -- 并把姓名处理成 张xx 的样式
 -- left(s,n)函数表示取字符串s最左边的n个字符
 -- 而rpad(str,len,pad)函数表示在字符串str的右边填充pad使得字符串长度达到len
 select rpad(left(ename,1),3,'x'),salary
 from t_employee
 where salary>15000 and gender='男';
 -- 在t_employee表中查询薪资高于10000的男员工姓名，姓名包含的字符数和占用的字节数
 select ename,char_length(ename) as 占用字符数,length(ename) as 占用字节数量
 from t_employee
 where salary>10000 and gender='男';
 -- 在t_employee表中查询薪资高于10000的男员工姓名和邮箱email
 -- 并把邮箱名 @ 字符之前的字符串截取出来
 -- MySQL中substring函数截取字符串，位置从1开始
 select ename,email,substring(email,1,position('@' in email)-1)
 from t_employee
 where salary>10000 and gender='男';
 -- trim()默认是去掉前后空白符
 select trim('    hello   world   ');
 select concat('[',trim('    hello   world   '),']');
 -- 去掉前后的 &
 select trim(both '&' from '&&&&hello   world&&&&');
 select trim(leading '&' from '&&&&hello   world&&&&');
 select trim(trailing '&' from '&&&&hello   world&&&&');
 use atguigu;
 -- 获取系统日期。curdate()和current_date()函数都可以获取当前系统日期
 select curdate(),current_date();
 -- 将日期值 +0
 select curdate()+0;
 -- 获取系统时间。curtime()和current_time()函数都可以获取当前系统时间
 select curtime(),current_time();
 -- 将时间值 +0
 select curtime()+0;
 -- 获取系统日期时间值。current_timestamp(),localtime(),sysdate(),now()
 select current_timestamp(),localtime(),sysdate(),now();
 -- 获取当前UTC（世界标准时间）日期或时间值
 -- 本地时间是根据地球上不同时区所处的位置调整 UTC 得来的
 -- 例如，北京时间比UTC时间晚8个小时
 -- utc_date(),curdate(),utc_time(),curtime()
 select utc_date(),curdate(),utc_time(),curtime();
 -- 获取UNIX时间戳
 select unix_timestamp(),unix_timestamp("2000-1-1");
 -- 获取具体的时间值，比如年、月、日、时、分、秒
 -- year(date),month(date),day(date)
 -- hour(time),minute(time),second(time)
 select year(now()),month(now()),day(now()),
        hour(now()),minute(now()),second(now());
 -- 获取日期时间的指定值。extract(type from date/time)函数
 select extract(year_month from now());
 -- 获取两个日期或时间之间的间隔
 -- datediff(date1,date2) 返回两个日期之间间隔的天数
 -- timediff(time1,time2) 返回两个时间之间间隔的时分秒
 select datediff(now(),"2000-1-1");
 select timediff(now(),"2000-1-1 12:00:00");
 -- 查询今天距离员工入职的日期间隔天数
 select ename,datediff(curdate(),hiredate) from t_employee;
 -- 查询现在距离中午放学还有多少时间
 select timediff("12:00:00",curtime());
 -- 在t_employee表中查询本月生日的员工姓名、生日
 select ename,birthday
 from t_employee
 where month(curdate()) = month(birthday);
 -- 查询入职时间超过5年的
 select ename,hiredate,datediff(curdate(),hiredate) 
 from t_employee
 where datediff(curdate(),hiredate)>365*5;
 
 use atguigu;
 -- 条件判断函数不是筛选记录的函数
 -- 而是根据条件不同显示不同的结果的函数
 -- 如果薪资大于20000，显示高薪，否则显示正常
 select ename,salary,if(salary>20000,'高薪','正常')
 from t_employee;
 -- 计算实发工资。实发工资 = 薪资 + 薪资 * 奖金比例
 select
     ename,
     salary,
     commission_pct,
     salary + salary * commission_pct as 实发工资
 from t_employee;
 -- 如果commission_pct是，计算完结果是NULL
 select
     ename,
     salary,
     commission_pct,
     salary + salary * ifnull(commission_pct,0) as 实发工资
 from t_employee;
 -- 查询员工编号，姓名，薪资，等级，等级根据薪资判断
 -- 如果薪资大于20000，显示 羡慕级别
 -- 如果薪资15000-20000，显示 努力级别
 -- 如果薪资10000-15000，显示 平均级别
 -- 如果薪资10000以下，显示 保底级别
 select eid,ename,salary,
 case
     when salary>20000 then '羡慕级别'
     when salary>15000 then '努力级别'
     when salary>10000 then '平均级别'
     else '保底级别'
 end as "等级"
 from t_employee;  
 -- 在t_employee表中查询入职7年以上的员工姓名、工作地点、轮岗的工作地点数量情况
 -- 计算工作地点的数量可以转换为求work_place中逗号的数量+1
 -- work_place中逗号的数量 = work_place的总字符数 - work_place去掉逗号的字符数
 -- 使用replace函数去掉work_place中逗号
 select work_place,
 char_length(work_place)-char_length(replace(work_place,",",""))+1 as 工作地点数量
 from t_employee;
 
 select ename,work_place,
 case char_length(work_place)-char_length(replace(work_place,",",""))+1
     when 1 then '只在一个地方工作'
     when 2 then '在两个地方来回奔波'
     when 3 then '在三个地方流动'
     else '频繁出差'
 end as "工作地点数量情况"
 from t_employee
 where datediff(curdate(),hiredate)>365*7;
 
 use atguigu;
 -- 统计t_employee表的员工的数量
 select count(*) from t_employee;
 select count(1) from t_employee;
 select count(eid) from t_employee;
 select count(commission_pct) from t_employee;
 /*
 count(*)或count(常量值)：都是统计实际的行数
 count(字段/表达式)：统计时忽略NULL值
 
 -- 找出t_employee表中最高的薪资值
 select max(salary) from t_employee;
 -- 找出t_employee表中最低的薪资值
 select min(salary) from t_employee;
 -- 统计t_employee表中平均薪资值
 select avg(salary) from t_employee;
 -- 统计所有人的薪资总和
 select sum(salary) from t_employee;
 select sum(salary+salary*ifnull(commission_pct,0)) from t_employee;
 -- 找出年龄最小、最大的员工的出生日期
 select min(birthday),max(birthday) from t_employee;
 -- 查询最新入职的员工的入职日期
 select max(hiredate) from t_employee;
 -- 查询每一个部门的平均薪资
 select did,round(avg(salary),2)
 from t_employee
 group by did;
 
 
 
 use atguigu;
 -- 在t_employee表中查询薪资在[8000,10000]之间的员工姓名和薪资并给每一行记录编序号
 select row_number() over() as rn,ename,salary
 from t_employee
 where salary between 8000 and 10000;
 -- 计算每一个部门的平均薪资与全公司的平均薪资的差值
 select distinct
     did,
     avg(salary) over(partition by did),
     avg(salary) over(),
     round(avg(salary) over(partition by did)-avg(salary) over(),2) as deviation
 from t_employee;
 -- 在t_employee表中查询女员工姓名，部门编号，薪资
 -- 查询结果按照部门编号分组后在按薪资升序排列
 -- 并分别使用row_number()、rank()、dense_rank()三个序号函数给每一行记录编序号
 select ename,did,salary,gender,
 row_number() over(partition by did order by salary) as "row_num",
 rank() over(partition by did order by salary) as "rank_num",
 dense_rank() over(partition by did order by salary) as "ds_rank_num"
 from t_employee where gender='女';
 -- 或使用window给窗口指定别名
 select ename,did,salary,
 row_number() over w as "row_num",
 rank() over w as "rank_num" ,
 dense_rank() over w as "ds_rank_num" 
 from t_employee where gender='女'
 window w as(partition by did order by salary);
 -- 在t_employee表中查询每个部门最低3个薪资值的女员工姓名，部门编号，薪资值
 select row_number() over() as rn,temp.*
 from(select ename,did,salary,
 row_number() over w as "row_num",
 rank() over w as "rank_num" ,
 dense_rank() over w as "ds_rank_num"
 from t_employee where gender='女'
 window w as(partition by did order by salary))temp
 where temp.rank_num<=3;
 -- 在t_employee表中查询每个部门薪资排名前3的员工姓名，部门编号，薪资值
 select temp.*
 from(select ename,did,salary,
 dense_rank() over w as "ds_rank_num"
 from t_employee
 window w as(partition by did order by salary desc))temp
 where temp.ds_rank_num<=3;
 -- 在t_employee表中查询全公司薪资排名前3的员工姓名，部门编号，薪资值
 select temp.*
 from(select ename,did,salary,
 dense_rank() over w as "ds_rank_num"
 from t_employee
 window w as(order by salary desc))temp
 where temp.ds_rank_num<=3;
 -- 查找薪资排名的上一位、下一位、首位、末位
 select
     ename,
     salary,
     lag(ename,1,'-') over(order by salary) as '上一位姓名',
     lag(salary,1,0) over(order by salary) as '上一位薪资',
     lead(ename) over(order by salary) as '下一位姓名',
     lead(salary) over(order by salary) as '下一位薪资',
     first_value(salary) over(order by salary) as '首位薪资',
     last_value(ename) over(order by salary rows between unbounded preceding and unbounded following) as '末位姓名'
 from t_employee;
 */
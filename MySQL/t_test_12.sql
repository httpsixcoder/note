-- 在t_employee表中查询每个人薪资和公司平均薪资的差值
-- 并显示员工薪资和公司平均薪资相差5000元以上的记录
SELECT
  ename,
  salary,
  round(salary - (SELECT avg(salary) FROM t_employee), 2) 
FROM
  t_employee 
WHERE
  abs(salary - (SELECT avg(salary) FROM t_employee)) > 5000;-- 在t_employee表中查询每个部门平均薪资和公司平均薪资的差值
SELECT
  did,
  round(avg(salary) - (SELECT avg(salary) FROM t_employee), 2) 
FROM
  t_employee 
GROUP BY
  did;-- 使用子查询按薪资大小编号
-- 【】
SELECT
      ename,
      salary,
      (SELECT count(*) FROM t_employee AS temp2 WHERE temp1.salary > temp2.salary) AS rk 
FROM
  t_employee AS temp1 
ORDER BY
  rk;-- 在t_employee表中查询薪资最高的员工姓名和薪资
-- 取表中第一行员工的姓名和全公司最高的薪资值一起显示
SELECT
  ename,
  salary 
FROM
  t_employee 
ORDER BY
  salary DESC 
  LIMIT 1;-- 在t_employee表中查询比全公司平均薪资高的男员工姓名和薪资
SELECT
  ename,
  salary 
FROM
  t_employee 
WHERE
  gender = '男' 
  AND salary > (SELECT AVG(salary) FROM t_employee);-- 在t_employee表中查询和 白露，谢吉娜 同一部门的员工姓名和电话
SELECT
  ename,
  tel 
FROM
  t_employee 
WHERE
  did IN (SELECT did FROM t_employee WHERE ename = '白露' OR ename = '谢吉娜');-- 在t_employee表中查询薪资比 白露，李诗雨，黄冰茹 三个人的薪资都要高的员工姓名和薪资
SELECT
  ename,
  salary 
FROM
  t_employee 
WHERE
  salary > ALL (SELECT salary FROM t_employee WHERE ename IN ('白露', '李诗雨', '黄冰茹'));-- 查询t_employee和t_department表，按部门统计平均工资
-- 显示部门平均工资比全公司的总平均工资高的部门编号、部门名称、部门平均薪资
-- 并按照部门平均薪资升序排列
SELECT
  td.did,
  td.dname,
  avg(salary) 
FROM
  t_employee AS te
  JOIN t_department AS td ON te.did = td.did 
GROUP BY
  td.did,
  td.dname 
HAVING
  avg(salary) > (SELECT avg(salary) FROM t_employee) 
ORDER BY
  avg(salary);-- 查询t_employee表中是否存在部门编号为null的员工
-- 如果存在，查询t_department表的部门编号、部门名称
SELECT
  did,
  dname 
FROM
  t_department 
WHERE
  EXISTS (SELECT * FROM t_employee WHERE did IS NULL);-- 查询t_department表是否存在与t_employee表相同部门编号的记录
-- 如果存在，查询这些部门的编号和名称
SELECT DISTINCT
  td.did,
  td.dname 
FROM
  t_employee AS te
  JOIN t_department AS td ON te.did = td.did;-- 在t_employee表中，查询每个部门的平均薪资
-- 然后与t_department表联合查询
-- 所有部门的部门编号、部门名称、部门平均薪资
SELECT
  * 
FROM
  t_department AS td
  LEFT JOIN (SELECT did, avg(salary) FROM t_employee GROUP BY did) AS te ON td.did = te.did;-- 在t_employee表中查询每个部门中薪资排名前2的员工姓名、部门编号和薪资
SELECT
  ename,
  did,
  salary 
FROM
  (SELECT ename, did, salary, ROW_NUMBER() over (PARTITION BY did ORDER BY salary DESC) AS rn FROM t_employee) AS temp 
WHERE
  temp.rn <= 2;--  修改t_employee表中部门编号和测试部部门编号相同的员工薪资为原来薪资的1.5倍
UPDATE t_employee 
SET salary = round(salary * 1.5, 2) 
WHERE
  did IN (SELECT did FROM t_department WHERE dname = '测试部');-- 修改t_employee表中did为null的员工信息
-- 将他们的did值修改为测试部的部门编号
UPDATE t_employee 
SET did = (SELECT did FROM t_department WHERE dname = '测试部') 
WHERE
  did IS NULL;-- 修改t_employee表中李冰冰的薪资值等于孙红梅的薪资值
UPDATE t_employee 
SET salary = ((SELECT salary FROM (SELECT salary FROM t_employee WHERE ename = '孙红梅') AS temp)) 
WHERE
  ename = '李冰冰';-- 修改t_employee表李冰冰的薪资与她所在部门的平均薪资一样
UPDATE t_employee t1
JOIN (SELECT did, AVG(salary) AS avg_salary FROM t_employee GROUP BY did) t2 ON t1.did = t2.did 
SET t1.salary = t2.avg_salary 
WHERE
  t1.ename = '李冰冰';-- 从t_employee表中删除测试部的员工记录
DELETE 
FROM
  t_employee 
WHERE
  did IN (SELECT did FROM t_department WHERE dname = '测试部');-- 从t_employee表中删除和李冰冰同一个部门的员工记录
DELETE t1 
FROM
  t_employee t1
  JOIN t_employee t2 ON t1.did = t2.did 
WHERE
  t2.ename = '李冰冰';-- 仅复制表结构，可以用create语句
CREATE TABLE temp LIKE t_employee;-- 使用insert语句+子查询，复制数据，此时insert不用写values
INSERT INTO temp SELECT
* 
FROM
  t_employee;-- 同时复制表结构+数据
CREATE TABLE temp AS (SELECT * FROM t_employee);-- 在t_employee表中查询每个人薪资和公司平均薪资的的差值
SELECT
  ename,
  ROUND(salary - (SELECT avg(salary) FROM t_employee), 2) 
FROM
  t_employee;-- 查询薪资低于9000的员工编号，员工姓名，员工薪资，领导编号，领导姓名，领导薪资
SELECT
  te1.eid,
  te1.ename,
  te1.salary,
  te2.eid,
  te2.ename,
  te2.salary 
FROM
  t_employee te1
  JOIN t_employee te2 ON te1.mid = te2.eid 
WHERE
  te1.salary < 9000;-- 查询eid为21的员工，和他所有领导，直到最高领导
-- 建表，设置多层领导
SELECT
  * 
FROM
  emp;
WITH recursive cte AS (
      SELECT
  eid,
  ename,
  `mid`     
  FROM
    emp     
  WHERE
    eid = 21     UNION ALL
        SELECT
    emp.eid,
    emp.ename,
    emp.mid
        
  FROM
    emp
    JOIN cte     ON emp.eid = cte.mid
        
  WHERE
emp.eid IS NOT NULL) SELECT
* 
FROM
  cte;-- 答案
/*
-- 在t_employee表中查询每个人薪资和公司平均薪资的差值
-- 并显示员工薪资和公司平均薪资相差5000元以上的记录
select
    ename as "姓名",
    salary as "薪资",
    round((select avg(salary) from t_employee),2) as "全公司平均薪资",
    round(salary-(select avg(salary) from t_employee),2) as "差值"
from t_employee
where abs(round(salary-(select avg(salary) from t_employee),2))>5000;
-- 在t_employee表中查询每个部门平均薪资和公司平均薪资的差值
select
    did,
    avg(salary),
    avg(salary)-(select avg(salary) from t_employee)
from t_employee
group by did;
-- 使用子查询按薪资大小编号
select
    ename,
    salary,
    (select count(*) from t_employee as temp2 where temp1.salary>temp2.salary) as rk
from t_employee as temp1
order by rk;
-- 在t_employee表中查询薪资最高的员工姓名和薪资
-- 取表中第一行员工的姓名和全公司最高的薪资值一起显示
select ename,salary
from t_employee
where salary=(select max(salary) from t_employee);
-- 在t_employee表中查询比全公司平均薪资高的男员工姓名和薪资
select ename,salary
from t_employee
where salary>(select avg(salary) from t_employee) and gender='男';
-- 在t_employee表中查询和 白露，谢吉娜 同一部门的员工姓名和电话
select ename,tel,did
from t_employee
where did in (select did from t_employee where ename='白露' or ename='谢吉娜');

select ename,tel,did
from t_employee
where did=any(select did from t_employee where ename='白露' or ename='谢吉娜');
-- 在t_employee表中查询薪资比 白露，李诗雨，黄冰茹 三个人的薪资都要高的员工姓名和薪资
select ename,salary
from t_employee
where salary>all(select salary from t_employee where ename in('白露','李诗雨','黄冰茹'));

select ename,salary
from t_employee
where salary>(select max(salary) from t_employee where ename in('白露','李诗雨','黄冰茹'));
-- 查询t_employee和t_department表，按部门统计平均工资
-- 显示部门平均工资比全公司的总平均工资高的部门编号、部门名称、部门平均薪资
-- 并按照部门平均薪资升序排列
select t_department.did,dname,avg(salary)
from t_employee
right join t_department
on t_employee.did=t_department.did
group by t_department.did
having avg(salary)>(select avg(salary) from t_employee)
order by avg(salary);

-- 查询t_employee表中是否存在部门编号为null的员工
-- 如果存在，查询t_department表的部门编号、部门名称
select * from t_department 
where exists(select * from t_employee where did is null);
-- 查询t_department表是否存在与t_employee表相同部门编号的记录
-- 如果存在，查询这些部门的编号和名称
select * from t_department
where exists(select * from t_employee where t_employee.did=t_department.did);
-- 查询结果等价于下面的SQL
select distinct t_department.*
from t_department
inner join t_employee
on t_department.did=t_employee.did;
-- 在t_employee表中，查询每个部门的平均薪资
-- 然后与t_department表联合查询
-- 所有部门的部门编号、部门名称、部门平均薪资
select t_department.did,dname,pingjun
from t_department
left join (select did,avg(salary) as pingjun from t_employee group by did) temp
on t_department.did=temp.did;
-- 在t_employee表中查询每个部门中薪资排名前2的员工姓名、部门编号和薪资
select *
from (
    select
        ename,
        did,
        salary,
        dense_rank() over (partition by did order by salary desc) as paiming
    from t_employee
) temp
where temp.paiming<=2;
- 修改t_employee表中部门编号和测试部部门编号相同的员工薪资为原来薪资的1.5倍
update t_employee
set salary = salary * 1.5
where did=(select did from t_department where dname='测试部');
-- 修改t_employee表中did为null的员工信息
-- 将他们的did值修改为测试部的部门编号
-- 这种子查询必须是单个值，否则无法赋值
update t_employee 
set did = (select did from t_department where dname='测试部')
where did is null;
-- 修改t_employee表中李冰冰的薪资值等于孙红梅的薪资值
update t_employee
set salary = (select salary from(select salary from t_employee where ename='孙红梅')temp)
where ename='李冰冰';
-- 当update的表和子查询的表是同一个表时，需要将子查询的结果用临时表的方式表示
-- 即再套一层子查询，使得update和最外层的子查询不是同一张表

-- 修改t_employee表李冰冰的薪资与她所在部门的平均薪资一样
update t_employee
set salary = 
(
    select pingjun
    from 
        (
            select avg(salary) pingjun
            from t_employee
            where did=(
                        select did
                        from t_employee
                        where ename='李冰冰'
                    )
        ) temp
)
where ename='李冰冰';
-- 从t_employee表中删除测试部的员工记录
delete from t_employee 
where did = (select did from t_department where dname='测试部');
-- 从t_employee表中删除和李冰冰同一个部门的员工记录
delete from t_employee
where did=(select did from t_employee where ename='李冰冰');
-- 报错，因为删除和子查询是同一张表
delete from t_employee
where did=(select did from (select did from t_employee where ename='李冰冰')temp);



-- 仅复制表结构，可以用create语句
create table department like t_department;

-- 使用insert语句+子查询，复制数据，此时insert不用写values
insert into department (select * from t_department where did<=3);

-- 同时复制表结构+数据
create table d_department as (select * from t_department);
-- 如果select后面是部分字段，复制的新表就只有这一部分字段

-- 在t_employee表中查询每个人薪资和公司平均薪资的的差值
with
temp as (select round(avg(salary),2) as pingjun from t_employee)
select
    ename as "员工姓名",
    salary as "薪资",
    pingjun "公司平均薪资",
    round(salary - pingjun,2) "差值"
from t_employee,temp
having abs(差值)>5000;
-- 查询薪资低于9000的员工编号，员工姓名，员工薪资，领导编号，领导姓名，领导薪资
with 
emp as (select eid,ename,salary,`mid` from t_employee where salary<9000),
mgr(meid,mename,msalary) as (select eid,ename,salary from t_employee)
select
    eid as "员工薪资",
    ename as "员工姓名",
    salary as "员工薪资",
    meid as "领导编号",
    mename as "领导姓名",
    msalary as "领导薪资"
from emp join mgr on emp.mid=mgr.meid;
-- 查询eid为21的员工，和他所有领导，直到最高领导
-- 建表，设置多层领导
create table emp as (select eid,ename,salary,tel,`mid` from t_employee where salary<10000);
update emp set mid=19 where eid=21; 
update emp set mid=17 where eid=19; 
update emp set mid=16 where eid=17; 
update emp set mid=15 where eid=16;
update emp set mid=4 where eid=15; 
update emp set mid=null where eid=4;
select * from emp;
with recursive
cte as(
    select eid,ename,`mid`
    from emp
    where eid=21
    union all
    select emp.eid,emp.ename,emp.mid
    from emp join cte
    on emp.eid=cte.mid
    where emp.eid is not null
)
select * from cte;
*/
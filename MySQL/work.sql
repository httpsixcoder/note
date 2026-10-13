-- 17.2选择与过滤练习
-- （1）查询薪资大于12000的员工姓名和薪资
select CONCAT(first_name,last_name),salary
from employees where salary>12000;
-- （2）查询员工号为176的员工的姓名和部门编号
select CONCAT(first_name,last_name),department_id
from employees where employee_id=176;
-- （3）查询薪资不在5000到12000的员工的姓名和薪资
select CONCAT(first_name,last_name),salary
from employees where salary NOT BETWEEN 5000 and 12000;
-- （4）查询在20或50号部门工作的员工姓名和部门编号
select CONCAT(first_name,last_name),department_id
from employees where department_id in(20,50);
-- （5）查询公司中没有管理者的员工姓名及job_id
select CONCAT(first_name,last_name),job_id
from employees where manager_id is NUll;
-- （6）查询公司中有奖金的员工姓名，薪资和佣金
select CONCAT(first_name,last_name),salary,ROUND(salary*commission_pct,2)
from employees where commission_pct is NOT NULL;
-- （7）查询员工姓名的第三个字母是a的员工姓名
select CONCAT(first_name,last_name)
from employees where first_name LIKE '__a%';
-- （8）查询姓名中有字母a和e的员工姓名
SELECT full_name
FROM (
    SELECT CONCAT(first_name, last_name) AS full_name
    FROM employees
) AS t
WHERE full_name LIKE '%a%'
  AND full_name LIKE '%e%';
-- 17.3多表查询练习
-- （1）查询所有员工的姓名，部门编号和部门名称
select CONCAT(e.first_name,e.last_name),d.department_id,d.department_name
from employees AS e
left join departments AS d
on e.department_id=d.department_id; 
-- （2）查询90号部门员工的job_id和90号部门的位置编号
select CONCAT(e.first_name,e.last_name),e.job_id,d.location_id
from employees AS e
join departments AS d
on e.department_id=d.department_id
where e.department_id=90;
-- （3）查询所有有奖金的员工的姓名，部门名称，位置编号，城市
select CONCAT(e.first_name,e.last_name),d.department_name,d.location_id,l.city
from employees AS e
left join departments AS d
on e.department_id=d.department_id
left join locations AS l
on d.location_id=l.location_id
WHERE commission_pct IS NOT NULL
-- （4）查询city在toronto工作的员工的姓名,job_id,部门编号,部门名称
select CONCAT(e.first_name,e.last_name),e.job_id,e.department_id,d.department_name
from employees AS e
join departments AS d
on e.department_id=d.department_id
join locations AS l
on d.location_id=l.location_id
WHERE l.city='toronto';
-- （5）查询指定员工的姓名，员工号，以及他的管理者的姓名和员工号，结果类似于下面的格式
-- employees    emp#    manager   mgr#
-- kochhar     101     king       100

select CONCAT(e1.first_name,e1.last_name) employees,e1.employee_id 'emp#',
CONCAT(e2.first_name,e2.last_name) manager,e2.employee_id 'mgr#'
from employees AS e1
left join employees AS e2
on e1.manager_id=e2.employee_id;
-- 17.4单行函数练习
-- （1）查询系统时间(注：日期+时间)
select SYSDATE();
-- （2）查询员工编号，姓名，薪资，以及薪资提高百分之20%后的结果(new salary)
select employee_id,CONCAT(first_name,last_name),salary,ROUND(salary*1.2,2) 'new salary'
from employees;
-- （3）将员工的姓名按首字母排序，并写出姓名的长度
select CONCAT(first_name,last_name),CHAR_LENGTH(CONCAT(first_name,last_name))
from employees order by first_name,last_name;
-- （4）写一个查询，产生下面的结果
-- <last_name> earns <salary> monthly but wants <salary*3> dream salary
-- 比如：king earns 24000 monthly but wants 72000
select concat(
last_name,
' earns ',
salary,
' monthly but wants ',
salary * 3,
' dream salary'
)
from employees;
-- （5）使用case-when
-- 按照下面的条件：
-- job          grade
-- ad_pres      a
-- st_man       b
-- it_prog      c
-- sa_rep       d
-- st_clerk     e
-- 产生下面的结果：
-- last_name    job_id    grade
-- king         ad_pres   a
SELECT last_name,job_id,
CASE job_id
	WHEN 'ad_pres' THEN 'a'
	WHEN 'st_man' THEN 'b'
  WHEN 'it_prog' THEN 'c'
	WHEN 'sa_rep' THEN 'd'
	WHEN 'st_clerk' THEN 'e'
	ELSE '暂无'
END grade
from employees;
-- 17.5分组函数练习
-- （1）查询公司员工薪资的最大值，最小值，平均值，总和
select max(salary),min(salary),avg(salary),sum(salary) FROM employees;
-- （2）查询各job_id的员工薪资的最大值，最小值，平均值，总和
select job_id,max(salary),min(salary),avg(salary),sum(salary) 
FROM employees GROUP BY job_id;
-- （3）查询各个job_id的员工人数
select job_id,COUNT(job_id) 
FROM employees GROUP BY job_id;
-- （4）查询员工最高薪资和最低薪资的差距
select max(salary)-min(salary) 差距 FROM employees;
-- （5）查询各个管理者手下员工的不低于6000的最低薪资，不计算没有管理者的员工
SELECT manager_id, MIN(salary)
FROM employees
WHERE manager_id IS NOT NULL
GROUP BY manager_id
HAVING MIN(salary) >= 6000;
-- （6）查询所有部门的名字，位置编号，员工数量和薪资平均值
select d.department_name,d.location_id,count(e.department_id),AVG(salary)
from employees e
right JOIN departments d
on e.department_id=d.department_id
GROUP BY e.department_id,d.location_id ;
-- 17.6子查询练习
-- （1）查询和zlotkey相同部门的员工姓名和薪资
select CONCAT(first_name,last_name),salary FROM employees 
where department_id =(SELECT department_id from employees where last_name= 'zlotkey' );
-- （2）查询薪资比公司平均薪资高的员工的员工编号，姓名和薪资
select employee_id, CONCAT(first_name,last_name),salary FROM employees 
where salary >(SELECT AVG(salary) from employees);
-- （3）查询各部门中薪资比本部门平均薪资高的员工的员工编号,姓名和薪资
SELECT e1.employee_id, CONCAT(e1.first_name, e1.last_name), e1.salary
FROM employees e1
JOIN (
    SELECT department_id, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY department_id
) e2 ON e1.department_id = e2.department_id
WHERE e1.salary > e2.avg_sal;
-- （4）查询与姓名中包含字母u的员工在相同部门的员工的员工编号和姓名
select employee_id, CONCAT(first_name,last_name)
FROM employees 
WHERE department_id in(
  select department_id from employees WHERE first_name like '%u%' or last_name like '%u%'
);
-- （5）查询管理者是king的员工姓名和薪资
-- 两个 last_name ='king' 所以用in
select  CONCAT(first_name,last_name),salary
FROM employees 
WHERE manager_id in(
  select employee_id from employees WHERE last_name ='king'
);
-- （6）查询薪资最低的员工的姓名和薪资
select  CONCAT(first_name,last_name),salary
FROM employees 
WHERE salary =(
  SELECT min(salary) from employees
);








-- 答案：
/*

17.7练习题参考答案
17.7.1选择与过滤练习
-- 1.查询薪资大于12000的员工姓名和薪资
select first_name,salary
from employees
where salary > 12000;

-- 2.查询员工号为176的员工的姓名和部门编号
select first_name,department_id
from employees
where employee_id = 176;

-- 3.查询薪资不在5000到12000的员工的姓名和薪资
select first_name,salary
from employees
where salary not between 5000 and 12000;

-- 4.查询在20或50号部门工作的员工姓名和部门编号
select first_name,department_id
from employees
where department_id in (20, 50);

-- 5.查询公司中没有管理者的员工姓名及job_id
select first_name,job_id
from employees
where manager_id is null;

-- 6.查询公司中有奖金的员工姓名，薪资和佣金
select first_name,salary,salary * commission_pct
from employees
where commission_pct is not null;

-- 7.查询员工姓名的第三个字母是a的员工姓名
select first_name
from employees
where first_name like '__a%';

-- 8.查询姓名中有字母a和e的员工姓名
select first_name
from employees
where first_name like '%a%' and first_name like '%e%';
17.7.2多表查询练习
-- 1.查询所有员工的姓名，部门编号和部门名称
select last_name, e.department_id, department_name
from employees e
left outer join departments d
on e.department_id = d.department_id;

-- 2.查询90号部门员工的job_id和90号部门的位置编号
select job_id, location_id
from employees e
join departments d
on e.department_id = d.department_id
where e.department_id = 90;

-- 3.查询所有有奖金的员工的姓名，部门名称，位置编号，城市
select last_name,department_name,d.location_id,city
from employees e
left join departments d
on e.department_id = d.department_id
left join locations l
on d.location_id = l.location_id
where commission_pct is not null;

-- 4.查询city在toronto工作的员工的姓名,job_id,部门编号,部门名称
select last_name,job_id,e.department_id,department_name
from employees e
join departments d
on e.department_id = d.department_id
join locations l
on l.location_id = d.location_id
where l.city = 'toronto';

-- 5.查询指定员工的姓名，员工号，以及他的管理者的姓名和员工号，结果类似于下面的格式
-- employees    emp#    manager mgr#
-- kochhar      101 king    100
select
    emp.last_name as employees,
    emp.employee_id as "emp#",
    mgr.last_name as manager,
    mgr.employee_id as "mgr#"
from employees emp
left join employees mgr
on emp.manager_id = mgr.employee_id;
17.7.3单行函数练习
-- 1.查询系统时间(注：日期+时间)
select now();

-- 2.查询员工编号，姓名，薪资，以及薪资提高百分之20%后的结果(new salary)
select
    employee_id,
    first_name,
    salary,
    salary * 1.2 as new_salary
from employees;

-- 3.将员工的姓名按首字母排序，并写出姓名的长度
select first_name,char_length(first_name)
from employees
order by first_name;

-- 4.写一个查询，产生下面的结果
-- <last_name> earns <salary> monthly but wants <salary*3> dream salary
-- 比如：king earns 24000 monthly but wants 72000
select concat(
        last_name,
        ' earns ',
        salary,
        ' monthly but wants ',
        salary * 3,
        ' dream salary'
    )
from employees;

-- 5.使用case-when
-- 按照下面的条件：
-- job          grade
-- ad_pres      a
-- st_man       b
-- it_prog      c
-- sa_rep       d
-- st_clerk     e
-- 产生下面的结果：
-- last_name    job_id    grade
-- king         ad_pres   a
select
    last_name,
    job_id,
    case job_id
        when 'ad_pres' then 'a'
        when 'st_man' then 'b'
        when 'it_prog' then 'c'
        when 'sa_rep' then 'd'
        when 'st_clerk' then 'e'
        else 'x'
    end 'grade'
from employees;
17.7.4分组函数练习
-- 1.查询公司员工薪资的最大值，最小值，平均值，总和
select max(salary),min(salary),avg(salary),sum(salary)
from employees;

-- 2.查询各job_id的员工薪资的最大值，最小值，平均值，总和
select job_id,max(salary),min(salary),avg(salary),sum(salary)
from employees
group by job_id;

-- 3.查询各个job_id的员工人数
select job_id,count(*)
from employees
group by job_id;

-- 4.查询员工最高薪资和最低薪资的差距
select max(salary) - min(salary)
from employees;

-- 5.查询各个管理者手下员工的不低于6000的最低薪资，不计算没有管理者的员工
select manager_id,min(salary)
from employees
where manager_id is not null
group by manager_id
having min(salary) > 6000;

-- 6.查询所有部门的名字，位置编号，员工数量和薪资平均值
select
    department_name,
    location_id,
    count(employee_id),
    avg(salary)
from employees e
right join departments d
on e.department_id = d.department_id
group by department_name,location_id;
17.7.5子查询练习
-- 1.查询和zlotkey相同部门的员工姓名和薪资
select last_name,salary
from employees
where department_id = (
    select department_id
    from employees
    where last_name = 'zlotkey'
    );

-- 2.查询薪资比公司平均薪资高的员工的员工编号，姓名和薪资
select employee_id,last_name,salary
from employees
where salary > (
    select avg(salary)
    from employees
    );

-- 3.查询各部门中薪资比本部门平均薪资高的员工的员工编号,姓名和薪资
select employee_id,first_name,salary,avg_sal
from employees e1
join (
    select department_id,avg(salary) avg_sal
    from employees
    group by department_id
    ) e2
on e1.department_id = e2.department_id
where salary > avg_sal;

-- 4.查询与姓名中包含字母u的员工在相同部门的员工的员工编号和姓名
select employee_id,last_name
from employees
where department_id in (
    select department_id
    from employees
    where last_name like '%u%'
    );

-- 5.查询管理者是king的员工姓名和薪资
select e1.first_name,e1.salary,e1.manager_id,e2.last_name
from employees e1
join employees e2
on e1.manager_id = e2.employee_id
where e1.manager_id in (
    select employee_id
    from employees
    where last_name = 'king'
    );

-- 6.查询薪资最低的员工的姓名和薪资
select last_name,salary
from employees
where salary = (
    select min(salary)
    from employees
    );


*/
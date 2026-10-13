-- 查询每一个部门的平均薪资
select did,
    avg(salary) 'avg_salary'
from t_employee
GROUP BY did;
-- 查询每一个部门的平均薪资，显示部门编号，部门的名称，该部门的平均薪资
select td.did,
    td.dname,
    avg(salary) 'avg_salary'
from t_employee te
    right join t_department td on te.did = td.did
GROUP BY td.did,
    td.dname;
-- 查询每一个部门的平均薪资，显示部门编号，部门的名称，该部门的平均薪资
-- 要求，如果没有员工的部门，平均薪资不显示null，显示0
select td.did,
    td.dname,
    IFNULL(avg(salary), 0) 'avg_salary'
from t_employee te
    right join t_department td on te.did = td.did
GROUP BY td.did,
    td.dname;
-- 按照部门统计人数
select did,
    COUNT(1) 'num_people'
from t_employee
where did is not NULL
GROUP BY did;
-- 按照部门统计人数，并合计总数
select did,
    COUNT(1) 'num_people'
from t_employee
where did is not NULL
GROUP BY did with ROLLUP;
-- 按照不同的部门，不同的职位，分别统计男和女的员工人数
select did,
    job_id,
    gender,
    COUNT(1) 'num_people'
from t_employee
GROUP BY did,
    job_id,
    gender;
-- 查询每一个部门的女员工的平均薪资，显示部门编号，部门的名称，该部门的平均薪资
-- 要求，如果没有员工的部门，平均薪资不显示null，显示0
-- 最后只显示平均薪资高于12000的部门
select td.did,
    td.dname,
    IFNULL(avg(salary), 0) 'avg_salary'
from t_employee te
    right join t_department td on te.did = td.did
WHERE te.gender = '女'
GROUP BY td.did,
    td.dname
HAVING AVG(salary) > 12000;
-- 查询每一个部门薪资超过10000的男女员工的人数，显示部门编号，部门的名称，性别，人数
-- 只显示人数低于3人的
select td.did,
    td.dname,
    te.gender,
    COUNT(te.eid) 'num_people'
from t_employee te
    right join t_department td on te.did = td.did
WHERE te.salary > 10000
GROUP BY td.did,
    td.dname,
    te.gender
HAVING count(te.eid) < 3;
-- 查询员工信息，按照薪资从高到低
select ename,
    salary
from t_employee
ORDER BY salary desc;
-- 查询每一个部门薪资超过10000的男女员工的人数，显示部门编号，部门的名称，性别，人数
-- 只显示人数低于3人的，按照人数升序排列
select td.did,
    td.dname,
    te.gender,
    COUNT(te.eid) 'num_people'
from t_employee te
    right join t_department td on te.did = td.did
WHERE te.salary > 10000
GROUP BY td.did,
    td.dname,
    te.gender
HAVING count(te.eid) < 3
ORDER BY count(te.eid);
-- 查询员工的薪资，按照薪资从低到高，薪资相同按照员工编号从高到低
select ename,
    salary
from t_employee
ORDER BY salary asc,
    eid desc;
-- 查询所有的男员工信息，分页显示，每页显示3条，第2页
select *
from t_employee
where gender = '男'
LIMIT 3, 3;
-- 查询每一个编号为偶数的部门，显示部门编号，名称，员工数量
-- 只显示员工数量>=2的结果，按照员工数量升序排列
-- 每页显示2条，显示第1页
select td.did,
    td.dname,
    COUNT(te.eid) 'num_people'
from t_employee te
    right join t_department td on te.did = td.did
WHERE MOD(td.did, 2) = 0
GROUP BY td.did,
    td.dname
HAVING count(te.eid) >= 2
ORDER BY count(te.eid) asc
LIMIT 2;
-- 答案
/*
 -- 查询每一个部门的平均薪资
 select did,round(avg(salary),2)
 from t_employee
 group by did;
 -- 查询每一个部门的平均薪资，显示部门编号，部门的名称，该部门的平均薪资
 select t_department.did,dname,round(avg(salary),2)
 from t_department left join t_employee
 on t_department.did = t_employee.did
 group by t_department.did;
 -- 查询每一个部门的平均薪资，显示部门编号，部门的名称，该部门的平均薪资
 -- 要求，如果没有员工的部门，平均薪资不显示null，显示0
 select t_department.did,dname,ifnull(round(avg(salary),2),0)
 from t_department left join t_employee
 on t_department.did = t_employee.did
 group by t_department.did;
 -- 按照部门统计人数
 select did,count(*)
 from t_employee
 group by did;
 -- 按照部门统计人数，并合计总数
 select did,count(*)
 from t_employee
 group by did with rollup;
 
 select
     ifnull(did,'合计') as "部门编号",
     count(*) as "人数"
 from t_employee
 group by did with rollup;
 -- 按照不同的部门，不同的职位，分别统计男和女的员工人数
 select did,job_id,gender,count(*)
 from t_employee 
 group by did,job_id,gender;
 -- 分组统计时，select后面只写和分组统计有关的字段
 -- 其他无关字段不要出现，否则会引起歧义
 select eid,ename,did,count(*)
 from t_employee
 group by did;
 -- eid,ename此时不应该出现在select后面
 select did,count(*)
 from t_employee
 group by did;
 -- 查询每一个部门的女员工的平均薪资，显示部门编号，部门的名称，该部门的平均薪资
 -- 要求，如果没有员工的部门，平均薪资不显示null，显示0
 -- 最后只显示平均薪资高于12000的部门
 select t_department.did,dname,ifnull(round(avg(salary),2),0)
 from t_department left join t_employee
 on t_department.did=t_employee.did
 where gender='女'
 group by t_department.did
 having ifnull(round(avg(salary),2),0)>12000;
 -- 查询每一个部门薪资超过10000的男女员工的人数，显示部门编号，部门的名称，性别，人数
 -- 只显示人数低于3人的
 select t_department.did,dname,gender,count(eid)
 from t_employee right join t_department
 on t_employee.did=t_department.did
 where salary>10000
 group by t_department.did,gender
 having count(eid)<3;
 -- 查询员工信息，按照薪资从高到低
 select * from t_employee
 order by salary desc;
 -- 查询每一个部门薪资超过10000的男女员工的人数，显示部门编号，部门的名称，性别，人数
 -- 只显示人数低于3人的，按照人数升序排列
 select t_department.did,dname,gender,count(eid)
 from t_employee
 right join t_department
 on t_employee.did=t_department.did
 where salary>10000
 group by t_department.did,gender
 having count(eid)<3
 order by count(eid);
 -- 查询员工的薪资，按照薪资从低到高，薪资相同按照员工编号从高到低
 select *
 from t_employee
 order by salary asc,eid desc;
 -- 查询所有的男员工信息，分页显示，每页显示3条，第2页
 select *
 from t_employee
 where gender='男'
 limit 3,3;
 -- 查询每一个编号为偶数的部门，显示部门编号，名称，员工数量
 -- 只显示员工数量>=2的结果，按照员工数量升序排列
 -- 每页显示2条，显示第1页
 select t_department.did,dname,count(eid)
 from t_employee
 right join t_department
 on t_employee.did=t_department.did
 where t_department.did%2=0
 group by t_department.did
 having count(eid)>=2
 order by count(eid)
 limit 0,2;
 */
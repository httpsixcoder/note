-- 查询部门编号为1的女员工的姓名、部门编号、部门名称、薪资等情况
select te.ename,
    te.did,
    td.dname,
    te.salary
from t_employee te
    join t_department td on te.did = td.did
where te.did = 1
    and gender = '女' -- 查询部门编号为1的员工姓名、部门编号、部门名称、薪资、职位编号、职位名称等情况
select te.ename,
    te.did,
    td.dname,
    te.salary,
    tj.jid,
    tj.jname
from t_employee te
    join t_department td on te.did = td.did
    join t_job tj on te.job_id = tj.jid
where te.did = 1 -- 答案
    /*
     -- 查询部门编号为1的女员工的姓名、部门编号、部门名称、薪资等情况
     select ename,gender,t_department.did,dname,salary
     from t_employee inner join t_department 
     on t_employee.did = t_department.did
     where t_department.did = 1 and gender = '女';
     
     -- 查询部门编号为1的员工姓名、部门编号、部门名称、薪资、职位编号、职位名称等情况
     select ename,gender,t_department.did,dname,salary,job_id,jname
     from t_employee
     inner join t_department on t_employee.did = t_department.did
     inner join t_job on t_employee.job_id = t_job.jid
     where t_department.did = 1;
     */
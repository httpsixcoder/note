-- 练习：第七章 运算符

use atguigu;
-- 查询薪资高于15000的员工姓名和薪资
select ename'员工姓名',salary '薪资' from t_employee where salary>15000;
-- 查询薪资为9000的员工的姓名和薪资
select ename'员工姓名',salary '薪资' from t_employee where salary = 9000;
-- 查询地址不在北苑的
select ename'员工姓名',address '住址' from t_employee where address != '北苑';
-- 查询薪资在[10000,15000]
select ename'员工姓名',salary '薪资' from t_employee where salary between 10000 and 15000;
-- 查询薪资不在[10000,15000]
select ename'员工姓名',salary '薪资' from t_employee where salary not  between 10000 and 15000;
-- 查询地址在这几个地方的'北苑', '望京', '龙泽'
select ename'员工姓名',address '住址' from t_employee where address in ('北苑','望京','龙泽');
-- 查询地址不在这几个地方的'北苑', '望京', '龙泽'
select ename'员工姓名',address '住址' from t_employee where address not in ('北苑','望京','龙泽');
-- 查询名字有 冰 字的
select ename'员工姓名' from t_employee where ename like '%冰%';
-- 查询名字以 雨 结尾的
select ename'员工姓名' from t_employee where ename like '%雨';
-- 查询名字以 李 开头的
select ename'员工姓名' from t_employee where ename like '李%';
-- 查询名字有 红 这个字，但是 红 的前面只能有1个字
select ename'员工姓名' from t_employee where ename like '_红%';
-- 查询当前MySQL数据库的字符集情况
show variables like '%character%';
-- 查询薪资高于15000，并且性别是男的员工
select ename'员工姓名',salary '薪资',gender '性别' from t_employee where salary>15000 and gender = '男';
-- 查询薪资高于15000，或者did为1的员工
select eid 'id',ename'员工姓名',salary '薪资' from t_employee where salary>15000 or did = 1;
-- 查询薪资不在[15000,20000]范围的
select ename'员工姓名',salary '薪资' from t_employee where salary not between 15000 and 20000;
-- 查询薪资高于15000，或者did为1的员工，两者只能满足其一
-- select eid 'id',ename'员工姓名',salary '薪资' from t_employee where (salary>15000 and eid not like 1) or (salary<=15000 and eid  like 1);
select eid 'id',ename'员工姓名',salary '薪资' from t_employee where salary>15000 xor did  = 1;
-- 【NULL 只能用is 判断】
select ename'员工姓名',commission_pct '奖金比例' from t_employee where commission_pct is NULL;
-- 查询奖金比例不为null的员工
select ename'员工姓名',commission_pct '奖金比例' from t_employee where  commission_pct  is not NULL;
-- 查询员工的实发工资，实发工资 = 薪资 + 薪资 * 奖金比例
-- 【NULL参与计算时候要处理】
select ename'员工姓名',salary + salary * ifnull(commission_pct, 0) '实发工资' from t_employee;



/*
-- 答案：
use atguigu;
-- 查询薪资高于15000的员工姓名和薪资
select ename,salary from t_employee where salary>15000;
-- 查询薪资为9000的员工的姓名和薪资
select ename,salary from t_employee where salary=9000;
-- 查询地址不在北苑的
select * from t_employee where address!="北苑";
select * from t_employee where address<>"北苑";
use atguigu;
-- 查询薪资在[10000,15000]
select * from t_employee where salary>=10000 && salary<=15000;
select * from t_employee where salary between 10000 and 15000;
-- 查询薪资不在[10000,15000]
select * from t_employee where salary not between 10000 and 15000;
-- 查询地址在这几个地方的
select * from t_employee where address in ('北苑', '望京', '龙泽');
-- 查询地址不在这几个地方的
select * from t_employee where address not in ('北苑', '望京', '龙泽');
use atguigu;
-- 查询名字有 冰 字的
select * from t_employee where ename like '%冰%';
-- 查询名字以 雨 结尾的
select * from t_employee where ename like '%雨';
-- 查询名字以 李 开头的
select * from t_employee where ename like '李%';
-- 查询名字有 红 这个字，但是 红 的前面只能有1个字
select * from t_employee where ename like '_红%';
-- 查询当前MySQL数据库的字符集情况
show variables like '%character%';
use atguigu;
-- 查询薪资高于15000，并且性别是男的员工
select * from t_employee where salary>15000 and gender='男';
-- 查询薪资高于15000，或者did为1的员工
select * from t_employee where salary>15000 || did = 1;
-- 查询薪资不在[15000,20000]范围的
select * from t_employee where !(salary between 15000 and 20000);
-- 查询薪资高于15000，或者eid为1的员工，两者只能满足其一
select * from t_employee where salary>15000 xor did = 1;
select * from t_employee where (salary>15000) ^ (did = 1);
use atguigu;
-- 查询奖金比例为null的员工
select * from t_employee where commission_pct is null;
select * from t_employee where commission_pct <=> null;
-- 查询奖金比例不为null的员工
select * from t_employee where commission_pct is not null;
-- 查询员工的实发工资，实发工资 = 薪资 + 薪资 * 奖金比例
select ename ,salary , commission_pct, salary + salary * ifnull(commission_pct,0) "实发工资" from t_employee;
*/
-- ### 操作题
-- 1. 假设有一个employees表，包含employee_id（员工编号）、first_name（名字）、
-- last_name（姓氏）、salary（工资）、department_id（部门编号）字段。
-- 编写 SQL 语句，将部门编号为10的员工工资提高 10%。
update employees
set salary = salary * 1.1
where department_id = 10;
-- 2. 假设有一个orders表，包含order_id（订单编号）、customer_id（客户编号）、
-- order_date（订单日期）、order_amount（订单金额）字段。
-- 编写 SQL 语句，计算每个客户的订单总金额，并按总金额从高到低显示客户编号和总金额。   
-- 提示：降序排序用order by  字段1 desc
select customer_id,
    sum(order_amount)
from orders
group by customer_id
order by sum(order_amount) desc;
/*
 **答案**：
 
 ```sql
 UPDATE employees
 SET salary = salary * 1.1
 WHERE department_id = 10;
 ```
 
 **分析**：使用UPDATE语句更新employees表。SET子句将salary字段的值更新为原来的 1.1 倍，即提高 10%。WHERE子句筛选出department_id为10的员工记录，确保只对这些员工的工资进行更新。
 
 2. 假设有一个orders表，包含order_id（订单编号）、customer_id（客户编号）、order_date（订单日期）、order_amount（订单金额）字段。编写 SQL 语句，计算每个客户的订单总金额，并按总金额从高到低显示客户编号和总金额。
 
 **答案**：
 
 ```sql
 SELECT customer_id, SUM(order_amount) AS total_amount
 FROM orders
 GROUP BY customer_id
 ORDER BY total_amount DESC;
 ```
 
 **分析**：使用SELECT语句选择customer_id和通过SUM(order_amount)计算出的每个客户的订单总金额，并将总金额命名为total_amount。FROM子句指定数据源为orders表。GROUP BY customer_id将数据按customer_id分组，以便对每个客户的订单金额进行汇总。最后，ORDER BY total_amount DESC按照总金额从高到低排序，展示结果。
 */
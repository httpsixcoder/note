###
操作题

-- 1. 假设有两个表customers（包含customer_id、customer_name）和
    -- orders（包含order_id、customer_id、order_date）。
    -- 编写 SQL 语句，使用内连接查询出每个客户的姓名及其对应的订单日期。
select c.customer_name,o.order_date
from customers c
join orders o
on c.customer_id=o.customer_id;

-- 2. 假设有products表（包含product_id、product_name、category_id、price）和
    -- categories表（包含category_id、category_name）。
    -- 编写 SQL 语句，使用左外连接查询所有产品类别及其对应的产品名称（如果该类别有产品），
    -- 若某类别没有产品，产品名称显示为 NULL。
select c.category_name,p.product_name
from categories c
left join products p
on c.category_id=p.category_id;


-- 3. 在t_employee表中查询和 白露，谢吉娜同一部门的员工姓名和电话
select ename,tel
from t_employee
where did in(select did from t_employee where ename in('白露','谢吉娜'))



-- 答案：
/*
1. 假设有两个表customers（包含customer_id、customer_name）和orders（包含order_id、customer_id、order_date）。编写 SQL 语句，使用内连接查询出每个客户的姓名及其对应的订单日期。
**答案**：
```sql
SELECT customers.customer_name, orders.order_date
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id;
```
**分析**：使用SELECT语句选择customers表中的customer_name和orders表中的order_date列。通过INNER JOIN将customers表和orders表连接起来，连接条件是两个表中的customer_id相等。这样就可以获取每个客户的姓名及其对应的订单日期，只有当customers表和orders表中有匹配的customer_id时，对应的记录才会出现在结果集中。
2. 假设有products表（包含product_id、product_name、category_id、price）和categories表（包含category_id、category_name）。编写 SQL 语句，使用左外连接查询所有产品类别及其对应的产品名称（如果该类别有产品），若某类别没有产品，产品名称显示为 NULL。
**答案**：
```sql
SELECT categories.category_name, products.product_name
FROM categoriesLEFT JOIN products ON categories.category_id = products.category_id;
```
**分析**：使用SELECT语句选择categories表中的category_name和products表中的product_name列。通过LEFT JOIN将categories表作为左表与products表进行连接，连接条件是两个表中的category_id相等。这样会返回categories表中的所有类别名称，对于有产品的类别，会显示对应的产品名称；对于没有产品的类别，product_name列会显示为 NULL。
*/

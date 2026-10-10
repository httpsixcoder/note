### 操作题
-- 1. 编写 SQL 语句，在 MySQL 中创建一个名为employees的数据库，并在该数据库中创建一个名为staff的表，
-- 表中包含id（整数类型）、name（可变长度字符串，最大长度 50）、salary（浮点数类型）三个字段。
CREATE DATABASE employees;
USE employees;
CREATE TABLE staff(
    id int primary key auto_increment,
    name varchar(50),
    salary float
);
-- 2. 先创建一个名为products的表，
-- 表中包含product_id（整数类型）、
-- product_name（可变长度字符串，最大长度 100）、
-- price（浮点数类型）字段。
-- 编写 SQL 语句，在该表中添加一个名为description的字段，数据类型为可变长度字符串，最大长度 200。
CREATE TABLE products(
    product_id int primary key auto_increment,
    product_name varchar(100),
    price float
);
ALTER TABLE products
ADD COLUMN description varchar(200);
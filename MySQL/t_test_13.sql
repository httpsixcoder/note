-- ALTER TABLE not_null_demo MODIFY COLUMN birthday DATE NOT NULL;
-- 给birthday字段添加非空约束
ALTER TABLE not_null_demo MODIFY COLUMN birthday DATE NOT NULL;-- 删除birthday字段的非空约束
ALTER TABLE not_null_demo MODIFY COLUMN birthday DATE;
DESC not_null_demo;-- 修改name字段的数据类型为varchar(30)，本来想要保留非空约束的
ALTER TABLE not_null_demo MODIFY COLUMN NAME VARCHAR (30);
DESC not_null_demo;-- 删除唯一键约束需要手动删除对应的索引
ALTER TABLE 表名 DROP INDEX 索引名;-- 查看emp表的索引
SHOW
INDEX
FROM
  emp;-- 删除复合唯一键约束
ALTER TABLE xuanke DROP INDEX sid;
DESC xuanke;
SHOW
INDEX
FROM
  xuanke;-- 查看emp表和xuanke表的索引
SHOW
INDEX
FROM
  emp;
SHOW
INDEX
FROM
  xuanke;-- 删除xuanke表的主键约束
ALTER TABLE xuanke DROP PRIMARY KEY;
SHOW
INDEX
FROM
  xuanke;
DESC xuanke;
建表后增加主键约束
ALTER TABLE xuanke
    ADD PRIMARY KEY (sid, cid);
DESC xuanke;-- 删除emp的主键约束
ALTER TABLE emp DROP PRIMARY KEY;
DESC emp;-- 自动把cardid识别为主键，因为cardid定义了唯一键+非空约束，但是不同于真正的主键
SHOW
INDEX
FROM
  emp;-- 给emp表的id字段增加主键约束
ALTER TABLE emp
    ADD PRIMARY KEY (id);
SHOW
INDEX
FROM
  emp;-- 修改emp表 AUTO_INCREMENT 值为8
ALTER TABLE emp AUTO_INCREMENT = 8;
SHOW
CREATE TABLE emp;
-- AUTO_INCREMENT值都不能修改为<当前自增字段最大的值
-- 删除eid字段的自增属性
ALTER TABLE emp MODIFY COLUMN eid INT;
DESC emp;-- 删除emp表的address的默认值约束
ALTER TABLE emp MODIFY COLUMN address VARCHAR (100);
DESC emp;-- 给emp表address增加 不详 默认值
ALTER TABLE emp MODIFY COLUMN address VARCHAR (100) DEFAULT '不详';
DESC emp;-- 删除emp表的age字段的检查约束 emp_chk_1 
-- 删除emp表的hiredate和birthday字段的检查约束 emp_chk_2
ALTER TABLE emp DROP CHECK emp_chk_1;
ALTER TABLE emp DROP CHECK emp_chk_2;
SHOW
CREATE TABLE emp;-- 使用add check给age字段添加检查约束age>=18
ALTER TABLE emp
    ADD CHECK (age >= 18);-- 因为表中有违反(age>=18)的数据，必须先处理
SELECT *
FROM emp;
UPDATE emp
SET age = 26
WHERE age < 18; -- 使用add check给age字段添加检查约束age>=18
ALTER TABLE emp
    ADD CHECK (age >= 18);
INSERT INTO emp
VALUES (NULL, '李四', 6, '1998-5-1', '2021-1-2');
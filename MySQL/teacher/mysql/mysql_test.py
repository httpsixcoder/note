"""
    测试：使用Python代码连接数据库
"""
from threading import current_thread

import pymysql
from pymysql import cursors


def get_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='admin',
            database='atguigu',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor  # 获取结果的方式DictCursor 字典
        )
        return connection
    except Exception as e:
        print("连接失败", e)


# 测试功能
def insert_data():
    # 获取连接对象
    connection = get_connection()
    # 获取cursor对象
    curosr = connection.cursor()
    # 编写SQL
    # sql="insert into t_student values(%s,%s,%s,%s,%s,%s)"
    sql = "insert into t_student values(null,'张三',23,'男','2000-01-01')"
    # 执行 SQL
    curosr.execute(sql)
    # 提交事务
    connection.commit()
    # 关闭 cursor对象
    curosr.close()


def delete_data():
    connection = get_connection()
    cursors = connection.cursor()
    sql = "delete from t_student"
    cursors.execute(sql)
    connection.commit()
    cursors.close()


def select_data():
    connection = get_connection()
    cursors = connection.cursor()
    sql = "select * from t_student"
    cursors.execute(sql)
    result = cursors.fetchall()
    print(result)
    # 默认元组返回
    # 设置DictCursor后，返回字典形式
    cursors.close()


if __name__ == '__main__':
    insert_data()

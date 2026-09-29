# ### 一、选择题
# - 以下哪种异常通常在尝试访问字典中不存在的键时引发？（ A ）
#   A. KeyError	B. IndexError	C. ValueError	D. TypeError
# - 以下关于try - except - finally语句的描述，正确的是（ B ）
#   A. finally块中的代码只有在没有异常发生时才会执行	B. finally块中的代码无论是否发生异常都会执行
#   C. 如果try块中发生异常，except块和finally块都不会执行	D. except块和finally块只能存在一个
# ### 二、编程题
# 1. 编写一段 Python 代码，尝试将字符串 "123abc" 转换为整数，
# 如果转换失败，捕获 ValueError 异常，将异常信息记录到一个文本文件 error.log 中。

try:
    int("123abc")
except ValueError as e:
    with open("error.log","a",encoding="utf-8") as f:
        f.write(str(e))
# 2. 定义一个函数check_age，该函数接受一个年龄参数。
# 如果年龄小于 0，抛出一个自定义异常InvalidAgeError；
# 如果年龄大于 120，抛出UnrealisticAgeError。
# 这两个自定义异常类都继承自Exception类。调用该函数并传入一个不合法的年龄值，捕获并处理异常。
class InvalidAgeError(Exception):
    pass
class UnrealisticAgeError(Exception):
    pass
def check_age(age):
    if age <0 :
        raise InvalidAgeError(f"年龄 {age} 小于 0")
    elif age>120:
        raise UnrealisticAgeError(f"年龄 {age} 大于 120")
    else:
        return f"合法年龄"
list1=[-10,18,666]
for i in list1:
    try:
        check_age(i)
    except InvalidAgeError as e:
        print(e)
    except UnrealisticAgeError as e:
        print(e)
    else:
        print(check_age(i))

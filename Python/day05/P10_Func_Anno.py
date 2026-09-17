"""
    该案例演示了函数的注释
"""
# 普通函数
def dog(name,age,species):
    return(name,age,species)

# 添加了注释的自定义函数
def dog(name:str,age:(1,99),species:'狗的品种') -> tuple:
    return(name,age,species)

# 通过函数.__annotations来查看函数的说明    【函数的注释不具备强制性，可以不按注释传值】
print(dog.__annotations__)
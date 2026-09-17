# 不定长参数
# 形式一：
def fun1(a, *b):
    print(a, b)


fun1(1, 2, 3, 4)  # 1 (2, 3, 4)


def fun2(*a, b):
    print(a, b)


fun2(1, 2, 3, b=4)  # (1, 2, 3) 4


# 形式二：
def fun3(a, **b):
    print(a, b)  # 1 {'b': 2, 'c': 3}


fun3(a=1, b=2, c=3)


# def fun4(**b,c): # 不可以

# 解包传参
def fun4(a, b, c):
    print(a, b, c)


tuple1 = (1, 2, 3)
fun4(1, 2, 3)  # 1 2 3
fun4(*tuple1)  # 1 2 3

dic1 = {'a': 1, 'b': 2, 'c': 3}
fun4(*dic1)  # a b c
fun4(**dic1)  # 1 2 3


# 强制传参类型
def fun5(a, b, c, /, d, e, *, f, g):
    print(a, b, c, d, e, f, g)
# fun5(1,2,3,4,5,6,7) #报错
# fun5(a=1,b=2,c=3,d=4,e=5,f=6,g=7) #报错
fun5(10,20,30,d=4,e=5,f=6,g=7) #10 20 30 4 5 6 7
fun5(10,20,30,4,5,f=6,g=7) #10 20 30 4 5 6 7
# /前必须位置传参
# *后必须关键字传参
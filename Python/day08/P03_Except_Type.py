"""
    该案例演示了处理不同类型的异常
"""

# print(int("abc"))             #ValueError: invalid literal for int() with base 10: 'abc'
# print(3/0)                    #ZeroDivisionError: division by zero
# list1=[1,2,3] print(list1[3]) #SyntaxError: invalid syntax. Did you mean 'in'?
# print(a)                      #NameError: name 'a' is not defined

try:
    print(int("abc"))
except ZeroDivisionError as e:
    print("ZeroDivisionError:",e)
except ValueError as e:
    print("ValueError:",e)
except SyntaxError as e:
    print("SyntaxError:",e)
except:
    print("发生异常了")
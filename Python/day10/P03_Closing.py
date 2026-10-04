"""
    该案例演示了闭包
"""
def outer():
     a,b=10,20
     def inner():
         print(a)
         print(b)
     return inner
ff=outer()
ff()
print(ff.__closure__)
print(ff.__closure__[0].cell_contents)
print(ff.__closure__[1].cell_contents)
"""
    该案例演示了with语句
"""

"""
try:
    file=open("test.txt","w")
    file.write(a)
    file.close()
finally:
    print(file.closed)
"""

"""
# 异常处理
try:
    try:
        file=open("test.txt","w")
        file.write(a)
    except:
        print("异常")
    finally:
        file.close()
finally:
    print(file.closed)
"""

# with 自动释放资源
# try:
#     with open("test.txt","w") as file:
#         file.write(a)
# finally:
#     print(file.closed)
print(type(open("test.txt", "w")))  #<class '_io.TextIOWrapper'>
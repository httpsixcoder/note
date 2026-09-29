num = 100


def add(a, b):
    return a + b

# 在其他文件导入这个模块时运行的是执行运行程序的那个模块的名字
#在当前文件中运行时打印【__main__】
# print(__name__)
if __name__ == "__main__":
    print(add(10,20))
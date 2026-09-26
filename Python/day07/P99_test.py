# 题目1:文件操作-写入文件
# 编写代码创建一个新的文本文件output.txt，并向其中写入字符串"Thisisa test."。
f = open("./output.txt", "w")
f.write("This is a test.")
f.close()
# 编写Python代码从output.txt读取该文件的内容并打印出来。
file = open("./output.txt", 'r')
print(file.read())
file.close()


# 【建议】
# 建议用 with open，可以自动关闭文件，遇到异常也不会漏掉 close()：
# with open("./output.txt", "w", encoding="utf-8") as f:
# f.write("This is a test.")
# with open("./output.txt", "r", encoding="utf-8") as f:
# print(f.read())
# 题目2:面向对象-类与对象基础
# 定义一个名为Dog的类，该类有两个属性name(名字)和age(年龄)，
# 以及一个方法bark(叫)bark方法打印出 "Woof! My name is [name] and I am [age] years old."。
# 创建一个Dog类的对象,并调用 bark 方法。
class Dog:
    """狗类"""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"Woof! My name is {self.name} and I am {self.age} years old.")


dog1 = Dog("旺财", 3)
dog1.bark()
# 题目3:面向对象-对象属性访问
# 基于上一题的Dog类，创建一个Dog对象，然后修改其age属性的值，并再次调用bark方法查看输出变化。
dog2 = Dog("大黄", 5)
dog2.bark()
dog2.age = 6
dog2.bark()

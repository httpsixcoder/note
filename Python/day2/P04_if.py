# 单分支
"""
price = 50
balance = float(input("请输入价钱"))
print(f"当前余额为{balance}")
if balance < price:
    print("余额不足")
print("欢迎下次光临")
"""
from random import randint

# from random import randint
# price = 50
# balance = randint(1, 100)
# print(f"当前余额为{balance}")
# if balance < price:
#     print("余额不足")
# print("欢迎下次光临")

# 双分支
# from random import randint
# price = 50
# balance = randint(1, 100)
# print(f"当前余额为{balance}")
# if balance < price:
#     print("余额不足")
# else:
#     print("消费成功")
# print("欢迎下次光临")

# 多分支
week = randint(1, 7)
print(week)
if week == 1:
    print("今天周一")
elif week == 2:
    print("今天周二")
elif week == 3:
    print("今天周三")
elif week == 4:
    print("今天周四")
elif week == 5:
    print("今天周五")
elif week == 6:
    print("今天周六")
else:
    print("今天周日")
print("美好的一天")

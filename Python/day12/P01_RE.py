
# # 15.8.1 匹配电话号码
# import re
#
# test = [
#     "13812345678",  # 合法
#     "11456817239",  # 非法
#     "19912345678",  # 合法
#     "17138412356",  # 合法
#     "1234567890",  # 非法
#     "14752345673",  # 合法
#     "1800123456",  # 非法
# ]
#
# # 以1开头，第二位为3，4，5，7，8，9，后面是9位数字
# pattern = r"^1[35789]\d{9}$"
#
#
# for i in test:
#     print(f"{i:20}{"合法" if re.match(pattern, i) else "非法"}")

# import re
#
# test = [
#     "example@example.com",
#     "user.name@subdomain.example.co",
#     "username@.com",
#     "@missingusername.com",
#     "-dasd@qq.com",
# ]
# # 匹配邮箱  [xxx@xxx.xx]  \.转义
# pattern = r"[\w!#$%&'*+-/=?^`{|}~.]+@[\w!#$%&'*+-/=?^`{|}~.]+\.[a-zA-Z]{2,}$"
# for i in test:
#     print(f"{i:40}{"合法" if re.match(pattern, i) else "非法"}")


# # 0-255
# import re
#
# test = ["0", "9", "50", "100", "199", "200", "255", "256", "-1", "01", "001"]
# # 十位为1-9，?表示可以没有十位，个位是0-9
# # 或 百位是1，十位是0-9，个位是0-9
# # 或 百位是2，十位是0-4，个位是0-9
# # 或 百位是2，十位是5，个位是0-5
# pattern = r"^([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])$"
# for num in test:
# print(f"{num:5} {"合法" if re.match(pattern, num) else "非法"}")


import re

test = """<link rel="alternate" hreflang="zh" href="https://zh.wikipedia.org/wiki/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F">
<link rel="alternate" hreflang="zh-Hans" href="https://zh.wikipedia.org/zh-hans/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F">
<link rel="alternate" hreflang="zh-Hans-CN" href="https://zh.wikipedia.org/zh-cn/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F">
<link rel="alternate" hreflang="zh-Hans-MY" href="https://zh.wikipedia.org/zh-my/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F">
<link rel="alternate" hreflang="zh-Hans-SG" href="https://zh.wikipedia.org/zh-sg/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F">
<link rel="alternate" hreflang="zh-Hant" href="https://zh.wikipedia.org/zh-hant/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F">
<link rel="alternate" hreflang="zh-Hant-HK" href="https://zh.wikipedia.org/zh-hk/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F">
<link rel="alternate" hreflang="zh-Hant-MO" href="https://zh.wikipedia.org/zh-mo/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F">
<link rel="alternate" hreflang="zh-Hant-TW" href="https://zh.wikipedia.org/zh-tw/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F">
<link rel="alternate" hreflang="x-default" href="https://zh.wikipedia.org/wiki/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F">"""

# 获取所有href中网址
pattern = r"href=\"(.+?)\""
for i in re.findall(pattern, test):
    print(i)

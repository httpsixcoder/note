"""
    该案例演示了文件的读写操作
"""
"""
# 向磁盘文件写入数据
# 建立和磁盘文件的连接（通道）
file= open("test.txt","a")
# 写入数据
file.write("中国Hello, Python!\n")
file.write("hello python\n")
# 关闭连接
file.close()
"""
# 从文件中读取数据
# 打开文件
file= open("test.txt","rt")
# 读取数据
# read()    读取文件全部内容
# content=file.read()
# read(size)    读取文件指定大小的内容
#       如果编码方式是t,那么size表示字符数,
#       如果编码方式是b,那么size表示读取的是字节数
# content=file.read(8)

# readline  读取文件的一行数据
# print(file.readlines())
# 读取文件指定大小的内容
# print(file.realine(8))

# 读取文件的所有行数据,放在列表中
# print(file.readlines())
# print(file.readlines(8)) #大约不确定

# 关闭连接
file.close()


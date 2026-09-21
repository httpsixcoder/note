"""
    该案例演示了文件的拷贝
"""
"""
# 方案一:读取整个文件

def copy_file(source_file_path, target_file_path):
    # 建立连接
    source_file=open(source_file_path,'rb')
    target_file=open(target_file_path,'wb')

    content=source_file.read()
    target_file.write(content)

    source_file.close()
    target_file.close()

# copy_file("F:\\1.png","E:\\2.png")
# copy_file("F:/1.png","E:/2.png")
copy_file(r"F:\1.png",r"E:\2.png")
"""
# 方案二:边读边写
def copy_file(source_file_path, target_file_path):
    # 建立连接
    source_file=open(source_file_path,'rb')
    target_file=open(target_file_path,'wb')

    # content=source_file.read(1024)
    # while content:
    #     target_file.write(content)
    #     # 迭代,读取位置会自动向后刷新
    #     content=source_file.read(1024)

    while content := source_file.read(1024):
        target_file.write(content)
        # 迭代,读取位置会自动向后刷新

    source_file.close()
    target_file.close()

copy_file(r"F:\1.png",r"E:\2.png")
# 构建Python自定义镜像
# 1. 指定基础镜像：Python 3.12（稳定版，兼容性好）
FROM python:3.12

# 2. 设置容器内的工作目录，用于存放脚本和依赖
WORKDIR /app

# 3. 复制本地项目目录下的所有文件（test_mysql.py、Dockerfile等），到容器的/app目录
COPY . /app

# 4. 安装Python依赖（pymysql），使用清华源加速下载，避免超时（初学者无需修改）
RUN pip install pymysql cryptography 

# 5. 容器启动时，自动执行的命令：运行Python连接脚本
CMD ["python", "test_mysql1.py"]
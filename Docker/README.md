# 🐳 Docker 学习笔记 (Docker Study Notes)

> 📢 **学习声明**：本笔记的知识体系、大纲脉络与案例演示，**学习课程源于尚硅谷 (Atguigu) 的 Docker 课程**。在此特别感谢尚硅谷老师的悉心教导，本仓库仅为个人学习过程中的知识点梳理、踩坑记录与心得沉淀。

这里记录了我学习 Docker 过程中的知识点梳理、踩坑记录与心得。欢迎各位前辈和大神交流指正！

## 📖 目录
- [1.Docker 概述与环境搭建](#1.docker概述与环境搭建)
- [2.镜像与容器基础](#2.镜像与容器基础)
- [3.Dockerfile 详解](#3.dockerfile详解)
- [4.数据卷与网络](#4.数据卷与网络)
- [5.Docker Compose](#5.docker-compose)
- [6实战部署](#6.实战部署)

---

# 1.Docker 概述与环境搭建

## 1. Docker 简介
- **Docker 是什么**：一个开源的**容器化平台**，把应用及其依赖打包到一个轻量级、可移植的容器中。
- **Docker 和虚拟机的区别**：
  - 虚拟机：模拟完整操作系统，占用资源多，启动慢。
  - Docker：共享宿主机内核，占用资源少，秒级启动。
- **Docker 的核心概念**：
  - **镜像（Image）**：只读模板，用来创建容器。
  - **容器（Container）**：镜像的运行实例，可启动、停止、删除。
  - **仓库（Registry）**：存放镜像的地方，如 Docker Hub、阿里云镜像仓库。

## 2. Docker 安装
- **官方安装文档**：`https://docs.docker.com/engine/install/`
- **Ubuntu 安装步骤**：
  ```bash
  # 卸载旧版本
  sudo apt remove docker docker-engine docker.io containerd runc
  
  # 安装依赖
  sudo apt update
  sudo apt install ca-certificates curl gnupg lsb-release
  
  # 添加 Docker 官方 GPG 密钥
  sudo mkdir -p /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  
  # 设置仓库
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
  # 安装 Docker
  sudo apt update
  sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
  ```

- **验证安装**：

    ```bash
    docker version
    docker info
    ```

- **配置国内镜像加速**：

    ```bash
    sudo mkdir -p /etc/docker
    sudo tee /etc/docker/daemon.json <<-'EOF'
    {
      "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
    }
    EOF
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    ```

## 3. Docker 服务管理

```bash
# 启动 Docker
sudo systemctl start docker

# 停止 Docker
sudo systemctl stop docker

# 重启 Docker
sudo systemctl restart docker

# 开机自启
sudo systemctl enable docker

# 查看状态
sudo systemctl status docker
```

## 4. Docker 免 sudo

```bash
# 将当前用户加入 docker 组
sudo usermod -aG docker $USER

# 重新登录或执行
newgrp docker
```

------

# 2.镜像与容器基础

## 1. 镜像操作

| 命令             | 作用             | 示例                             |
| ---------------- | ---------------- | -------------------------------- |
| `docker images`  | 列出本地镜像     | `docker images`                  |
| `docker pull`    | 拉取镜像         | `docker pull nginx`              |
| `docker rmi`     | 删除镜像         | `docker rmi nginx`               |
| `docker tag`     | 给镜像打标签     | `docker tag nginx mynginx:v1`    |
| `docker save`    | 导出镜像         | `docker save -o nginx.tar nginx` |
| `docker load`    | 导入镜像         | `docker load -i nginx.tar`       |
| `docker inspect` | 查看镜像详情     | `docker inspect nginx`           |
| `docker history` | 查看镜像构建历史 | `docker history nginx`           |

## 2. 容器操作

| 命令             | 作用                 | 示例                            |
| ---------------- | -------------------- | ------------------------------- |
| `docker run`     | 创建并启动容器       | `docker run -d -p 80:80 nginx`  |
| `docker ps`      | 查看运行中的容器     | `docker ps`                     |
| `docker ps -a`   | 查看所有容器         | `docker ps -a`                  |
| `docker start`   | 启动容器             | `docker start 容器ID`           |
| `docker stop`    | 停止容器             | `docker stop 容器ID`            |
| `docker restart` | 重启容器             | `docker restart 容器ID`         |
| `docker rm`      | 删除容器             | `docker rm 容器ID`              |
| `docker exec`    | 进入容器执行命令     | `docker exec -it 容器ID bash`   |
| `docker logs`    | 查看容器日志         | `docker logs -f 容器ID`         |
| `docker cp`      | 宿主机与容器互传文件 | `docker cp a.txt 容器ID:/root/` |
| `docker inspect` | 查看容器详情         | `docker inspect 容器ID`         |

## 3. `docker run` 常用参数

| 参数                     | 作用         |
| ------------------------ | ------------ |
| `-d`                     | 后台运行     |
| `-it`                    | 交互式终端   |
| `-p 宿主机端口:容器端口` | 端口映射     |
| `-v 宿主机目录:容器目录` | 数据卷挂载   |
| `--name 容器名`          | 指定容器名   |
| `--restart=always`       | 自动重启     |
| `-e 环境变量=值`         | 设置环境变量 |
| `--network 网络名`       | 指定网络     |

## 4. 常用示例

```bash
# 启动 nginx
docker run -d --name mynginx -p 80:80 nginx

# 启动 MySQL
docker run -d --name mysql \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=123456 \
  mysql:8.0

# 进入容器
docker exec -it mynginx bash

# 查看日志
docker logs -f mynginx
```

------

# 3.Dockerfile 详解

## 1. Dockerfile 是什么

Dockerfile 是一个**文本文件**，包含了一系列构建镜像的指令。通过 `docker build` 命令可以构建镜像。

## 2. 常用指令

| 指令         | 作用                            |
| ------------ | ------------------------------- |
| `FROM`       | 指定基础镜像                    |
| `RUN`        | 构建时执行命令                  |
| `COPY`       | 复制文件到镜像                  |
| `ADD`        | 复制文件（支持 URL 和自动解压） |
| `WORKDIR`    | 设置工作目录                    |
| `ENV`        | 设置环境变量                    |
| `EXPOSE`     | 暴露端口                        |
| `CMD`        | 容器启动时的默认命令            |
| `ENTRYPOINT` | 容器启动时的入口命令            |
| `VOLUME`     | 声明数据卷                      |
| `USER`       | 指定运行用户                    |
| `ARG`        | 构建参数                        |
| `LABEL`      | 添加元数据                      |

## 3. `CMD` vs `ENTRYPOINT`

| 对比       | `CMD`                              | `ENTRYPOINT` |
| ---------- | ---------------------------------- | ------------ |
| 是否被覆盖 | 可以被 `docker run` 后面的命令覆盖 | 不会被覆盖   |
| 用途       | 提供默认命令                       | 提供固定入口 |
| 推荐组合   | `ENTRYPOINT` + `CMD` 一起用        | 同上         |

## 4. 示例：构建 Python 应用镜像

```dockerfile
# 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 5. 构建镜像

```bash
# 构建
docker build -t myapp:v1 .

# 查看
docker images | grep myapp

# 运行
docker run -d -p 8000:8000 myapp:v1
```

## 6. 构建优化

- **减少层数**：多个 `RUN` 命令用 `&&` 合并。
- **利用缓存**：把不常变的层放前面。
- **多阶段构建**：用多个 `FROM` 减小镜像体积。
- **.dockerignore**：排除不需要的文件（如 `.git`、`__pycache__`）。

```dockerfile
# 多阶段构建示例
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

------

# 4.数据卷与网络

## 1. 数据卷（Volume）

**作用**：让容器内的数据持久化，容器删了数据还在。

| 类型         | 说明                                                    |
| ------------ | ------------------------------------------------------- |
| **匿名卷**   | `docker run -v /容器路径`，Docker 自动分配宿主机路径    |
| **具名卷**   | `docker run -v 卷名:/容器路径`，用 `docker volume` 管理 |
| **绑定挂载** | `docker run -v /宿主机路径:/容器路径`，直接挂宿主机目录 |

## 2. 数据卷命令

| 命令                         | 作用           |
| ---------------------------- | -------------- |
| `docker volume create 卷名`  | 创建数据卷     |
| `docker volume ls`           | 列出所有数据卷 |
| `docker volume inspect 卷名` | 查看卷详情     |
| `docker volume rm 卷名`      | 删除数据卷     |
| `docker volume prune`        | 清理未使用的卷 |

## 3. 挂载示例

```bash
# 具名卷
docker run -d --name mysql \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=123456 \
  mysql:8.0

# 绑定挂载（开发常用）
docker run -d --name myapp \
  -v $(pwd):/app \
  -p 8000:8000 \
  myapp:v1
```

## 4. Docker 网络

| 网络类型        | 说明                       |
| --------------- | -------------------------- |
| `bridge`        | 默认，容器间通过 IP 通信   |
| `host`          | 共享宿主机网络             |
| `none`          | 无网络                     |
| `overlay`       | 跨主机通信（Swarm）        |
| `自定义 bridge` | 推荐，容器间可用容器名通信 |

## 5. 网络命令

```bash
# 创建网络
docker network create mynet

# 列出网络
docker network ls

# 查看详情
docker network inspect mynet

# 容器连接网络
docker network connect mynet 容器ID

# 删除网络
docker network rm mynet
```

## 6. 容器间通信示例

```bash
# 创建网络
docker network create app-net

# 启动 MySQL
docker run -d --name mysql --network app-net \
  -e MYSQL_ROOT_PASSWORD=123456 mysql:8.0

# 启动应用（通过容器名访问 MySQL）
docker run -d --name myapp --network app-net \
  -e DB_HOST=mysql myapp:v1
```

------

# 5.Docker Compose

## 1. Compose 是什么

用一个 **YAML 文件**定义多个容器，一条命令批量管理。

## 2. 安装

```bash
# Docker Compose v2 已集成到 Docker 中
docker compose version
```

## 3. `docker-compose.yml` 示例

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: 123456
      MYSQL_DATABASE: atguigu
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - app-net

  redis:
    image: redis:7
    container_name: redis
    restart: always
    ports:
      - "6379:6379"
    networks:
      - app-net

  app:
    build: .
    container_name: myapp
    restart: always
    ports:
      - "8000:8000"
    environment:
      DB_HOST: mysql
      REDIS_HOST: redis
    depends_on:
      - mysql
      - redis
    networks:
      - app-net

volumes:
  mysql-data:

networks:
  app-net:
```

## 4. 常用命令

| 命令                              | 作用           |
| --------------------------------- | -------------- |
| `docker compose up -d`            | 启动所有服务   |
| `docker compose down`             | 停止并删除容器 |
| `docker compose ps`               | 查看服务状态   |
| `docker compose logs -f`          | 查看日志       |
| `docker compose restart`          | 重启服务       |
| `docker compose build`            | 重新构建镜像   |
| `docker compose pull`             | 拉取最新镜像   |
| `docker compose exec 服务名 bash` | 进入容器       |

## 5. Compose 常用字段

| 字段          | 作用                       |
| ------------- | -------------------------- |
| `image`       | 使用的镜像                 |
| `build`       | 构建镜像的 Dockerfile 路径 |
| `ports`       | 端口映射                   |
| `volumes`     | 数据卷挂载                 |
| `environment` | 环境变量                   |
| `depends_on`  | 依赖关系                   |
| `networks`    | 网络                       |
| `restart`     | 重启策略                   |

------

# 6.实战部署

## 1. 部署 FastAPI 应用

```yaml
version: '3.8'

services:
  fastapi:
    build: .
    ports:
      - "8000:8000"
    environment:
      DB_HOST: mysql
      DB_PORT: 3306
      DB_USER: root
      DB_PASSWORD: 123456
      DB_NAME: atguigu
    depends_on:
      - mysql
    networks:
      - app-net

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: 123456
      MYSQL_DATABASE: atguigu
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - app-net

volumes:
  mysql-data:

networks:
  app-net:
```

## 2. 部署 Nginx + 前端

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./dist:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/nginx.conf
    restart: always
```

## 3. 常见部署命令

```bash
# 拉取代码
git pull

# 构建并启动
docker compose up -d --build

# 查看日志
docker compose logs -f

# 滚动更新
docker compose up -d --no-deps --build app
```

## 4. 生产环境建议

- **镜像标签**：用具体版本号，不用 `latest`。
- **资源限制**：设置 `mem_limit`、`cpus`。
- **日志管理**：配置 `logging` 驱动，避免磁盘爆满。
- **健康检查**：用 `healthcheck` 监控服务状态。
- **数据备份**：定期备份数据卷。
- **安全加固**：非 root 用户运行容器。

------

*持续更新中，欢迎指点。*⭐
# Gunicorn 部署指南

> 本指南面向 Python 初学者，用于将 Flask 应用部署到生产环境

---

## 📌 知识点说明

- 🔴 **【必须掌握】** - 部署前必须理解和掌握
- 🟡 **【重要】** - 部署后需要了解，用于维护和优化
- 🟢 **【可选】** - 进阶知识，后续深入学习

---

## 一、Gunicorn 是什么 🔴【必须掌握】

### 1.1 WSGI 服务器概念

**WSGI**（Web Server Gateway Interface）是 Python Web 应用程序和 Web 服务器之间的标准接口。

```
为什么需要 Gunicorn？

Flask 自带的开发服务器 (app.run()):
├── ❌ 单线程，一次只能处理一个请求
├── ❌ 性能低，不适合高并发
├── ❌ 不够稳定，可能崩溃
└── ❌ 官方明确说明：不要用于生产环境

Gunicorn (Green Unicorn):
├── ✅ 多进程，可同时处理多个请求
├── ✅ 高性能，支持高并发
├── ✅ 稳定可靠，自动重启崩溃的进程
└── ✅ 生产环境标准选择
```

### 1.2 架构理解

```
生产环境典型架构:

用户请求 → Nginx (Web服务器) → Gunicorn (WSGI服务器) → Flask (应用)
               ↓
          静态文件直接返回

Nginx 职责:
- 处理静态文件
- SSL/HTTPS
- 负载均衡
- 反向代理

Gunicorn 职责:
- 运行 Python 应用
- 管理多个工作进程
- 处理请求并发
```

---

## 二、安装 Gunicorn 🔴【必须掌握】

### 2.1 安装方式

```bash
# 确保在虚拟环境中
source venv/bin/activate

# 使用 pip 安装
pip install gunicorn

# 验证安装
gunicorn --version
# 输出示例: gunicorn (version 21.2.0)
```

### 2.2 添加到 requirements.txt

```bash
# 更新 requirements.txt
pip freeze > requirements.txt

# 或手动添加
echo "gunicorn==21.2.0" >> requirements.txt
```

---

## 三、基本使用 🔴【必须掌握】

### 3.1 最简单的启动方式

```bash
# 进入项目目录
cd /var/www/ecommerce_knowledge

# 激活虚拟环境
source venv/bin/activate

# 启动 Gunicorn
gunicorn app:app

# 解释: gunicorn 模块名:应用实例名
# app:app 表示 app.py 文件中的 app 变量
```

### 3.2 常用启动参数

```bash
# 指定绑定地址和端口
gunicorn -b 127.0.0.1:5000 app:app

# 指定工作进程数
gunicorn -w 4 -b 127.0.0.1:5000 app:app

# 后台运行（守护进程模式）
gunicorn -D -w 4 -b 127.0.0.1:5000 app:app

# 指定日志文件
gunicorn -w 4 -b 127.0.0.1:5000 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    app:app
```

### 3.3 常用参数说明

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--bind` | `-b` | 绑定地址和端口 | `-b 127.0.0.1:5000` |
| `--workers` | `-w` | 工作进程数 | `-w 4` |
| `--daemon` | `-D` | 后台运行 | `-D` |
| `--timeout` | `-t` | 请求超时时间(秒) | `-t 120` |
| `--access-logfile` | | 访问日志路径 | `--access-logfile -` |
| `--error-logfile` | | 错误日志路径 | `--error-logfile -` |
| `--reload` | | 代码变更自动重载 | `--reload` |
| `--preload` | | 预加载应用 | `--preload` |

---

## 四、配置文件 🟡【重要】

### 4.1 创建配置文件

使用配置文件可以避免每次输入大量参数。

```bash
# 创建配置文件
nano /var/www/ecommerce_knowledge/gunicorn_config.py
```

### 4.2 配置文件示例

```python
# gunicorn_config.py
# Gunicorn 配置文件

import multiprocessing

# ==================== 基本配置 ====================

# 绑定地址和端口
bind = "127.0.0.1:5000"

# 工作进程数量
# 推荐公式: (2 × CPU核心数) + 1
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
# sync: 同步模式（默认）
# gevent: 协程模式（需要安装 gevent）
# eventlet: 协程模式（需要安装 eventlet）
worker_class = "sync"

# 每个工作进程的线程数
threads = 2

# ==================== 超时配置 ====================

# 请求超时时间（秒）
timeout = 120

# 优雅关闭超时时间
graceful_timeout = 30

# 保持连接超时时间
keepalive = 5

# ==================== 日志配置 ====================

# 访问日志
accesslog = "/var/log/gunicorn/access.log"

# 错误日志
errorlog = "/var/log/gunicorn/error.log"

# 日志级别: debug, info, warning, error, critical
loglevel = "info"

# 访问日志格式
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# ==================== 进程配置 ====================

# 守护进程模式（不建议在 systemd 下使用）
daemon = False

# PID 文件
pidfile = "/var/run/gunicorn/ecommerce.pid"

# 用户和组
user = "www-data"
group = "www-data"

# ==================== 性能优化 ====================

# 工作进程处理的最大请求数（之后重启）
max_requests = 1000

# 在 max_requests 基础上增加随机值，避免所有进程同时重启
max_requests_jitter = 50

# 预加载应用（节省内存，但不支持代码热重载）
preload_app = True
```

### 4.3 使用配置文件启动

```bash
# 使用配置文件启动
gunicorn -c gunicorn_config.py app:app

# 或指定完整路径
gunicorn -c /var/www/ecommerce_knowledge/gunicorn_config.py app:app
```

---

## 五、工作进程数量优化 🟡【重要】

### 5.1 计算公式

```python
# 推荐公式
workers = (2 × CPU核心数) + 1

# 查看 CPU 核心数
import multiprocessing
print(multiprocessing.cpu_count())
```

### 5.2 不同配置场景

```bash
# 1核 CPU 服务器
workers = 3

# 2核 CPU 服务器
workers = 5

# 4核 CPU 服务器
workers = 9

# 内存受限的小型服务器（1GB RAM）
workers = 2-3
```

### 5.3 检查服务器配置

```bash
# 查看 CPU 核心数
nproc
# 或
cat /proc/cpuinfo | grep processor | wc -l

# 查看内存
free -h

# 简单估算：每个 Gunicorn 工作进程约占用 30-100MB 内存
```

---

## 六、日志配置 🟡【重要】

### 6.1 创建日志目录

```bash
# 创建日志目录
sudo mkdir -p /var/log/gunicorn

# 设置权限
sudo chown www-data:www-data /var/log/gunicorn
```

### 6.2 日志级别说明

| 级别 | 说明 | 使用场景 |
|------|------|----------|
| `debug` | 调试信息 | 开发调试 |
| `info` | 一般信息 | 生产环境推荐 |
| `warning` | 警告信息 | 生产环境 |
| `error` | 错误信息 | 只关注错误 |
| `critical` | 严重错误 | 极少使用 |

### 6.3 查看日志

```bash
# 查看访问日志
tail -f /var/log/gunicorn/access.log

# 查看错误日志
tail -f /var/log/gunicorn/error.log

# 搜索错误
grep "error" /var/log/gunicorn/error.log
grep "500" /var/log/gunicorn/access.log
```

---

## 七、进程管理 🔴【必须掌握】

### 7.1 手动管理进程

```bash
# 启动（前台运行）
gunicorn -c gunicorn_config.py app:app

# 启动（后台运行）
gunicorn -D -c gunicorn_config.py app:app

# 查看进程
ps aux | grep gunicorn

# 优雅关闭（发送 SIGTERM）
kill -TERM 主进程PID

# 强制关闭（发送 SIGKILL）
kill -9 主进程PID

# 重启工作进程
kill -HUP 主进程PID
```

### 7.2 进程信号说明

| 信号 | 命令 | 作用 |
|------|------|------|
| TERM | `kill -TERM PID` | 优雅关闭 |
| HUP | `kill -HUP PID` | 重载配置，重启工作进程 |
| USR1 | `kill -USR1 PID` | 重新打开日志文件 |
| USR2 | `kill -USR2 PID` | 热升级（无缝重启） |
| QUIT | `kill -QUIT PID` | 优雅关闭 |

### 7.3 使用 PID 文件

```bash
# 配置中设置 pidfile 后
pidfile = "/var/run/gunicorn/ecommerce.pid"

# 创建 PID 目录
sudo mkdir -p /var/run/gunicorn
sudo chown www-data:www-data /var/run/gunicorn

# 根据 PID 文件操作
kill -HUP $(cat /var/run/gunicorn/ecommerce.pid)
```

---

## 八、与 systemd 集成 🔴【必须掌握】

> 详细内容请参考 《systemd服务管理指南.md》

### 8.1 快速配置

```bash
# 创建服务文件
sudo nano /etc/systemd/system/ecommerce.service
```

```ini
[Unit]
Description=Gunicorn instance to serve ecommerce knowledge
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ecommerce_knowledge
Environment="PATH=/var/www/ecommerce_knowledge/venv/bin"
ExecStart=/var/www/ecommerce_knowledge/venv/bin/gunicorn -c gunicorn_config.py app:app
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 8.2 启用服务

```bash
# 重新加载 systemd 配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start ecommerce

# 设置开机自启
sudo systemctl enable ecommerce

# 查看状态
sudo systemctl status ecommerce
```

---

## 九、性能优化 🟢【可选】

### 9.1 使用异步工作进程

```bash
# 安装 gevent
pip install gevent

# 配置使用 gevent
worker_class = "gevent"
worker_connections = 1000  # 每个工作进程的最大并发连接
```

### 9.2 使用 eventlet

```bash
# 安装 eventlet
pip install eventlet

# 配置使用 eventlet
worker_class = "eventlet"
worker_connections = 1000
```

### 9.3 预加载应用

```python
# gunicorn_config.py
preload_app = True  # 预加载应用，减少内存使用

# 注意：预加载后，代码更改需要重启服务，不能热重载
```

---

## 十、常见问题排查 🟡【重要】

### 10.1 启动失败

```bash
# 问题：ModuleNotFoundError
# 原因：虚拟环境未激活或依赖未安装
# 解决：
source venv/bin/activate
pip install -r requirements.txt

# 问题：Address already in use
# 原因：端口被占用
# 解决：
ss -tlnp | grep 5000
kill -9 占用的PID
```

### 10.2 502 Bad Gateway

```bash
# 检查 Gunicorn 是否运行
ps aux | grep gunicorn

# 检查日志
tail -50 /var/log/gunicorn/error.log

# 检查端口监听
ss -tlnp | grep 5000
```

### 10.3 超时问题

```python
# gunicorn_config.py
# 增加超时时间
timeout = 300  # 5分钟

# 或启动时指定
# gunicorn -t 300 -w 4 -b 127.0.0.1:5000 app:app
```

### 10.4 内存问题

```python
# gunicorn_config.py
# 定期重启工作进程，释放内存
max_requests = 1000
max_requests_jitter = 50

# 减少工作进程数
workers = 2
```

---

## 十一、完整部署示例

### 11.1 目录结构

```
/var/www/ecommerce_knowledge/
├── app.py                    # Flask 应用
├── gunicorn_config.py        # Gunicorn 配置
├── requirements.txt          # Python 依赖
├── venv/                     # 虚拟环境
├── static/                   # 静态文件
│   ├── css/
│   ├── js/
│   └── images/
└── templates/                # 模板文件
```

### 11.2 部署步骤

```bash
# 1. 创建项目目录
sudo mkdir -p /var/www/ecommerce_knowledge

# 2. 上传项目文件
scp -r ecommerce_knowledge/* root@服务器IP:/var/www/ecommerce_knowledge/

# 3. 创建虚拟环境
cd /var/www/ecommerce_knowledge
python3 -m venv venv
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt
pip install gunicorn

# 5. 创建日志目录
sudo mkdir -p /var/log/gunicorn
sudo chown www-data:www-data /var/log/gunicorn

# 6. 创建 Gunicorn 配置
nano gunicorn_config.py

# 7. 测试运行
gunicorn -c gunicorn_config.py app:app

# 8. 设置权限
sudo chown -R www-data:www-data /var/www/ecommerce_knowledge

# 9. 配置 systemd 服务
sudo nano /etc/systemd/system/ecommerce.service

# 10. 启动服务
sudo systemctl daemon-reload
sudo systemctl start ecommerce
sudo systemctl enable ecommerce
```

---

## 📋 命令速查表

| 操作 | 命令 | 重要程度 |
|------|------|----------|
| 安装 | `pip install gunicorn` | 🔴必须 |
| 基本启动 | `gunicorn app:app` | 🔴必须 |
| 指定端口 | `gunicorn -b 127.0.0.1:5000 app:app` | 🔴必须 |
| 多进程 | `gunicorn -w 4 -b 127.0.0.1:5000 app:app` | 🔴必须 |
| 使用配置 | `gunicorn -c config.py app:app` | 🟡重要 |
| 后台运行 | `gunicorn -D -c config.py app:app` | 🟡重要 |
| 查看进程 | `ps aux \| grep gunicorn` | 🔴必须 |
| 优雅停止 | `kill -TERM PID` | 🔴必须 |
| 重载配置 | `kill -HUP PID` | 🟡重要 |

---

*更新日期：2026-01-02*



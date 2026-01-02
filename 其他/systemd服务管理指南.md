# systemd 服务管理指南

> 本指南面向 Python 初学者，用于将 Flask 应用配置为系统服务

---

## 📌 知识点说明

- 🔴 **【必须掌握】** - 部署前必须理解和掌握
- 🟡 **【重要】** - 部署后需要了解，用于维护和优化
- 🟢 **【可选】** - 进阶知识，后续深入学习

---

## 一、systemd 是什么 🔴【必须掌握】

### 1.1 基本概念

**systemd** 是现代 Linux 系统的初始化系统和服务管理器。

```
systemd 的作用:
├── 系统启动管理
├── 服务（Service）管理
├── 日志管理（journald）
├── 定时任务（Timer）
└── 网络管理

为什么需要 systemd 管理 Gunicorn？
├── ✅ 开机自动启动应用
├── ✅ 应用崩溃自动重启
├── ✅ 统一的服务管理命令
├── ✅ 集中的日志管理
└── ✅ 简化运维操作
```

### 1.2 服务 vs 进程

```
手动运行 Gunicorn:
├── 终端关闭，进程停止
├── 服务器重启，需要手动启动
├── 进程崩溃，不会自动恢复
└── 日志分散，不易管理

使用 systemd 服务:
├── 终端关闭，服务继续运行
├── 服务器重启，自动启动
├── 服务崩溃，自动重启
└── 日志统一管理（journalctl）
```

---

## 二、服务文件基础 🔴【必须掌握】

### 2.1 服务文件位置

```bash
# 系统服务目录（系统自带服务）
/lib/systemd/system/

# 管理员自定义服务目录（推荐）
/etc/systemd/system/

# 用户级服务目录
~/.config/systemd/user/
```

### 2.2 创建服务文件

```bash
# 创建服务文件
sudo nano /etc/systemd/system/ecommerce.service
```

### 2.3 服务文件结构

```ini
# 服务文件由三个主要部分组成

[Unit]
# 服务描述和依赖关系

[Service]
# 服务执行配置

[Install]
# 服务安装配置
```

---

## 三、完整服务配置 🔴【必须掌握】

### 3.1 Flask + Gunicorn 服务配置

```ini
# /etc/systemd/system/ecommerce.service

[Unit]
# 服务描述
Description=Gunicorn instance to serve Ecommerce Knowledge Website

# 服务文档地址（可选）
Documentation=https://github.com/your-repo

# 依赖关系：在网络服务启动后启动
After=network.target

# 可选：依赖其他服务
# Requires=redis.service
# After=redis.service mysql.service

[Service]
# 运行用户和组
User=www-data
Group=www-data

# 工作目录
WorkingDirectory=/var/www/ecommerce_knowledge

# 环境变量
Environment="PATH=/var/www/ecommerce_knowledge/venv/bin"
Environment="FLASK_ENV=production"

# 启动命令
ExecStart=/var/www/ecommerce_knowledge/venv/bin/gunicorn -c gunicorn_config.py app:app

# 重载命令（发送 HUP 信号）
ExecReload=/bin/kill -HUP $MAINPID

# 停止命令（可选，默认发送 SIGTERM）
ExecStop=/bin/kill -TERM $MAINPID

# 重启策略：always=总是重启, on-failure=失败时重启
Restart=always

# 重启间隔时间（秒）
RestartSec=5

# 启动超时时间
TimeoutStartSec=60

# 停止超时时间
TimeoutStopSec=30

# 标准输出日志处理
StandardOutput=journal
StandardError=journal

# 系统日志标识
SyslogIdentifier=ecommerce

[Install]
# 设置为多用户模式下启动
WantedBy=multi-user.target
```

### 3.2 各部分详解

#### [Unit] 部分

```ini
[Unit]
Description=服务描述        # 服务的简短描述
Documentation=文档URL       # 服务文档地址（可选）

# 依赖和启动顺序
After=network.target       # 在网络启动后启动
Before=nginx.service       # 在 Nginx 之前启动（可选）
Requires=mysql.service     # 依赖 MySQL（MySQL 未启动则本服务也不启动）
Wants=redis.service        # 弱依赖 Redis（Redis 未启动不影响本服务）
```

#### [Service] 部分

```ini
[Service]
# 服务类型
Type=simple                # 默认类型，启动后即视为已启动
# Type=forking            # 适用于后台进程（daemon 模式）
# Type=oneshot            # 一次性任务

# 用户和组
User=www-data             # 运行服务的用户
Group=www-data            # 运行服务的组

# 目录
WorkingDirectory=/path    # 工作目录

# 环境变量
Environment="KEY=value"   # 设置环境变量
EnvironmentFile=/path     # 从文件加载环境变量

# 命令
ExecStart=启动命令        # 必须，服务启动命令
ExecReload=重载命令       # 可选，重载配置命令
ExecStop=停止命令         # 可选，停止命令

# 重启策略
Restart=always            # 总是重启
# Restart=on-failure      # 仅失败时重启
# Restart=no              # 不重启
RestartSec=5              # 重启间隔

# 资源限制
LimitNOFILE=65536         # 最大文件描述符数
LimitNPROC=4096           # 最大进程数
```

#### [Install] 部分

```ini
[Install]
WantedBy=multi-user.target    # 多用户模式下启动
# WantedBy=graphical.target   # 图形界面模式下启动
```

---

## 四、服务管理命令 🔴【必须掌握】

### 4.1 基本管理命令

```bash
# 重新加载 systemd 配置（修改服务文件后必须执行）
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start ecommerce

# 停止服务
sudo systemctl stop ecommerce

# 重启服务
sudo systemctl restart ecommerce

# 重载配置（不中断服务）
sudo systemctl reload ecommerce

# 查看服务状态
sudo systemctl status ecommerce
```

### 4.2 开机自启管理

```bash
# 设置开机自启
sudo systemctl enable ecommerce

# 取消开机自启
sudo systemctl disable ecommerce

# 查看是否开机自启
sudo systemctl is-enabled ecommerce

# 启动并设置开机自启（一条命令）
sudo systemctl enable --now ecommerce
```

### 4.3 查看服务状态

```bash
# 详细状态
sudo systemctl status ecommerce
# 输出示例:
# ● ecommerce.service - Gunicorn instance to serve Ecommerce Knowledge Website
#      Loaded: loaded (/etc/systemd/system/ecommerce.service; enabled)
#      Active: active (running) since Fri 2026-01-02 10:00:00 CST; 5h ago
#    Main PID: 12345 (gunicorn)
#       Tasks: 5 (limit: 4915)
#      Memory: 120.0M
#         CPU: 5min 30s
#      CGroup: /system.slice/ecommerce.service
#              ├─12345 /var/www/.../gunicorn app:app
#              ├─12346 /var/www/.../gunicorn app:app
#              └─12347 /var/www/.../gunicorn app:app

# 检查是否运行
sudo systemctl is-active ecommerce
# 输出: active 或 inactive

# 检查是否失败
sudo systemctl is-failed ecommerce
```

### 4.4 列出服务

```bash
# 列出所有服务
sudo systemctl list-units --type=service

# 列出所有运行中的服务
sudo systemctl list-units --type=service --state=running

# 列出所有失败的服务
sudo systemctl list-units --type=service --state=failed

# 列出所有自定义服务
sudo systemctl list-unit-files --type=service | grep enabled
```

---

## 五、日志管理（journalctl） 🔴【必须掌握】

### 5.1 查看服务日志

```bash
# 查看指定服务的日志
sudo journalctl -u ecommerce

# 查看最近的日志（最后100行）
sudo journalctl -u ecommerce -n 100

# 实时查看日志（类似 tail -f）
sudo journalctl -u ecommerce -f

# 查看今天的日志
sudo journalctl -u ecommerce --since today

# 查看最近1小时的日志
sudo journalctl -u ecommerce --since "1 hour ago"

# 查看指定时间段的日志
sudo journalctl -u ecommerce --since "2026-01-01" --until "2026-01-02"
```

### 5.2 日志过滤

```bash
# 只显示错误级别
sudo journalctl -u ecommerce -p err

# 显示警告及以上级别
sudo journalctl -u ecommerce -p warning

# 日志级别: emerg, alert, crit, err, warning, notice, info, debug
```

### 5.3 日志格式

```bash
# JSON 格式输出
sudo journalctl -u ecommerce -o json

# 详细输出
sudo journalctl -u ecommerce -o verbose

# 简洁输出
sudo journalctl -u ecommerce -o short
```

### 5.4 日志清理 🟢【可选】

```bash
# 查看日志占用空间
sudo journalctl --disk-usage

# 清理7天前的日志
sudo journalctl --vacuum-time=7d

# 限制日志总大小为500M
sudo journalctl --vacuum-size=500M

# 永久配置日志大小限制
sudo nano /etc/systemd/journald.conf
# 添加: SystemMaxUse=500M
```

---

## 六、环境变量管理 🟡【重要】

### 6.1 在服务文件中设置

```ini
[Service]
# 单个环境变量
Environment="FLASK_ENV=production"
Environment="SECRET_KEY=your-secret-key"

# 多个环境变量
Environment="FLASK_ENV=production" "SECRET_KEY=xxx" "DATABASE_URL=xxx"
```

### 6.2 使用环境变量文件

```bash
# 创建环境变量文件
sudo nano /var/www/ecommerce_knowledge/.env
```

```bash
# /var/www/ecommerce_knowledge/.env
FLASK_ENV=production
SECRET_KEY=your-very-secret-key
DATABASE_URL=sqlite:///data/app.db
```

```ini
# 服务文件中引用
[Service]
EnvironmentFile=/var/www/ecommerce_knowledge/.env
```

### 6.3 安全注意事项

```bash
# 设置 .env 文件权限
sudo chmod 600 /var/www/ecommerce_knowledge/.env
sudo chown www-data:www-data /var/www/ecommerce_knowledge/.env
```

---

## 七、服务依赖配置 🟡【重要】

### 7.1 依赖其他服务

```ini
[Unit]
Description=Ecommerce Knowledge Website

# 在这些服务之后启动
After=network.target redis.service mysql.service

# 强依赖（如果 MySQL 未启动，本服务也不启动）
Requires=mysql.service

# 弱依赖（Redis 未启动不影响本服务启动）
Wants=redis.service
```

### 7.2 启动顺序说明

```
启动顺序:
network.target → mysql.service → redis.service → ecommerce.service

After: 定义启动顺序，不会自动启动依赖服务
Requires: 强依赖，会自动启动依赖服务，依赖服务停止则本服务也停止
Wants: 弱依赖，会尝试启动依赖服务，依赖服务失败不影响本服务
```

---

## 八、重启策略 🟡【重要】

### 8.1 重启策略选项

```ini
[Service]
# 重启策略
Restart=always          # 总是重启（推荐）
# Restart=on-failure    # 仅在失败时重启
# Restart=on-abnormal   # 异常退出时重启
# Restart=no            # 不重启

# 重启间隔
RestartSec=5            # 重启前等待5秒

# 重启次数限制（在指定时间内）
StartLimitIntervalSec=300   # 5分钟内
StartLimitBurst=5           # 最多重启5次
```

### 8.2 退出状态码

```
Restart=always:
├── 无论什么原因停止都会重启

Restart=on-failure:
├── 非零退出码时重启
├── 被信号杀死时重启
└── 超时时重启

Restart=on-abnormal:
├── 被信号杀死时重启
└── 超时时重启
```

---

## 九、资源限制 🟢【可选】

### 9.1 常用资源限制

```ini
[Service]
# 文件描述符限制
LimitNOFILE=65536

# 进程数限制
LimitNPROC=4096

# 内存限制
MemoryMax=512M
MemoryHigh=400M

# CPU 限制
CPUQuota=50%

# 超时限制
TimeoutStartSec=60
TimeoutStopSec=30
```

### 9.2 查看资源使用

```bash
# 查看服务资源使用
sudo systemctl status ecommerce
# 会显示 Memory 和 CPU 使用情况

# 详细资源信息
sudo systemctl show ecommerce --property=MemoryCurrent,CPUUsageNSec
```

---

## 十、服务调试 🟡【重要】

### 10.1 启动失败排查

```bash
# 查看服务状态
sudo systemctl status ecommerce

# 查看详细日志
sudo journalctl -u ecommerce -n 50 --no-pager

# 手动测试启动命令
sudo -u www-data /var/www/ecommerce_knowledge/venv/bin/gunicorn -c gunicorn_config.py app:app
```

### 10.2 常见问题

```bash
# 问题1: 找不到模块
# 原因: 虚拟环境路径错误
# 解决: 检查 Environment="PATH=..." 配置

# 问题2: 权限不足
# 原因: 用户无权访问目录或文件
# 解决:
sudo chown -R www-data:www-data /var/www/ecommerce_knowledge

# 问题3: 端口被占用
# 原因: 其他进程占用了端口
# 解决:
ss -tlnp | grep 5000
kill -9 占用进程PID

# 问题4: 配置文件语法错误
# 检查:
sudo systemd-analyze verify /etc/systemd/system/ecommerce.service
```

### 10.3 验证配置文件

```bash
# 验证服务文件语法
sudo systemd-analyze verify /etc/systemd/system/ecommerce.service

# 查看服务依赖树
sudo systemctl list-dependencies ecommerce

# 查看服务属性
sudo systemctl show ecommerce
```

---

## 十一、实用技巧 🟡【重要】

### 11.1 服务状态监控脚本

```bash
#!/bin/bash
# check_service.sh - 检查服务状态

SERVICE_NAME="ecommerce"

if systemctl is-active --quiet $SERVICE_NAME; then
    echo "✅ $SERVICE_NAME is running"
else
    echo "❌ $SERVICE_NAME is not running"
    echo "尝试重启..."
    sudo systemctl restart $SERVICE_NAME
fi
```

### 11.2 多服务管理

```bash
# 同时操作多个服务
sudo systemctl restart nginx ecommerce

# 查看多个服务状态
sudo systemctl status nginx ecommerce
```

### 11.3 服务模板（多实例） 🟢【可选】

```ini
# /etc/systemd/system/gunicorn@.service
[Unit]
Description=Gunicorn instance for %i

[Service]
User=www-data
WorkingDirectory=/var/www/%i
ExecStart=/var/www/%i/venv/bin/gunicorn -c gunicorn_config.py app:app

[Install]
WantedBy=multi-user.target
```

```bash
# 启动不同实例
sudo systemctl start gunicorn@project1
sudo systemctl start gunicorn@project2
```

---

## 十二、完整部署示例

### 12.1 服务文件

```ini
# /etc/systemd/system/ecommerce.service

[Unit]
Description=Gunicorn instance to serve Ecommerce Knowledge Website
Documentation=https://github.com/your-repo/ecommerce_knowledge
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ecommerce_knowledge
Environment="PATH=/var/www/ecommerce_knowledge/venv/bin"
EnvironmentFile=/var/www/ecommerce_knowledge/.env
ExecStart=/var/www/ecommerce_knowledge/venv/bin/gunicorn -c gunicorn_config.py app:app
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ecommerce

[Install]
WantedBy=multi-user.target
```

### 12.2 部署步骤

```bash
# 1. 创建服务文件
sudo nano /etc/systemd/system/ecommerce.service

# 2. 验证配置
sudo systemd-analyze verify /etc/systemd/system/ecommerce.service

# 3. 重新加载 systemd
sudo systemctl daemon-reload

# 4. 启动服务
sudo systemctl start ecommerce

# 5. 检查状态
sudo systemctl status ecommerce

# 6. 设置开机自启
sudo systemctl enable ecommerce

# 7. 查看日志
sudo journalctl -u ecommerce -f
```

---

## 📋 命令速查表

| 操作 | 命令 | 重要程度 |
|------|------|----------|
| 重载配置 | `sudo systemctl daemon-reload` | 🔴必须 |
| 启动服务 | `sudo systemctl start 服务名` | 🔴必须 |
| 停止服务 | `sudo systemctl stop 服务名` | 🔴必须 |
| 重启服务 | `sudo systemctl restart 服务名` | 🔴必须 |
| 查看状态 | `sudo systemctl status 服务名` | 🔴必须 |
| 开机自启 | `sudo systemctl enable 服务名` | 🔴必须 |
| 取消自启 | `sudo systemctl disable 服务名` | 🔴必须 |
| 查看日志 | `sudo journalctl -u 服务名` | 🔴必须 |
| 实时日志 | `sudo journalctl -u 服务名 -f` | 🔴必须 |
| 验证配置 | `sudo systemd-analyze verify 文件` | 🟡重要 |
| 列出服务 | `sudo systemctl list-units --type=service` | 🟡重要 |

---

*更新日期：2026-01-02*



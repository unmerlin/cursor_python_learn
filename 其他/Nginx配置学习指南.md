# Nginx 配置学习指南

> 本指南面向 Python 初学者，用于理解和配置 Nginx 作为 Flask 应用的反向代理

---

## 📌 知识点说明

- 🔴 **【必须掌握】** - 部署前必须理解和掌握
- 🟡 **【重要】** - 部署后需要了解，用于维护和优化
- 🟢 **【可选】** - 进阶知识，后续深入学习

---

## 一、Nginx 是什么 🔴【必须掌握】

### 1.1 基本概念

Nginx（发音：engine-x）是一个高性能的 Web 服务器和反向代理服务器。

**为什么 Flask 需要 Nginx？**

```
用户请求流程对比：

开发环境（直接访问 Flask）:
用户 → Flask(5000端口) → 返回页面

生产环境（使用 Nginx）:
用户 → Nginx(80端口) → Gunicorn → Flask → 返回页面
```

**Nginx 的作用：**

| 功能 | 说明 |
|------|------|
| 反向代理 | 接收用户请求，转发给后端应用 |
| 静态文件服务 | 直接处理 CSS、JS、图片等静态资源 |
| 负载均衡 | 将请求分发到多个后端服务器 |
| SSL/HTTPS | 处理 HTTPS 加密连接 |
| 缓存 | 缓存静态资源，提高响应速度 |
| 安全防护 | 防止直接暴露后端应用 |

### 1.2 为什么需要 Nginx + Gunicorn

```
Flask 自带的开发服务器 (app.run())
├── 单线程，性能低
├── 不支持多并发
├── 安全性不足
└── 不适合生产环境

Gunicorn (WSGI 服务器)
├── 多进程/多线程处理请求
├── 支持并发
├── 生产环境标准
└── 只处理 Python 应用

Nginx (Web 服务器)
├── 处理静态文件更高效
├── 处理并发连接能力强
├── 支持 HTTPS
├── 反向代理和负载均衡
└── 提供额外的安全层
```

---

## 二、安装 Nginx 🔴【必须掌握】

### 2.1 Ubuntu/Debian 系统

```bash
# 更新软件包列表
sudo apt update

# 安装 Nginx
sudo apt install nginx

# 验证安装
nginx -v
# 输出示例: nginx version: nginx/1.18.0 (Ubuntu)
```

### 2.2 启动和管理

```bash
# 启动 Nginx
sudo systemctl start nginx

# 停止 Nginx
sudo systemctl stop nginx

# 重启 Nginx
sudo systemctl restart nginx

# 重新加载配置（不中断服务）
sudo systemctl reload nginx

# 设置开机自启
sudo systemctl enable nginx

# 查看状态
sudo systemctl status nginx
```

### 2.3 验证运行

```bash
# 检查 Nginx 是否运行
curl http://localhost
# 或在浏览器访问服务器IP，应该看到 Nginx 欢迎页面
```

---

## 三、Nginx 目录结构 🔴【必须掌握】

```
/etc/nginx/                      # Nginx 主配置目录
├── nginx.conf                   # 主配置文件
├── sites-available/             # 可用的站点配置
│   └── default                  # 默认站点配置
├── sites-enabled/               # 已启用的站点（软链接）
│   └── default -> ../sites-available/default
├── conf.d/                      # 额外配置文件目录
├── snippets/                    # 配置片段
└── mime.types                   # MIME 类型定义

/var/www/                        # 默认网站根目录
└── html/                        # 默认 HTML 文件目录
    └── index.nginx-debian.html  # 默认欢迎页

/var/log/nginx/                  # 日志目录
├── access.log                   # 访问日志
└── error.log                    # 错误日志
```

---

## 四、Nginx 配置基础 🔴【必须掌握】

### 4.1 配置文件结构

```nginx
# nginx.conf 主配置文件结构

# 全局块 - 影响整体运行
user www-data;                    # 运行用户
worker_processes auto;            # 工作进程数
error_log /var/log/nginx/error.log;  # 错误日志
pid /run/nginx.pid;               # PID 文件

# events 块 - 连接处理
events {
    worker_connections 1024;      # 每个进程最大连接数
}

# http 块 - HTTP 服务配置
http {
    # 基本设置
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # 日志格式
    access_log /var/log/nginx/access.log;
    
    # 性能优化
    sendfile on;
    keepalive_timeout 65;
    
    # 包含站点配置
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### 4.2 server 块（虚拟主机）

```nginx
# 一个 server 块代表一个虚拟主机（网站）
server {
    listen 80;                    # 监听端口
    server_name example.com;      # 域名
    root /var/www/html;           # 网站根目录
    index index.html;             # 默认首页
    
    # location 块 - 定义 URL 路径处理规则
    location / {
        # 处理所有请求
    }
    
    location /static/ {
        # 处理 /static/ 开头的请求
    }
}
```

---

## 五、Flask 项目 Nginx 配置 🔴【必须掌握】

### 5.1 创建站点配置文件

```bash
# 创建配置文件
sudo nano /etc/nginx/sites-available/ecommerce
```

### 5.2 基本配置示例

```nginx
# /etc/nginx/sites-available/ecommerce

server {
    # 监听 80 端口（HTTP）
    listen 80;
    
    # 你的域名或服务器IP
    server_name yourdomain.com www.yourdomain.com;
    # 如果没有域名，使用 IP：
    # server_name 123.456.789.0;
    
    # 字符编码
    charset utf-8;
    
    # 最大上传文件大小
    client_max_body_size 10M;
    
    # 静态文件处理
    location /static {
        alias /var/www/ecommerce_knowledge/static;
        expires 30d;  # 缓存30天
    }
    
    # 所有其他请求转发给 Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # 错误页面
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /var/www/html;
    }
}
```

### 5.3 启用站点配置

```bash
# 创建软链接到 sites-enabled
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/

# 删除默认站点（可选）
sudo rm /etc/nginx/sites-enabled/default

# 测试配置是否正确
sudo nginx -t
# 输出应该是:
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful

# 重新加载 Nginx
sudo systemctl reload nginx
```

---

## 六、配置详解 🟡【重要】

### 6.1 location 匹配规则

```nginx
# 精确匹配（优先级最高）
location = /exact-path {
    # 只匹配 /exact-path
}

# 前缀匹配（优先级次高，^~ 修饰符）
location ^~ /static/ {
    # 匹配 /static/ 开头的路径，不再检查正则
}

# 正则匹配（区分大小写）
location ~ \.php$ {
    # 匹配 .php 结尾
}

# 正则匹配（不区分大小写）
location ~* \.(jpg|png|gif)$ {
    # 匹配图片文件
}

# 普通前缀匹配
location /api/ {
    # 匹配 /api/ 开头
}

# 通用匹配（优先级最低）
location / {
    # 匹配所有请求
}
```

### 6.2 proxy_pass 配置详解

```nginx
location / {
    # 转发到后端服务器
    proxy_pass http://127.0.0.1:5000;
    
    # 传递原始请求信息
    proxy_set_header Host $host;                    # 原始主机名
    proxy_set_header X-Real-IP $remote_addr;        # 真实客户端IP
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  # 代理链
    proxy_set_header X-Forwarded-Proto $scheme;     # 原始协议(http/https)
    
    # 超时配置
    proxy_connect_timeout 60s;    # 连接超时
    proxy_send_timeout 60s;       # 发送超时
    proxy_read_timeout 60s;       # 读取超时
    
    # 缓冲配置
    proxy_buffering on;
    proxy_buffer_size 4k;
    proxy_buffers 4 32k;
}
```

### 6.3 静态文件配置详解

```nginx
# 方式1: alias（路径替换）
location /static {
    alias /var/www/ecommerce_knowledge/static;
    # 请求 /static/css/style.css 
    # 实际访问 /var/www/ecommerce_knowledge/static/css/style.css
}

# 方式2: root（路径拼接）
location /static {
    root /var/www/ecommerce_knowledge;
    # 请求 /static/css/style.css 
    # 实际访问 /var/www/ecommerce_knowledge/static/css/style.css
}

# 缓存设置
location /static {
    alias /var/www/ecommerce_knowledge/static;
    expires 30d;                          # 缓存30天
    add_header Cache-Control "public";    # 允许公共缓存
    access_log off;                       # 关闭静态文件访问日志
}
```

---

## 七、HTTPS 配置（SSL） 🟡【重要】

### 7.1 使用 Let's Encrypt 免费证书

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 自动获取证书并配置 Nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 按提示操作:
# 1. 输入邮箱（用于接收续期提醒）
# 2. 同意服务条款
# 3. 是否分享邮箱（可选）
# 4. 是否重定向 HTTP 到 HTTPS（建议选择是）
```

### 7.2 Certbot 配置后的 Nginx

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # HTTP 自动重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL 证书配置（Certbot 自动添加）
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    
    # 其他配置...
    location / {
        proxy_pass http://127.0.0.1:5000;
        # ...
    }
}
```

### 7.3 证书续期

```bash
# 测试续期（不实际执行）
sudo certbot renew --dry-run

# 手动续期
sudo certbot renew

# 自动续期（Certbot 自动添加了定时任务）
# 查看定时任务
sudo systemctl list-timers | grep certbot
```

---

## 八、日志管理 🟡【重要】

### 8.1 日志位置

```bash
# 访问日志
/var/log/nginx/access.log

# 错误日志
/var/log/nginx/error.log

# 站点特定日志（需要在配置中指定）
/var/log/nginx/ecommerce_access.log
/var/log/nginx/ecommerce_error.log
```

### 8.2 自定义日志配置

```nginx
server {
    # ...
    
    # 自定义日志
    access_log /var/log/nginx/ecommerce_access.log;
    error_log /var/log/nginx/ecommerce_error.log;
    
    # 或关闭访问日志（节省磁盘）
    # access_log off;
}
```

### 8.3 查看日志

```bash
# 查看最近的访问日志
tail -50 /var/log/nginx/access.log

# 实时查看日志
tail -f /var/log/nginx/access.log

# 搜索错误
grep "error" /var/log/nginx/error.log
grep "500" /var/log/nginx/access.log

# 统计访问IP
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -10
```

---

## 九、性能优化 🟢【可选】

### 9.1 Gzip 压缩

```nginx
http {
    # 开启 Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_proxied any;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    gzip_comp_level 6;
}
```

### 9.2 缓存优化

```nginx
# 静态资源缓存
location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
    access_log off;
}

# 代理缓存
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=100m inactive=60m;

location / {
    proxy_cache my_cache;
    proxy_cache_valid 200 1h;
    proxy_pass http://127.0.0.1:5000;
}
```

### 9.3 连接优化

```nginx
http {
    # 长连接
    keepalive_timeout 65;
    keepalive_requests 100;
    
    # 文件传输优化
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    
    # 缓冲区设置
    client_body_buffer_size 10K;
    client_header_buffer_size 1k;
    large_client_header_buffers 2 1k;
}
```

---

## 十、安全配置 🟡【重要】

### 10.1 基本安全设置

```nginx
server {
    # 隐藏 Nginx 版本号
    server_tokens off;
    
    # 安全响应头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
    }
    
    # 禁止访问敏感文件
    location ~* (\.py|\.pyc|\.log|\.ini|\.env)$ {
        deny all;
    }
}
```

### 10.2 限制请求

```nginx
http {
    # 限制请求频率
    limit_req_zone $binary_remote_addr zone=req_limit:10m rate=10r/s;
    
    # 限制连接数
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
}

server {
    location / {
        limit_req zone=req_limit burst=20 nodelay;
        limit_conn conn_limit 10;
        proxy_pass http://127.0.0.1:5000;
    }
}
```

---

## 十一、常用命令汇总 🔴【必须掌握】

```bash
# 安装
sudo apt install nginx

# 服务管理
sudo systemctl start nginx       # 启动
sudo systemctl stop nginx        # 停止
sudo systemctl restart nginx     # 重启
sudo systemctl reload nginx      # 重载配置（平滑重启）
sudo systemctl status nginx      # 查看状态
sudo systemctl enable nginx      # 开机自启

# 配置测试
sudo nginx -t                    # 测试配置语法

# 日志查看
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# 配置文件
sudo nano /etc/nginx/sites-available/sitename
sudo ln -s /etc/nginx/sites-available/sitename /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/sitename

# SSL 证书
sudo certbot --nginx -d domain.com
sudo certbot renew --dry-run
```

---

## 十二、完整配置示例

### 12.1 电商知识网站完整配置

```nginx
# /etc/nginx/sites-available/ecommerce

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS 主配置
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL 配置
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # 安全设置
    server_tokens off;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # 字符编码
    charset utf-8;
    
    # 上传限制
    client_max_body_size 10M;
    
    # 日志
    access_log /var/log/nginx/ecommerce_access.log;
    error_log /var/log/nginx/ecommerce_error.log;
    
    # 静态文件
    location /static {
        alias /var/www/ecommerce_knowledge/static;
        expires 30d;
        add_header Cache-Control "public";
        access_log off;
    }
    
    # 应用请求
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
    }
    
    # 错误页面
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /var/www/html;
    }
}
```

---

## 十三、常见问题排查

### 13.1 502 Bad Gateway

```bash
# 可能原因：后端服务没有运行
# 检查 Gunicorn 是否运行
sudo systemctl status ecommerce
ps aux | grep gunicorn

# 检查端口
ss -tlnp | grep 5000
```

### 13.2 403 Forbidden

```bash
# 可能原因：权限问题
# 检查文件权限
ls -la /var/www/ecommerce_knowledge/

# 修复权限
sudo chown -R www-data:www-data /var/www/ecommerce_knowledge/
sudo chmod -R 755 /var/www/ecommerce_knowledge/
```

### 13.3 配置不生效

```bash
# 测试配置
sudo nginx -t

# 重新加载
sudo systemctl reload nginx

# 查看错误日志
tail -50 /var/log/nginx/error.log
```

---

## 📋 配置检查清单

| 检查项 | 命令 | 预期结果 |
|--------|------|----------|
| Nginx 是否安装 | `nginx -v` | 显示版本号 |
| Nginx 是否运行 | `systemctl status nginx` | active (running) |
| 配置是否正确 | `sudo nginx -t` | syntax is ok |
| 80 端口是否监听 | `ss -tlnp \| grep 80` | LISTEN |
| 站点是否启用 | `ls /etc/nginx/sites-enabled/` | 显示配置文件 |
| 后端是否运行 | `ss -tlnp \| grep 5000` | LISTEN |

---

*更新日期：2026-01-02*



# Linux 命令行操作指南

> 本指南面向 Python 初学者，用于 Flask 项目部署到 Linux 服务器的场景

---

## 📌 知识点说明

- 🔴 **【必须掌握】** - 部署前必须熟练掌握
- 🟡 **【重要】** - 部署后需要了解，用于维护和排查
- 🟢 **【可选】** - 进阶知识，后续优化时学习

---

## 一、连接服务器 🔴【必须掌握】

### 1.1 SSH 连接

```bash
# 基本连接（会提示输入密码）
ssh root@服务器IP

# 示例
ssh root@123.456.789.0

# 指定端口连接（默认22端口）
ssh -p 端口号 root@服务器IP

# 退出连接
exit
```

### 1.2 SSH 密钥登录（推荐）

```bash
# 1. 在本地生成密钥对
ssh-keygen -t rsa -b 4096

# 2. 将公钥复制到服务器
ssh-copy-id root@服务器IP

# 之后登录就不需要密码了
ssh root@服务器IP
```

### 1.3 Windows 连接方式

- **PowerShell**：直接使用 `ssh` 命令
- **终端工具**：推荐 MobaXterm、Xshell、PuTTY

---

## 二、文件和目录操作 🔴【必须掌握】

### 2.1 目录导航

```bash
# 查看当前目录
pwd
# 输出示例: /root

# 列出目录内容
ls              # 简单列出
ls -l           # 详细列表（权限、大小、时间）
ls -la          # 包含隐藏文件
ls -lh          # 人类可读的文件大小（KB、MB）

# 切换目录
cd /var/www          # 进入指定目录
cd ..                # 返回上一级
cd ~                 # 返回用户主目录
cd -                 # 返回上一次的目录
```

### 2.2 创建和删除

```bash
# 创建目录
mkdir myproject                  # 创建单个目录
mkdir -p /var/www/myproject      # 创建多级目录（推荐）

# 创建文件
touch filename.txt               # 创建空文件

# 删除文件
rm filename.txt                  # 删除文件

# 删除目录
rmdir emptydir                   # 删除空目录
rm -r mydir                      # 删除目录及其内容
rm -rf mydir                     # 强制删除（⚠️ 谨慎使用！）
```

> ⚠️ **警告**：`rm -rf` 是危险命令，删除后无法恢复！永远不要执行 `rm -rf /`

### 2.3 复制和移动

```bash
# 复制文件
cp source.txt dest.txt           # 复制文件
cp -r sourcedir destdir          # 复制目录（-r 递归）

# 移动/重命名
mv oldname.txt newname.txt       # 重命名文件
mv file.txt /var/www/            # 移动文件到目录
mv olddir newdir                 # 重命名目录
```

### 2.4 查看文件内容

```bash
# 查看完整内容
cat filename.txt                 # 显示全部内容

# 分页查看（适合大文件）
less filename.txt                # 分页查看，按 q 退出
more filename.txt                # 分页查看

# 查看开头/结尾
head filename.txt                # 查看前10行
head -n 20 filename.txt          # 查看前20行
tail filename.txt                # 查看后10行
tail -n 50 filename.txt          # 查看后50行
tail -f logfile.log              # 实时查看文件更新（查看日志常用）
```

---

## 三、文件编辑 🔴【必须掌握】

### 3.1 nano 编辑器（推荐新手使用）

```bash
# 打开/创建文件
nano filename.txt

# 常用快捷键（^ 表示 Ctrl 键）
Ctrl + O        # 保存文件
Ctrl + X        # 退出编辑器
Ctrl + K        # 剪切当前行
Ctrl + U        # 粘贴
Ctrl + W        # 搜索
Ctrl + G        # 查看帮助
```

### 3.2 vim 编辑器 🟡【重要】

```bash
# 打开文件
vim filename.txt

# vim 有两种主要模式：
# 1. 命令模式（默认）- 用于导航和操作
# 2. 插入模式 - 用于编辑文本

# 基本操作
i               # 进入插入模式（在光标前插入）
Esc             # 返回命令模式
:w              # 保存
:q              # 退出
:wq             # 保存并退出
:q!             # 强制退出不保存

# 命令模式下的操作
dd              # 删除当前行
yy              # 复制当前行
p               # 粘贴
/keyword        # 搜索关键词
n               # 查找下一个
u               # 撤销
```

---

## 四、文件权限 🔴【必须掌握】

### 4.1 理解权限表示

```bash
# 使用 ls -l 查看权限
ls -l
# 输出示例:
# -rw-r--r-- 1 root root 1234 Jan 1 12:00 file.txt
# drwxr-xr-x 2 root root 4096 Jan 1 12:00 mydir

# 权限解读（10个字符）:
# 第1位: d=目录, -=文件, l=链接
# 第2-4位: 所有者权限 (r读 w写 x执行)
# 第5-7位: 所属组权限
# 第8-10位: 其他用户权限

# 示例: -rwxr-xr--
# - : 普通文件
# rwx : 所有者可读、写、执行
# r-x : 所属组可读、执行
# r-- : 其他用户只读
```

### 4.2 修改权限

```bash
# 使用数字方式（推荐）
# r=4, w=2, x=1，相加得到权限数字

chmod 755 filename      # rwxr-xr-x（常用于脚本）
chmod 644 filename      # rw-r--r--（常用于普通文件）
chmod 600 filename      # rw-------（私密文件）
chmod -R 755 dirname    # 递归修改目录下所有文件

# 使用符号方式
chmod +x script.sh      # 添加执行权限
chmod u+w filename      # 给所有者添加写权限
chmod go-w filename     # 移除组和其他用户的写权限
```

### 4.3 修改所有者

```bash
# 修改文件所有者
chown username filename
chown username:groupname filename

# 递归修改目录
chown -R www-data:www-data /var/www/myproject
```

---

## 五、用户和权限管理 🟡【重要】

### 5.1 sudo 命令

```bash
# 以管理员权限执行命令
sudo 命令

# 示例
sudo apt update
sudo systemctl restart nginx

# 切换到 root 用户
sudo su
# 或
sudo -i
```

### 5.2 用户管理 🟢【可选】

```bash
# 创建新用户
sudo adduser username

# 将用户添加到 sudo 组
sudo usermod -aG sudo username

# 切换用户
su - username

# 查看当前用户
whoami

# 查看用户所属组
groups username
```

---

## 六、软件包管理 🔴【必须掌握】

### 6.1 Ubuntu/Debian 系统（apt）

```bash
# 更新软件包列表
sudo apt update

# 升级已安装的软件包
sudo apt upgrade

# 安装软件
sudo apt install 软件名
sudo apt install nginx python3 python3-pip python3-venv

# 卸载软件
sudo apt remove 软件名
sudo apt purge 软件名        # 同时删除配置文件

# 搜索软件
apt search 关键词

# 清理不需要的包
sudo apt autoremove
```

### 6.2 CentOS/RHEL 系统（yum/dnf） 🟢【可选】

```bash
# 更新
sudo yum update
# 或（CentOS 8+）
sudo dnf update

# 安装
sudo yum install nginx python3
```

---

## 七、查找命令 🟡【重要】

### 7.1 查找文件

```bash
# find 命令（功能强大）
find /path -name "filename"           # 按名称查找
find /var/www -name "*.py"            # 查找所有 .py 文件
find / -name "app.py" 2>/dev/null     # 全局查找，忽略错误

# 按类型查找
find /path -type f                    # 只查找文件
find /path -type d                    # 只查找目录

# 按时间查找
find /path -mtime -7                  # 7天内修改过的文件
```

### 7.2 搜索文件内容

```bash
# grep 命令
grep "关键词" filename                # 在文件中搜索
grep -r "关键词" /path                # 递归搜索目录
grep -n "关键词" filename             # 显示行号
grep -i "关键词" filename             # 忽略大小写

# 实用组合
grep -rn "ERROR" /var/log/            # 在日志中搜索错误
```

### 7.3 查找命令位置

```bash
# 查找命令路径
which python3         # 输出: /usr/bin/python3
which nginx           # 输出: /usr/sbin/nginx

# 查找相关文件
whereis python3       # 显示程序、源码、手册位置
```

---

## 八、进程管理 🔴【必须掌握】

### 8.1 查看进程

```bash
# 查看所有进程
ps aux

# 查找特定进程
ps aux | grep python
ps aux | grep gunicorn
ps aux | grep nginx

# 实时监控进程（按 q 退出）
top

# 更友好的进程监控（需要安装）
htop
```

### 8.2 结束进程

```bash
# 根据 PID 结束进程
kill PID              # 正常结束
kill -9 PID           # 强制结束

# 根据名称结束进程
pkill python          # 结束所有 python 进程
pkill -f "gunicorn"   # 匹配命令行

# 查找并结束进程（常用组合）
ps aux | grep gunicorn
# 找到 PID 后
kill -9 PID
```

### 8.3 后台运行

```bash
# 后台运行命令
command &

# 使用 nohup（退出终端后继续运行）
nohup command &
nohup python app.py > output.log 2>&1 &

# 查看后台任务
jobs

# 将后台任务调到前台
fg %1
```

---

## 九、系统信息 🟡【重要】

### 9.1 磁盘空间

```bash
# 查看磁盘使用情况
df -h

# 查看目录大小
du -sh /var/www              # 查看单个目录大小
du -sh *                     # 查看当前目录下所有文件/目录大小
du -sh * | sort -h           # 按大小排序
```

### 9.2 内存使用

```bash
# 查看内存使用
free -h
# 输出示例:
#               total        used        free      shared  buff/cache   available
# Mem:          1.9Gi       512Mi       256Mi       8.0Mi       1.2Gi       1.2Gi
```

### 9.3 系统信息

```bash
# 系统版本
cat /etc/os-release

# 内核版本
uname -a

# 主机名
hostname

# 运行时间
uptime
```

---

## 十、网络命令 🔴【必须掌握】

### 10.1 网络状态

```bash
# 查看网络接口
ip addr
# 或
ifconfig              # 较旧的命令

# 查看端口监听状态
netstat -tlnp         # 查看 TCP 监听端口
# 或（推荐）
ss -tlnp              # 更现代的命令

# 测试网络连接
ping www.baidu.com
ping -c 4 8.8.8.8     # 只发送4个包
```

### 10.2 防火墙（UFW） 🟡【重要】

```bash
# 查看防火墙状态
sudo ufw status
sudo ufw status verbose

# 开放端口
sudo ufw allow 22       # SSH
sudo ufw allow 80       # HTTP
sudo ufw allow 443      # HTTPS
sudo ufw allow 5000     # Flask 开发端口

# 删除规则
sudo ufw delete allow 5000

# 启用/禁用防火墙
sudo ufw enable
sudo ufw disable
```

### 10.3 下载文件

```bash
# 使用 wget
wget https://example.com/file.zip

# 使用 curl
curl -O https://example.com/file.zip
curl -o newname.zip https://example.com/file.zip
```

---

## 十一、文件传输 🔴【必须掌握】

### 11.1 SCP（Secure Copy）

```bash
# 从本地上传到服务器
scp localfile.txt root@服务器IP:/remote/path/
scp -r localdir root@服务器IP:/remote/path/      # 上传目录

# 从服务器下载到本地
scp root@服务器IP:/remote/file.txt ./
scp -r root@服务器IP:/remote/dir ./              # 下载目录

# 示例：上传项目
scp -r ecommerce_knowledge root@123.456.789.0:/var/www/
```

### 11.2 SFTP

```bash
# 连接服务器
sftp root@服务器IP

# SFTP 命令
ls              # 列出远程文件
lls             # 列出本地文件
cd dir          # 切换远程目录
lcd dir         # 切换本地目录
put file        # 上传文件
put -r dir      # 上传目录
get file        # 下载文件
get -r dir      # 下载目录
exit            # 退出
```

### 11.3 rsync（增量同步） 🟢【可选】

```bash
# 同步本地到远程（只传输变化的文件）
rsync -avz localdir/ root@服务器IP:/remote/dir/

# 常用选项
# -a : 归档模式，保留权限
# -v : 显示详细信息
# -z : 压缩传输
# --delete : 删除目标中多余的文件
```

---

## 十二、压缩和解压 🟡【重要】

### 12.1 tar 命令

```bash
# 创建 tar.gz 压缩包
tar -czvf archive.tar.gz dirname/
# -c : 创建
# -z : gzip 压缩
# -v : 显示过程
# -f : 指定文件名

# 解压 tar.gz
tar -xzvf archive.tar.gz
tar -xzvf archive.tar.gz -C /target/dir    # 解压到指定目录

# 查看压缩包内容（不解压）
tar -tzvf archive.tar.gz
```

### 12.2 zip 命令

```bash
# 压缩
zip -r archive.zip dirname/

# 解压
unzip archive.zip
unzip archive.zip -d /target/dir
```

---

## 十三、常用组合命令 🟡【重要】

### 13.1 管道和重定向

```bash
# 管道 |（将前一个命令的输出作为后一个命令的输入）
ps aux | grep python
cat file.txt | head -20

# 输出重定向
command > file.txt      # 覆盖写入
command >> file.txt     # 追加写入
command 2> error.txt    # 错误输出重定向
command > out.txt 2>&1  # 标准输出和错误都重定向

# 输入重定向
command < input.txt
```

### 13.2 常用技巧

```bash
# 历史命令
history                 # 查看历史命令
!100                    # 执行第100条命令
!!                      # 执行上一条命令
Ctrl + R                # 搜索历史命令

# 快捷键
Ctrl + C                # 中断当前命令
Ctrl + D                # 退出/发送EOF
Ctrl + L                # 清屏（等同于 clear）
Tab                     # 自动补全

# 命令替换
$(command)              # 将命令输出作为参数
echo "Today is $(date)"
```

---

## 十四、实用脚本示例 🟢【可选】

### 14.1 简单的部署脚本

```bash
#!/bin/bash
# deploy.sh - 简单部署脚本

# 进入项目目录
cd /var/www/ecommerce_knowledge

# 拉取最新代码
git pull origin main

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 重启服务
sudo systemctl restart ecommerce

echo "部署完成！"
```

### 14.2 使用脚本

```bash
# 添加执行权限
chmod +x deploy.sh

# 运行脚本
./deploy.sh
# 或
bash deploy.sh
```

---

## 📋 命令速查表

| 类别 | 命令 | 说明 | 重要程度 |
|------|------|------|----------|
| **连接** | `ssh root@IP` | SSH连接服务器 | 🔴必须 |
| **导航** | `pwd` / `cd` / `ls` | 查看/切换目录 | 🔴必须 |
| **文件** | `cp` / `mv` / `rm` | 复制/移动/删除 | 🔴必须 |
| **查看** | `cat` / `less` / `tail` | 查看文件内容 | 🔴必须 |
| **编辑** | `nano` / `vim` | 编辑文件 | 🔴必须 |
| **权限** | `chmod` / `chown` | 修改权限/所有者 | 🔴必须 |
| **权限** | `sudo` | 管理员权限 | 🔴必须 |
| **软件** | `apt install` | 安装软件 | 🔴必须 |
| **进程** | `ps` / `kill` | 查看/结束进程 | 🔴必须 |
| **网络** | `ss -tlnp` | 查看端口 | 🔴必须 |
| **防火墙** | `ufw allow` | 开放端口 | 🟡重要 |
| **传输** | `scp` / `sftp` | 文件传输 | 🔴必须 |
| **压缩** | `tar` / `zip` | 压缩解压 | 🟡重要 |
| **搜索** | `find` / `grep` | 查找文件/内容 | 🟡重要 |
| **系统** | `df` / `free` / `top` | 系统信息 | 🟡重要 |

---

## 💡 学习建议

1. **先在本地练习**：可以使用 WSL（Windows Subsystem for Linux）或虚拟机练习
2. **多用 Tab 补全**：减少输入错误
3. **善用 man 命令**：`man 命令名` 查看帮助文档
4. **记录常用命令**：建立自己的命令笔记
5. **谨慎使用 rm -rf**：删除前先用 ls 确认

---

*更新日期：2026-01-02*



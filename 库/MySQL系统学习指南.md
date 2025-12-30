# MySQL系统学习指南

> 从入门到精通MySQL，重点掌握日常工作中最常用的功能和CSV文件操作

## 📋 目录

1. [学习路线概览](#学习路线概览)
2. [MySQL vs 其他关系数据库对比](#mysql-vs-其他关系数据库对比)
3. [阶段一：MySQL入门基础](#阶段一mysql入门基础)
4. [阶段二：核心查询操作](#阶段二核心查询操作)
5. [阶段三：数据管理与优化](#阶段三数据管理与优化)
6. [阶段四：CSV文件操作专题](#阶段四csv文件操作专题)
7. [阶段五：高级特性与实战](#阶段五高级特性与实战)
8. [实战场景应用](#实战场景应用)
9. [快速查询指南](#快速查询指南)
10. [学习资源和工具](#学习资源和工具)
11. [常见问题解决方案](#常见问题解决方案)

---

## 🎯 学习路线概览

### 完整学习路径

```
阶段一：入门基础 (1-2周)
    ↓
阶段二：核心查询 (2-3周)
    ↓
阶段三：数据管理与优化 (2-3周)
    ↓
阶段四：CSV文件操作专题 (1-2周) ⭐重点
    ↓
阶段五：高级特性与实战 (持续实践)
```

### 各阶段学习目标

| 阶段 | 学习内容 | 预计时间 | 重要性 | 完成标志 |
|------|---------|---------|--------|---------|
| 阶段一 | 数据库基础、SQL基础语法 | 1-2周 | ⭐⭐⭐⭐⭐ | 能独立创建数据库和表 |
| 阶段二 | 查询、筛选、排序、聚合 | 2-3周 | ⭐⭐⭐⭐⭐ | 能编写复杂查询语句 |
| 阶段三 | 索引、优化、事务处理 | 2-3周 | ⭐⭐⭐⭐ | 能优化慢查询 |
| 阶段四 | CSV导入导出、批量处理 | 1-2周 | ⭐⭐⭐⭐⭐ | 能处理日常CSV任务 |
| 阶段五 | 存储过程、触发器、实战 | 持续 | ⭐⭐⭐ | 能解决复杂业务问题 |

---

## 🔄 MySQL vs 其他关系数据库对比

### 主流数据库对比表

| 特性 | MySQL | PostgreSQL | SQL Server | Oracle |
|------|-------|------------|------------|--------|
| **开源** | ✅ 开源 | ✅ 开源 | ❌ 商业 | ❌ 商业 |
| **性能** | 读取快 | 复杂查询强 | 企业级 | 最强 |
| **易用性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **成本** | 免费 | 免费 | 高 | 极高 |
| **适用场景** | Web应用、中小型项目 | 复杂数据处理 | 企业应用 | 大型企业 |
| **CSV导入** | LOAD DATA INFILE | COPY FROM | BULK INSERT | SQL*Loader |

### 核心语法差异对比

#### 1. 字符串拼接

```sql
-- MySQL（使用CONCAT函数）
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users;

-- PostgreSQL（使用 || 运算符）
SELECT first_name || ' ' || last_name AS full_name FROM users;

-- SQL Server（使用 + 运算符）
SELECT first_name + ' ' + last_name AS full_name FROM users;

-- Oracle（使用 || 运算符）
SELECT first_name || ' ' || last_name AS full_name FROM users;
```

#### 2. 限制返回行数

```sql
-- MySQL（使用LIMIT）⭐ MySQL特有
SELECT * FROM users LIMIT 10;
SELECT * FROM users LIMIT 10 OFFSET 20;  -- 跳过前20条

-- PostgreSQL（支持LIMIT和FETCH）
SELECT * FROM users LIMIT 10;
SELECT * FROM users FETCH FIRST 10 ROWS ONLY;

-- SQL Server（使用TOP）
SELECT TOP 10 * FROM users;
-- SQL Server 2012+（使用OFFSET-FETCH）
SELECT * FROM users ORDER BY id OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;

-- Oracle（使用ROWNUM或FETCH）
SELECT * FROM users WHERE ROWNUM <= 10;
-- Oracle 12c+
SELECT * FROM users FETCH FIRST 10 ROWS ONLY;
```

#### 3. 自增主键

```sql
-- MySQL（使用AUTO_INCREMENT）⭐ MySQL特有
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50)
);

-- PostgreSQL（使用SERIAL或IDENTITY）
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50)
);

-- SQL Server（使用IDENTITY）
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50)
);

-- Oracle（使用SEQUENCE）
CREATE SEQUENCE user_seq;
CREATE TABLE users (
    id NUMBER DEFAULT user_seq.NEXTVAL PRIMARY KEY,
    name VARCHAR2(50)
);
```

#### 4. 当前日期时间

```sql
-- MySQL ⭐
SELECT NOW();           -- 日期+时间
SELECT CURDATE();       -- 仅日期
SELECT CURTIME();       -- 仅时间

-- PostgreSQL
SELECT NOW();
SELECT CURRENT_DATE;
SELECT CURRENT_TIME;

-- SQL Server
SELECT GETDATE();
SELECT CONVERT(DATE, GETDATE());

-- Oracle
SELECT SYSDATE FROM DUAL;
SELECT CURRENT_DATE FROM DUAL;
```

#### 5. 条件判断

```sql
-- MySQL（使用IF或CASE）⭐
SELECT IF(score >= 60, '及格', '不及格') AS result FROM students;
SELECT CASE WHEN score >= 60 THEN '及格' ELSE '不及格' END FROM students;

-- PostgreSQL/SQL Server/Oracle（都使用CASE，不支持IF）
SELECT CASE WHEN score >= 60 THEN '及格' ELSE '不及格' END FROM students;
```

### MySQL的独特优势

✅ **优势**：
- 安装配置简单，上手快
- 读操作性能优秀，适合Web应用
- 社区活跃，资料丰富
- 与Python、PHP等语言集成良好
- 主从复制配置简单
- 开源免费，成本低

⚠️ **局限**：
- 复杂查询性能不如PostgreSQL
- 存储过程功能较弱
- JSON支持晚于PostgreSQL（5.7才引入）
- 全文搜索功能相对较弱

---

## 阶段一：MySQL入门基础

### 目标
掌握MySQL基础概念和基本操作（⭐⭐⭐⭐⭐ 必须掌握）

### 预计时间
1-2周

---

### 1.1 数据库基本概念

#### 核心概念理解

```
数据库服务器（MySQL Server）
    ├── 数据库1（Database）
    │   ├── 表1（Table）
    │   │   ├── 列1（Column）- 字段
    │   │   ├── 列2
    │   │   └── 行（Row）- 记录
    │   └── 表2
    └── 数据库2
```

#### 数据类型选择

| 数据类型 | MySQL类型 | 说明 | 使用场景 |
|---------|----------|------|---------|
| **整数** | INT, BIGINT | 存储整数 | 用户ID、数量 |
| **小数** | DECIMAL(M,D) | 精确小数 | 金额（必须用DECIMAL） |
| **浮点数** | FLOAT, DOUBLE | 近似小数 | 科学计算 |
| **字符串** | VARCHAR(N) | 可变长度 | 姓名、地址（最常用） |
| **文本** | TEXT | 长文本 | 文章内容 |
| **日期** | DATE | 日期 | 出生日期 |
| **日期时间** | DATETIME | 日期+时间 | 创建时间 |
| **时间戳** | TIMESTAMP | 自动更新 | 最后修改时间 |

⚠️ **重要提示**：
- 金额必须使用 `DECIMAL` 类型，不要用 `FLOAT`
- 字符串长度规划要合理，VARCHAR(255) 是常见选择
- 手机号使用 `VARCHAR(20)` 而不是数字类型
- 时间字段优先使用 `DATETIME`，存储更稳定

---

### 1.2 数据库和表的基本操作

#### 数据库操作

```sql
-- 创建数据库（指定字符集）⭐ 重要
CREATE DATABASE sales_db 
    DEFAULT CHARACTER SET utf8mb4 
    DEFAULT COLLATE utf8mb4_unicode_ci;

-- 查看所有数据库
SHOW DATABASES;

-- 使用数据库
USE sales_db;

-- 查看当前使用的数据库
SELECT DATABASE();

-- 删除数据库（危险操作！）
DROP DATABASE sales_db;
```

⚠️ **字符集设置**：
- 必须使用 `utf8mb4`，不要用 `utf8`（utf8不完整）
- `utf8mb4` 支持emoji和中文
- 这是MySQL的常见坑点

#### 创建表的最佳实践

```sql
-- 完整的表创建示例（推荐格式）⭐
CREATE TABLE users (
    -- 主键：自增ID
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- 基本信息
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    password VARCHAR(255) NOT NULL COMMENT '密码',
    
    -- 个人信息
    real_name VARCHAR(50) COMMENT '真实姓名',
    phone VARCHAR(20) COMMENT '手机号',
    gender ENUM('M', 'F', 'Other') DEFAULT 'Other' COMMENT '性别',
    birth_date DATE COMMENT '出生日期',
    
    -- 状态字段
    status TINYINT DEFAULT 1 COMMENT '状态：0-禁用，1-启用',
    
    -- 时间字段（重要）
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
```

💡 **表设计最佳实践**：
1. 每个表都应有主键（通常是自增ID）
2. 必须有 `created_at` 和 `updated_at` 时间字段
3. 字段添加 `COMMENT` 注释
4. 使用 `InnoDB` 引擎（支持事务）
5. 字符集使用 `utf8mb4`

#### 查看表结构

```sql
-- 查看所有表
SHOW TABLES;

-- 查看表结构（3种方式）
DESCRIBE users;
DESC users;
SHOW COLUMNS FROM users;

-- 查看建表语句
SHOW CREATE TABLE users;
```

#### 修改表结构

```sql
-- 添加列
ALTER TABLE users ADD COLUMN address VARCHAR(200) COMMENT '地址';

-- 修改列类型
ALTER TABLE users MODIFY COLUMN phone VARCHAR(30);

-- 重命名列
ALTER TABLE users CHANGE COLUMN real_name full_name VARCHAR(50);

-- 删除列
ALTER TABLE users DROP COLUMN address;

-- 重命名表
RENAME TABLE users TO members;
-- 或
ALTER TABLE users RENAME TO members;
```

---

## 阶段二：核心查询操作

### 目标
熟练掌握数据查询和筛选（⭐⭐⭐⭐⭐ 最常用）

### 预计时间
2-3周

---

### 2.1 基本查询（SELECT）

#### 基础查询语法

```sql
-- 查询所有列
SELECT * FROM users;

-- 查询指定列（推荐，性能更好）⭐
SELECT id, username, email FROM users;

-- 列别名
SELECT 
    id AS 用户ID,
    username AS 用户名,
    email AS 邮箱
FROM users;

-- 去重查询
SELECT DISTINCT city FROM users;

-- 限制返回行数（MySQL特有）⭐
SELECT * FROM users LIMIT 10;           -- 前10条
SELECT * FROM users LIMIT 10 OFFSET 20; -- 跳过20条，取10条
SELECT * FROM users LIMIT 20, 10;       -- 同上（旧语法）
```

---

### 2.2 条件筛选（WHERE）

#### WHERE子句常用操作

```sql
-- 等值查询
SELECT * FROM users WHERE id = 1;
SELECT * FROM users WHERE username = 'admin';

-- 不等于
SELECT * FROM users WHERE status != 0;
SELECT * FROM users WHERE status <> 0;  -- 同上

-- 比较运算
SELECT * FROM orders WHERE amount > 1000;
SELECT * FROM orders WHERE order_date >= '2024-01-01';

-- 范围查询
SELECT * FROM orders WHERE amount BETWEEN 100 AND 1000;
SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

-- IN 查询
SELECT * FROM users WHERE id IN (1, 2, 3, 5, 8);
SELECT * FROM users WHERE city IN ('北京', '上海', '深圳');

-- 模糊查询（LIKE）⭐ 常用
SELECT * FROM users WHERE username LIKE 'admin%';    -- admin开头
SELECT * FROM users WHERE username LIKE '%admin%';   -- 包含admin
SELECT * FROM users WHERE username LIKE '_dmin';     -- 第一个字符任意
SELECT * FROM users WHERE email LIKE '%@gmail.com';  -- gmail邮箱

-- 空值查询
SELECT * FROM users WHERE phone IS NULL;
SELECT * FROM users WHERE phone IS NOT NULL;

-- 逻辑运算（AND, OR, NOT）
SELECT * FROM users 
WHERE city = '北京' AND status = 1;

SELECT * FROM users 
WHERE city = '北京' OR city = '上海';

SELECT * FROM users 
WHERE city = '北京' AND (status = 1 OR status = 2);
```

⚠️ **LIKE性能注意**：
- `LIKE 'keyword%'` 可以使用索引（高效）
- `LIKE '%keyword%'` 无法使用索引（慢）
- 大数据量时避免使用 `%keyword%` 开头的模糊查询

---

### 2.3 排序（ORDER BY）

```sql
-- 升序排序（默认）
SELECT * FROM users ORDER BY created_at;
SELECT * FROM users ORDER BY created_at ASC;

-- 降序排序（常用）⭐
SELECT * FROM users ORDER BY created_at DESC;

-- 多列排序
SELECT * FROM orders 
ORDER BY status ASC, order_date DESC;

-- 按计算结果排序
SELECT *, (price * quantity) AS total 
FROM order_items 
ORDER BY total DESC;

-- NULL值排序
SELECT * FROM users ORDER BY phone IS NULL, phone;  -- NULL在后
```

---

### 2.4 聚合函数

#### 常用聚合函数

```sql
-- 计数
SELECT COUNT(*) FROM users;                    -- 总行数
SELECT COUNT(phone) FROM users;                -- phone非空的行数
SELECT COUNT(DISTINCT city) FROM users;        -- 不同城市数量

-- 求和
SELECT SUM(amount) FROM orders;
SELECT SUM(price * quantity) FROM order_items;

-- 平均值
SELECT AVG(amount) FROM orders;
SELECT ROUND(AVG(amount), 2) FROM orders;     -- 保留2位小数

-- 最大值/最小值
SELECT MAX(amount) FROM orders;
SELECT MIN(amount) FROM orders;
SELECT MAX(created_at), MIN(created_at) FROM orders;  -- 最新和最早时间
```

---

### 2.5 分组查询（GROUP BY）⭐ 重要

#### 基本分组

```sql
-- 按城市分组统计用户数
SELECT city, COUNT(*) AS user_count 
FROM users 
GROUP BY city;

-- 按日期分组统计订单
SELECT 
    DATE(order_date) AS order_day,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount
FROM orders 
GROUP BY DATE(order_date)
ORDER BY order_day DESC;

-- 多列分组
SELECT 
    city, 
    gender, 
    COUNT(*) AS count 
FROM users 
GROUP BY city, gender;
```

#### 分组过滤（HAVING）

```sql
-- HAVING用于过滤分组结果（WHERE是过滤原始数据）⭐
SELECT 
    city, 
    COUNT(*) AS user_count 
FROM users 
GROUP BY city 
HAVING user_count > 100;  -- 只显示用户数超过100的城市

-- WHERE和HAVING结合使用
SELECT 
    city, 
    COUNT(*) AS user_count 
FROM users 
WHERE status = 1          -- 先过滤：只统计启用的用户
GROUP BY city 
HAVING user_count > 50    -- 再过滤：只显示用户数>50的城市
ORDER BY user_count DESC;
```

⚠️ **WHERE vs HAVING**：
- `WHERE`：过滤原始数据（分组前）
- `HAVING`：过滤分组结果（分组后）
- `WHERE` 不能使用聚合函数
- `HAVING` 可以使用聚合函数

---

### 2.6 表连接（JOIN）⭐⭐⭐⭐⭐ 核心重点

#### 表连接类型对比

```
LEFT JOIN（左连接）     INNER JOIN（内连接）    RIGHT JOIN（右连接）
    
左表全部显示               只显示匹配的             右表全部显示
右表不匹配显示NULL         不匹配的不显示           左表不匹配显示NULL
```

#### INNER JOIN（内连接）- 最常用

```sql
-- 查询订单及对应的用户信息
SELECT 
    orders.id,
    orders.order_no,
    orders.amount,
    users.username,
    users.email
FROM orders
INNER JOIN users ON orders.user_id = users.id;

-- 使用表别名（推荐写法）⭐
SELECT 
    o.id,
    o.order_no,
    o.amount,
    u.username,
    u.email
FROM orders o
INNER JOIN users u ON o.user_id = u.id
WHERE o.status = 1
ORDER BY o.created_at DESC;
```

#### LEFT JOIN（左连接）- 常用

```sql
-- 查询所有用户及其订单（没有订单的用户也显示）
SELECT 
    u.id,
    u.username,
    o.order_no,
    o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- 查询没有下过订单的用户
SELECT 
    u.id,
    u.username
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;  -- 关键：右表没有匹配时为NULL
```

#### 多表连接

```sql
-- 订单 + 用户 + 订单明细
SELECT 
    o.order_no AS 订单号,
    u.username AS 用户名,
    oi.product_name AS 商品名称,
    oi.quantity AS 数量,
    oi.price AS 单价,
    (oi.quantity * oi.price) AS 小计
FROM orders o
INNER JOIN users u ON o.user_id = u.id
INNER JOIN order_items oi ON o.id = oi.order_id
WHERE o.order_date >= '2024-01-01'
ORDER BY o.order_no, oi.id;
```

#### 自连接（Self Join）

```sql
-- 查询员工及其上级
SELECT 
    e1.name AS employee,
    e2.name AS manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;
```

💡 **JOIN最佳实践**：
1. 总是使用表别名，代码更清晰
2. 连接条件放在 `ON` 中，筛选条件放在 `WHERE` 中
3. 大表连接时确保连接字段有索引
4. 避免连接过多表（超过5个表性能下降）

---

### 2.7 子查询

#### 标量子查询（返回单个值）

```sql
-- 查询工资高于平均工资的员工
SELECT name, salary 
FROM employees 
WHERE salary > (SELECT AVG(salary) FROM employees);

-- 查询最新订单的信息
SELECT * 
FROM orders 
WHERE created_at = (SELECT MAX(created_at) FROM orders);
```

#### 列子查询（返回一列）

```sql
-- 查询在北京或上海的用户的订单
SELECT * 
FROM orders 
WHERE user_id IN (
    SELECT id FROM users WHERE city IN ('北京', '上海')
);
```

#### 表子查询（返回多行多列）

```sql
-- 查询每个城市最高工资的员工
SELECT * 
FROM employees e
INNER JOIN (
    SELECT city, MAX(salary) AS max_salary
    FROM employees
    GROUP BY city
) t ON e.city = t.city AND e.salary = t.max_salary;
```

#### EXISTS子查询

```sql
-- 查询有订单的用户
SELECT * 
FROM users u 
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- 查询没有订单的用户
SELECT * 
FROM users u 
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);
```

---

## 阶段三：数据管理与优化

### 目标
掌握数据增删改、索引优化和事务处理（⭐⭐⭐⭐ 重要）

### 预计时间
2-3周

---

### 3.1 数据插入（INSERT）

#### 基本插入

```sql
-- 插入单条记录（指定列）
INSERT INTO users (username, email, password) 
VALUES ('zhangsan', 'zhangsan@example.com', 'password123');

-- 插入单条记录（所有列，不推荐）
INSERT INTO users 
VALUES (NULL, 'lisi', 'lisi@example.com', 'password123', NOW(), NOW());

-- 插入多条记录（推荐，效率高）⭐
INSERT INTO users (username, email, password) VALUES
('user1', 'user1@example.com', 'pass1'),
('user2', 'user2@example.com', 'pass2'),
('user3', 'user3@example.com', 'pass3');
```

#### 插入查询结果

```sql
-- 从另一个表插入数据
INSERT INTO users_backup (id, username, email)
SELECT id, username, email FROM users WHERE status = 0;

-- 创建表并插入数据
CREATE TABLE users_2024 AS 
SELECT * FROM users WHERE YEAR(created_at) = 2024;
```

#### 忽略重复/更新重复

```sql
-- 遇到重复键则忽略（MySQL特有）⭐
INSERT IGNORE INTO users (username, email, password) 
VALUES ('admin', 'admin@example.com', 'password');

-- 遇到重复键则更新（MySQL特有，非常实用）⭐
INSERT INTO users (id, username, email, login_count) 
VALUES (1, 'admin', 'admin@example.com', 1)
ON DUPLICATE KEY UPDATE 
    login_count = login_count + 1,
    updated_at = NOW();
```

💡 **ON DUPLICATE KEY UPDATE** 常用场景：
- 统计数据（存在则累加，不存在则插入）
- 缓存数据更新
- 同步数据

---

### 3.2 数据更新（UPDATE）

```sql
-- 更新单条记录
UPDATE users 
SET email = 'newemail@example.com' 
WHERE id = 1;

-- 更新多个字段
UPDATE users 
SET 
    email = 'newemail@example.com',
    phone = '13800138000',
    updated_at = NOW()
WHERE id = 1;

-- 批量更新
UPDATE users 
SET status = 1 
WHERE city = '北京' AND status = 0;

-- 使用计算更新
UPDATE products 
SET price = price * 1.1 
WHERE category = '电子产品';

-- 基于其他表更新（使用JOIN）
UPDATE orders o
INNER JOIN users u ON o.user_id = u.id
SET o.user_email = u.email
WHERE o.user_email IS NULL;
```

⚠️ **UPDATE注意事项**：
- 务必加 `WHERE` 条件，否则更新全表！
- 更新前先用 `SELECT` 验证条件是否正确
- 重要数据更新前先备份
- 生产环境建议开启安全模式：`SET sql_safe_updates = 1;`

---

### 3.3 数据删除（DELETE）

```sql
-- 删除单条记录
DELETE FROM users WHERE id = 1;

-- 批量删除
DELETE FROM users WHERE status = 0 AND created_at < '2020-01-01';

-- 删除全表数据（保留表结构）
DELETE FROM users;  -- 慢，可回滚
TRUNCATE TABLE users;  -- 快，不可回滚，重置自增ID

-- 基于其他表删除
DELETE o 
FROM orders o
INNER JOIN users u ON o.user_id = u.id
WHERE u.status = 0;
```

⚠️ **DELETE注意事项**：
- 务必加 `WHERE` 条件！
- 删除前先 `SELECT` 验证
- 重要数据考虑软删除（标记状态而不是真删除）
- `TRUNCATE` 速度快但无法回滚

#### 软删除最佳实践

```sql
-- 不要真删除，添加deleted_at字段
ALTER TABLE users ADD COLUMN deleted_at DATETIME DEFAULT NULL;

-- "删除"时更新字段
UPDATE users SET deleted_at = NOW() WHERE id = 1;

-- 查询时过滤已删除数据
SELECT * FROM users WHERE deleted_at IS NULL;

-- 恢复数据
UPDATE users SET deleted_at = NULL WHERE id = 1;
```

---

### 3.4 索引优化（⭐⭐⭐⭐⭐ 性能关键）

#### 索引基础概念

```
索引就像书的目录：
- 没有索引：全表扫描（翻遍整本书）
- 有索引：快速定位（通过目录直接翻到对应页）
```

#### 索引类型

| 索引类型 | MySQL关键字 | 说明 | 使用场景 |
|---------|------------|------|---------|
| **主键索引** | PRIMARY KEY | 唯一且非空 | 主键（id） |
| **唯一索引** | UNIQUE | 值唯一 | 用户名、邮箱 |
| **普通索引** | INDEX | 加速查询 | 查询字段 |
| **全文索引** | FULLTEXT | 文本搜索 | 文章搜索 |
| **组合索引** | INDEX(col1,col2) | 多列索引 | 多条件查询 |

#### 创建索引

```sql
-- 创建单列索引
CREATE INDEX idx_username ON users(username);
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_created_at ON users(created_at);

-- 创建唯一索引
CREATE UNIQUE INDEX idx_email_unique ON users(email);

-- 创建组合索引（最左前缀原则）⭐
CREATE INDEX idx_city_status ON users(city, status);

-- 在表创建时定义索引（推荐）
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_no VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2),
    status TINYINT,
    created_at DATETIME,
    
    UNIQUE INDEX idx_order_no (order_no),
    INDEX idx_user_id (user_id),
    INDEX idx_status_created (status, created_at)
) ENGINE=InnoDB;
```

#### 查看和删除索引

```sql
-- 查看表的索引
SHOW INDEX FROM users;

-- 查看SQL执行计划（重要！）⭐
EXPLAIN SELECT * FROM users WHERE username = 'admin';

-- 删除索引
DROP INDEX idx_username ON users;
ALTER TABLE users DROP INDEX idx_username;
```

#### 索引优化原则（⭐⭐⭐⭐⭐ 必读）

✅ **应该创建索引的情况**：
1. WHERE 条件中经常使用的列
2. JOIN 连接条件的列
3. ORDER BY 排序的列
4. GROUP BY 分组的列
5. 数据区分度高的列（如用户ID、订单号）

❌ **不应该创建索引的情况**：
1. 很少查询的列
2. 数据重复度高的列（如性别：只有男/女）
3. 频繁更新的列
4. 数据量很小的表（<1000行）

💡 **组合索引最左前缀原则**：

```sql
-- 创建组合索引
CREATE INDEX idx_abc ON users(a, b, c);

-- 可以使用索引的查询
WHERE a = 1
WHERE a = 1 AND b = 2
WHERE a = 1 AND b = 2 AND c = 3
WHERE a = 1 AND c = 3  -- 只用到a

-- 不能使用索引的查询
WHERE b = 2
WHERE c = 3
WHERE b = 2 AND c = 3
```

#### 慢查询优化步骤

```sql
-- 1. 开启慢查询日志
SET GLOBAL slow_query_log = 1;
SET GLOBAL long_query_time = 2;  -- 超过2秒记录

-- 2. 使用EXPLAIN分析查询
EXPLAIN SELECT * FROM orders WHERE user_id = 123;

-- 3. 查看EXPLAIN结果重点关注
-- type: ALL(全表扫描，最差) < index < range < ref < eq_ref < const(最好)
-- key: 使用了哪个索引
-- rows: 扫描行数（越少越好）
-- Extra: Using filesort(需优化), Using temporary(需优化)

-- 4. 优化示例
-- 优化前（全表扫描）
SELECT * FROM orders WHERE YEAR(created_at) = 2024;

-- 优化后（使用索引）
SELECT * FROM orders 
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

---

### 3.5 事务处理（⭐⭐⭐⭐ 重要）

#### ACID特性

| 特性 | 英文 | 说明 | 例子 |
|------|------|------|------|
| **原子性** | Atomicity | 全部成功或全部失败 | 转账：扣款和到账必须同时成功 |
| **一致性** | Consistency | 数据前后一致 | 转账前后总金额不变 |
| **隔离性** | Isolation | 事务间互不干扰 | 两人同时转账不冲突 |
| **持久性** | Durability | 提交后永久保存 | 断电后数据不丢失 |

#### 事务基本操作

```sql
-- 开启事务
START TRANSACTION;
-- 或
BEGIN;

-- 执行SQL操作
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- 提交事务（成功）
COMMIT;

-- 回滚事务（失败）
ROLLBACK;
```

#### 转账案例（完整版）

```sql
-- 转账示例：A向B转账100元
START TRANSACTION;

-- 1. 检查A的余额
SELECT @balance := balance FROM accounts WHERE id = 1 FOR UPDATE;

-- 2. 判断余额是否足够
IF @balance >= 100 THEN
    -- 3. A扣款
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    
    -- 4. B到账
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
    
    -- 5. 记录转账日志
    INSERT INTO transfer_logs (from_id, to_id, amount, created_at) 
    VALUES (1, 2, 100, NOW());
    
    -- 6. 提交事务
    COMMIT;
ELSE
    -- 余额不足，回滚
    ROLLBACK;
END IF;
```

#### 事务隔离级别

| 隔离级别 | 脏读 | 不可重复读 | 幻读 | 说明 |
|---------|------|-----------|------|------|
| **READ UNCOMMITTED** | ✅会 | ✅会 | ✅会 | 最低级别 |
| **READ COMMITTED** | ❌不会 | ✅会 | ✅会 | 大多数数据库默认 |
| **REPEATABLE READ** | ❌不会 | ❌不会 | ✅会 | MySQL默认⭐ |
| **SERIALIZABLE** | ❌不会 | ❌不会 | ❌不会 | 最高级别，性能最差 |

```sql
-- 查看当前隔离级别
SELECT @@transaction_isolation;

-- 设置隔离级别
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

💡 **隔离级别使用建议**：
- 一般使用MySQL默认的 `REPEATABLE READ`
- 对一致性要求极高：`SERIALIZABLE`
- 对性能要求高且可接受不一致：`READ COMMITTED`

---

### 3.6 字符集与编码（⭐⭐⭐⭐⭐ MySQL常见坑）

#### 字符集对比

| 字符集 | 说明 | 是否推荐 |
|-------|------|---------|
| **utf8mb4** | 完整UTF-8，支持emoji | ✅ 强烈推荐 |
| **utf8** | 不完整UTF-8，不支持emoji | ❌ 不推荐 |
| **gbk** | 中文编码 | ❌ 不推荐 |
| **latin1** | 西欧编码 | ❌ 不推荐 |

⚠️ **关键问题**：MySQL的 `utf8` 不是真正的UTF-8！
- MySQL的 `utf8` 最多存储3字节字符
- 不支持emoji（需要4字节）
- 必须使用 `utf8mb4` 才是完整UTF-8

#### 查看和设置字符集

```sql
-- 查看数据库字符集
SHOW CREATE DATABASE sales_db;

-- 查看表字符集
SHOW CREATE TABLE users;

-- 查看所有字符集设置
SHOW VARIABLES LIKE 'character%';

-- 创建数据库时指定字符集（推荐）⭐
CREATE DATABASE mydb 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 修改数据库字符集
ALTER DATABASE mydb 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 修改表字符集
ALTER TABLE users 
CONVERT TO CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 修改列字符集
ALTER TABLE users 
MODIFY COLUMN username VARCHAR(50) 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

#### 配置文件设置（推荐）

在 `my.cnf` 或 `my.ini` 中添加：

```ini
[client]
default-character-set = utf8mb4

[mysql]
default-character-set = utf8mb4

[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
init_connect='SET NAMES utf8mb4'
```

💡 **字符集最佳实践**：
1. 新项目一律使用 `utf8mb4`
2. 排序规则使用 `utf8mb4_unicode_ci`
3. 连接数据库时设置：`SET NAMES utf8mb4`
4. Python连接时指定：`charset='utf8mb4'`

---

## 阶段四：CSV文件操作专题

### 目标
精通MySQL与CSV文件的导入导出（⭐⭐⭐⭐⭐ 工作重点）

### 预计时间
1-2周

---

### 4.1 CSV导入（LOAD DATA INFILE）⭐⭐⭐⭐⭐

#### 完整语法

```sql
LOAD DATA 
    [LOW_PRIORITY | CONCURRENT] 
    [LOCAL] 
    INFILE 'file_path'
    [REPLACE | IGNORE]
    INTO TABLE table_name
    [CHARACTER SET charset_name]
    [FIELDS
        [TERMINATED BY 'string']
        [[OPTIONALLY] ENCLOSED BY 'char']
        [ESCAPED BY 'char']
    ]
    [LINES
        [STARTING BY 'string']
        [TERMINATED BY 'string']
    ]
    [IGNORE number LINES]
    [(col_name_or_user_var,...)]
    [SET col_name = expr,...]
```

#### 基础导入示例

```sql
-- 示例1：最简单的导入
LOAD DATA LOCAL INFILE 'C:/data/users.csv'
INTO TABLE users
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;  -- 跳过表头

-- 示例2：指定字符集（重要）⭐
LOAD DATA LOCAL INFILE 'C:/data/users.csv'
INTO TABLE users
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- 示例3：指定列映射
LOAD DATA LOCAL INFILE 'C:/data/users.csv'
INTO TABLE users
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(username, email, phone);  -- CSV中只有这3列
```

#### 参数详解

| 参数 | 说明 | 常用值 |
|------|------|--------|
| **LOCAL** | 从客户端读取文件 | 必加（否则需要服务器权限） |
| **TERMINATED BY** | 字段分隔符 | ',' 或 '\t' |
| **ENCLOSED BY** | 字段包围符 | '"' |
| **ESCAPED BY** | 转义字符 | '\\' |
| **LINES TERMINATED BY** | 行分隔符 | '\n' (Linux/Mac) 或 '\r\n' (Windows) |
| **IGNORE n LINES** | 跳过前n行 | 1（跳过表头） |
| **CHARACTER SET** | 字符集 | utf8mb4 |

#### 高级导入示例

```sql
-- 示例4：数据转换
LOAD DATA LOCAL INFILE 'C:/data/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(order_no, @amount, @order_date, status)
SET 
    amount = @amount * 100,  -- 转换单位（元转分）
    order_date = STR_TO_DATE(@order_date, '%Y-%m-%d'),  -- 日期格式转换
    created_at = NOW();

-- 示例5：条件导入（使用REPLACE或IGNORE）
LOAD DATA LOCAL INFILE 'C:/data/products.csv'
REPLACE INTO TABLE products  -- 遇到重复主键则替换
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- 示例6：导入部分列
LOAD DATA LOCAL INFILE 'C:/data/partial.csv'
INTO TABLE users
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(username, email)  -- 只导入这两列
SET 
    status = 1,  -- 其他列设置默认值
    created_at = NOW();
```

---

### 4.2 CSV导出（SELECT INTO OUTFILE）

#### 基础导出

```sql
-- 示例1：导出整表
SELECT * FROM users
INTO OUTFILE 'C:/data/users_export.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

-- 示例2：导出指定列和条件
SELECT username, email, phone, created_at
FROM users
WHERE status = 1 AND created_at >= '2024-01-01'
INTO OUTFILE 'C:/data/active_users.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

-- 示例3：导出带表头
SELECT 'username', 'email', 'phone', 'created_at'
UNION ALL
SELECT username, email, phone, DATE_FORMAT(created_at, '%Y-%m-%d')
FROM users
INTO OUTFILE 'C:/data/users_with_header.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

#### 导出汇总数据

```sql
-- 导出统计报表
SELECT 
    DATE(order_date) AS 日期,
    COUNT(*) AS 订单数,
    SUM(amount) AS 总金额,
    AVG(amount) AS 平均金额
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY DATE(order_date)
INTO OUTFILE 'C:/data/daily_report.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

---

### 4.3 CSV编码问题处理（⭐⭐⭐⭐⭐ 常见坑）

#### 问题诊断

```sql
-- 检查数据库字符集
SHOW VARIABLES LIKE 'character%';

-- 检查表字符集
SHOW CREATE TABLE users;

-- 检查连接字符集
SHOW VARIABLES LIKE 'collation%';
```

#### UTF-8 CSV导入

```sql
-- UTF-8编码的CSV（最常见）
LOAD DATA LOCAL INFILE 'C:/data/users_utf8.csv'
INTO TABLE users
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```

#### GBK CSV导入

```sql
-- GBK编码的CSV（中文Windows默认）
LOAD DATA LOCAL INFILE 'C:/data/users_gbk.csv'
INTO TABLE users
CHARACTER SET gbk
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```

#### 编码转换

```bash
# 使用iconv转换编码（Linux/Mac）
iconv -f GBK -t UTF-8 input.csv > output.csv

# 使用Python转换
python -c "import sys; open('output.csv','wb').write(open('input.csv','rb').read().decode('gbk').encode('utf-8'))"
```

💡 **编码问题排查流程**：
1. 确认CSV文件编码（UTF-8还是GBK）
2. 确认MySQL数据库和表的字符集（应该是utf8mb4）
3. 导入时指定正确的 `CHARACTER SET`
4. 如果乱码，用工具转换CSV编码后再导入

---

### 4.4 CSV导入权限问题

#### 启用LOCAL INFILE

```sql
-- 查看是否启用
SHOW GLOBAL VARIABLES LIKE 'local_infile';

-- 启用LOCAL INFILE（需要管理员权限）
SET GLOBAL local_infile = 1;
```

#### 文件路径注意事项

⚠️ **路径格式**：
- Windows：使用正斜杠 `/` 或双反斜杠 `\\`
  - 正确：`'C:/data/file.csv'`
  - 正确：`'C:\\data\\file.csv'`
  - 错误：`'C:\data\file.csv'`
- Linux/Mac：直接使用绝对路径
  - 正确：`'/home/user/data/file.csv'`

#### 权限错误解决

```sql
-- 错误1：The MySQL server is running with the --secure-file-priv option
-- 解决：查看允许的目录
SHOW VARIABLES LIKE 'secure_file_priv';

-- 解决方案：
-- 1. 将CSV文件放到允许的目录
-- 2. 或修改my.cnf：secure_file_priv = ""

-- 错误2：Access denied
-- 解决：授予FILE权限
GRANT FILE ON *.* TO 'username'@'localhost';

-- 使用LOCAL关键字绕过（推荐）⭐
LOAD DATA LOCAL INFILE ...
```

---

### 4.5 大文件CSV导入优化

#### 性能优化技巧

```sql
-- 1. 临时禁用索引和约束（大幅提速）⭐
ALTER TABLE users DISABLE KEYS;  -- 禁用非主键索引

LOAD DATA LOCAL INFILE 'C:/data/large.csv'
INTO TABLE users
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

ALTER TABLE users ENABLE KEYS;  -- 重新启用索引

-- 2. 调整批量插入大小
SET SESSION bulk_insert_buffer_size = 256 * 1024 * 1024;  -- 256MB

-- 3. 关闭自动提交（提高性能）
SET autocommit = 0;

LOAD DATA LOCAL INFILE 'C:/data/large.csv'
INTO TABLE users
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

COMMIT;
SET autocommit = 1;

-- 4. 临时禁用外键检查
SET FOREIGN_KEY_CHECKS = 0;

LOAD DATA LOCAL INFILE 'C:/data/large.csv'
INTO TABLE users
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

SET FOREIGN_KEY_CHECKS = 1;
```

#### 分批导入策略

```sql
-- 方案1：按行数分割CSV文件（推荐）
-- 使用split命令或Python脚本分割成多个小文件

-- 方案2：使用LIMIT分批（如果数据在临时表中）
INSERT INTO target_table 
SELECT * FROM temp_table LIMIT 0, 10000;

INSERT INTO target_table 
SELECT * FROM temp_table LIMIT 10000, 10000;
-- 继续...
```

#### 导入监控

```sql
-- 查看导入进度（另开终端）
SELECT COUNT(*) FROM users;

-- 查看表大小
SELECT 
    table_name,
    ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb
FROM information_schema.tables
WHERE table_schema = 'your_database'
AND table_name = 'users';
```

---

### 4.6 CSV数据验证

#### 导入前验证

```sql
-- 创建临时表测试
CREATE TEMPORARY TABLE users_temp LIKE users;

LOAD DATA LOCAL INFILE 'C:/data/test.csv'
INTO TABLE users_temp
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- 检查数据
SELECT COUNT(*) FROM users_temp;
SELECT * FROM users_temp LIMIT 10;

-- 检查异常数据
SELECT * FROM users_temp WHERE email NOT LIKE '%@%';  -- 无效邮箱
SELECT * FROM users_temp WHERE phone NOT REGEXP '^[0-9]{11}$';  -- 无效手机号

-- 没问题后导入正式表
INSERT INTO users SELECT * FROM users_temp;
```

#### 导入后验证

```sql
-- 1. 验证行数
-- CSV行数（使用wc -l 或 Python）
-- MySQL行数
SELECT COUNT(*) FROM users;

-- 2. 验证数据完整性
SELECT COUNT(*) AS total,
       COUNT(DISTINCT email) AS unique_emails,
       COUNT(*) - COUNT(phone) AS null_phones
FROM users;

-- 3. 验证数据范围
SELECT MIN(created_at), MAX(created_at) FROM users;
SELECT MIN(amount), MAX(amount), AVG(amount) FROM orders;

-- 4. 查找异常数据
SELECT * FROM users WHERE created_at > NOW();  -- 未来日期
SELECT * FROM orders WHERE amount < 0;  -- 负数金额
```

---

### 4.7 CSV导入错误处理

#### 常见错误和解决方案

```sql
-- 错误1：Data too long for column
-- 原因：字段长度不够
-- 解决：修改表结构
ALTER TABLE users MODIFY COLUMN address VARCHAR(500);

-- 错误2：Incorrect date value
-- 原因：日期格式不匹配
-- 解决：使用STR_TO_DATE转换
LOAD DATA LOCAL INFILE 'C:/data/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(order_no, amount, @order_date)
SET order_date = STR_TO_DATE(@order_date, '%m/%d/%Y');  -- 转换格式

-- 错误3：Duplicate entry for key 'PRIMARY'
-- 原因：主键重复
-- 解决：使用IGNORE或REPLACE
LOAD DATA LOCAL INFILE 'C:/data/users.csv'
IGNORE INTO TABLE users  -- 忽略重复行
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```

#### 错误日志记录

```sql
-- 创建错误日志表
CREATE TABLE import_errors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50),
    error_line TEXT,
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 导入时记录警告
SHOW WARNINGS;  -- 导入后立即执行
```

---

## 阶段五：高级特性与实战

### 目标
掌握存储过程、触发器等高级特性（⭐⭐⭐ 进阶）

### 预计时间
持续实践

---

### 5.1 存储过程

#### 基础语法

```sql
-- 创建简单存储过程
DELIMITER //

CREATE PROCEDURE GetUserCount()
BEGIN
    SELECT COUNT(*) AS user_count FROM users;
END //

DELIMITER ;

-- 调用存储过程
CALL GetUserCount();
```

#### 带参数的存储过程

```sql
DELIMITER //

CREATE PROCEDURE GetUsersByCity(IN city_name VARCHAR(50))
BEGIN
    SELECT * FROM users WHERE city = city_name;
END //

DELIMITER ;

-- 调用
CALL GetUsersByCity('北京');
```

#### 输出参数

```sql
DELIMITER //

CREATE PROCEDURE GetOrderStats(
    IN start_date DATE,
    IN end_date DATE,
    OUT total_orders INT,
    OUT total_amount DECIMAL(10,2)
)
BEGIN
    SELECT 
        COUNT(*),
        SUM(amount)
    INTO total_orders, total_amount
    FROM orders
    WHERE order_date BETWEEN start_date AND end_date;
END //

DELIMITER ;

-- 调用
CALL GetOrderStats('2024-01-01', '2024-12-31', @orders, @amount);
SELECT @orders, @amount;
```

---

### 5.2 触发器

#### 创建触发器

```sql
-- 示例：记录用户信息修改日志
CREATE TABLE users_audit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    old_email VARCHAR(100),
    new_email VARCHAR(100),
    changed_at DATETIME
);

DELIMITER //

CREATE TRIGGER users_after_update
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email <> NEW.email THEN
        INSERT INTO users_audit (user_id, old_email, new_email, changed_at)
        VALUES (NEW.id, OLD.email, NEW.email, NOW());
    END IF;
END //

DELIMITER ;
```

#### 触发器类型

| 类型 | 说明 | 使用场景 |
|------|------|---------|
| **BEFORE INSERT** | 插入前触发 | 数据验证、自动填充 |
| **AFTER INSERT** | 插入后触发 | 记录日志、更新统计 |
| **BEFORE UPDATE** | 更新前触发 | 数据验证、权限检查 |
| **AFTER UPDATE** | 更新后触发 | 记录变更、同步数据 |
| **BEFORE DELETE** | 删除前触发 | 权限检查、防止误删 |
| **AFTER DELETE** | 删除后触发 | 记录日志、清理关联 |

---

### 5.3 视图

```sql
-- 创建视图（简化复杂查询）
CREATE VIEW active_users AS
SELECT id, username, email, created_at
FROM users
WHERE status = 1;

-- 使用视图
SELECT * FROM active_users;

-- 创建统计视图
CREATE VIEW daily_sales AS
SELECT 
    DATE(order_date) AS sale_date,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount
FROM orders
GROUP BY DATE(order_date);

-- 查询视图
SELECT * FROM daily_sales WHERE sale_date >= '2024-01-01';
```

---

## 实战场景应用

### 场景1：从CSV导入每日销售数据

#### 业务需求
每天早上8点接收昨日销售数据CSV文件，需要导入数据库并生成报表。

#### 实现步骤

```sql
-- 步骤1：创建表
CREATE TABLE daily_sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATE NOT NULL,
    product_id INT NOT NULL,
    product_name VARCHAR(100),
    quantity INT,
    price DECIMAL(10,2),
    amount DECIMAL(10,2),
    salesman VARCHAR(50),
    region VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sale_date (sale_date),
    INDEX idx_product_id (product_id),
    INDEX idx_region (region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 步骤2：导入CSV
LOAD DATA LOCAL INFILE 'C:/data/sales_20241229.csv'
INTO TABLE daily_sales
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(sale_date, product_id, product_name, quantity, price, @amount, salesman, region)
SET 
    amount = quantity * price,  -- 自动计算金额
    created_at = NOW();

-- 步骤3：数据验证
SELECT 
    COUNT(*) AS 总记录数,
    SUM(amount) AS 总金额,
    MIN(sale_date) AS 最早日期,
    MAX(sale_date) AS 最晚日期
FROM daily_sales
WHERE DATE(created_at) = CURDATE();

-- 步骤4：生成日报表
SELECT 
    region AS 区域,
    COUNT(*) AS 订单数,
    SUM(quantity) AS 销售数量,
    SUM(amount) AS 销售金额
FROM daily_sales
WHERE sale_date = CURDATE() - INTERVAL 1 DAY
GROUP BY region
ORDER BY 销售金额 DESC;
```

---

### 场景2：定期备份数据到CSV文件

#### 业务需求
每周末备份活跃用户数据到CSV文件，用于市场分析。

```sql
-- 导出最近30天活跃用户
SELECT 
    u.id AS 用户ID,
    u.username AS 用户名,
    u.email AS 邮箱,
    u.city AS 城市,
    COUNT(o.id) AS 订单数,
    SUM(o.amount) AS 消费金额,
    MAX(o.order_date) AS 最后购买日期
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.order_date >= CURDATE() - INTERVAL 30 DAY
GROUP BY u.id, u.username, u.email, u.city
HAVING 订单数 >= 3
INTO OUTFILE 'C:/backup/active_users_20241229.csv'
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

---

### 场景3：处理包含中文/特殊字符的CSV数据

#### 问题描述
CSV文件中包含中文、换行符、逗号等特殊字符。

#### 解决方案

```sql
-- CSV示例内容：
-- 张三,"北京市朝阳区望京街道SOHO,3号楼",备注：VIP客户
-- 上午收货

-- 1. 确保字段用引号包围
-- 2. 换行符在引号内会被正确处理
LOAD DATA LOCAL INFILE 'C:/data/customers.csv'
INTO TABLE customers
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'  -- 重要：包围符
ESCAPED BY '\\'  -- 转义符
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- 如果数据中有特殊字符问题，导入后清理
UPDATE customers 
SET address = REPLACE(address, '\r', '') 
WHERE address LIKE '%\r%';

UPDATE customers 
SET address = REPLACE(address, '\n', ' ') 
WHERE address LIKE '%\n%';
```

---

### 场景4：大文件CSV分批导入

#### 业务需求
导入500万行的CSV文件（2GB），避免内存溢出和超时。

```sql
-- 方案1：先导入临时表，再分批插入
CREATE TABLE users_temp (
    username VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50),
    created_at DATETIME
) ENGINE=InnoDB;

-- 临时表不加索引（加快导入）
LOAD DATA LOCAL INFILE 'C:/data/users_5m.csv'
INTO TABLE users_temp
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- 分批插入正式表（每次10万行）
SET @offset = 0;
SET @batch_size = 100000;

-- 循环插入（实际使用存储过程或脚本）
INSERT INTO users (username, email, city, created_at)
SELECT username, email, city, created_at
FROM users_temp
LIMIT 0, 100000;

-- 继续下一批...

-- 方案2：拆分CSV文件（推荐）⭐
-- 使用Python脚本拆分成多个小文件
```

**Python拆分脚本**：

```python
# split_csv.py
import pandas as pd

# 分块读取大CSV
chunk_size = 100000
i = 0

for chunk in pd.read_csv('users_5m.csv', chunksize=chunk_size):
    chunk.to_csv(f'users_part_{i}.csv', index=False)
    i += 1
    print(f'已生成第 {i} 个文件')
```

然后分别导入每个小文件：

```sql
LOAD DATA LOCAL INFILE 'C:/data/users_part_0.csv'
INTO TABLE users
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES;

LOAD DATA LOCAL INFILE 'C:/data/users_part_1.csv'
INTO TABLE users
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES;

-- 继续...
```

---

### 场景5：数据对账和验证流程

#### 业务需求
导入第三方提供的订单数据，需要与系统数据对账。

```sql
-- 步骤1：导入第三方数据到临时表
CREATE TEMPORARY TABLE orders_import (
    order_no VARCHAR(50),
    amount DECIMAL(10,2),
    order_date DATE,
    status VARCHAR(20)
);

LOAD DATA LOCAL INFILE 'C:/data/third_party_orders.csv'
INTO TABLE orders_import
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES;

-- 步骤2：对账 - 找出系统有但第三方没有的
SELECT o.*
FROM orders o
LEFT JOIN orders_import oi ON o.order_no = oi.order_no
WHERE oi.order_no IS NULL
  AND o.order_date = '2024-12-29';

-- 步骤3：对账 - 找出第三方有但系统没有的
SELECT oi.*
FROM orders_import oi
LEFT JOIN orders o ON oi.order_no = o.order_no
WHERE o.order_no IS NULL;

-- 步骤4：对账 - 找出金额不一致的
SELECT 
    o.order_no,
    o.amount AS 系统金额,
    oi.amount AS 第三方金额,
    (o.amount - oi.amount) AS 差异
FROM orders o
INNER JOIN orders_import oi ON o.order_no = oi.order_no
WHERE ABS(o.amount - oi.amount) > 0.01;  -- 允许0.01误差

-- 步骤5：生成对账报告
SELECT 
    '系统订单数' AS 项目, COUNT(*) AS 数量, SUM(amount) AS 金额
FROM orders WHERE order_date = '2024-12-29'
UNION ALL
SELECT 
    '第三方订单数', COUNT(*), SUM(amount)
FROM orders_import
UNION ALL
SELECT 
    '差异订单数', COUNT(*), SUM(ABS(o.amount - oi.amount))
FROM orders o
INNER JOIN orders_import oi ON o.order_no = oi.order_no
WHERE ABS(o.amount - oi.amount) > 0.01;
```

---

## 快速查询指南

### 按任务分类的SQL模板

#### 查询类

```sql
-- 查询前N条记录
SELECT * FROM table_name LIMIT 10;

-- 条件查询
SELECT * FROM table_name WHERE column = 'value';

-- 模糊查询
SELECT * FROM table_name WHERE column LIKE '%keyword%';

-- 范围查询
SELECT * FROM table_name WHERE column BETWEEN value1 AND value2;

-- 排序查询
SELECT * FROM table_name ORDER BY column DESC LIMIT 10;

-- 分组统计
SELECT column, COUNT(*) FROM table_name GROUP BY column;

-- 去重查询
SELECT DISTINCT column FROM table_name;

-- 表连接
SELECT a.*, b.column 
FROM table_a a 
INNER JOIN table_b b ON a.id = b.table_a_id;
```

#### 修改类

```sql
-- 插入单条
INSERT INTO table_name (col1, col2) VALUES ('val1', 'val2');

-- 批量插入
INSERT INTO table_name (col1, col2) VALUES
('val1', 'val2'),
('val3', 'val4');

-- 更新数据
UPDATE table_name SET column = 'new_value' WHERE id = 1;

-- 删除数据
DELETE FROM table_name WHERE condition;

-- 清空表
TRUNCATE TABLE table_name;
```

#### 结构类

```sql
-- 创建表
CREATE TABLE table_name (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 添加列
ALTER TABLE table_name ADD COLUMN new_column VARCHAR(50);

-- 修改列
ALTER TABLE table_name MODIFY COLUMN column_name VARCHAR(100);

-- 删除列
ALTER TABLE table_name DROP COLUMN column_name;

-- 添加索引
CREATE INDEX idx_column ON table_name(column_name);

-- 删除索引
DROP INDEX idx_column ON table_name;
```

#### CSV操作类

```sql
-- 导入CSV
LOAD DATA LOCAL INFILE '/path/to/file.csv'
INTO TABLE table_name
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- 导出CSV
SELECT * FROM table_name
INTO OUTFILE '/path/to/output.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

---

### 常见SQL速查表

#### 日期时间函数

| 函数 | 说明 | 示例 |
|------|------|------|
| NOW() | 当前日期时间 | SELECT NOW(); |
| CURDATE() | 当前日期 | SELECT CURDATE(); |
| CURTIME() | 当前时间 | SELECT CURTIME(); |
| DATE() | 提取日期部分 | SELECT DATE(NOW()); |
| YEAR(), MONTH(), DAY() | 提取年月日 | SELECT YEAR(NOW()); |
| DATE_ADD() | 日期加法 | DATE_ADD(NOW(), INTERVAL 7 DAY) |
| DATE_SUB() | 日期减法 | DATE_SUB(NOW(), INTERVAL 1 MONTH) |
| DATEDIFF() | 日期差 | DATEDIFF(date1, date2) |
| DATE_FORMAT() | 格式化日期 | DATE_FORMAT(NOW(), '%Y-%m-%d') |

#### 字符串函数

| 函数 | 说明 | 示例 |
|------|------|------|
| CONCAT() | 连接字符串 | CONCAT('Hello', ' ', 'World') |
| LENGTH() | 字符串长度 | LENGTH('Hello') |
| UPPER(), LOWER() | 大小写转换 | UPPER('hello') |
| TRIM() | 去除空格 | TRIM('  text  ') |
| SUBSTRING() | 截取字符串 | SUBSTRING('Hello', 1, 3) |
| REPLACE() | 替换字符串 | REPLACE('Hello', 'l', 'L') |
| LEFT(), RIGHT() | 左右截取 | LEFT('Hello', 2) |

#### 数学函数

| 函数 | 说明 | 示例 |
|------|------|------|
| ROUND() | 四舍五入 | ROUND(3.14159, 2) |
| CEIL() | 向上取整 | CEIL(3.14) |
| FLOOR() | 向下取整 | FLOOR(3.99) |
| ABS() | 绝对值 | ABS(-10) |
| MOD() | 取余 | MOD(10, 3) |

---

## 学习资源和工具

### 推荐的MySQL客户端工具

#### 1. MySQL Workbench（官方工具）⭐
- **优点**：免费、功能全面、可视化建模
- **适合**：初学者、数据库设计
- **下载**：https://dev.mysql.com/downloads/workbench/

#### 2. Navicat（最流行）⭐⭐⭐⭐⭐
- **优点**：界面美观、功能强大、支持多数据库
- **缺点**：商业软件（有试用版）
- **适合**：日常开发、数据管理

#### 3. DBeaver（开源推荐）⭐⭐⭐⭐
- **优点**：免费开源、支持多数据库、插件丰富
- **适合**：开发者、跨数据库使用
- **下载**：https://dbeaver.io/

#### 4. phpMyAdmin（Web工具）
- **优点**：基于Web、无需安装客户端
- **适合**：服务器管理、远程访问

#### 5. HeidiSQL（Windows轻量级）
- **优点**：免费、轻量、速度快
- **适合**：Windows用户

### 在线学习资源

| 资源 | 类型 | 推荐指数 | 链接 |
|------|------|---------|------|
| MySQL官方文档 | 文档 | ⭐⭐⭐⭐⭐ | https://dev.mysql.com/doc/ |
| SQLBolt | 互动教程 | ⭐⭐⭐⭐⭐ | https://sqlbolt.com/ |
| LeetCode数据库题 | 刷题 | ⭐⭐⭐⭐ | https://leetcode.com/problemset/database/ |
| W3Schools SQL | 教程 | ⭐⭐⭐⭐ | https://www.w3schools.com/sql/ |

### 性能测试工具

- **mysqlslap**：MySQL自带压测工具
- **sysbench**：综合性能测试
- **pt-query-digest**：慢查询分析（Percona Toolkit）

---

## 常见问题解决方案

### 问题1：中文乱码

**症状**：插入中文显示为 ????

**解决**：

```sql
-- 1. 检查字符集
SHOW VARIABLES LIKE 'character%';

-- 2. 设置连接字符集
SET NAMES utf8mb4;

-- 3. 修改表字符集
ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4;

-- 4. 确保客户端连接指定utf8mb4
-- Python示例
import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='mydb',
    charset='utf8mb4'  # 重要
)
```

---

### 问题2：导入CSV权限错误

**错误**：The MySQL server is running with the --secure-file-priv option

**解决**：

```sql
-- 查看允许的目录
SHOW VARIABLES LIKE 'secure_file_priv';

-- 方案1：将文件放到允许的目录

-- 方案2：使用LOCAL关键字（推荐）
LOAD DATA LOCAL INFILE ...

-- 方案3：修改配置文件my.cnf（需重启MySQL）
[mysqld]
secure_file_priv = ""
```

---

### 问题3：慢查询优化

**症状**：查询速度很慢

**排查步骤**：

```sql
-- 1. 使用EXPLAIN分析
EXPLAIN SELECT * FROM orders WHERE user_id = 123;

-- 2. 检查是否使用索引
-- 看type列：ALL(全表扫描)最差，const最好

-- 3. 添加索引
CREATE INDEX idx_user_id ON orders(user_id);

-- 4. 避免SELECT *，只查询需要的列
SELECT id, order_no, amount FROM orders WHERE user_id = 123;

-- 5. 避免在WHERE中使用函数
-- 慢：WHERE YEAR(created_at) = 2024
-- 快：WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'
```

---

### 问题4：连接数过多

**错误**：Too many connections

**解决**：

```sql
-- 查看当前连接数
SHOW PROCESSLIST;

-- 查看最大连接数
SHOW VARIABLES LIKE 'max_connections';

-- 临时增加连接数
SET GLOBAL max_connections = 500;

-- 永久修改：编辑my.cnf
[mysqld]
max_connections = 500

-- 杀死空闲连接
KILL 连接ID;
```

---

### 问题5：锁表问题

**症状**：更新或删除时长时间等待

**解决**：

```sql
-- 查看锁表情况
SHOW OPEN TABLES WHERE In_use > 0;

-- 查看正在执行的事务
SELECT * FROM information_schema.INNODB_TRX;

-- 查看锁等待
SELECT * FROM information_schema.INNODB_LOCK_WAITS;

-- 杀死锁表的进程
KILL 进程ID;

-- 优化：大批量更新分批执行
UPDATE table_name SET column = value WHERE id BETWEEN 1 AND 1000;
UPDATE table_name SET column = value WHERE id BETWEEN 1001 AND 2000;
-- 继续...
```

---

### 问题6：MySQL 8.0认证问题

**错误**：Authentication plugin 'caching_sha2_password' cannot be loaded

**解决**：

```sql
-- 方案1：修改用户认证方式
ALTER USER 'username'@'localhost' 
IDENTIFIED WITH mysql_native_password BY 'password';

-- 方案2：创建用户时指定
CREATE USER 'username'@'localhost' 
IDENTIFIED WITH mysql_native_password BY 'password';

-- 方案3：修改默认认证插件（my.cnf）
[mysqld]
default_authentication_plugin=mysql_native_password
```

---

### 问题7：主键冲突

**错误**：Duplicate entry '1' for key 'PRIMARY'

**解决**：

```sql
-- 方案1：使用IGNORE忽略冲突
INSERT IGNORE INTO table_name ...

-- 方案2：使用REPLACE替换
REPLACE INTO table_name ...

-- 方案3：使用ON DUPLICATE KEY UPDATE
INSERT INTO table_name (id, name, count) 
VALUES (1, 'test', 10)
ON DUPLICATE KEY UPDATE count = count + 10;

-- 方案4：先删除再插入
DELETE FROM table_name WHERE id = 1;
INSERT INTO table_name VALUES (1, 'test');

-- 方案5：重置自增ID
ALTER TABLE table_name AUTO_INCREMENT = 1;
```

---

## 附录：MySQL 8.0 新特性

### 窗口函数（Window Functions）

```sql
-- ROW_NUMBER：行号
SELECT 
    username,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank
FROM employees;

-- RANK：排名（相同值排名相同，跳过）
SELECT 
    username,
    salary,
    RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;

-- DENSE_RANK：密集排名（相同值排名相同，不跳过）
SELECT 
    username,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;

-- 分组窗口
SELECT 
    department,
    username,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg
FROM employees;
```

### CTE（公用表表达式）

```sql
-- 使用WITH定义临时结果集
WITH sales_summary AS (
    SELECT 
        product_id,
        SUM(quantity) AS total_qty,
        SUM(amount) AS total_amount
    FROM orders
    GROUP BY product_id
)
SELECT 
    p.product_name,
    s.total_qty,
    s.total_amount
FROM sales_summary s
INNER JOIN products p ON s.product_id = p.id
WHERE s.total_amount > 10000;

-- 递归CTE
WITH RECURSIVE employee_hierarchy AS (
    -- 基础查询
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- 递归查询
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy;
```

### JSON支持增强

```sql
-- JSON字段查询
SELECT 
    id,
    data->>'$.name' AS name,
    data->>'$.age' AS age
FROM users
WHERE data->>'$.city' = '北京';

-- JSON数组处理
SELECT 
    id,
    JSON_EXTRACT(tags, '$[0]') AS first_tag,
    JSON_LENGTH(tags) AS tag_count
FROM products;
```

---

## 学习检查清单

### 阶段一：入门基础 ✅
- [ ] 能创建数据库和表
- [ ] 理解数据类型选择
- [ ] 掌握字符集设置（utf8mb4）
- [ ] 能修改表结构

### 阶段二：核心查询 ✅
- [ ] 熟练使用WHERE条件查询
- [ ] 掌握ORDER BY排序
- [ ] 掌握GROUP BY分组
- [ ] 熟练使用JOIN连接
- [ ] 理解子查询

### 阶段三：数据管理与优化 ✅
- [ ] 熟练使用INSERT/UPDATE/DELETE
- [ ] 理解索引原理
- [ ] 能使用EXPLAIN分析查询
- [ ] 掌握事务基础
- [ ] 能解决字符集问题

### 阶段四：CSV操作 ✅
- [ ] 熟练使用LOAD DATA INFILE
- [ ] 能处理编码问题
- [ ] 掌握数据验证方法
- [ ] 能处理大文件导入
- [ ] 能解决权限问题

### 阶段五：高级特性 ✅
- [ ] 了解存储过程
- [ ] 了解触发器
- [ ] 了解视图
- [ ] 能进行性能优化

---

## 总结

### 日常工作最常用的操作（优先掌握）⭐⭐⭐⭐⭐

1. **查询**：SELECT、WHERE、JOIN、GROUP BY
2. **CSV导入**：LOAD DATA INFILE
3. **索引优化**：CREATE INDEX、EXPLAIN
4. **数据修改**：INSERT、UPDATE、DELETE
5. **字符集**：utf8mb4设置

### 学习建议

1. **多实践**：每学一个知识点立即动手练习
2. **看官方文档**：遇到问题先查官方文档
3. **用EXPLAIN**：养成分析查询计划的习惯
4. **做笔记**：记录踩过的坑和解决方案
5. **项目驱动**：结合实际项目学习效果最好

### 下一步行动

1. 安装MySQL和客户端工具
2. 创建练习数据库
3. 跟着文档从阶段一开始实践
4. 重点练习CSV导入导出
5. 遇到问题查阅快速查询指南

---

*最后更新：2024-12-30*

祝学习顺利！有问题随时查阅本指南 📚


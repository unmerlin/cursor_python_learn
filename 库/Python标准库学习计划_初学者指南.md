# Python标准库学习计划 - 初学者完整指南

## 📚 目录
- [学习路线概览](#学习路线概览)
- [初级阶段（第1-4周）](#初级阶段第1-4周)
- [中级阶段（第5-8周）](#中级阶段第5-8周)
- [高级阶段（第9-12周）](#高级阶段第9-12周)
- [核心模块详解](#核心模块详解)
- [实践项目推荐](#实践项目推荐)
- [学习资源建议](#学习资源建议)
- [常见问题解答](#常见问题解答)

---

## 学习路线概览

### 🎯 总体目标
在12周内系统掌握Python标准库中20-30个最常用模块的核心功能，能够独立完成日常编程任务。

### 📊 学习阶段划分

| 阶段 | 周次 | 核心模块 | 学习重点 |
|------|------|----------|----------|
| **初级** | 1-4周 | os, sys, datetime, json, random, math | 基础操作、文件系统、数据类型 |
| **中级** | 5-8周 | re, collections, pathlib, csv, pickle | 数据处理、高级数据结构 |
| **高级** | 9-12周 | logging, functools, itertools, threading, argparse | 高级特性、并发、优化 |

---

## 初级阶段（第1-4周）

### 第1周：文件和系统操作基础
**学习模块**：`os`, `sys`
**学习目标**：掌握文件、目录操作和系统交互
**每日时间**：1-2小时

### 第2周：时间处理与数据序列化
**学习模块**：`datetime`, `json`
**学习目标**：处理日期时间、JSON数据
**每日时间**：1-2小时

### 第3周：数学计算与随机数
**学习模块**：`math`, `random`
**学习目标**：数学运算、随机数生成
**每日时间**：1小时

### 第4周：初级综合实践
**实践项目**：文件管理工具、简单数据处理脚本
**复习时间**：3-4小时

---

## 中级阶段（第5-8周）

### 第5周：正则表达式
**学习模块**：`re`
**学习目标**：文本模式匹配和提取
**每日时间**：1.5-2小时

### 第6周：高级数据结构
**学习模块**：`collections`
**学习目标**：Counter, defaultdict, deque等
**每日时间**：1.5小时

### 第7周：现代路径处理与数据文件
**学习模块**：`pathlib`, `csv`, `pickle`
**学习目标**：面向对象路径操作、数据持久化
**每日时间**：1.5小时

### 第8周：中级综合实践
**实践项目**：数据清洗工具、日志分析器
**复习时间**：4-5小时

---

## 高级阶段（第9-12周）

### 第9周：日志系统
**学习模块**：`logging`
**学习目标**：专业日志记录和管理
**每日时间**：1.5小时

### 第10周：函数式编程工具
**学习模块**：`functools`, `itertools`
**学习目标**：高阶函数、迭代器优化
**每日时间**：2小时

### 第11周：并发与命令行
**学习模块**：`threading`, `argparse`
**学习目标**：多线程、CLI开发
**每日时间**：2-3小时

### 第12周：综合项目实战
**大型项目**：多功能命令行工具
**时间投入**：10-15小时

---

## 核心模块详解

### 1️⃣ os - 操作系统接口

#### 📝 模块简介
提供与操作系统交互的功能，用于文件和目录操作、环境变量管理、进程控制等。

#### 🔑 核心方法
```python
os.getcwd()          # 获取当前工作目录
os.listdir(path)     # 列出目录内容
os.mkdir(path)       # 创建目录
os.makedirs(path)    # 递归创建目录
os.remove(file)      # 删除文件
os.rmdir(path)       # 删除空目录
os.path.join()       # 路径拼接
os.path.exists()     # 检查路径是否存在
os.path.isfile()     # 判断是否为文件
os.path.isdir()      # 判断是否为目录
```

#### 💡 实际应用场景
1. **批量文件重命名**：遍历目录，批量修改文件名
2. **目录清理**：删除临时文件或过期文件
3. **文件组织**：按类型或日期自动分类文件

#### 💻 代码示例

**示例1：遍历目录并统计文件类型**
```python
import os
from collections import Counter

def count_file_types(directory):
    """统计目录中各类型文件的数量"""
    extensions = []
    
    # 遍历目录
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        # 只处理文件
        if os.path.isfile(filepath):
            # 获取文件扩展名
            _, ext = os.path.splitext(filename)
            extensions.append(ext if ext else '无扩展名')
    
    # 统计并打印
    counter = Counter(extensions)
    for ext, count in counter.most_common():
        print(f"{ext}: {count}个")

# 使用示例
count_file_types('.')
```

**示例2：创建目录结构**
```python
import os

def create_project_structure(project_name):
    """创建Python项目的标准目录结构"""
    directories = [
        f'{project_name}',
        f'{project_name}/src',
        f'{project_name}/tests',
        f'{project_name}/docs',
        f'{project_name}/data'
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)  # exist_ok避免已存在时报错
            print(f"✓ 创建目录: {directory}")
        except Exception as e:
            print(f"✗ 创建失败: {directory} - {e}")

# 使用示例
create_project_structure('my_project')
```

**示例3：查找特定类型的文件**
```python
import os

def find_files(directory, extension):
    """递归查找指定扩展名的所有文件"""
    found_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                full_path = os.path.join(root, file)
                found_files.append(full_path)
    
    return found_files

# 使用示例：查找所有Python文件
python_files = find_files('.', '.py')
print(f"找到 {len(python_files)} 个Python文件")
for file in python_files[:5]:  # 显示前5个
    print(f"  - {file}")
```

#### ⚠️ 易错点
1. **路径拼接错误**
   - ❌ 错误：`path = dir + '/' + file`（不跨平台）
   - ✅ 正确：`path = os.path.join(dir, file)`

2. **删除非空目录**
   - ❌ 错误：`os.rmdir()`只能删除空目录
   - ✅ 正确：使用`shutil.rmtree()`删除非空目录

3. **相对路径问题**
   - ❌ 错误：假设当前目录始终不变
   - ✅ 正确：使用`os.path.abspath()`获取绝对路径

---

### 2️⃣ sys - 系统相关参数和函数

#### 📝 模块简介
提供与Python解释器交互的功能，包括命令行参数、系统路径、标准输入输出等。

#### 🔑 核心方法
```python
sys.argv             # 命令行参数列表
sys.exit([code])     # 退出程序
sys.path             # 模块搜索路径
sys.version          # Python版本信息
sys.platform         # 操作系统平台
sys.stdin/stdout/stderr  # 标准输入输出
sys.getrecursionlimit()  # 获取递归限制
sys.setrecursionlimit()  # 设置递归限制
```

#### 💡 实际应用场景
1. **命令行工具开发**：解析命令行参数
2. **脚本退出控制**：根据条件优雅退出
3. **动态导入模块**：修改模块搜索路径

#### 💻 代码示例

**示例1：简单的命令行计算器**
```python
import sys

def calculator():
    """简单的命令行计算器"""
    # 检查参数数量
    if len(sys.argv) != 4:
        print("用法: python calculator.py <数字1> <运算符> <数字2>")
        print("示例: python calculator.py 10 + 5")
        sys.exit(1)  # 非0退出码表示错误
    
    try:
        num1 = float(sys.argv[1])
        operator = sys.argv[2]
        num2 = float(sys.argv[3])
        
        # 执行计算
        operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y
        }
        
        if operator not in operations:
            print(f"不支持的运算符: {operator}")
            sys.exit(1)
        
        result = operations[operator](num1, num2)
        print(f"结果: {num1} {operator} {num2} = {result}")
        sys.exit(0)  # 0表示成功
        
    except ValueError:
        print("错误: 请输入有效的数字")
        sys.exit(1)
    except ZeroDivisionError:
        print("错误: 除数不能为0")
        sys.exit(1)

# 使用示例
calculator()
```

**示例2：系统信息查看器**
```python
import sys

def show_system_info():
    """显示Python和系统信息"""
    print("=" * 50)
    print("Python系统信息")
    print("=" * 50)
    print(f"Python版本: {sys.version}")
    print(f"操作系统: {sys.platform}")
    print(f"最大整数: {sys.maxsize}")
    print(f"递归限制: {sys.getrecursionlimit()}")
    print(f"默认编码: {sys.getdefaultencoding()}")
    print(f"\n模块搜索路径前3个:")
    for i, path in enumerate(sys.path[:3], 1):
        print(f"  {i}. {path}")

# 使用示例
show_system_info()
```

#### ⚠️ 易错点
1. **sys.argv索引错误**
   - ❌ 错误：忘记`sys.argv[0]`是脚本名
   - ✅ 正确：参数从`sys.argv[1]`开始

2. **不检查参数数量**
   - ❌ 错误：直接访问可能不存在的参数
   - ✅ 正确：先检查`len(sys.argv)`

3. **修改sys.path的副作用**
   - ⚠️ 注意：修改`sys.path`会影响全局模块导入

---

### 3️⃣ datetime - 日期和时间处理

#### 📝 模块简介
提供日期和时间的处理功能，包括日期创建、格式化、时间运算等。

#### 🔑 核心方法
```python
datetime.datetime.now()           # 当前日期时间
datetime.date.today()             # 当前日期
datetime.datetime.strptime()      # 字符串转日期
datetime.datetime.strftime()      # 日期转字符串
datetime.timedelta()              # 时间间隔
datetime.datetime.timestamp()     # 转时间戳
datetime.datetime.fromtimestamp() # 时间戳转日期
```

#### 💡 实际应用场景
1. **日志时间戳**：记录操作发生的时间
2. **日期计算**：计算截止日期、年龄等
3. **时间格式转换**：解析和格式化日期字符串

#### 💻 代码示例

**示例1：年龄计算器**
```python
from datetime import datetime, date

def calculate_age(birth_date_str):
    """计算年龄（精确到天）"""
    # 解析生日字符串
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
    today = date.today()
    
    # 计算年龄
    age_years = today.year - birth_date.year
    
    # 检查今年生日是否已过
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age_years -= 1
    
    # 计算距离下次生日的天数
    next_birthday = date(today.year, birth_date.month, birth_date.day)
    if next_birthday < today:
        next_birthday = date(today.year + 1, birth_date.month, birth_date.day)
    days_to_birthday = (next_birthday - today).days
    
    print(f"年龄: {age_years}岁")
    print(f"距离下次生日还有: {days_to_birthday}天")

# 使用示例
calculate_age('1990-05-15')
```

**示例2：工作日计算器**
```python
from datetime import datetime, timedelta

def add_business_days(start_date, days):
    """添加指定工作日数（不含周末）"""
    current_date = start_date
    days_added = 0
    
    while days_added < days:
        current_date += timedelta(days=1)
        # 跳过周末（周一=0, 周日=6）
        if current_date.weekday() < 5:  # 0-4是周一到周五
            days_added += 1
    
    return current_date

# 使用示例
start = datetime.now()
deadline = add_business_days(start, 10)
print(f"开始日期: {start.strftime('%Y-%m-%d %A')}")
print(f"10个工作日后: {deadline.strftime('%Y-%m-%d %A')}")
```

**示例3：时间格式转换器**
```python
from datetime import datetime

def format_time_converter(time_str, input_format, output_format):
    """时间格式转换"""
    # 常用格式说明
    formats = {
        'iso': '%Y-%m-%d %H:%M:%S',
        'cn': '%Y年%m月%d日 %H时%M分%S秒',
        'us': '%m/%d/%Y %I:%M:%S %p',
        'simple': '%Y-%m-%d'
    }
    
    # 获取格式
    in_fmt = formats.get(input_format, input_format)
    out_fmt = formats.get(output_format, output_format)
    
    try:
        # 解析并转换
        dt = datetime.strptime(time_str, in_fmt)
        return dt.strftime(out_fmt)
    except ValueError as e:
        return f"格式错误: {e}"

# 使用示例
print(format_time_converter('2025-12-30 14:30:00', 'iso', 'cn'))
# 输出: 2025年12月30日 14时30分00秒

print(format_time_converter('2025-12-30', 'simple', 'us'))
# 输出: 12/30/2025 12:00:00 AM
```

#### ⚠️ 易错点
1. **时区问题**
   - ❌ 错误：忽略时区，使用naive datetime
   - ✅ 正确：使用`pytz`库处理时区或使用`timezone`

2. **格式化字符串错误**
   - ❌ 错误：`%d/%m/%Y`和`%m/%d/%Y`混淆
   - ✅ 正确：仔细核对格式说明符

3. **时间运算类型不匹配**
   - ❌ 错误：`datetime.date` + 整数
   - ✅ 正确：使用`timedelta`对象

---

### 4️⃣ json - JSON数据处理

#### 📝 模块简介
用于JSON数据的编码和解码，实现Python对象与JSON字符串之间的转换。

#### 🔑 核心方法
```python
json.dumps()      # Python对象转JSON字符串
json.loads()      # JSON字符串转Python对象
json.dump()       # Python对象写入JSON文件
json.load()       # 从JSON文件读取
# 常用参数: indent, ensure_ascii, sort_keys
```

#### 💡 实际应用场景
1. **配置文件管理**：读写JSON格式的配置
2. **API数据交换**：处理RESTful API的JSON响应
3. **数据持久化**：保存和加载简单的数据结构

#### 💻 代码示例

**示例1：配置文件管理器**
```python
import json
import os

class ConfigManager:
    """JSON配置文件管理器"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load()
    
    def load(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save(self):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    def get(self, key, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置项"""
        self.config[key] = value
        self.save()
    
    def display(self):
        """显示所有配置"""
        print(json.dumps(self.config, indent=2, ensure_ascii=False))

# 使用示例
config = ConfigManager()
config.set('username', '张三')
config.set('settings', {'theme': 'dark', 'language': 'zh-CN'})
config.display()
```

**示例2：数据格式美化器**
```python
import json

def beautify_json(json_string):
    """美化JSON字符串"""
    try:
        # 解析JSON
        data = json.loads(json_string)
        
        # 美化输出
        beautiful = json.dumps(
            data, 
            indent=4,           # 缩进4个空格
            ensure_ascii=False, # 允许中文
            sort_keys=True      # 按键排序
        )
        
        return beautiful
    except json.JSONDecodeError as e:
        return f"JSON解析错误: {e}"

# 使用示例
ugly_json = '{"name":"李四","age":25,"city":"北京","hobbies":["读书","旅游"]}'
print(beautify_json(ugly_json))
```

**示例3：JSON数据验证器**
```python
import json

def validate_and_parse(json_str, required_keys):
    """验证JSON数据是否包含必需字段"""
    try:
        data = json.loads(json_str)
        
        # 检查必需字段
        missing_keys = [key for key in required_keys if key not in data]
        
        if missing_keys:
            return {
                'valid': False,
                'error': f"缺少必需字段: {', '.join(missing_keys)}",
                'data': None
            }
        
        return {
            'valid': True,
            'error': None,
            'data': data
        }
    
    except json.JSONDecodeError as e:
        return {
            'valid': False,
            'error': f"JSON格式错误: {e}",
            'data': None
        }

# 使用示例
user_json = '{"username": "admin", "email": "admin@example.com"}'
result = validate_and_parse(user_json, ['username', 'email', 'password'])

if result['valid']:
    print("验证通过:", result['data'])
else:
    print("验证失败:", result['error'])
```

#### ⚠️ 易错点
1. **中文显示问题**
   - ❌ 错误：中文显示为`\uxxxx`
   - ✅ 正确：使用`ensure_ascii=False`

2. **文件编码问题**
   - ❌ 错误：不指定编码导致乱码
   - ✅ 正确：使用`encoding='utf-8'`

3. **类型不可序列化**
   - ❌ 错误：尝试序列化datetime、set等
   - ✅ 正确：自定义`default`函数处理特殊类型

---

### 5️⃣ random - 随机数生成

#### 📝 模块简介
生成伪随机数，提供随机选择、打乱序列等功能，适用于模拟、游戏、测试等场景。

#### 🔑 核心方法
```python
random.random()           # 返回[0.0, 1.0)的随机浮点数
random.randint(a, b)      # 返回[a, b]的随机整数
random.choice(seq)        # 从序列中随机选择一个元素
random.choices(seq, k=n)  # 可重复地随机选择n个
random.sample(seq, k)     # 不重复地随机选择k个
random.shuffle(seq)       # 打乱序列（原地修改）
random.uniform(a, b)      # 返回[a, b]的随机浮点数
random.seed(n)            # 设置随机种子
```

#### 💡 实际应用场景
1. **抽奖系统**：随机选择获奖者
2. **密码生成**：生成随机密码
3. **测试数据生成**：创建随机测试用例

#### 💻 代码示例

**示例1：密码生成器**
```python
import random
import string

def generate_password(length=12, use_symbols=True):
    """生成随机密码"""
    # 定义字符集
    lowercase = string.ascii_lowercase      # a-z
    uppercase = string.ascii_uppercase      # A-Z
    digits = string.digits                  # 0-9
    symbols = string.punctuation            # 特殊符号
    
    # 确保密码包含各类字符
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits)
    ]
    
    if use_symbols:
        password.append(random.choice(symbols))
    
    # 填充剩余长度
    all_chars = lowercase + uppercase + digits
    if use_symbols:
        all_chars += symbols
    
    password += random.choices(all_chars, k=length - len(password))
    
    # 打乱顺序
    random.shuffle(password)
    
    return ''.join(password)

# 使用示例
for i in range(3):
    print(f"密码{i+1}: {generate_password(16)}")
```

**示例2：随机抽奖系统**
```python
import random

def lottery_draw(participants, num_winners=3):
    """抽奖系统"""
    if num_winners > len(participants):
        return "错误: 获奖人数超过参与者数量"
    
    # 随机抽取获奖者（不重复）
    winners = random.sample(participants, num_winners)
    
    print("🎉 抽奖结果公布 🎉")
    print("=" * 40)
    
    prizes = ["一等奖", "二等奖", "三等奖", "四等奖", "五等奖"]
    
    for i, winner in enumerate(winners):
        prize = prizes[i] if i < len(prizes) else f"第{i+1}名"
        print(f"{prize}: {winner}")
    
    return winners

# 使用示例
participants = [f"用户{i}" for i in range(1, 101)]
lottery_draw(participants, 5)
```

**示例3：随机测试数据生成器**
```python
import random
from datetime import datetime, timedelta

def generate_test_users(count=10):
    """生成随机测试用户数据"""
    first_names = ['张', '李', '王', '刘', '陈', '杨', '赵', '黄', '周', '吴']
    second_names = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军']
    
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '西安', '武汉']
    
    users = []
    
    for i in range(count):
        # 生成随机年龄（18-60岁）
        age = random.randint(18, 60)
        
        # 生成随机注册日期（最近一年内）
        days_ago = random.randint(0, 365)
        register_date = datetime.now() - timedelta(days=days_ago)
        
        user = {
            'id': i + 1,
            'name': random.choice(first_names) + random.choice(second_names),
            'age': age,
            'city': random.choice(cities),
            'balance': round(random.uniform(0, 10000), 2),
            'register_date': register_date.strftime('%Y-%m-%d'),
            'is_vip': random.choice([True, False])
        }
        
        users.append(user)
    
    return users

# 使用示例
test_users = generate_test_users(5)
for user in test_users:
    print(user)
```

#### ⚠️ 易错点
1. **随机种子的误用**
   - ⚠️ 注意：设置相同种子会产生相同序列
   - 💡 提示：测试时用固定种子，生产环境不设置

2. **sample vs choices混淆**
   - `sample()`：不重复抽样
   - `choices()`：可重复抽样

3. **安全性问题**
   - ❌ 错误：使用`random`生成安全令牌
   - ✅ 正确：使用`secrets`模块生成密码学安全的随机数

---

### 6️⃣ math - 数学函数

#### 📝 模块简介
提供标准数学函数，包括三角函数、对数、幂运算、常数等。

#### 🔑 核心方法
```python
math.ceil(x)      # 向上取整
math.floor(x)     # 向下取整
math.sqrt(x)      # 平方根
math.pow(x, y)    # x的y次方
math.factorial(n) # 阶乘
math.gcd(a, b)    # 最大公约数
math.sin/cos/tan  # 三角函数
math.log(x)       # 自然对数
math.pi           # 圆周率
math.e            # 自然常数
```

#### 💡 实际应用场景
1. **数值计算**：科学计算、工程计算
2. **几何运算**：距离计算、角度转换
3. **统计分析**：数据处理中的数学运算

#### 💻 代码示例

**示例1：几何计算器**
```python
import math

class GeometryCalculator:
    """几何图形计算器"""
    
    @staticmethod
    def circle_area(radius):
        """计算圆的面积"""
        return math.pi * radius ** 2
    
    @staticmethod
    def circle_circumference(radius):
        """计算圆的周长"""
        return 2 * math.pi * radius
    
    @staticmethod
    def distance_2d(x1, y1, x2, y2):
        """计算两点间距离"""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    @staticmethod
    def triangle_area(a, b, c):
        """用海伦公式计算三角形面积"""
        # 半周长
        s = (a + b + c) / 2
        # 海伦公式
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        return area

# 使用示例
calc = GeometryCalculator()
print(f"半径为5的圆面积: {calc.circle_area(5):.2f}")
print(f"点(0,0)到(3,4)的距离: {calc.distance_2d(0, 0, 3, 4):.2f}")
print(f"边长为3,4,5的三角形面积: {calc.triangle_area(3, 4, 5):.2f}")
```

**示例2：贷款计算器**
```python
import math

def calculate_loan_payment(principal, annual_rate, years):
    """计算等额本息还款"""
    # 月利率
    monthly_rate = annual_rate / 12 / 100
    # 还款月数
    months = years * 12
    
    if monthly_rate == 0:
        # 无息贷款
        monthly_payment = principal / months
    else:
        # 等额本息公式
        monthly_payment = (principal * monthly_rate * 
                          math.pow(1 + monthly_rate, months)) / \
                         (math.pow(1 + monthly_rate, months) - 1)
    
    # 总还款额
    total_payment = monthly_payment * months
    # 总利息
    total_interest = total_payment - principal
    
    print(f"贷款本金: ¥{principal:,.2f}")
    print(f"年利率: {annual_rate}%")
    print(f"贷款年限: {years}年")
    print(f"每月还款: ¥{monthly_payment:,.2f}")
    print(f"总还款额: ¥{total_payment:,.2f}")
    print(f"总利息: ¥{total_interest:,.2f}")

# 使用示例：贷款100万，年利率4.5%，30年
calculate_loan_payment(1000000, 4.5, 30)
```

#### ⚠️ 易错点
1. **角度与弧度混淆**
   - ❌ 错误：`math.sin(90)`期望得到1
   - ✅ 正确：使用`math.radians()`转换或`math.sin(math.pi/2)`

2. **整数除法与浮点除法**
   - 💡 提示：Python3中`/`总是返回浮点数

3. **精度问题**
   - ⚠️ 注意：浮点运算存在精度误差
   - 💡 建议：使用`decimal`模块进行精确计算

---

### 7️⃣ re - 正则表达式

#### 📝 模块简介
提供正则表达式匹配操作，用于文本模式匹配、搜索、替换等高级字符串处理。

#### 🔑 核心方法
```python
re.match()      # 从字符串开头匹配
re.search()     # 搜索整个字符串
re.findall()    # 查找所有匹配
re.finditer()   # 返回迭代器
re.sub()        # 替换匹配的子串
re.split()      # 按模式分割字符串
re.compile()    # 编译正则表达式
```

#### 💡 实际应用场景
1. **数据验证**：验证邮箱、电话、身份证等格式
2. **文本提取**：从文本中提取特定信息
3. **数据清洗**：清理和规范化文本数据

#### 💻 代码示例

**示例1：常用格式验证器**
```python
import re

class Validator:
    """常用格式验证器"""
    
    @staticmethod
    def is_valid_email(email):
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_phone(phone):
        """验证中国手机号"""
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def is_valid_id_card(id_card):
        """验证18位身份证号"""
        pattern = r'^\d{17}[\dXx]$'
        return bool(re.match(pattern, id_card))
    
    @staticmethod
    def is_strong_password(password):
        """验证强密码（至少8位，包含大小写字母和数字）"""
        if len(password) < 8:
            return False
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        return has_upper and has_lower and has_digit

# 使用示例
validator = Validator()
print(validator.is_valid_email("user@example.com"))      # True
print(validator.is_valid_phone("13812345678"))           # True
print(validator.is_strong_password("Abc123456"))         # True
```

**示例2：文本信息提取器**
```python
import re

def extract_info(text):
    """从文本中提取各类信息"""
    info = {}
    
    # 提取邮箱
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    info['emails'] = emails
    
    # 提取手机号
    phones = re.findall(r'1[3-9]\d{9}', text)
    info['phones'] = phones
    
    # 提取URL
    urls = re.findall(r'https?://[^\s]+', text)
    info['urls'] = urls
    
    # 提取金额（支持¥123.45或123.45元格式）
    amounts = re.findall(r'¥?\d+\.?\d*元?', text)
    info['amounts'] = amounts
    
    # 提取日期（YYYY-MM-DD格式）
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
    info['dates'] = dates
    
    return info

# 使用示例
text = """
联系方式：
邮箱：admin@example.com, support@test.com
电话：13812345678
网站：https://www.example.com
订单金额：¥1299.99
发货日期：2025-12-30
"""

result = extract_info(text)
for key, value in result.items():
    print(f"{key}: {value}")
```

**示例3：文本清洗和替换**
```python
import re

def clean_text(text):
    """清洗文本数据"""
    # 移除多余空白字符
    text = re.sub(r'\s+', ' ', text)
    
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 移除特殊字符（保留中英文、数字、基本标点）
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s,.!?，。！？]', '', text)
    
    # 统一标点符号（中文标点转英文）
    replacements = {
        '，': ',',
        '。': '.',
        '！': '!',
        '？': '?',
        '：': ':',
        '；': ';'
    }
    for cn, en in replacements.items():
        text = text.replace(cn, en)
    
    return text.strip()

def mask_sensitive_info(text):
    """脱敏处理"""
    # 手机号脱敏（保留前3位和后4位）
    text = re.sub(r'(1[3-9]\d)\d{4}(\d{4})', r'\1****\2', text)
    
    # 身份证脱敏（保留前6位和后4位）
    text = re.sub(r'(\d{6})\d{8}(\d{4})', r'\1********\2', text)
    
    # 邮箱脱敏
    text = re.sub(r'([a-zA-Z0-9._%+-]{1,3})[a-zA-Z0-9._%+-]*@', r'\1***@', text)
    
    return text

# 使用示例
dirty_text = "<p>这是一段   包含多余空格的  文本！！！</p>"
print("清洗后:", clean_text(dirty_text))

sensitive = "手机号：13812345678，邮箱：admin@example.com"
print("脱敏后:", mask_sensitive_info(sensitive))
```

#### ⚠️ 易错点
1. **贪婪匹配vs非贪婪匹配**
   - 贪婪：`.*`匹配尽可能多的字符
   - 非贪婪：`.*?`匹配尽可能少的字符

2. **特殊字符未转义**
   - ❌ 错误：`re.search('.', text)`匹配任意字符
   - ✅ 正确：`re.search(r'\.', text)`匹配句点

3. **忘记使用原始字符串**
   - ❌ 错误：`'\d+'`需要写成`'\\d+'`
   - ✅ 正确：使用`r'\d+'`

---

### 8️⃣ collections - 高级数据结构

#### 📝 模块简介
提供专门的容器数据类型，是对内置容器（list、dict、set、tuple）的补充和增强。

#### 🔑 核心类型
```python
Counter          # 计数器
defaultdict      # 带默认值的字典
OrderedDict      # 有序字典
deque            # 双端队列
namedtuple       # 命名元组
ChainMap         # 链式字典
```

#### 💡 实际应用场景
1. **数据统计**：使用Counter统计频率
2. **缓存实现**：使用deque实现LRU缓存
3. **配置管理**：使用ChainMap管理多层配置

#### 💻 代码示例

**示例1：文本分析器（Counter）**
```python
from collections import Counter
import re

def analyze_text(text):
    """分析文本的词频、字符频率等"""
    # 提取单词（只保留字母）
    words = re.findall(r'[a-zA-Z]+', text.lower())
    
    # 统计词频
    word_counter = Counter(words)
    
    # 统计字符频率
    char_counter = Counter(text.lower())
    
    print("=" * 50)
    print("文本分析结果")
    print("=" * 50)
    print(f"总字符数: {len(text)}")
    print(f"总单词数: {len(words)}")
    print(f"不重复单词数: {len(word_counter)}")
    
    print("\n最常见的5个单词:")
    for word, count in word_counter.most_common(5):
        print(f"  {word}: {count}次")
    
    print("\n最常见的5个字母:")
    letter_counter = Counter({k: v for k, v in char_counter.items() 
                             if k.isalpha()})
    for letter, count in letter_counter.most_common(5):
        print(f"  {letter}: {count}次")

# 使用示例
text = """
Python is a high-level programming language. 
Python is easy to learn and powerful.
"""
analyze_text(text)
```

**示例2：分组统计（defaultdict）**
```python
from collections import defaultdict

def group_students_by_score(students):
    """按分数段分组学生"""
    # 使用defaultdict，默认值为列表
    groups = defaultdict(list)
    
    for student in students:
        name, score = student
        
        # 确定分数段
        if score >= 90:
            grade = 'A (优秀)'
        elif score >= 80:
            grade = 'B (良好)'
        elif score >= 70:
            grade = 'C (中等)'
        elif score >= 60:
            grade = 'D (及格)'
        else:
            grade = 'F (不及格)'
        
        groups[grade].append((name, score))
    
    # 打印分组结果
    print("学生成绩分组:")
    print("=" * 50)
    for grade, students in sorted(groups.items()):
        print(f"\n{grade}: {len(students)}人")
        for name, score in students:
            print(f"  - {name}: {score}分")

# 使用示例
students = [
    ('张三', 95), ('李四', 87), ('王五', 76),
    ('赵六', 92), ('孙七', 65), ('周八', 58),
    ('吴九', 88), ('郑十', 72)
]
group_students_by_score(students)
```

**示例3：滑动窗口（deque）**
```python
from collections import deque

class SlidingWindow:
    """滑动窗口统计"""
    
    def __init__(self, size):
        self.size = size
        self.window = deque(maxlen=size)  # 自动维护大小
    
    def add(self, value):
        """添加新值"""
        self.window.append(value)
    
    def average(self):
        """计算窗口内平均值"""
        if not self.window:
            return 0
        return sum(self.window) / len(self.window)
    
    def maximum(self):
        """获取窗口内最大值"""
        return max(self.window) if self.window else None
    
    def minimum(self):
        """获取窗口内最小值"""
        return min(self.window) if self.window else None

# 使用示例：股票价格移动平均
print("5日移动平均线:")
prices = [100, 102, 98, 105, 103, 107, 110, 108, 112, 115]
window = SlidingWindow(5)

for i, price in enumerate(prices, 1):
    window.add(price)
    if i >= 5:  # 至少5个数据点才开始计算
        print(f"第{i}天: 价格={price}, "
              f"5日均价={window.average():.2f}")
```

**示例4：命名元组（namedtuple）**
```python
from collections import namedtuple

# 定义学生记录
Student = namedtuple('Student', ['name', 'age', 'grade', 'score'])

def create_student_report(students):
    """生成学生报告"""
    print("学生成绩单")
    print("=" * 60)
    print(f"{'姓名':<10} {'年龄':<8} {'年级':<8} {'分数':<8}")
    print("-" * 60)
    
    total_score = 0
    for student in students:
        print(f"{student.name:<10} {student.age:<8} "
              f"{student.grade:<8} {student.score:<8}")
        total_score += student.score
    
    print("-" * 60)
    print(f"平均分: {total_score / len(students):.2f}")

# 使用示例
students = [
    Student('张三', 18, '高三', 92),
    Student('李四', 17, '高二', 88),
    Student('王五', 18, '高三', 95),
    Student('赵六', 17, '高二', 85)
]

create_student_report(students)

# namedtuple的优势：可读性强
student = students[0]
print(f"\n{student.name}的成绩是{student.score}分")  # 比student[3]更清晰
```

#### ⚠️ 易错点
1. **defaultdict的默认工厂函数**
   - ❌ 错误：`defaultdict([])`
   - ✅ 正确：`defaultdict(list)`

2. **deque的maxlen参数**
   - 💡 提示：设置maxlen后，添加新元素会自动删除旧元素

3. **namedtuple的不可变性**
   - ⚠️ 注意：namedtuple是不可变的，不能修改字段值
   - 💡 替代：使用`_replace()`方法创建新实例

---

### 9️⃣ pathlib - 面向对象的路径操作

#### 📝 模块简介
提供面向对象的文件系统路径操作，比传统的`os.path`更直观、更易用。

#### 🔑 核心类和方法
```python
Path()              # 创建路径对象
Path.cwd()          # 当前工作目录
Path.home()         # 用户主目录
path.exists()       # 路径是否存在
path.is_file()      # 是否为文件
path.is_dir()       # 是否为目录
path.glob()         # 模式匹配
path.mkdir()        # 创建目录
path.read_text()    # 读取文本文件
path.write_text()   # 写入文本文件
path / 'subdir'     # 路径拼接（使用/运算符）
```

#### 💡 实际应用场景
1. **项目文件管理**：组织项目目录结构
2. **文件搜索**：使用glob模式查找文件
3. **跨平台路径**：自动处理不同操作系统的路径差异

#### 💻 代码示例

**示例1：项目文件管理器**
```python
from pathlib import Path

class ProjectManager:
    """项目文件管理器"""
    
    def __init__(self, project_name):
        self.root = Path.cwd() / project_name
    
    def create_structure(self):
        """创建标准项目结构"""
        directories = [
            self.root / 'src',
            self.root / 'tests',
            self.root / 'docs',
            self.root / 'data' / 'raw',
            self.root / 'data' / 'processed',
            self.root / 'output'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✓ 创建: {directory}")
        
        # 创建初始文件
        (self.root / 'README.md').write_text('# ' + self.root.name)
        (self.root / 'src' / '__init__.py').touch()
        (self.root / 'tests' / '__init__.py').touch()
        
        print("\n✓ 项目结构创建完成!")
    
    def list_files(self, pattern='**/*'):
        """列出所有文件"""
        files = list(self.root.glob(pattern))
        print(f"\n找到 {len(files)} 个文件:")
        for file in sorted(files):
            if file.is_file():
                size = file.stat().st_size
                print(f"  {file.relative_to(self.root)} ({size} bytes)")
    
    def get_summary(self):
        """获取项目摘要"""
        if not self.root.exists():
            return "项目不存在"
        
        py_files = list(self.root.glob('**/*.py'))
        md_files = list(self.root.glob('**/*.md'))
        
        total_lines = 0
        for py_file in py_files:
            total_lines += len(py_file.read_text().splitlines())
        
        print(f"\n项目摘要: {self.root.name}")
        print("=" * 50)
        print(f"Python文件: {len(py_files)}个")
        print(f"Markdown文件: {len(md_files)}个")
        print(f"总代码行数: {total_lines}行")

# 使用示例
pm = ProjectManager('my_awesome_project')
pm.create_structure()
pm.list_files()
pm.get_summary()
```

**示例2：智能文件查找器**
```python
from pathlib import Path
from datetime import datetime, timedelta

def find_recent_files(directory, days=7, extensions=None):
    """查找最近修改的文件"""
    path = Path(directory)
    cutoff_time = datetime.now().timestamp() - (days * 86400)
    
    recent_files = []
    
    for file in path.rglob('*'):
        if file.is_file():
            # 检查扩展名
            if extensions and file.suffix not in extensions:
                continue
            
            # 检查修改时间
            mtime = file.stat().st_mtime
            if mtime > cutoff_time:
                modified = datetime.fromtimestamp(mtime)
                recent_files.append((file, modified))
    
    # 按时间排序
    recent_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"最近{days}天修改的文件:")
    print("=" * 70)
    for file, modified in recent_files[:10]:  # 只显示前10个
        rel_path = file.relative_to(path) if file.is_relative_to(path) else file
        print(f"{modified.strftime('%Y-%m-%d %H:%M')} - {rel_path}")

# 使用示例
find_recent_files('.', days=7, extensions=['.py', '.md'])
```

**示例3：配置文件处理器**
```python
from pathlib import Path
import json

class ConfigHandler:
    """配置文件处理器"""
    
    def __init__(self, config_dir='config'):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
    
    def save_config(self, name, data):
        """保存配置"""
        config_file = self.config_dir / f"{name}.json"
        config_file.write_text(
            json.dumps(data, indent=4, ensure_ascii=False),
            encoding='utf-8'
        )
        print(f"✓ 配置已保存: {config_file}")
    
    def load_config(self, name):
        """加载配置"""
        config_file = self.config_dir / f"{name}.json"
        
        if not config_file.exists():
            print(f"✗ 配置不存在: {config_file}")
            return None
        
        data = json.loads(config_file.read_text(encoding='utf-8'))
        print(f"✓ 配置已加载: {config_file}")
        return data
    
    def list_configs(self):
        """列出所有配置"""
        configs = list(self.config_dir.glob('*.json'))
        print(f"\n可用配置 ({len(configs)}个):")
        for config in sorted(configs):
            size = config.stat().st_size
            print(f"  - {config.stem} ({size} bytes)")
        return [c.stem for c in configs]

# 使用示例
handler = ConfigHandler()
handler.save_config('database', {
    'host': 'localhost',
    'port': 3306,
    'database': 'mydb'
})
handler.save_config('app', {
    'debug': True,
    'language': 'zh-CN'
})
handler.list_configs()
data = handler.load_config('database')
print(f"\n数据库配置: {data}")
```

#### ⚠️ 易错点
1. **路径拼接**
   - ❌ 错误：`path + '/file.txt'`
   - ✅ 正确：`path / 'file.txt'`

2. **存在性检查**
   - 💡 建议：在操作前先用`exists()`检查

3. **相对路径vs绝对路径**
   - 使用`resolve()`获取绝对路径
   - 使用`relative_to()`获取相对路径

---

### 🔟 logging - 日志记录

#### 📝 模块简介
提供灵活的日志记录系统，支持多级别日志、多输出目标、自定义格式等，是专业应用必备工具。

#### 🔑 核心概念
```python
# 日志级别（从低到高）
DEBUG     # 详细信息，调试用
INFO      # 一般信息
WARNING   # 警告信息
ERROR     # 错误信息
CRITICAL  # 严重错误

# 核心组件
Logger    # 日志记录器
Handler   # 处理器（输出目标）
Formatter # 格式化器
Filter    # 过滤器
```

#### 💡 实际应用场景
1. **应用调试**：记录程序运行状态
2. **错误追踪**：记录异常和错误信息
3. **审计日志**：记录用户操作历史

#### 💻 代码示例

**示例1：基础日志配置**
```python
import logging
from datetime import datetime

def setup_logger(name='app', log_file=None, level=logging.INFO):
    """配置日志记录器"""
    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 定义格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（如果指定）
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# 使用示例
logger = setup_logger('MyApp', 'app.log')

logger.debug('这是调试信息')
logger.info('程序启动成功')
logger.warning('这是一个警告')
logger.error('发生了一个错误')
logger.critical('严重错误！')
```

**示例2：高级日志系统**
```python
import logging
import logging.handlers
from pathlib import Path

class AppLogger:
    """应用日志系统"""
    
    def __init__(self, name, log_dir='logs'):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """配置多级日志"""
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        
        # 详细格式
        detailed_formatter = logging.Formatter(
            '[%(asctime)s] %(name)s - %(levelname)s - '
            '%(filename)s:%(lineno)d - %(message)s'
        )
        
        # 简单格式
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # 1. 控制台处理器（INFO及以上）
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        
        # 2. 常规日志文件（DEBUG及以上）
        debug_file = self.log_dir / f'{self.name}_debug.log'
        debug_handler = logging.handlers.RotatingFileHandler(
            debug_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(detailed_formatter)
        
        # 3. 错误日志文件（ERROR及以上）
        error_file = self.log_dir / f'{self.name}_error.log'
        error_handler = logging.handlers.RotatingFileHandler(
            error_file,
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        
        # 添加所有处理器
        logger.addHandler(console_handler)
        logger.addHandler(debug_handler)
        logger.addHandler(error_handler)
        
        return logger
    
    def log_function_call(self, func):
        """装饰器：记录函数调用"""
        def wrapper(*args, **kwargs):
            self.logger.debug(f'调用函数: {func.__name__}')
            try:
                result = func(*args, **kwargs)
                self.logger.debug(f'函数 {func.__name__} 执行成功')
                return result
            except Exception as e:
                self.logger.error(f'函数 {func.__name__} 执行失败: {e}')
                raise
        return wrapper

# 使用示例
app_logger = AppLogger('MyApplication')
logger = app_logger.logger

# 记录各级别日志
logger.debug('调试信息：变量x的值为10')
logger.info('用户登录成功：admin')
logger.warning('内存使用率超过80%')
logger.error('数据库连接失败')
logger.critical('系统崩溃！')

# 使用装饰器
@app_logger.log_function_call
def divide(a, b):
    return a / b

try:
    divide(10, 0)
except ZeroDivisionError:
    logger.error('除零错误', exc_info=True)  # exc_info=True记录异常堆栈
```

#### ⚠️ 易错点
1. **重复添加处理器**
   - ⚠️ 问题：多次调用会添加多个处理器，导致重复日志
   - ✅ 解决：检查`logger.handlers`或使用单例模式

2. **日志级别设置**
   - 💡 提示：Logger和Handler都有级别，两者都要满足才会输出

3. **文件编码**
   - ❌ 错误：不指定encoding导致中文乱码
   - ✅ 正确：`encoding='utf-8'`

---

## 实践项目推荐

### 🎯 初级项目（第1-4周后）

#### 1. 文件整理工具
**涉及模块**: `os`, `pathlib`, `shutil`, `datetime`

**功能需求**:
- 扫描指定目录
- 按文件类型分类（图片、文档、视频等）
- 按日期归档
- 删除重复文件

**学习重点**:
- 文件系统遍历
- 路径操作
- 文件操作

---

#### 2. 简单日记本
**涉及模块**: `datetime`, `json`, `pathlib`

**功能需求**:
- 记录每日日记
- JSON格式存储
- 按日期查询
- 统计写作天数

**学习重点**:
- 数据序列化
- 文件读写
- 日期处理

---

### 🎯 中级项目（第5-8周后）

#### 3. 日志分析工具
**涉及模块**: `re`, `collections`, `datetime`, `csv`

**功能需求**:
- 解析服务器日志
- 提取IP、时间、请求等信息
- 统计访问频率
- 生成分析报告

**学习重点**:
- 正则表达式
- 数据统计
- CSV导出

---

#### 4. 数据清洗脚本
**涉及模块**: `pandas`, `re`, `json`, `pathlib`

**功能需求**:
- 读取CSV/Excel文件
- 清洗脏数据
- 格式标准化
- 导出处理结果

**学习重点**:
- 数据处理
- 正则匹配
- 文件操作

---

### 🎯 高级项目（第9-12周后）

#### 5. 多线程文件下载器
**涉及模块**: `threading`, `urllib`, `logging`, `argparse`

**功能需求**:
- 命令行参数解析
- 多线程并发下载
- 进度显示
- 错误日志记录

**学习重点**:
- 多线程编程
- 日志系统
- CLI开发

---

#### 6. 自动化备份系统
**涉及模块**: `pathlib`, `shutil`, `schedule`, `logging`, `configparser`

**功能需求**:
- 定时备份文件
- 压缩备份文件
- 保留最近N个备份
- 邮件通知（可选）

**学习重点**:
- 任务调度
- 配置管理
- 错误处理

---

## 学习资源建议

### 📖 官方文档
1. **Python官方文档** (https://docs.python.org/zh-cn/3/)
   - 最权威的学习资源
   - 中文版质量高
   - 建议先看Tutorial，再查Reference

2. **模块文档查阅技巧**:
   - 使用目录快速定位
   - 关注"See also"部分
   - 查看示例代码

### 💻 学习方法

#### 1. 主动学习法
```
理论学习 → 编写示例 → 解决问题 → 总结反思
```

#### 2. 每周学习计划
- **周一至周五**: 每天1-2小时学习新模块
- **周六**: 2-3小时综合练习
- **周日**: 1-2小时复习和整理笔记

#### 3. 学习检查清单
每学完一个模块，确保能回答：
- [ ] 这个模块解决什么问题？
- [ ] 最常用的5个功能是什么？
- [ ] 有哪些注意事项和陷阱？
- [ ] 能用它完成一个小项目吗？

### 🎯 练习资源

#### 1. 在线平台
- **LeetCode**: 算法练习
- **HackerRank**: Python专项练习
- **实验楼**: 实战项目教程

#### 2. 实战练习建议
- **简单练习**: 每个模块5-10个小练习
- **综合项目**: 每个阶段1个中型项目
- **代码审查**: 定期回顾自己的代码

### 📚 推荐书籍
1. **《Python标准库》by Doug Hellmann**
   - 深入讲解标准库
   - 实用示例丰富

2. **《Python Cookbook》**
   - 解决实际问题的配方
   - 涵盖最佳实践

---

## 常见问题解答

### ❓ Q1: 标准库这么多，需要全部学会吗？

**A**: 不需要！建议采用"**二八原则**"：
- **核心20%**: 深入掌握（os, sys, datetime, json, re, collections, logging等）
- **其他80%**: 知道存在，需要时查文档

**学习策略**:
1. 先学最常用的10-15个模块
2. 其他模块"知道有这个东西"即可
3. 遇到具体需求时再深入学习

---

### ❓ Q2: 看文档看不懂，记不住怎么办？

**A**: 这是正常现象！解决方法：

**记忆技巧**:
- ✅ **不要背**：理解原理，记住大概功能
- ✅ **多动手**：写10遍胜过看100遍
- ✅ **做笔记**：记录常用代码片段
- ✅ **建立索引**：知道"在哪里找"比"记住所有"更重要

**实践方法**:
```python
# 建立自己的代码片段库
# snippets.py

# 文件操作
def list_files(directory):
    """列出目录下所有文件"""
    import os
    return [f for f in os.listdir(directory) if os.path.isfile(f)]

# 日期格式化
def format_date(date_obj):
    """格式化日期"""
    return date_obj.strftime('%Y-%m-%d')
```

---

### ❓ Q3: 何时用os，何时用pathlib？

**A**: **推荐优先使用pathlib**，它更现代、更易用。

| 场景 | 推荐 | 原因 |
|------|------|------|
| 路径拼接 | pathlib | 使用`/`运算符更直观 |
| 文件读写 | pathlib | `read_text()`/`write_text()`更简洁 |
| 复杂文件操作 | os | 某些功能pathlib不支持 |
| 旧项目维护 | os | 保持代码风格一致 |

**对比示例**:
```python
# os方式
import os
path = os.path.join('data', 'file.txt')
if os.path.exists(path):
    with open(path, 'r') as f:
        content = f.read()

# pathlib方式（更简洁）
from pathlib import Path
path = Path('data') / 'file.txt'
if path.exists():
    content = path.read_text()
```

---

### ❓ Q4: datetime的时区问题太复杂，如何处理？

**A**: 时区确实复杂，建议采用以下策略：

**简单场景**（不跨时区）:
```python
from datetime import datetime

# 直接使用naive datetime（无时区信息）
now = datetime.now()
```

**复杂场景**（需要时区）:
```python
from datetime import datetime, timezone
import zoneinfo  # Python 3.9+

# 使用timezone-aware datetime
now = datetime.now(timezone.utc)  # UTC时间

# 转换到其他时区
beijing_tz = zoneinfo.ZoneInfo('Asia/Shanghai')
beijing_time = now.astimezone(beijing_tz)
```

**最佳实践**:
- 服务器统一使用UTC时间
- 显示给用户时转换为本地时区
- 数据库存储使用UTC时间戳

---

### ❓ Q5: 正则表达式太难，有没有简单方法？

**A**: 正则确实有学习曲线，但掌握基础就能解决80%的问题。

**学习路径**:
1. **第1周**: 只学基础语法
   - `.` - 任意字符
   - `\d` - 数字
   - `\w` - 字母数字
   - `*` `+` `?` - 重复
   - `[]` - 字符集
   - `()` - 分组

2. **第2周**: 常用模式
   - 邮箱、手机号、URL等

3. **第3周**: 进阶技巧
   - 非贪婪匹配
   - 前后断言

**实用技巧**:
```python
import re

# 建立常用正则库
PATTERNS = {
    'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    'phone': r'1[3-9]\d{9}',
    'url': r'https?://[^\s]+',
    'ip': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
}

def extract_info(text, info_type):
    """使用预定义模式提取信息"""
    pattern = PATTERNS.get(info_type)
    if pattern:
        return re.findall(pattern, text)
    return []
```

**调试工具**:
- 使用 https://regex101.com/ 在线测试
- 使用 https://regexr.com/ 可视化理解

---

## 学习进度追踪表

### 📊 12周学习检查表

#### 初级阶段（第1-4周）
- [ ] Week 1: os, sys
- [ ] Week 2: datetime, json
- [ ] Week 3: random, math
- [ ] Week 4: 初级项目实战

#### 中级阶段（第5-8周）
- [ ] Week 5: re
- [ ] Week 6: collections
- [ ] Week 7: pathlib, csv, pickle
- [ ] Week 8: 中级项目实战

#### 高级阶段（第9-12周）
- [ ] Week 9: logging
- [ ] Week 10: functools, itertools
- [ ] Week 11: threading, argparse
- [ ] Week 12: 综合项目实战

---

## 最后的建议

### 🎓 学习心态
1. **不要贪多**: 每次只专注1-2个模块
2. **多写代码**: 实践是最好的学习方法
3. **不怕出错**: 错误是学习的机会
4. **持续学习**: 每天进步一点点

### 💪 坚持技巧
1. **设定小目标**: 每周完成一个小项目
2. **记录进度**: 写学习日志
3. **寻找乐趣**: 做自己感兴趣的项目
4. **交流分享**: 加入学习社区

### 🚀 下一步
完成12周学习后，你应该：
- 能够阅读理解大部分Python代码
- 能够独立完成中小型项目
- 知道如何查文档解决问题
- 为学习第三方库打下良好基础

---

**祝学习顺利！记住：编程是一门手艺，需要大量练习。坚持下去，你一定能掌握！** 💪🎉

---

*更新日期: 2025-12-30*
*版本: v1.0*


# Python常用库与框架汇总

## 目录
- [Python标准库](#python标准库)
- [数据处理与科学计算](#数据处理与科学计算)
- [Web开发框架](#web开发框架)
- [数据库操作](#数据库操作)
- [网络爬虫](#网络爬虫)
- [数据可视化](#数据可视化)
- [机器学习与深度学习](#机器学习与深度学习)
- [自动化与测试](#自动化与测试)
- [文件处理](#文件处理)
- [其他常用库](#其他常用库)

---

## Python标准库

### 1. **os** - 操作系统接口
- 文件和目录操作
- 路径处理
- 环境变量管理
- 进程管理

### 2. **sys** - 系统相关参数和函数
- 命令行参数处理
- Python解释器交互
- 系统路径管理
- 程序退出控制

### 3. **datetime** - 日期和时间处理
- 日期时间对象创建
- 时间计算和格式化
- 时区处理
- 时间间隔计算

### 4. **json** - JSON数据处理
- JSON数据序列化和反序列化
- 字典与JSON转换
- 文件读写JSON数据

### 5. **re** - 正则表达式
- 文本模式匹配
- 字符串搜索和替换
- 数据验证和提取

### 6. **collections** - 容器数据类型
- Counter（计数器）
- defaultdict（默认字典）
- OrderedDict（有序字典）
- deque（双端队列）
- namedtuple（命名元组）

### 7. **itertools** - 迭代器工具
- 无限迭代器
- 组合迭代器
- 高效循环工具

### 8. **functools** - 函数工具
- 装饰器工具
- 偏函数
- 函数缓存（lru_cache）

### 9. **pathlib** - 面向对象的文件路径
- 路径操作
- 文件系统操作
- 跨平台路径处理

### 10. **threading** - 线程管理
- 多线程编程
- 线程同步
- 锁机制

### 11. **multiprocessing** - 多进程
- 并行处理
- 进程池
- 进程间通信

### 12. **logging** - 日志记录
- 日志输出和管理
- 多级别日志
- 日志格式化

### 13. **argparse** - 命令行参数解析
- CLI工具开发
- 参数验证
- 帮助文档生成

### 14. **csv** - CSV文件处理
- CSV文件读写
- 数据导入导出

### 15. **sqlite3** - SQLite数据库
- 轻量级数据库操作
- SQL查询执行

### 16. **urllib** - URL处理
- URL请求
- URL解析
- 网络数据获取

### 17. **pickle** - 对象序列化
- Python对象持久化
- 数据保存和加载

### 18. **random** - 随机数生成
- 随机数生成
- 随机选择
- 洗牌算法

### 19. **math** - 数学函数
- 基本数学运算
- 三角函数
- 对数和指数

### 20. **time** - 时间访问和转换
- 时间戳
- 程序暂停
- 性能测试

---

## 数据处理与科学计算

### 1. **NumPy** - 数值计算基础
- 多维数组对象
- 矩阵运算
- 线性代数
- 随机数生成
- 数学函数库

### 2. **Pandas** - 数据分析
- DataFrame和Series数据结构
- 数据清洗和预处理
- 数据聚合和分组
- 时间序列分析
- 数据导入导出（CSV、Excel、SQL等）

### 3. **SciPy** - 科学计算
- 优化算法
- 信号处理
- 统计函数
- 数值积分
- 插值和拟合

### 4. **SymPy** - 符号计算
- 符号数学
- 代数运算
- 微积分
- 方程求解

---

## Web开发框架

### 1. **Django** - 全功能Web框架
- MTV架构（Model-Template-View）
- ORM数据库抽象
- 用户认证系统
- 管理后台
- 表单处理
- 适合大型企业级应用

### 2. **Flask** - 轻量级Web框架
- 微框架设计
- 灵活扩展
- RESTful API开发
- 模板引擎（Jinja2）
- 适合中小型项目和API服务

### 3. **FastAPI** - 现代异步Web框架
- 高性能异步处理
- 自动API文档生成（Swagger/OpenAPI）
- 类型提示支持
- 数据验证（Pydantic）
- 适合构建高性能API

### 4. **Tornado** - 异步网络框架
- 非阻塞网络I/O
- WebSocket支持
- 长连接处理
- 高并发场景

### 5. **Pyramid** - 灵活的Web框架
- 可扩展性强
- URL分发
- 多种数据库支持

---

## 数据库操作

### 1. **SQLAlchemy** - SQL工具包和ORM
- 数据库ORM映射
- 多数据库支持
- 查询构建器
- 连接池管理

### 2. **PyMySQL** - MySQL数据库连接
- MySQL数据库操作
- 纯Python实现
- 兼容MySQLdb

### 3. **psycopg2** - PostgreSQL适配器
- PostgreSQL数据库连接
- 高性能数据库操作

### 4. **pymongo** - MongoDB驱动
- MongoDB NoSQL数据库操作
- 文档型数据库交互

### 5. **redis-py** - Redis客户端
- Redis缓存操作
- 键值存储
- 发布订阅

### 6. **DuckDB** - 嵌入式分析数据库
- SQL分析查询
- 高性能数据分析
- Pandas集成

---

## 网络爬虫

### 1. **Requests** - HTTP库
- HTTP请求发送
- RESTful API调用
- Session管理
- 文件上传下载

### 2. **BeautifulSoup4** - HTML/XML解析
- 网页内容解析
- DOM树遍历
- 数据提取

### 3. **lxml** - XML和HTML处理
- 高性能解析
- XPath支持
- XML处理

### 4. **Scrapy** - 爬虫框架
- 完整的爬虫解决方案
- 分布式爬取
- 数据管道
- 中间件系统
- 自动限速和去重

### 5. **Selenium** - 浏览器自动化
- 动态网页爬取
- 浏览器模拟
- 自动化测试
- JavaScript渲染

### 6. **Playwright** - 现代浏览器自动化
- 多浏览器支持
- 异步操作
- 自动等待机制
- 网络拦截

---

## 数据可视化

### 1. **Matplotlib** - 基础绘图库
- 2D图表绘制
- 线图、柱状图、散点图
- 高度可定制
- 科学出版级图表

### 2. **Seaborn** - 统计可视化
- 基于Matplotlib
- 美观的默认样式
- 统计图表
- 热力图、分布图

### 3. **Plotly** - 交互式可视化
- 交互式图表
- 3D可视化
- 在线分享
- Dash仪表板

### 4. **Bokeh** - 交互式Web可视化
- 浏览器中的交互图表
- 大数据可视化
- 实时流数据

### 5. **Altair** - 声明式可视化
- 简洁的API
- Vega-Lite语法
- 交互式图表

---

## 机器学习与深度学习

### 1. **Scikit-learn** - 机器学习
- 分类、回归、聚类算法
- 数据预处理
- 模型评估
- 特征工程
- 模型选择和调参

### 2. **TensorFlow** - 深度学习框架
- 神经网络构建
- 大规模机器学习
- 模型部署
- TPU支持

### 3. **PyTorch** - 深度学习框架
- 动态计算图
- 研究友好
- GPU加速
- 自然的Python风格

### 4. **Keras** - 高级神经网络API
- 简化的深度学习接口
- 快速原型开发
- 多后端支持

### 5. **XGBoost** - 梯度提升
- 高性能梯度提升
- 特征重要性
- 竞赛利器

### 6. **LightGBM** - 轻量级梯度提升
- 快速训练速度
- 低内存消耗
- 高准确率

### 7. **OpenCV** - 计算机视觉
- 图像处理
- 视频分析
- 目标检测
- 人脸识别

### 8. **NLTK** - 自然语言处理
- 文本处理
- 分词、词性标注
- 语义分析

### 9. **spaCy** - 工业级NLP
- 快速文本处理
- 命名实体识别
- 依存句法分析

### 10. **transformers** - 预训练模型
- BERT、GPT等模型
- 文本生成
- 问答系统
- 翻译

---

## 自动化与测试

### 1. **pytest** - 测试框架
- 单元测试
- 集成测试
- 插件生态系统
- 参数化测试

### 2. **unittest** - 标准测试框架
- Python内置
- 测试套件
- Mock对象

### 3. **Mock** - 模拟对象
- 测试隔离
- 依赖模拟

### 4. **coverage** - 代码覆盖率
- 测试覆盖度分析
- 报告生成

### 5. **tox** - 自动化测试
- 多环境测试
- 持续集成

### 6. **PyAutoGUI** - GUI自动化
- 鼠标键盘控制
- 屏幕截图
- 图像识别

---

## 文件处理

### 1. **openpyxl** - Excel操作
- Excel文件读写
- 样式设置
- 公式处理
- 图表创建

### 2. **xlsxwriter** - Excel写入
- 创建Excel文件
- 格式化
- 图表生成

### 3. **python-docx** - Word文档
- Word文档创建和编辑
- 段落和表格处理
- 样式设置

### 4. **PyPDF2** - PDF处理
- PDF读取和合并
- 页面提取
- 元数据编辑

### 5. **pdfplumber** - PDF数据提取
- 文本提取
- 表格提取
- 精确定位

### 6. **Pillow (PIL)** - 图像处理
- 图像读取和保存
- 图像编辑
- 格式转换
- 滤镜效果

---

## 其他常用库

### 1. **virtualenv / venv** - 虚拟环境
- 项目环境隔离
- 依赖管理

### 2. **pip** - 包管理器
- 包安装和卸载
- 依赖解析

### 3. **pipenv** - 包和虚拟环境管理
- Pipfile依赖声明
- 自动虚拟环境

### 4. **poetry** - 现代依赖管理
- 依赖解析
- 项目打包
- 发布管理

### 5. **black** - 代码格式化
- 自动代码格式化
- PEP 8风格

### 6. **flake8** - 代码检查
- 代码质量检查
- PEP 8合规性

### 7. **pylint** - 代码分析
- 静态代码分析
- 代码评分

### 8. **mypy** - 类型检查
- 静态类型检查
- 类型提示验证

### 9. **click** - 命令行工具
- CLI应用开发
- 参数解析
- 命令组织

### 10. **python-dotenv** - 环境变量管理
- .env文件加载
- 配置管理

### 11. **schedule** - 任务调度
- 定时任务
- 周期性任务执行

### 12. **APScheduler** - 高级调度器
- 复杂任务调度
- 多种触发器
- 持久化支持

### 13. **Celery** - 分布式任务队列
- 异步任务处理
- 定时任务
- 分布式系统

### 14. **Paramiko** - SSH协议
- SSH连接
- SFTP文件传输
- 远程命令执行

### 15. **cryptography** - 加密库
- 数据加密解密
- 密钥管理
- 证书处理

### 16. **hashlib** - 哈希算法（标准库）
- MD5、SHA等哈希
- 数据签名
- 密码存储

### 17. **tqdm** - 进度条
- 循环进度显示
- 美观的进度条

### 18. **Rich** - 终端美化
- 彩色终端输出
- 表格显示
- 进度条
- 语法高亮

### 19. **loguru** - 简化日志
- 简单易用的日志库
- 自动日志轮转
- 异常捕获

### 20. **pydantic** - 数据验证
- 数据模型定义
- 类型验证
- JSON序列化

---

## 使用建议

### 初学者推荐学习路径：
1. **标准库基础**：os, sys, datetime, json, re
2. **数据处理**：Pandas, NumPy
3. **Web开发**：Flask → Django / FastAPI
4. **爬虫**：Requests + BeautifulSoup4 → Scrapy
5. **可视化**：Matplotlib → Seaborn / Plotly
6. **机器学习**：Scikit-learn → PyTorch / TensorFlow

### 项目类型推荐：

#### 数据分析项目
- Pandas, NumPy, Matplotlib, Seaborn, Jupyter

#### Web应用开发
- Flask/Django/FastAPI, SQLAlchemy, Redis

#### 爬虫项目
- Requests, BeautifulSoup4, Selenium/Playwright, Scrapy

#### 机器学习项目
- NumPy, Pandas, Scikit-learn, TensorFlow/PyTorch

#### 自动化脚本
- os, sys, schedule, PyAutoGUI, openpyxl

---

## 安装常用命令

```bash
# 数据处理
pip install numpy pandas scipy

# Web开发
pip install flask django fastapi

# 爬虫
pip install requests beautifulsoup4 lxml scrapy selenium playwright

# 可视化
pip install matplotlib seaborn plotly bokeh

# 机器学习
pip install scikit-learn tensorflow pytorch transformers

# 文件处理
pip install openpyxl xlsxwriter python-docx PyPDF2 pdfplumber pillow

# 数据库
pip install sqlalchemy pymysql psycopg2 pymongo redis

# 测试
pip install pytest coverage

# 实用工具
pip install requests tqdm rich loguru python-dotenv click
```

---

**更新日期**：2025年12月

**版权说明**：本文档整理常用Python库和框架，供学习参考使用。


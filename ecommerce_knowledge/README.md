# 电商运营数据分析知识网页

一个基于 Flask 构建的电商运营数据公式学习网站，帮助电商运营人员快速掌握核心数据指标。

## 功能特点

- 📊 **六大分类**：销售、转化、流量、复购、库存、营销指标
- 🧮 **在线计算器**：输入数据即时计算结果
- 📖 **详细说明**：每个公式包含含义、原理、示例和应用场景
- 📱 **响应式设计**：支持电脑、平板、手机访问
- 🎨 **简洁美观**：现代化UI设计

## 包含公式

### 销售指标 💰
- GMV（成交总额）
- 销售额
- 客单价（AOV）
- 人均消费额

### 转化指标 🔄
- 转化率（CVR）
- 点击率（CTR）
- 加购率
- 收藏率
- 支付转化率

### 流量指标 📊
- 浏览量（PV）
- 访客数（UV）
- 人均浏览量
- 跳出率
- 平均停留时长

### 复购指标 🔁
- 复购率
- 复购频次
- 客户生命周期价值（LTV）
- 留存率

### 库存指标 📦
- 库存周转率
- 库存周转天数
- 售罄率
- 缺货率

### 营销指标 📢
- 投资回报率（ROI）
- 广告投入产出比（ROAS）
- 获客成本（CAC）
- 单次点击成本（CPC）
- 千次展现成本（CPM）
- 毛利率

## 快速开始

### 1. 安装依赖

```bash
cd ecommerce_knowledge
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

### 3. 访问网站

打开浏览器访问：http://localhost:5000

## 项目结构

```
ecommerce_knowledge/
├── app.py                    # Flask 主应用
├── requirements.txt          # 依赖包
├── README.md                 # 项目说明
├── templates/                # HTML 模板
│   ├── base.html            # 基础模板
│   ├── index.html           # 首页
│   ├── category.html        # 分类页面
│   └── 404.html             # 404 错误页
├── static/                   # 静态文件
│   ├── css/
│   │   └── style.css        # 样式文件
│   ├── js/
│   │   └── main.js          # JavaScript
│   └── images/              # 图片资源
└── data/                     # 数据文件（可选）
```

## 技术栈

- **后端**：Python 3.8+ / Flask 3.0
- **前端**：HTML5 / CSS3 / JavaScript (原生)
- **字体**：Noto Sans SC / JetBrains Mono

## 使用说明

1. **首页**：浏览所有公式分类，点击进入详情
2. **分类页**：查看该类别的所有公式
3. **公式卡片**：
   - 查看公式表达式和说明
   - 了解应用场景
   - 使用在线计算器计算结果

## 自定义

### 添加新公式

在 `app.py` 中的 `FORMULAS` 字典中添加新公式：

```python
{
    'id': 'new_formula',
    'name': '新公式名称',
    'english': 'New Formula',
    'formula': '公式表达式',
    'description': '公式说明',
    'variables': [
        {'name': 'var1', 'label': '变量1', 'unit': '单位'}
    ],
    'result_unit': '结果单位',
    'example': {
        'var1': 100,
        'result': 100
    },
    'application': '应用场景说明'
}
```

### 修改样式

编辑 `static/css/style.css` 中的 CSS 变量：

```css
:root {
    --primary-color: #1a365d;  /* 主色调 */
    --accent-color: #ed8936;   /* 强调色 */
}
```

## 许可

MIT License

## 作者

电商运营学习项目








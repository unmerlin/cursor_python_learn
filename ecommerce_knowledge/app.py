"""
电商运营数据分析知识网页
Flask应用主入口
"""

import os
import io
from flask import Flask, render_template, jsonify, request, send_file, make_response
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ecommerce-knowledge-2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 平台配置
PLATFORMS = {
    'taobao': {
        'name': '淘宝',
        'icon': '🛒',
        'color': '#ff5000'
    },
    'jd': {
        'name': '京东',
        'icon': '📦',
        'color': '#e1251b'
    },
    'douyin': {
        'name': '抖音',
        'icon': '🎵',
        'color': '#000000'
    },
    'pdd': {
        'name': '拼多多',
        'icon': '💰',
        'color': '#e02e24'
    },
    'waimai': {
        'name': '外卖',
        'icon': '🍔',
        'color': '#ff6600'
    }
}

# 指标分类配置
METRICS = {
    'sales': {
        'title': '销售指标',
        'icon': '💰',
        'description': '电商销售核心指标，衡量店铺销售能力'
    },
    'conversion': {
        'title': '转化指标',
        'icon': '🔄',
        'description': '衡量用户从浏览到购买的转化效率'
    },
    'traffic': {
        'title': '流量指标',
        'icon': '📊',
        'description': '衡量店铺流量规模和用户行为'
    },
    'repurchase': {
        'title': '复购指标',
        'icon': '🔁',
        'description': '衡量用户忠诚度和复购能力'
    },
    'inventory': {
        'title': '库存指标',
        'icon': '📦',
        'description': '衡量库存管理效率和资金占用'
    },
    'marketing': {
        'title': '营销指标',
        'icon': '📢',
        'description': '衡量营销投入产出效率'
    }
}

# 公式数据
FORMULAS = {
    'sales': {
        'title': '销售指标',
        'icon': '💰',
        'description': '电商销售核心指标，衡量店铺销售能力',
        'formulas': [
            {
                'id': 'gmv',
                'name': 'GMV（成交总额）',
                'english': 'Gross Merchandise Volume',
                'formula': 'GMV = 订单数 × 订单均价',
                'formula_latex': 'GMV = Orders \\times AvgPrice',
                'description': 'GMV是指在一定时间内，平台或店铺的成交总额，包含已付款和未付款的订单金额。是衡量电商规模的重要指标。',
                'variables': [
                    {'name': 'orders', 'label': '订单数', 'unit': '单'},
                    {'name': 'avg_price', 'label': '订单均价', 'unit': '元'}
                ],
                'result_unit': '元',
                'example': {
                    'orders': 1000,
                    'avg_price': 150,
                    'result': 150000
                },
                'application': '评估店铺整体销售规模，制定销售目标，对比同行数据。'
            },
            {
                'id': 'sales_amount',
                'name': '销售额',
                'english': 'Sales Amount',
                'formula': '销售额 = 访客数 × 转化率 × 客单价',
                'formula_latex': 'Sales = UV \\times CVR \\times AOV',
                'description': '销售额是店铺实际成交的金额总和，是电商最核心的经营指标。可分解为流量、转化、客单价三要素。',
                'variables': [
                    {'name': 'uv', 'label': '访客数(UV)', 'unit': '人'},
                    {'name': 'cvr', 'label': '转化率', 'unit': '%'},
                    {'name': 'aov', 'label': '客单价', 'unit': '元'}
                ],
                'result_unit': '元',
                'example': {
                    'uv': 10000,
                    'cvr': 3,
                    'aov': 200,
                    'result': 60000
                },
                'application': '分析销售构成，找出提升销售的关键因素（提流量/提转化/提客单价）。'
            },
            {
                'id': 'aov',
                'name': '客单价（AOV）',
                'english': 'Average Order Value',
                'formula': '客单价 = 销售额 ÷ 订单数',
                'formula_latex': 'AOV = \\frac{Sales}{Orders}',
                'description': '客单价表示每个订单的平均金额，反映顾客的单次消费能力。提升客单价是提高销售额的重要方式。',
                'variables': [
                    {'name': 'sales', 'label': '销售额', 'unit': '元'},
                    {'name': 'orders', 'label': '订单数', 'unit': '单'}
                ],
                'result_unit': '元',
                'example': {
                    'sales': 100000,
                    'orders': 500,
                    'result': 200
                },
                'application': '优化商品组合、设计满减活动、调整定价策略。'
            },
            {
                'id': 'per_customer_value',
                'name': '人均消费额',
                'english': 'Average Revenue Per User',
                'formula': '人均消费额 = 销售额 ÷ 购买人数',
                'formula_latex': 'ARPU = \\frac{Sales}{Buyers}',
                'description': '人均消费额反映每个购买用户的平均消费金额，与客单价不同的是考虑了同一用户的多次购买。',
                'variables': [
                    {'name': 'sales', 'label': '销售额', 'unit': '元'},
                    {'name': 'buyers', 'label': '购买人数', 'unit': '人'}
                ],
                'result_unit': '元',
                'example': {
                    'sales': 100000,
                    'buyers': 400,
                    'result': 250
                },
                'application': '评估用户价值，制定会员策略，分析复购贡献。'
            }
        ]
    },
    'conversion': {
        'title': '转化指标',
        'icon': '🔄',
        'description': '衡量用户从浏览到购买的转化效率',
        'formulas': [
            {
                'id': 'cvr',
                'name': '转化率（CVR）',
                'english': 'Conversion Rate',
                'formula': '转化率 = 成交订单数 ÷ 访客数 × 100%',
                'formula_latex': 'CVR = \\frac{Orders}{UV} \\times 100\\%',
                'description': '转化率是衡量店铺运营效率的核心指标，反映访客转化为买家的比例。行业平均转化率约2-5%。',
                'variables': [
                    {'name': 'orders', 'label': '成交订单数', 'unit': '单'},
                    {'name': 'uv', 'label': '访客数', 'unit': '人'}
                ],
                'result_unit': '%',
                'example': {
                    'orders': 150,
                    'uv': 5000,
                    'result': 3
                },
                'application': '评估流量质量、页面体验、商品吸引力，优化转化漏斗。'
            },
            {
                'id': 'ctr',
                'name': '点击率（CTR）',
                'english': 'Click Through Rate',
                'formula': '点击率 = 点击数 ÷ 展现量 × 100%',
                'formula_latex': 'CTR = \\frac{Clicks}{Impressions} \\times 100\\%',
                'description': '点击率反映商品或广告的吸引力，是评估主图、标题、创意效果的重要指标。',
                'variables': [
                    {'name': 'clicks', 'label': '点击数', 'unit': '次'},
                    {'name': 'impressions', 'label': '展现量', 'unit': '次'}
                ],
                'result_unit': '%',
                'example': {
                    'clicks': 500,
                    'impressions': 10000,
                    'result': 5
                },
                'application': '优化商品主图、标题、广告创意，提升流量获取效率。'
            },
            {
                'id': 'add_cart_rate',
                'name': '加购率',
                'english': 'Add to Cart Rate',
                'formula': '加购率 = 加购人数 ÷ 访客数 × 100%',
                'formula_latex': 'AddCartRate = \\frac{AddCartUsers}{UV} \\times 100\\%',
                'description': '加购率反映商品的吸引力和购买意向，是预测未来销售的重要指标。',
                'variables': [
                    {'name': 'add_cart_users', 'label': '加购人数', 'unit': '人'},
                    {'name': 'uv', 'label': '访客数', 'unit': '人'}
                ],
                'result_unit': '%',
                'example': {
                    'add_cart_users': 800,
                    'uv': 10000,
                    'result': 8
                },
                'application': '评估商品吸引力，识别潜在爆款，优化详情页设计。'
            },
            {
                'id': 'collect_rate',
                'name': '收藏率',
                'english': 'Collect Rate',
                'formula': '收藏率 = 收藏人数 ÷ 访客数 × 100%',
                'formula_latex': 'CollectRate = \\frac{CollectUsers}{UV} \\times 100\\%',
                'description': '收藏率反映用户对商品的兴趣程度，高收藏率的商品在促销期间容易转化。',
                'variables': [
                    {'name': 'collect_users', 'label': '收藏人数', 'unit': '人'},
                    {'name': 'uv', 'label': '访客数', 'unit': '人'}
                ],
                'result_unit': '%',
                'example': {
                    'collect_users': 600,
                    'uv': 10000,
                    'result': 6
                },
                'application': '大促前分析收藏数据，预估活动销量，制定库存计划。'
            },
            {
                'id': 'payment_rate',
                'name': '支付转化率',
                'english': 'Payment Conversion Rate',
                'formula': '支付转化率 = 支付订单数 ÷ 下单数 × 100%',
                'formula_latex': 'PayRate = \\frac{PaidOrders}{Orders} \\times 100\\%',
                'description': '支付转化率反映从下单到支付的转化效率，低支付率可能意味着支付体验问题或价格犹豫。',
                'variables': [
                    {'name': 'paid_orders', 'label': '支付订单数', 'unit': '单'},
                    {'name': 'orders', 'label': '下单数', 'unit': '单'}
                ],
                'result_unit': '%',
                'example': {
                    'paid_orders': 450,
                    'orders': 500,
                    'result': 90
                },
                'application': '优化支付流程、分析放弃支付原因、设计催付策略。'
            }
        ]
    },
    'traffic': {
        'title': '流量指标',
        'icon': '📊',
        'description': '衡量店铺流量规模和用户行为',
        'formulas': [
            {
                'id': 'pv',
                'name': '浏览量（PV）',
                'english': 'Page View',
                'formula': 'PV = 所有页面被访问的总次数',
                'formula_latex': 'PV = \\sum PageViews',
                'description': 'PV是页面浏览量的总和，同一用户多次访问同一页面会被重复计算。反映页面的热度和用户活跃度。',
                'variables': [
                    {'name': 'page_views', 'label': '页面访问次数', 'unit': '次'}
                ],
                'result_unit': '次',
                'example': {
                    'page_views': 50000,
                    'result': 50000
                },
                'application': '分析页面热度、用户路径、内容受欢迎程度。'
            },
            {
                'id': 'uv',
                'name': '访客数（UV）',
                'english': 'Unique Visitor',
                'formula': 'UV = 去重后的访问用户数',
                'formula_latex': 'UV = CountDistinct(Visitors)',
                'description': 'UV是独立访客数，同一用户在统计周期内多次访问只计算一次。反映店铺的流量规模。',
                'variables': [
                    {'name': 'visitors', 'label': '独立访客数', 'unit': '人'}
                ],
                'result_unit': '人',
                'example': {
                    'visitors': 10000,
                    'result': 10000
                },
                'application': '评估店铺流量规模、流量来源分析、制定引流目标。'
            },
            {
                'id': 'avg_page_views',
                'name': '人均浏览量',
                'english': 'Pages Per Session',
                'formula': '人均浏览量 = PV ÷ UV',
                'formula_latex': 'AvgPV = \\frac{PV}{UV}',
                'description': '人均浏览量反映用户的浏览深度，数值越高说明用户对店铺内容越感兴趣。',
                'variables': [
                    {'name': 'pv', 'label': '浏览量(PV)', 'unit': '次'},
                    {'name': 'uv', 'label': '访客数(UV)', 'unit': '人'}
                ],
                'result_unit': '页/人',
                'example': {
                    'pv': 50000,
                    'uv': 10000,
                    'result': 5
                },
                'application': '评估店铺内容质量、关联推荐效果、用户粘性。'
            },
            {
                'id': 'bounce_rate',
                'name': '跳出率',
                'english': 'Bounce Rate',
                'formula': '跳出率 = 只访问一个页面就离开的访客数 ÷ 总访客数 × 100%',
                'formula_latex': 'BounceRate = \\frac{SinglePageVisitors}{UV} \\times 100\\%',
                'description': '跳出率反映用户对着陆页的满意度，高跳出率通常意味着页面内容与用户预期不符。',
                'variables': [
                    {'name': 'single_page_visitors', 'label': '单页访客数', 'unit': '人'},
                    {'name': 'uv', 'label': '总访客数', 'unit': '人'}
                ],
                'result_unit': '%',
                'example': {
                    'single_page_visitors': 4000,
                    'uv': 10000,
                    'result': 40
                },
                'application': '优化着陆页设计、提升内容相关性、降低无效流量。'
            },
            {
                'id': 'avg_stay_time',
                'name': '平均停留时长',
                'english': 'Average Session Duration',
                'formula': '平均停留时长 = 总停留时长 ÷ 访问次数',
                'formula_latex': 'AvgTime = \\frac{TotalTime}{Sessions}',
                'description': '平均停留时长反映用户对页面内容的关注程度，时间越长说明内容越有吸引力。',
                'variables': [
                    {'name': 'total_time', 'label': '总停留时长', 'unit': '秒'},
                    {'name': 'sessions', 'label': '访问次数', 'unit': '次'}
                ],
                'result_unit': '秒',
                'example': {
                    'total_time': 300000,
                    'sessions': 10000,
                    'result': 30
                },
                'application': '评估页面内容质量、优化详情页设计、分析用户行为。'
            }
        ]
    },
    'repurchase': {
        'title': '复购指标',
        'icon': '🔁',
        'description': '衡量用户忠诚度和复购能力',
        'formulas': [
            {
                'id': 'repurchase_rate',
                'name': '复购率',
                'english': 'Repurchase Rate',
                'formula': '复购率 = 复购用户数 ÷ 总购买用户数 × 100%',
                'formula_latex': 'RepurchaseRate = \\frac{RepeatBuyers}{TotalBuyers} \\times 100\\%',
                'description': '复购率反映用户的忠诚度和产品满意度，是衡量私域运营效果的核心指标。',
                'variables': [
                    {'name': 'repeat_buyers', 'label': '复购用户数', 'unit': '人'},
                    {'name': 'total_buyers', 'label': '总购买用户数', 'unit': '人'}
                ],
                'result_unit': '%',
                'example': {
                    'repeat_buyers': 200,
                    'total_buyers': 1000,
                    'result': 20
                },
                'application': '评估产品质量、优化用户体验、制定会员策略。'
            },
            {
                'id': 'repurchase_frequency',
                'name': '复购频次',
                'english': 'Purchase Frequency',
                'formula': '复购频次 = 总订单数 ÷ 购买用户数',
                'formula_latex': 'Frequency = \\frac{TotalOrders}{Buyers}',
                'description': '复购频次反映用户的购买活跃度，结合复购率可以全面评估用户价值。',
                'variables': [
                    {'name': 'total_orders', 'label': '总订单数', 'unit': '单'},
                    {'name': 'buyers', 'label': '购买用户数', 'unit': '人'}
                ],
                'result_unit': '次/人',
                'example': {
                    'total_orders': 1500,
                    'buyers': 1000,
                    'result': 1.5
                },
                'application': '设计复购激励活动、优化商品上新节奏、制定会员等级。'
            },
            {
                'id': 'ltv',
                'name': '客户生命周期价值（LTV）',
                'english': 'Customer Lifetime Value',
                'formula': 'LTV = 客单价 × 复购频次 × 客户生命周期',
                'formula_latex': 'LTV = AOV \\times Frequency \\times Lifetime',
                'description': 'LTV是一个客户在整个生命周期内为企业带来的总价值，是衡量获客成本合理性的重要参考。',
                'variables': [
                    {'name': 'aov', 'label': '客单价', 'unit': '元'},
                    {'name': 'frequency', 'label': '年均复购频次', 'unit': '次'},
                    {'name': 'lifetime', 'label': '客户生命周期', 'unit': '年'}
                ],
                'result_unit': '元',
                'example': {
                    'aov': 200,
                    'frequency': 4,
                    'lifetime': 3,
                    'result': 2400
                },
                'application': '制定获客预算、评估用户质量、优化用户分层策略。'
            },
            {
                'id': 'retention_rate',
                'name': '留存率',
                'english': 'Retention Rate',
                'formula': '留存率 = 第N日/周/月仍活跃的用户数 ÷ 初始用户数 × 100%',
                'formula_latex': 'Retention = \\frac{ActiveUsers_N}{InitialUsers} \\times 100\\%',
                'description': '留存率反映用户的持续活跃程度，常用于分析用户生命周期和产品粘性。',
                'variables': [
                    {'name': 'active_users', 'label': '留存用户数', 'unit': '人'},
                    {'name': 'initial_users', 'label': '初始用户数', 'unit': '人'}
                ],
                'result_unit': '%',
                'example': {
                    'active_users': 300,
                    'initial_users': 1000,
                    'result': 30
                },
                'application': '分析用户流失节点、优化用户召回策略、评估运营活动效果。'
            }
        ]
    },
    'inventory': {
        'title': '库存指标',
        'icon': '📦',
        'description': '衡量库存管理效率和资金占用',
        'formulas': [
            {
                'id': 'inventory_turnover',
                'name': '库存周转率',
                'english': 'Inventory Turnover',
                'formula': '库存周转率 = 销售成本 ÷ 平均库存金额',
                'formula_latex': 'Turnover = \\frac{COGS}{AvgInventory}',
                'description': '库存周转率反映库存变现的速度，数值越高说明库存管理越高效，资金占用越少。',
                'variables': [
                    {'name': 'cogs', 'label': '销售成本', 'unit': '元'},
                    {'name': 'avg_inventory', 'label': '平均库存金额', 'unit': '元'}
                ],
                'result_unit': '次',
                'example': {
                    'cogs': 600000,
                    'avg_inventory': 100000,
                    'result': 6
                },
                'application': '优化库存结构、加快滞销品处理、提高资金使用效率。'
            },
            {
                'id': 'inventory_days',
                'name': '库存周转天数',
                'english': 'Days Sales of Inventory',
                'formula': '库存周转天数 = 365 ÷ 库存周转率',
                'formula_latex': 'DSI = \\frac{365}{Turnover}',
                'description': '库存周转天数反映库存平均多少天能销售出去，天数越少说明库存效率越高。',
                'variables': [
                    {'name': 'turnover', 'label': '库存周转率', 'unit': '次'}
                ],
                'result_unit': '天',
                'example': {
                    'turnover': 6,
                    'result': 60.83
                },
                'application': '制定补货计划、控制库存水平、预测资金需求。'
            },
            {
                'id': 'sell_through_rate',
                'name': '售罄率',
                'english': 'Sell Through Rate',
                'formula': '售罄率 = 销售数量 ÷ (期初库存 + 进货数量) × 100%',
                'formula_latex': 'SellThrough = \\frac{Sold}{BeginInv + Purchase} \\times 100\\%',
                'description': '售罄率反映商品的畅销程度，是评估选品和采购决策的重要指标。',
                'variables': [
                    {'name': 'sold', 'label': '销售数量', 'unit': '件'},
                    {'name': 'begin_inv', 'label': '期初库存', 'unit': '件'},
                    {'name': 'purchase', 'label': '进货数量', 'unit': '件'}
                ],
                'result_unit': '%',
                'example': {
                    'sold': 800,
                    'begin_inv': 200,
                    'purchase': 1000,
                    'result': 66.67
                },
                'application': '评估商品畅销度、优化采购计划、识别滞销品。'
            },
            {
                'id': 'stockout_rate',
                'name': '缺货率',
                'english': 'Stockout Rate',
                'formula': '缺货率 = 缺货SKU数 ÷ 总SKU数 × 100%',
                'formula_latex': 'Stockout = \\frac{OutOfStockSKU}{TotalSKU} \\times 100\\%',
                'description': '缺货率反映库存管理的及时性，高缺货率会导致销售损失和用户流失。',
                'variables': [
                    {'name': 'out_of_stock', 'label': '缺货SKU数', 'unit': '个'},
                    {'name': 'total_sku', 'label': '总SKU数', 'unit': '个'}
                ],
                'result_unit': '%',
                'example': {
                    'out_of_stock': 15,
                    'total_sku': 500,
                    'result': 3
                },
                'application': '设置安全库存、优化补货机制、分析缺货原因。'
            }
        ]
    },
    'marketing': {
        'title': '营销指标',
        'icon': '📢',
        'description': '衡量营销投入产出效率',
        'formulas': [
            {
                'id': 'roi',
                'name': '投资回报率（ROI）',
                'english': 'Return on Investment',
                'formula': 'ROI = (收入 - 成本) ÷ 成本 × 100%',
                'formula_latex': 'ROI = \\frac{Revenue - Cost}{Cost} \\times 100\\%',
                'description': 'ROI是衡量投资效益的核心指标，反映每投入1元能获得多少回报。正值表示盈利，负值表示亏损。',
                'variables': [
                    {'name': 'revenue', 'label': '收入', 'unit': '元'},
                    {'name': 'cost', 'label': '成本', 'unit': '元'}
                ],
                'result_unit': '%',
                'example': {
                    'revenue': 50000,
                    'cost': 10000,
                    'result': 400
                },
                'application': '评估营销活动效果、优化投放策略、分配营销预算。'
            },
            {
                'id': 'roas',
                'name': '广告投入产出比（ROAS）',
                'english': 'Return on Ad Spend',
                'formula': 'ROAS = 广告带来的收入 ÷ 广告花费',
                'formula_latex': 'ROAS = \\frac{AdRevenue}{AdSpend}',
                'description': 'ROAS专门衡量广告投放的效率，数值大于1表示广告带来了正向收益。',
                'variables': [
                    {'name': 'ad_revenue', 'label': '广告带来的收入', 'unit': '元'},
                    {'name': 'ad_spend', 'label': '广告花费', 'unit': '元'}
                ],
                'result_unit': '',
                'example': {
                    'ad_revenue': 30000,
                    'ad_spend': 5000,
                    'result': 6
                },
                'application': '评估广告渠道效果、优化投放素材、调整出价策略。'
            },
            {
                'id': 'cac',
                'name': '获客成本（CAC）',
                'english': 'Customer Acquisition Cost',
                'formula': 'CAC = 营销总成本 ÷ 新增客户数',
                'formula_latex': 'CAC = \\frac{MarketingCost}{NewCustomers}',
                'description': 'CAC反映获取一个新客户的平均成本，需要与LTV对比评估获客的合理性。健康的比例是LTV:CAC > 3:1。',
                'variables': [
                    {'name': 'marketing_cost', 'label': '营销总成本', 'unit': '元'},
                    {'name': 'new_customers', 'label': '新增客户数', 'unit': '人'}
                ],
                'result_unit': '元/人',
                'example': {
                    'marketing_cost': 10000,
                    'new_customers': 200,
                    'result': 50
                },
                'application': '控制获客成本、优化渠道结构、评估用户质量。'
            },
            {
                'id': 'cpc',
                'name': '单次点击成本（CPC）',
                'english': 'Cost Per Click',
                'formula': 'CPC = 广告花费 ÷ 点击次数',
                'formula_latex': 'CPC = \\frac{AdSpend}{Clicks}',
                'description': 'CPC反映每获得一次点击需要支付的成本，是评估广告成本效益的基础指标。',
                'variables': [
                    {'name': 'ad_spend', 'label': '广告花费', 'unit': '元'},
                    {'name': 'clicks', 'label': '点击次数', 'unit': '次'}
                ],
                'result_unit': '元/次',
                'example': {
                    'ad_spend': 1000,
                    'clicks': 500,
                    'result': 2
                },
                'application': '评估广告竞争程度、优化关键词出价、控制投放成本。'
            },
            {
                'id': 'cpm',
                'name': '千次展现成本（CPM）',
                'english': 'Cost Per Mille',
                'formula': 'CPM = 广告花费 ÷ 展现量 × 1000',
                'formula_latex': 'CPM = \\frac{AdSpend}{Impressions} \\times 1000',
                'description': 'CPM反映每千次广告展现的成本，常用于品牌曝光类广告的成本评估。',
                'variables': [
                    {'name': 'ad_spend', 'label': '广告花费', 'unit': '元'},
                    {'name': 'impressions', 'label': '展现量', 'unit': '次'}
                ],
                'result_unit': '元/千次',
                'example': {
                    'ad_spend': 500,
                    'impressions': 100000,
                    'result': 5
                },
                'application': '评估曝光成本、选择投放渠道、制定品牌推广预算。'
            },
            {
                'id': 'gross_profit_margin',
                'name': '毛利率',
                'english': 'Gross Profit Margin',
                'formula': '毛利率 = (销售收入 - 销售成本) ÷ 销售收入 × 100%',
                'formula_latex': 'GPM = \\frac{Revenue - COGS}{Revenue} \\times 100\\%',
                'description': '毛利率反映商品的盈利能力，是定价策略和成本控制的重要参考。',
                'variables': [
                    {'name': 'revenue', 'label': '销售收入', 'unit': '元'},
                    {'name': 'cogs', 'label': '销售成本', 'unit': '元'}
                ],
                'result_unit': '%',
                'example': {
                    'revenue': 100000,
                    'cogs': 60000,
                    'result': 40
                },
                'application': '优化定价策略、控制采购成本、评估商品盈利能力。'
            }
        ]
    }
}


@app.route('/')
def index():
    """首页 - 展示所有平台"""
    return render_template('index.html', platforms=PLATFORMS, metrics=METRICS)


@app.route('/platform/<platform_id>')
def platform_index(platform_id):
    """平台首页"""
    if platform_id not in PLATFORMS:
        return render_template('404.html'), 404
    platform = PLATFORMS[platform_id]
    return render_template('platform.html', 
                         platform_id=platform_id,
                         platform=platform,
                         platforms=PLATFORMS,
                         metrics=METRICS,
                         all_categories=FORMULAS)


@app.route('/platform/<platform_id>/<metric_id>')
def platform_metric(platform_id, metric_id):
    """平台+指标页面"""
    if platform_id not in PLATFORMS or metric_id not in FORMULAS:
        return render_template('404.html'), 404
    
    platform = PLATFORMS[platform_id]
    metric_data = FORMULAS[metric_id]
    metric_info = METRICS[metric_id]
    
    return render_template('category.html',
                         platform_id=platform_id,
                         platform=platform,
                         metric_id=metric_id,
                         metric=metric_data,
                         metric_info=metric_info,
                         platforms=PLATFORMS,
                         metrics=METRICS,
                         all_categories=FORMULAS)


# 保留旧路由以兼容
@app.route('/category/<category_id>')
def category(category_id):
    """分类页面 - 展示某一类别的所有公式（兼容旧路由）"""
    if category_id not in FORMULAS:
        return render_template('404.html'), 404
    category_data = FORMULAS[category_id]
    metric_info = METRICS.get(category_id, {
        'title': category_data['title'],
        'icon': category_data['icon'],
        'description': category_data['description']
    })
    return render_template('category.html', 
                         platform_id='taobao',  # 默认淘宝
                         platform=PLATFORMS['taobao'],
                         category_id=category_id,
                         metric_id=category_id,
                         metric=category_data,
                         metric_info=metric_info,
                         platforms=PLATFORMS,
                         metrics=METRICS,
                         all_categories=FORMULAS)


# 京东专属功能
JD_SPECIAL_FEATURES = {
    'maobao': {
        'name': '自营毛保',
        'icon': '🛡️',
        'description': '京东自营毛利保护计算'
    },
    'rucang': {
        'name': '入仓预估',
        'icon': '📦',
        'description': '根据历史销量预估入仓数量'
    }
}

# 活动效果预测工具
ACTIVITY_TOOLS = {
    'ab_test': {
        'name': 'A/B测试',
        'icon': '🔬',
        'description': '活动对比效果预测'
    }
}

# 数据可视化分析工具
VISUAL_TOOLS = {
    'funnel': {
        'name': '漏斗图',
        'icon': '📊',
        'description': '订单转化漏斗分析'
    }
}


@app.route('/platform/jd/maobao')
def jd_maobao():
    """京东自营毛保页面"""
    platform = PLATFORMS['jd']
    return render_template('jd_maobao.html', 
                         platform_id='jd',
                         platform=platform,
                         platforms=PLATFORMS,
                         metrics=METRICS,
                         jd_features=JD_SPECIAL_FEATURES)


@app.route('/platform/jd/rucang')
def jd_rucang():
    """京东入仓预估页面"""
    platform = PLATFORMS['jd']
    return render_template('jd_rucang.html', 
                         platform_id='jd',
                         platform=platform,
                         platforms=PLATFORMS,
                         metrics=METRICS,
                         jd_features=JD_SPECIAL_FEATURES)


@app.route('/platform/jd/rucang/template')
def jd_rucang_template():
    """下载入仓预估模板文件"""
    # 创建模板DataFrame
    template_data = {
        '商品ID': ['示例001', '示例002', '示例003'],
        '7天销量': [100, 200, 150],
        '15天销量': [180, 350, 280],
        '30天销量': [350, 700, 500],
        '90天销量': [1000, 2000, 1500],
        '现有库存数量': [50, 100, 80]
    }
    df = pd.DataFrame(template_data)
    
    # 创建Excel文件
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='入仓预估数据')
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='入仓预估模板.xlsx'
    )


@app.route('/platform/jd/rucang/calculate', methods=['POST'])
def jd_rucang_calculate():
    """计算入仓预估"""
    try:
        # 获取上传的文件
        if 'file' not in request.files:
            return jsonify({'error': '请上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '请选择文件'}), 400
        
        if not file.filename.endswith('.xlsx'):
            return jsonify({'error': '请上传xlsx格式文件'}), 400
        
        # 获取参数
        safety_factor = float(request.form.get('safety_factor', 1.2))
        weight_7 = float(request.form.get('weight_7', 4))
        weight_15 = float(request.form.get('weight_15', 3))
        weight_30 = float(request.form.get('weight_30', 2))
        weight_90 = float(request.form.get('weight_90', 1))
        
        # 读取Excel文件
        df = pd.read_excel(file)
        
        # 验证必需列
        required_cols = ['商品ID', '7天销量', '15天销量', '30天销量', '90天销量', '现有库存数量']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return jsonify({'error': f'缺少必需列: {", ".join(missing_cols)}'}), 400
        
        # 计算各周期日均销量
        df['7天日均'] = (df['7天销量'] / 7).round(2)
        df['15天日均'] = (df['15天销量'] / 15).round(2)
        df['30天日均'] = (df['30天销量'] / 30).round(2)
        df['90天日均'] = (df['90天销量'] / 90).round(2)
        
        # 计算加权平均日均销量
        total_weight = weight_7 + weight_15 + weight_30 + weight_90
        df['加权日均'] = (
            (df['7天日均'] * weight_7 + 
             df['15天日均'] * weight_15 + 
             df['30天日均'] * weight_30 + 
             df['90天日均'] * weight_90) / total_weight
        ).round(2)
        
        # 预估30天销量
        df['预估30天销量'] = (df['加权日均'] * 30).round(0).astype(int)
        
        # 建议入仓数量（含安全系数）
        df['建议入仓数量'] = (df['预估30天销量'] * safety_factor - df['现有库存数量']).round(0).astype(int)
        df['建议入仓数量'] = df['建议入仓数量'].apply(lambda x: max(0, x))
        
        # 是否需入仓
        df['是否需入仓'] = df['建议入仓数量'].apply(lambda x: '是' if x > 0 else '否')
        
        # 选择输出列
        output_cols = ['商品ID', '7天日均', '15天日均', '30天日均', '90天日均', 
                      '预估30天销量', '现有库存数量', '建议入仓数量', '是否需入仓']
        result_df = df[output_cols].copy()
        result_df.columns = ['商品ID', '7天日均', '15天日均', '30天日均', '90天日均',
                            '预估30天销量', '现有库存', '建议入仓数量', '是否需入仓']
        
        # 汇总统计
        need_rucang_count = (df['是否需入仓'] == '是').sum()
        total_rucang_qty = df['建议入仓数量'].sum()
        
        # 返回结果
        return jsonify({
            'success': True,
            'data': result_df.to_dict('records'),
            'summary': {
                'need_rucang_count': int(need_rucang_count),
                'total_rucang_qty': int(total_rucang_qty),
                'total_products': len(df)
            },
            'params': {
                'safety_factor': safety_factor,
                'weights': {
                    '7天': weight_7,
                    '15天': weight_15,
                    '30天': weight_30,
                    '90天': weight_90
                }
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'处理失败: {str(e)}'}), 500


@app.route('/platform/jd/rucang/export', methods=['POST'])
def jd_rucang_export():
    """导出入仓预估结果"""
    try:
        data = request.json
        if not data or 'results' not in data:
            return jsonify({'error': '无数据可导出'}), 400
        
        df = pd.DataFrame(data['results'])
        
        # 创建Excel文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='入仓预估结果')
            
            # 添加汇总sheet
            if 'summary' in data:
                summary_df = pd.DataFrame([
                    {'指标': '总商品数', '数值': data['summary'].get('total_products', 0)},
                    {'指标': '需入仓商品数', '数值': data['summary'].get('need_rucang_count', 0)},
                    {'指标': '总入仓件数', '数值': data['summary'].get('total_rucang_qty', 0)}
                ])
                summary_df.to_excel(writer, index=False, sheet_name='汇总统计')
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='入仓预估结果.xlsx'
        )
        
    except Exception as e:
        return jsonify({'error': f'导出失败: {str(e)}'}), 500


@app.route('/activity/ab-test')
def ab_test():
    """A/B测试页面"""
    return render_template('ab_test.html',
                         platforms=PLATFORMS,
                         metrics=METRICS,
                         activity_tools=ACTIVITY_TOOLS)


@app.route('/visual/funnel')
def funnel_chart():
    """漏斗图分析页面"""
    return render_template('funnel_chart.html',
                         platforms=PLATFORMS,
                         metrics=METRICS,
                         visual_tools=VISUAL_TOOLS)


@app.route('/visual/funnel/template')
def funnel_template():
    """下载漏斗图模板"""
    template_data = {
        '订单状态': [
            '等待买家付款',
            '买家已付款',
            '买家已付款',
            '待发货',
            '卖家已发货',
            '卖家已发货',
            '交易成功',
            '已取消',
            '退款中的订单'
        ]
    }
    df = pd.DataFrame(template_data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='订单状态数据')
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='订单漏斗图模板.xlsx'
    )


@app.route('/visual/funnel/analyze', methods=['POST'])
def funnel_analyze():
    """分析订单漏斗数据"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '请上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '请选择文件'}), 400
        
        if not file.filename.endswith('.xlsx'):
            return jsonify({'error': '请上传xlsx格式文件'}), 400
        
        # 读取Excel文件
        df = pd.read_excel(file)
        
        # 验证必需列
        if '订单状态' not in df.columns:
            return jsonify({'error': '文件中缺少"订单状态"列'}), 400
        
        # 统计各状态数量
        status_counts = df['订单状态'].value_counts().to_dict()
        
        # 定义正向流程和异常订单
        funnel_statuses = ['等待买家付款', '买家已付款', '待发货', '卖家已发货', '交易成功']
        abnormal_statuses = ['已取消', '退款中的订单']
        
        # 构建漏斗数据
        funnel_data = []
        for status in funnel_statuses:
            count = status_counts.get(status, 0)
            funnel_data.append({
                'status': status,
                'count': count
            })
        
        # 计算转化率（以第一个状态为基准）
        base_count = funnel_data[0]['count'] if funnel_data[0]['count'] > 0 else 1
        for item in funnel_data:
            item['rate'] = round((item['count'] / base_count) * 100, 2)
        
        # 统计异常订单
        abnormal_data = {
            '已取消': status_counts.get('已取消', 0),
            '退款中的订单': status_counts.get('退款中的订单', 0)
        }
        
        # 汇总统计
        total_orders = len(df)
        valid_orders = sum(item['count'] for item in funnel_data)
        abnormal_orders = sum(abnormal_data.values())
        success_rate = round((funnel_data[-1]['count'] / base_count) * 100, 2) if base_count > 0 else 0
        
        # 计算效率指标
        # 获取各状态订单数
        wait_pay = funnel_data[0]['count']  # 等待买家付款
        paid = funnel_data[1]['count']      # 买家已付款
        wait_ship = funnel_data[2]['count'] # 待发货
        shipped = funnel_data[3]['count']   # 卖家已发货
        success = funnel_data[4]['count']   # 交易成功
        
        efficiency = {
            # 交易转化效率：从下单到成功
            'conversion_rate': round((success / wait_pay * 100) if wait_pay > 0 else 0, 2),
            # 支付效率：付款环节转化
            'payment_rate': round((paid / wait_pay * 100) if wait_pay > 0 else 0, 2),
            # 履约效率：从付款到发货
            'fulfillment_rate': round((shipped / paid * 100) if paid > 0 else 0, 2),
            # 交付完成率：从发货到成交
            'delivery_rate': round((success / shipped * 100) if shipped > 0 else 0, 2)
        }
        
        return jsonify({
            'success': True,
            'funnel_data': funnel_data,
            'abnormal_data': abnormal_data,
            'summary': {
                'total_orders': total_orders,
                'valid_orders': valid_orders,
                'abnormal_orders': abnormal_orders,
                'success_rate': success_rate
            },
            'efficiency': efficiency
        })
        
    except Exception as e:
        return jsonify({'error': f'处理失败: {str(e)}'}), 500


@app.route('/api/formulas')
def api_formulas():
    """API接口 - 返回所有公式数据"""
    return jsonify(FORMULAS)


@app.route('/api/category/<category_id>')
def api_category(category_id):
    """API接口 - 返回某一类别的公式数据"""
    if category_id not in FORMULAS:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(FORMULAS[category_id])


@app.errorhandler(404)
def page_not_found(e):
    """404错误页面"""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.4', port=5000)


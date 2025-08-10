# utils/config.py
"""
全天候策略配置文件
管理各种参数和阈值
"""

# 股票筛选参数
STOCK_SCREENING_CONFIG = {
    # 市值筛选
    "MIN_MARKET_CAP": 10e9,  # 最小市值：10亿美元
    
    # 财务稳定性筛选
    "MIN_ROE": 0,  # 最小ROE：0%
    "MIN_GROSS_MARGIN": 0,  # 最小毛利率：0%
    "MIN_FREE_CASHFLOW": 0,  # 最小自由现金流：0
    "MAX_DEBT_TO_EQUITY": 2,  # 最大负债率：200%
    "MIN_PE": 0,  # 最小PE：0
    "MAX_PE": 100,  # 最大PE：100
    "MIN_PB": 0,  # 最小PB：0
    "MAX_PB": 20,  # 最大PB：20
    
    # 动量计算
    "MOMENTUM_PERIOD": 180,  # 动量计算周期：180天
    "MIN_PRICE_DATA_DAYS": 30,  # 最小价格数据天数：30天
    
    # 因子计算
    "PE_NORMALIZATION": 20,  # PE标准化基准：20
    "PB_NORMALIZATION": 5,   # PB标准化基准：5
    "MOMENTUM_MIN": -0.5,    # 动量最小值：-50%
    "MOMENTUM_MAX": 1.0,     # 动量最大值：100%
    
    # 最终选择
    "TARGET_STOCK_COUNT": 40,  # 目标股票数量：40只
    "BATCH_SIZE": 20,  # 批量下载大小：20只
    "REQUEST_DELAY": 0.5,  # 请求延迟：0.5秒
}

# 宏观分析参数
MACRO_ANALYSIS_CONFIG = {
    "DATA_PERIOD": 90,  # 数据获取周期：90天
    "Z_SCORE_SCALE": 1.5,  # Z-score调整系数
    "MAX_ADJUSTMENT": 3,  # 最大调整幅度：3%
}

# 资产配置基准权重
BASELINE_WEIGHTS = {
    "equities": 30,      # 股票类资产
    "bonds_mid": 15,     # 中期债券
    "bonds_long": 40,    # 长期债券
    "gold": 7.5,         # 黄金资产
    "commodities": 7.5   # 大宗商品
}

# 数据源配置
DATA_SOURCES = {
    "FRED_API_KEY": "FRED_API_KEY",  # 需要在.env文件中设置
    "YAHOO_FINANCE": "yfinance",
    "SLICKCHARTS": "https://www.slickcharts.com"
}

# 文件路径配置
FILE_PATHS = {
    "EQUITY_LIST": "fundamental_analysis/equities/tickers/us_equity_top517.txt",
    "OUTPUT_DIR": "fundamental_analysis/equities/tickers",
    "REPORT_DIR": "reports"
}

# 日志配置
LOGGING_CONFIG = {
    "LOG_LEVEL": "INFO",
    "LOG_FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "LOG_FILE": "tiger_all_weather.log"
}

# 性能配置
PERFORMANCE_CONFIG = {
    "CACHE_TTL": 3600,  # 缓存时间：1小时
    "MAX_RETRIES": 3,   # 最大重试次数：3次
    "TIMEOUT": 30,      # 超时时间：30秒
}

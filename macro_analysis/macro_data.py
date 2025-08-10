# macro_analysis/macro_data.py

import pandas as pd
from fredapi import Fred
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# ✅ 加载本地 .env 文件中的 FRED API 密钥
load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

fred = Fred(api_key=FRED_API_KEY)

def fetch_macro_data():
    """
    使用 FRED API 获取过去3个月的关键宏观指标数据
    每个宏观指标都带注释说明其资产配置含义
    """

    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)

    # ✅ 宏观指标与其含义说明（扩展专业金融人士使用的指标）
    indicators = {
        # 通胀类
        "CPIAUCSL": "通胀 - CPI：用于判断通胀压力，通胀上升利好黄金、商品，利空债券",
        "PCEPI": "PCE价格指数：通胀的核心指标之一，常被美联储作为参考",
        "CPILFESL": "核心CPI：剔除食品和能源，更稳定的通胀衡量",
        "T5YIFR": "5Y5Y通胀预期：反映市场对未来通胀的长期预期",
        "PPIACO": "PPI总指数：生产者价格指数，领先于CPI反映上游压力",

        # 利率类
        "FEDFUNDS": "联邦基金利率：货币政策基准",
        "GS10": "10年期美债收益率：长期利率代表",
        "GS2": "2年期美债收益率：短端利率代表",

        # 增长/就业类
        "GDP": "GDP：整体经济增长水平，强增长利好股票",
        "PAYEMS": "非农就业总人数：衡量经济强弱，增长快则股票受益",
        "UNRATE": "失业率：经济衰退信号，失业率高 → 债券上涨、股票下跌",
        "INDPRO": "工业产出指数：反映产能与生产周期",
        "UMCSENT": "密歇根消费者信心指数：消费预期的领先指标",

        # 流动性/信用类
        "M2SL": "M2货币供应：衡量市场流动性，扩张意味着宽松 → 股市上涨",
        "TEDRATE": "TED利差：衡量金融市场风险偏好，升高代表信用紧张",
        "BAA10Y": "BAA公司债收益率：高收益信用利差指标",
        "AAA10Y": "AAA公司债收益率：高信用等级债券指标",

        # 风险情绪类
        "VIXCLS": "VIX恐慌指数：高VIX代表市场避险情绪浓厚，利空股票、利好债券"
    }

    macro_data = {}

    for fred_code, description in indicators.items():
        try:
            data = fred.get_series(fred_code, observation_start=start_date, observation_end=end_date)
            df = pd.DataFrame(data, columns=["value"])
            df.index.name = "date"
            df.name = fred_code
            macro_data[fred_code] = {
                "description": description,
                "data": df
            }
        except Exception as e:
            print(f"[Error] 获取 {fred_code} 失败：{e}")

    return macro_data


if __name__ == "__main__":
    macro_data = fetch_macro_data()

    print("✅ 最近宏观指标数据预览（带解释）")
    for code, content in macro_data.items():
        print(f"\n📊 {code} - {content['description']}")
        print(content["data"].tail(3))
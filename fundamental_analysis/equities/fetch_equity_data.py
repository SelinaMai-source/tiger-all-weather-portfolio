# ✅ fetch_equity_data.py ｜重写筛选逻辑：双重因子筛选 + 确保40只标的

import yfinance as yf
import pandas as pd
import os
import time
from datetime import datetime, timedelta
from tqdm import tqdm
import numpy as np

def is_financially_stable(row):
    """
    财务稳定性检查
    剔除财务数据有问题的/有风险的股票
    """
    # 检查ROE是否为正（允许None，因为有些公司可能没有ROE数据）
    if row["returnOnEquity"] is not None and row["returnOnEquity"] < 0:
        return False
    
    # 检查毛利率是否为正（允许None）
    if row["grossMargins"] is not None and row["grossMargins"] < 0:
        return False
    
    # 检查自由现金流是否为正（允许None）
    if row["freeCashflow"] is not None and row["freeCashflow"] < 0:
        return False
    
    # 检查负债率是否过高（>2）
    if row["debtToEquity"] is not None and row["debtToEquity"] > 2:
        return False
    
    # 检查PE是否合理（>0且<300，进一步放宽条件）
    if row["trailingPE"] is None or row["trailingPE"] <= 0 or row["trailingPE"] > 300:
        return False
    
    # 检查PB是否合理（>0且<100，进一步放宽条件）
    if row["priceToBook"] is None or row["priceToBook"] <= 0 or row["priceToBook"] > 100:
        return False
    
    return True

def calculate_value_score(row):
    """
    计算价值因子得分
    越低越好（价值型股票）
    """
    # 标准化PE和PB，然后加权平均
    pe_score = min(row["trailingPE"] / 20, 1.0)  # PE/20，最高1分
    pb_score = min(row["priceToBook"] / 5, 1.0)  # PB/5，最高1分
    
    # 价值得分 = (PE得分 + PB得分) / 2，越低越好
    return (pe_score + pb_score) / 2

def calculate_momentum_score(row):
    """
    计算动量因子得分
    越高越好（动量型股票）
    """
    momentum = row["momentum_6m"]
    if momentum is None:
        return 0
    
    # 将动量标准化到0-1之间
    # 使用更合理的动量范围：-30%到+60%
    normalized_momentum = (momentum + 0.3) / 0.9
    return max(0, min(1, normalized_momentum))

def screen_vm_candidates(ticker_file="fundamental_analysis/equities/tickers/us_equity_top517.txt") -> pd.DataFrame:
    """
    双重因子股票筛选：价值因子 + 动量因子
    目标：从517只股票中筛选出40只优质标的
    """
    print("🚀 开始双重因子股票筛选...")
    
    # 1. 读取股票列表
    with open(ticker_file, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]
    
    print(f"📊 原始股票池：{len(tickers)} 只")
    
    # 2. 第一轮筛选：获取基础财务数据
    print("🔍 第一轮筛选：获取财务数据...")
    results = []
    total = len(tickers)
    
    # 添加调试统计
    market_cap_filtered = 0
    financial_filtered = 0
    
    for i, ticker in enumerate(tqdm(tickers, desc="获取财务数据")):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            row = {
                "ticker": ticker,
                "marketCap": info.get("marketCap"),
                "priceToBook": info.get("priceToBook"),
                "trailingPE": info.get("trailingPE"),
                "returnOnEquity": info.get("returnOnEquity"),
                "grossMargins": info.get("grossMargins"),
                "freeCashflow": info.get("freeCashflow"),
                "debtToEquity": info.get("debtToEquity"),
                "currentPrice": info.get("currentPrice"),
                "volume": info.get("volume")
            }
            
            # 市值筛选：剔除市值小于5亿的（放宽条件）
            if row["marketCap"] is not None and row["marketCap"] >= 5e9:  # 5亿
                market_cap_filtered += 1
                # 财务稳定性筛选
                if is_financially_stable(row):
                    financial_filtered += 1
                    results.append(row)
            
        except Exception as e:
            if i % 50 == 0:  # 减少日志输出频率
                print(f"⚠️ {ticker} 获取失败：{str(e)[:50]}...")
        
        # 控制请求频率
        if i % 10 == 0:
            time.sleep(0.5)
    
    print(f"📊 筛选统计：")
    print(f"   市值筛选通过：{market_cap_filtered} 只")
    print(f"   财务筛选通过：{financial_filtered} 只")
    
    print(f"✅ 第一轮筛选后：{len(results)} 只股票")
    
    if len(results) == 0:
        print("❌ 没有符合条件的股票，请检查数据源")
        return pd.DataFrame()
    
    # 3. 转换为DataFrame并计算价值因子
    df = pd.DataFrame(results)
    df["value_score"] = df.apply(calculate_value_score, axis=1)
    
    # 4. 第二轮筛选：获取历史价格计算动量
    print("📈 第二轮筛选：计算动量因子...")
    start_date = datetime.today() - timedelta(days=180)
    end_date = datetime.today()
    tickers_for_price = df["ticker"].tolist()
    
    price_dict = {}
    batch_size = 20  # 减小批次大小，避免超时
    
    for i in tqdm(range(0, len(tickers_for_price), batch_size), desc="下载历史价格"):
        batch = tickers_for_price[i:i+batch_size]
        try:
            batch_price = yf.download(batch, start=start_date, end=end_date, 
                                    group_by="ticker", threads=False, progress=False)
            
            for symbol in batch:
                if symbol in batch_price.columns.get_level_values(0):
                    # 尝试获取Adj Close，如果不存在则使用Close
                    if "Adj Close" in batch_price[symbol].columns:
                        price_dict[symbol] = batch_price[symbol]["Adj Close"]
                    elif "Close" in batch_price[symbol].columns:
                        price_dict[symbol] = batch_price[symbol]["Close"]
                    else:
                        print(f"⚠️ {symbol} 没有价格数据")
                    
        except Exception as e:
            print(f"❌ 批次下载失败: {str(e)[:50]}...")
        
        time.sleep(1)  # 增加延迟
    
    # 5. 计算动量因子
    momentums = {}
    for ticker in tickers_for_price:
        try:
            series = price_dict.get(ticker)
            if series is not None and len(series) >= 30:  # 至少需要30天数据
                # 计算6个月动量
                momentum = (series.iloc[-1] - series.iloc[0]) / series.iloc[0]
                momentums[ticker] = momentum
            else:
                momentums[ticker] = None
        except:
            momentums[ticker] = None
    
    df["momentum_6m"] = df["ticker"].map(momentums)
    df["momentum_score"] = df.apply(calculate_momentum_score, axis=1)
    
    # 剔除动量数据缺失的股票
    df = df[df["momentum_6m"].notna()]
    print(f"✅ 动量计算后：{len(df)} 只股票")
    
    # 6. 双重因子排名
    print("🎯 双重因子排名...")
    
    # 价值因子排名（越低越好）
    df["value_rank"] = df["value_score"].rank(ascending=True)
    
    # 动量因子排名（越高越好）
    df["momentum_rank"] = df["momentum_score"].rank(ascending=False)
    
    # 综合排名 = 价值排名 + 动量排名（越小越好）
    df["combined_rank"] = df["value_rank"] + df["momentum_rank"]
    
    # 按综合排名排序
    df_ranked = df.sort_values("combined_rank").reset_index(drop=True)
    
    # 7. 选择前40只股票（如果不足40只，则选择所有可用的股票）
    target_count = min(40, len(df_ranked))
    final_df = df_ranked.head(target_count).copy()
    
    # 添加来源标记
    final_df["来源"] = "双重因子筛选"
    
    # 8. 保存结果
    os.makedirs("tickers", exist_ok=True)
    final_df.to_csv("tickers/equities_list_labeled.csv", index=False)
    final_df[["ticker"]].to_csv("tickers/equities_list.txt", index=False, header=False)
    
    print(f"✅ 最终筛选结果：{len(final_df)} 只股票")
    print(f"📊 价值因子范围：{final_df['value_score'].min():.3f} - {final_df['value_score'].max():.3f}")
    print(f"📈 动量因子范围：{final_df['momentum_6m'].min():.1%} - {final_df['momentum_6m'].max():.1%}")
    
    return final_df

def analyze_selected_stocks(df):
    """
    分析选中的股票
    """
    if df.empty:
        print("❌ 没有选中的股票")
        return
    
    print("\n" + "="*80)
    print("📊 选中股票分析报告")
    print("="*80)
    
    # 基础统计
    print(f"📈 股票数量：{len(df)} 只")
    print(f"💰 平均市值：${df['marketCap'].mean()/1e9:.1f}B")
    print(f"📊 平均PE：{df['trailingPE'].mean():.1f}")
    print(f"📊 平均PB：{df['priceToBook'].mean():.2f}")
    print(f"📈 平均动量：{df['momentum_6m'].mean():.1%}")
    
    # 行业分布（简化版）
    print(f"\n🏭 市值分布：")
    large_cap = len(df[df['marketCap'] >= 100e9])
    mid_cap = len(df[(df['marketCap'] >= 10e9) & (df['marketCap'] < 100e9)])
    print(f"   大盘股（>100B）：{large_cap} 只")
    print(f"   中盘股（10B-100B）：{mid_cap} 只")
    
    # 显示前10只股票
    print(f"\n🏆 前10只股票：")
    print("-" * 100)
    print(f"{'代码':<8} {'市值(B)':<10} {'PE':<8} {'PB':<8} {'动量':<8} {'价值得分':<10} {'动量得分':<10}")
    print("-" * 100)
    
    for _, row in df.head(10).iterrows():
        market_cap_b = row['marketCap'] / 1e9
        print(f"{row['ticker']:<8} {market_cap_b:<10.1f} {row['trailingPE']:<8.1f} "
              f"{row['priceToBook']:<8.2f} {row['momentum_6m']:<8.1%} "
              f"{row['value_score']:<10.3f} {row['momentum_score']:<10.3f}")
    
    print("="*80)

if __name__ == "__main__":
    # 运行股票筛选
    final_df = screen_vm_candidates()
    
    # 分析结果
    if not final_df.empty:
        analyze_selected_stocks(final_df)
        
        # 保存详细报告
        report_file = f"tickers/stock_screening_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        final_df.to_csv(report_file, index=False)
        print(f"📄 详细报告已保存：{report_file}")
    else:
        print("❌ 股票筛选失败")
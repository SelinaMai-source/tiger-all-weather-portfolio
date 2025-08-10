# fundamental_analysis/equities/equity_list.py (反403版本)

import pandas as pd
import requests
import os
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


def fetch_from_slickcharts(url, label):
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("table")
        df = pd.read_html(str(table))[0]
        df = df[["Symbol"]].rename(columns={"Symbol": "ticker"})
        df["source"] = label
        print(f"✅ 成功抓取 {label}：{len(df)} 支")
        return df
    except Exception as e:
        print(f"❌ 抓取 {label} 失败：{e}")
        return pd.DataFrame(columns=["ticker"])


def combine_slickcharts_lists():
    urls = [
        ("https://www.slickcharts.com/sp500", "S&P500"),
        ("https://www.slickcharts.com/sp1000", "S&P1000"),
        ("https://www.slickcharts.com/nasdaq100", "Nasdaq100"),
        ("https://www.slickcharts.com/russell1000", "Russell1000")
    ]

    frames = [fetch_from_slickcharts(url, label) for url, label in urls]
    combined = pd.concat(frames).drop_duplicates(subset="ticker").reset_index(drop=True)

    tickers_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tickers"
    )
    os.makedirs(tickers_path, exist_ok=True)
    save_path = os.path.join(tickers_path, "us_equity_top3000.txt")

    combined[["ticker"]].to_csv(save_path, index=False, header=False)
    print(f"📦 最终保存 {len(combined)} 支股票到 {save_path}")


if __name__ == "__main__":
    combine_slickcharts_lists()
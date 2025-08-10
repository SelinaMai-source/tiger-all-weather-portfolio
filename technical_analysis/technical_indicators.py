# technical_indicators.py
"""
技术指标计算模块
包含常用的技术指标计算函数
"""

import pandas as pd
import numpy as np
from typing import Union, Optional
import warnings
warnings.filterwarnings('ignore')

def calculate_sma(data: pd.Series, window: int) -> pd.Series:
    """
    计算简单移动平均线 (Simple Moving Average)
    
    Args:
        data: 价格数据
        window: 移动平均窗口
    
    Returns:
        移动平均线
    """
    return data.rolling(window=window).mean()

def calculate_ema(data: pd.Series, window: int) -> pd.Series:
    """
    计算指数移动平均线 (Exponential Moving Average)
    
    Args:
        data: 价格数据
        window: 移动平均窗口
    
    Returns:
        指数移动平均线
    """
    return data.ewm(span=window).mean()

def calculate_rsi(data: pd.Series, window: int = 14) -> pd.Series:
    """
    计算相对强弱指数 (Relative Strength Index)
    
    Args:
        data: 价格数据
        window: RSI窗口，默认14
    
    Returns:
        RSI值
    """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
    """
    计算MACD指标
    
    Args:
        data: 价格数据
        fast: 快线周期，默认12
        slow: 慢线周期，默认26
        signal: 信号线周期，默认9
    
    Returns:
        (MACD线, 信号线, 柱状图)
    """
    ema_fast = calculate_ema(data, fast)
    ema_slow = calculate_ema(data, slow)
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(data: pd.Series, window: int = 20, std_dev: float = 2) -> tuple:
    """
    计算布林带
    
    Args:
        data: 价格数据
        window: 移动平均窗口，默认20
        std_dev: 标准差倍数，默认2
    
    Returns:
        (上轨, 中轨, 下轨)
    """
    sma = calculate_sma(data, window)
    std = data.rolling(window=window).std()
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    return upper_band, sma, lower_band

def calculate_stochastic(high: pd.Series, low: pd.Series, close: pd.Series, 
                        k_window: int = 14, d_window: int = 3) -> tuple:
    """
    计算随机指标
    
    Args:
        high: 最高价
        low: 最低价
        close: 收盘价
        k_window: %K窗口，默认14
        d_window: %D窗口，默认3
    
    Returns:
        (%K, %D)
    """
    lowest_low = low.rolling(window=k_window).min()
    highest_high = high.rolling(window=k_window).max()
    k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d_percent = calculate_sma(k_percent, d_window)
    return k_percent, d_percent

def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.Series:
    """
    计算平均真实波幅 (Average True Range)
    
    Args:
        high: 最高价
        low: 最低价
        close: 收盘价
        window: ATR窗口，默认14
    
    Returns:
        ATR值
    """
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = calculate_ema(tr, window)
    return atr

def calculate_volume_sma(volume: pd.Series, window: int = 20) -> pd.Series:
    """
    计算成交量移动平均
    
    Args:
        volume: 成交量数据
        window: 移动平均窗口，默认20
    
    Returns:
        成交量移动平均
    """
    return calculate_sma(volume, window)

def calculate_price_momentum(data: pd.Series, period: int = 10) -> pd.Series:
    """
    计算价格动量
    
    Args:
        data: 价格数据
        period: 动量周期，默认10
    
    Returns:
        动量值
    """
    return data / data.shift(period) - 1

def calculate_volatility(data: pd.Series, window: int = 20) -> pd.Series:
    """
    计算波动率
    
    Args:
        data: 价格数据
        window: 波动率窗口，默认20
    
    Returns:
        波动率
    """
    returns = data.pct_change()
    volatility = returns.rolling(window=window).std() * np.sqrt(252)  # 年化波动率
    return volatility

def calculate_support_resistance(data: pd.Series, window: int = 20) -> tuple:
    """
    计算支撑位和阻力位
    
    Args:
        data: 价格数据
        window: 窗口大小，默认20
    
    Returns:
        (支撑位, 阻力位)
    """
    support = data.rolling(window=window).min()
    resistance = data.rolling(window=window).max()
    return support, resistance

def calculate_fibonacci_retracements(high: float, low: float) -> dict:
    """
    计算斐波那契回撤位
    
    Args:
        high: 最高价
        low: 最低价
    
    Returns:
        斐波那契回撤位字典
    """
    diff = high - low
    levels = {
        '0.0': low,
        '0.236': low + 0.236 * diff,
        '0.382': low + 0.382 * diff,
        '0.5': low + 0.5 * diff,
        '0.618': low + 0.618 * diff,
        '0.786': low + 0.786 * diff,
        '1.0': high
    }
    return levels

def calculate_ichimoku(high: pd.Series, low: pd.Series, close: pd.Series) -> dict:
    """
    计算一目均衡表指标
    
    Args:
        high: 最高价
        low: 最低价
        close: 收盘价
    
    Returns:
        一目均衡表指标字典
    """
    # 转换线 (Conversion Line)
    period9_high = high.rolling(window=9).max()
    period9_low = low.rolling(window=9).min()
    conversion = (period9_high + period9_low) / 2
    
    # 基准线 (Base Line)
    period26_high = high.rolling(window=26).max()
    period26_low = low.rolling(window=26).min()
    base = (period26_high + period26_low) / 2
    
    # 先行带A (Leading Span A)
    leading_span_a = ((conversion + base) / 2).shift(26)
    
    # 先行带B (Leading Span B)
    period52_high = high.rolling(window=52).max()
    period52_low = low.rolling(window=52).min()
    leading_span_b = ((period52_high + period52_low) / 2).shift(26)
    
    # 滞后线 (Lagging Span)
    lagging_span = close.shift(-26)
    
    return {
        'conversion': conversion,
        'base': base,
        'leading_span_a': leading_span_a,
        'leading_span_b': leading_span_b,
        'lagging_span': lagging_span
    }

def calculate_adx(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> tuple:
    """
    计算平均方向指数 (Average Directional Index)
    
    Args:
        high: 最高价
        low: 最低价
        close: 收盘价
        window: ADX窗口，默认14
    
    Returns:
        (ADX, +DI, -DI)
    """
    # 计算方向移动
    up_move = high - high.shift(1)
    down_move = low.shift(1) - low
    
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
    
    # 计算真实波幅
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # 计算平滑值
    tr_smooth = calculate_ema(tr, window)
    plus_dm_smooth = calculate_ema(pd.Series(plus_dm, index=high.index), window)
    minus_dm_smooth = calculate_ema(pd.Series(minus_dm, index=high.index), window)
    
    # 计算方向指标
    plus_di = 100 * (plus_dm_smooth / tr_smooth)
    minus_di = 100 * (minus_dm_smooth / tr_smooth)
    
    # 计算ADX
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = calculate_ema(dx, window)
    
    return adx, plus_di, minus_di

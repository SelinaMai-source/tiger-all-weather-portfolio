# macro_analysis/allocation_adjust.py

import numpy as np
from scipy.stats import zscore
from macro_data import fetch_macro_data

# Ray Dalio baseline weights
BASELINE_WEIGHTS = {
    "equities": 30,      # 股票类资产
    "bonds_mid": 15,     # 中期债券，如2-5年国债或信用债
    "bonds_long": 40,    # 长期债券，如10年及以上国债
    "gold": 7.5,         # 黄金资产
    "commodities": 7.5   # 大宗商品（如原油、铜等）
}

# 定义每类资产的先验（均值，标准差）
PRIOR_DISTRIBUTIONS = {
    "equities": (30, 5),
    "bonds_mid": (15, 3),
    "bonds_long": (40, 5),
    "gold": (7.5, 2),
    "commodities": (7.5, 2)
}

# Z-score转权重调整（限制在±3%内）
def z_to_adjustment(z, scale=1.5, max_adjust=3):
    score = z * scale
    return max(-max_adjust, min(max_adjust, score))

# 计算z-score并应用调整逻辑
def infer_observed_means(macro_data):
    observed = BASELINE_WEIGHTS.copy()

    def calc_z(df):
        series = df["data"]["value"]
        return ((series - series.mean()) / series.std()).iloc[-1]

    # 🟡 CPI总通胀指标，高通胀 → 增加黄金/商品，减少长期债
    if "CPIAUCSL" in macro_data:
        z = calc_z(macro_data["CPIAUCSL"])
        delta = z_to_adjustment(z)
        observed["gold"] += delta
        observed["commodities"] += delta
        observed["bonds_long"] -= delta

    # 🟡 PCE核心通胀，反映价格上升粘性，偏保守地增加黄金
    if "PCEPI" in macro_data:
        z = calc_z(macro_data["PCEPI"])
        delta = z_to_adjustment(z)
        observed["gold"] += delta * 0.7

    # 🟡 核心CPI：剔除波动项的价格指标，适度加黄金
    if "CPILFESL" in macro_data:
        z = calc_z(macro_data["CPILFESL"])
        delta = z_to_adjustment(z)
        observed["gold"] += delta * 0.5

    # 🔵 GS10：10年国债利率上升 → 减配长期债
    if "GS10" in macro_data:
        z = calc_z(macro_data["GS10"])
        delta = z_to_adjustment(z)
        observed["bonds_long"] -= delta

    # 🔵 GS2：2年短债利率上升 → 增配中期债
    if "GS2" in macro_data:
        z = calc_z(macro_data["GS2"])
        delta = z_to_adjustment(z)
        observed["bonds_mid"] += delta

    # 🔵 联邦基金利率：代表政策利率，升高时增配短债
    if "FEDFUNDS" in macro_data:
        z = calc_z(macro_data["FEDFUNDS"])
        delta = z_to_adjustment(z)
        observed["bonds_mid"] += delta

    # 🟢 GDP增长强 → 增股减债；衰退 → 减股加债
    if "GDP" in macro_data:
        z = calc_z(macro_data["GDP"])
        delta = z_to_adjustment(z)
        observed["equities"] += delta
        observed["bonds_long"] -= delta * 0.5

    # 🟢 PAYEMS：非农就业人数增长 → 增股
    if "PAYEMS" in macro_data:
        z = calc_z(macro_data["PAYEMS"])
        delta = z_to_adjustment(z)
        observed["equities"] += delta

    # 🟢 UNRATE：失业率升高 → 减股加债
    if "UNRATE" in macro_data:
        z = calc_z(macro_data["UNRATE"])
        delta = z_to_adjustment(z)
        observed["equities"] -= delta
        observed["bonds_long"] += delta

    # 🟢 INDPRO：工业产出改善 → 增股
    if "INDPRO" in macro_data:
        z = calc_z(macro_data["INDPRO"])
        delta = z_to_adjustment(z)
        observed["equities"] += delta

    # 🔴 UMCSENT：消费者信心上升 → 增配股票
    if "UMCSENT" in macro_data:
        z = calc_z(macro_data["UMCSENT"])
        delta = z_to_adjustment(z)
        observed["equities"] += delta

    # 🔴 M2货币扩张 → 股/商品受益；紧缩 → 减仓
    if "M2SL" in macro_data:
        z = calc_z(macro_data["M2SL"])
        delta = z_to_adjustment(z)
        observed["equities"] += delta
        observed["commodities"] += delta

    # 🔴 VIX上升 → 恐慌情绪 ↑，减股加债避险
    if "VIXCLS" in macro_data:
        z = calc_z(macro_data["VIXCLS"])
        delta = z_to_adjustment(z)
        observed["equities"] -= delta
        observed["bonds_mid"] += delta

    return observed

# 贝叶斯更新函数
def bayesian_update(prior_mu, prior_sigma, obs_mu, obs_sigma):
    post_mean = (prior_mu / prior_sigma**2 + obs_mu / obs_sigma**2) / (1 / prior_sigma**2 + 1 / obs_sigma**2)
    post_std = np.sqrt(1 / (1 / prior_sigma**2 + 1 / obs_sigma**2))
    return round(post_mean, 2), round(post_std, 2)

def adjust_allocation(macro_data):
    obs_means = infer_observed_means(macro_data)
    OBS_SIGMA = 3

    updated_weights = {}
    for asset in BASELINE_WEIGHTS:
        mu_prior, sigma_prior = PRIOR_DISTRIBUTIONS[asset]
        mu_obs = obs_means[asset]
        mu_post, sigma_post = bayesian_update(mu_prior, sigma_prior, mu_obs, OBS_SIGMA)
        updated_weights[asset] = mu_post

    total = sum(updated_weights.values())
    for asset in updated_weights:
        updated_weights[asset] = round(updated_weights[asset] * 100 / total, 2)

    return updated_weights

if __name__ == "__main__":
    macro_data = fetch_macro_data()
    weights = adjust_allocation(macro_data)
    print("\n📊 本季度贝叶斯 + Z-score 调整后的资产配置建议：")
    for asset, weight in weights.items():
        print(f"{asset}: {weight}%")
import pandas as pd
import numpy as np
import datetime as dt

# 讀取檔案
og_rfm_master = pd.read_csv("RFM_Master.csv")
# 拷貝
df_master = og_rfm_master.copy()

# print(df_master.info())
# 更改格式
df_master["reg_ts_datetime"] = pd.to_datetime(df_master["reg_ts_datetime"])
df_master["last_login"] = pd.to_datetime(df_master["last_login"])

# print(df_master.info())

# 3. 設定分析基準日 (Analysis Date)
# 「資料裡的最後一天」+1
analysis_date = df_master["last_login"].max(
)+dt.timedelta(days=1)
print(f"{analysis_date}是分析基準日")

# Recency計算
df_master['Recency'] = (analysis_date-df_master["last_login"]).dt.days

# Frequency(活躍天數) = active_days
# Monetary(消費金額) = revenue
# 都有了，重新命名
df_master = df_master.rename(
    columns={'active_days': 'Frequency', 'revenue': 'Monetary'})
# print(df_master.head())

# 建立新的df，只保留 uid+ RFM
df_rfm = df_master[["uid", "Recency", "Frequency", "Monetary"]].copy()
# print(df_rfm)
# print(df_rfm.describe())

# 計算F


def get_f_score(x):
    if x <= 1:
        return 1
    elif x <= 5:
        return 2
    elif x <= 15:
        return 3
    else:
        return 4

# M_score
# 無課玩家佔超過75%，確認去除無課玩家以後的中位數
# df_rfm[df_rfm['Monetary'] > 0]['Monetary'].quantile([0.5, 0.8, 0.9, 0.99])


def get_m_score(x):
    if x == 0:
        return 1      # 沒花錢免費仔
    elif x <= 2000:
        return 2  # 上面算出的中位數
    elif x <= 3700:
        return 3  # 上面算出的前 10% 門檻
    else:
        return 4      # top0.01，頂級 vip


# 計算 r_score 並轉換為數字
df_rfm["r_score"] = pd.qcut(df_rfm["Recency"], q=4, labels=[
                            4, 3, 2, 1]).astype(int)

# f_score 和 m_score 已經是 int，保持不變
df_rfm["f_score"] = df_rfm["Frequency"].apply(get_f_score)
df_rfm["m_score"] = df_rfm["Monetary"].apply(get_m_score)

# 計算RFM加總
df_rfm['rfm_segment'] = df_rfm['r_score'].astype(
    str) + df_rfm['f_score'].astype(str) + df_rfm['m_score'].astype(str)
df_rfm['rfm_sum'] = df_rfm['r_score'] + df_rfm['f_score'] + df_rfm['m_score']

print(df_rfm.head())

# 存檔
df_rfm.to_csv("RFM_Final_Scored.csv", index=False)
print("檔案已儲存：RFM_Final_Scored.csv")

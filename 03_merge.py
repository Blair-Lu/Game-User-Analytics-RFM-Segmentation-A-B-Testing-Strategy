import numpy as np
import pandas as pd

df_reg = pd.read_csv("cleaned_reg_data.csv")
df_auth = pd.read_csv("cleaned_auth_summary.csv")
# print(df_reg.head(10))
# print(df_auth.head(10))

df_master = pd.merge(df_reg, df_auth, on="uid", how='left')
# print(df_master.head(10))
# print(df_master.columns)


# 處理幽靈人口 定義：「註冊後一次都沒登入」的人
# 沒登入過的人，活躍天數就是 0，不是空值。
values_to_fill = {
    'active_days': 0,
    'total_logins': 0
}
df_master = df_master.fillna(value=values_to_fill)


df_master["reg_ts_datetime"] = pd.to_datetime(df_master["reg_ts_datetime"])
df_master["last_login"] = pd.to_datetime(df_master["last_login"])

# print(df_master.info())


# 載入 clean_ab_test
df_revenue = pd.read_csv("cleaned_ab_test.csv")
# 合併進 Master Table
# 只需要 'uid' 和 'revenue' 這兩欄
df_master = pd.merge(
    df_master, df_revenue[['uid', 'revenue']], on="uid", how='left')
# 查找是否有NaN
# print(df_master.isna().sum())
df_master["revenue"] = df_master["revenue"].fillna(0)
# print(df_master.isna().sum())


# 存檔
df_master.to_csv("RFM_Master.csv", index=False)
print("Master Table 建置完成")

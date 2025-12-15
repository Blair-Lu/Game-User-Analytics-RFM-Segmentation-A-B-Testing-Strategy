import numpy as np
import pandas as pd

# ETL reg_data.csv檔案
# og_reg_df = pd.read_csv("reg_data.csv", sep=';')
# print(og_reg_df)

# reg_df = og_reg_df.copy()
# reg_df.info()
# # 缺失值
# print("缺失值檢查")
# print(reg_df.isnull().sum())

# print("\n" + "-"*20 + "\n")

# # 重複數據
# print("重複值檢查")
# print(reg_df.duplicated().sum())

# print("\n" + "-"*20 + "\n")

# # reg_ts 更改格式
# reg_df['reg_ts_datetime'] = pd.to_datetime(reg_df['reg_ts'], unit='s')
# print(reg_df['reg_ts_datetime'].head(10))

# # 存檔
# reg_df.to_csv("cleaned_reg_data.csv", index=False)

# ETL auth_data.csv檔案
og_auth_df = pd.read_csv("auth_data.csv", sep=";")
# print(og_auth_df.head(10))

auth_df = og_auth_df.copy()
auth_df.info()

# 缺失值
print("缺失值檢查")
print(auth_df.isnull().sum())

# 重複值
print("重複值檢查")
print(auth_df.duplicated().sum())

# 更改auth_ts 格式
auth_df["auth_ts_datetime"] = pd.to_datetime(
    auth_df["auth_ts"], unit='s')
# print(og_auth_df["auth_ts_datetime"].head(10))
auth_df['date'] = auth_df['auth_ts_datetime'].dt.date
# print(auth_df.head(10))

# 存檔
auth_df.to_csv("cleaned_auth_data.csv", index=False)

# 聚合
auth_summary = auth_df.groupby("uid").agg({
    'auth_ts_datetime': 'max',
    'date': 'nunique',
    'uid': 'count'
})

auth_summary.columns = ['last_login', 'active_days', 'total_logins']
auth_summary = auth_summary.reset_index()

print(auth_summary.head(10))

# 存檔
auth_summary.to_csv('cleaned_auth_summary.csv', index=False)

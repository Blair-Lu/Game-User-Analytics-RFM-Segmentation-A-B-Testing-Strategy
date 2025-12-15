import pandas as pd

og_ab_test = pd.read_csv("ab_test.csv", sep=';')
# print(og_ab_test.head(10))

df_revenue = og_ab_test.copy()
print(df_revenue.head(10))
# user_id 應該要對應主表 uid
df_revenue = df_revenue.rename(columns={'user_id': 'uid'})
print(df_revenue.info())

# 存檔
df_revenue.to_csv("cleaned_ab_test.csv", index=False)
print("ab_test存檔完畢")

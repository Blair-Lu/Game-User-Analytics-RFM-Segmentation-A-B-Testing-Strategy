import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 設定繪圖風格與中文字型
sns.set_style("whitegrid")
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 1. 讀取數據並合併
# ==========================================
print("🚀 正在合併 A/B Test 資料...")

# 讀取我們算好的 RFM 表
og_df_rfm = pd.read_csv("RFM_Final_Scored_segment_names.csv")

df_rfm = og_df_rfm.copy()
# 讀取原始的 A/B Test 表 (為了拿 testgroup 欄位)
og_df_ab = pd.read_csv("ab_test.csv", sep=';')
df_ab = og_df_ab.copy()
# 改名以便合併
df_ab = df_ab.rename(columns={'user_id': 'uid'})

# 分數修改字串
df_rfm['r_score'] = df_rfm['r_score'].astype(str)
df_rfm['f_score'] = df_rfm['f_score'].astype(str)
df_rfm['m_score'] = df_rfm['m_score'].astype(str)


# 合併！把 testgroup 加進去 RFM 表
df_merged = pd.merge(df_rfm, df_ab[['uid', 'testgroup']], on='uid', how='left')
# print(df_merged)

# 發現有些用戶未參與ab_test，需要drop掉
df_final = df_merged.dropna(subset=['testgroup']).copy()

print(df_final)
print(df_final['testgroup'].value_counts())

print(f"原本總人數: {len(df_merged)}")
print(f"刪除後的人數: {len(df_final)}")
print(f"刪除人數: {len(df_merged)-len(df_final)}")


# ==========================================
# 2. 挖掘真相：哪一組的鯨魚比較多？
# ==========================================
print("📊 正在分析 A/B 組差異...")

# 過濾出我們最在意的「頂級王者」和「流失鯨魚」
target_segments = ['頂級王者 (Champions)', '流失的鯨魚 (Hibernating Whales)']
df_targets = df_final[df_final['Segment_Name'].isin(target_segments)]

# 畫圖：A/B 組在這些關鍵族群的人數對比
plt.figure(figsize=(10, 6))

ax = sns.countplot(
    data=df_targets,
    x='Segment_Name',
    hue='testgroup',  # 這就是重點！分組比較
    palette='Set2'
)

plt.title('A/B 測試結果：關鍵族群分佈 (A vs B)', fontsize=16, fontweight='bold')
plt.xlabel('關鍵族群 (Key Segments)', fontsize=12)
plt.ylabel('人數 (Count)', fontsize=12)

# 標上數字
for container in ax.containers:
    ax.bar_label(container)

plt.tight_layout()
plt.savefig("AB_Test_Comparison.png", dpi=300)
plt.show()

# ==========================================
# 3. 終極數據：兩組的總營收 PK
# ==========================================
print("\n=== 💰 A/B 組營收大對決 ===")
revenue_compare = df_final.groupby('testgroup')['Monetary'].sum()
print(revenue_compare)

# 算出人均營收 (ARPU)
user_count = df_final['testgroup'].value_counts()
arpu = revenue_compare / user_count
print("\n=== 🧑‍🤝‍🧑 人均貢獻 (ARPU) ===")
print(arpu)

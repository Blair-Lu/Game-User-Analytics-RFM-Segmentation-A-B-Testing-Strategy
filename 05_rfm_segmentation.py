import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 設定畫圖風格與中文字型
sns.set_style("whitegrid")
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 讀取
og_df = pd.read_csv("RFM_Final_Scored.csv")

df = og_df.copy()

# 分數修改字串
df['r_score'] = df['r_score'].astype(str)
df['f_score'] = df['f_score'].astype(str)
df['m_score'] = df['m_score'].astype(str)

# 定義標籤規則 (The Mapping Rules)


def map_segment_names(row):
    r, f, m = row['r_score'], row['f_score'], row['m_score']
    rfm = row['rfm_segment']  # 這是字串 "444"

    # --- 第一層：頂級與流失 (最極端的) ---
    if rfm == '444':
        return '頂級王者 (Champions)'

    elif r == '1' and m == '4':
        return '流失的鯨魚 (Hibernating Whales)'  # 以前花大錢，現在不來了

    elif r == '1' and m == '1':
        return '已流失 (Lost)'  # 沒花錢又很久沒來

    # --- 第二層：活躍用戶 (R分數高) ---
    elif r in ['3', '4'] and f == '1':
        return '潛力新手 (New Users)'  # 剛來，只玩一次

    elif r in ['3', '4'] and m in ['3', '4']:
        return '忠誠大戶 (Loyalists)'  # 常來且花不少錢

    elif r in ['3', '4'] and f in ['3', '4']:
        return '活躍鐵粉 (Active Loyal)'  # 常來玩 (可能沒花大錢)

    # --- 第三層：風險用戶 (R分數低/中) ---
    elif r == '2':
        return '快睡著了 (About to Sleep)'

    else:
        return '一般大眾 (Others)'


# 應用規則
df['Segment_Name'] = df.apply(map_segment_names, axis=1)
print(df.head(10))
print(df.columns.tolist())
# 存檔
df.to_csv("RFM_Final_Scored_segment_names.csv", index=False)
print("檔案已儲存：RFM_Final_Scored_segment_names.csv")


# print("標籤貼好了！預覽前 10 筆")
# print(df[['uid', 'rfm_segment', 'Segment_Name', 'Monetary']].head(10))

# 統計一下各族群人數
# print("各族群人數統計")
# print(df['Segment_Name'].value_counts())


# 畫圖
# plt.figure(figsize=(12, 6))
# # 統計人數並排序
# segment_counts = df['Segment_Name'].value_counts()
# 長條圖
# ax = sns.barplot(y=segment_counts.index,
#                  x=segment_counts.values, palette="pastel")
# for i, v in enumerate(segment_counts.values):
#     ax.text(v + 2000, i, f'{v:,}', color='black',
#             va='center', fontweight='bold')

# plt.title('RFM 玩家族群分佈 (User Segmentation)', fontsize=16)
# plt.xlabel('人數 (Count)', fontsize=12)
# plt.ylabel('族群名稱 (Segment)', fontsize=12)

# plt.tight_layout()
# # 存檔
# plt.savefig("RFM_Segmentation_Chart.png", dpi=300)
# print("💾 圖表已存檔：RFM_Segmentation_Chart.png")

# plt.show()


# # ==========================================
# # 4. 顯示重要數據摘要
# # ==========================================
# print("\n=== 📊 重點數據摘要 ===")
# print(f"1. 頂級王者人數: {len(df[df['Segment_Name'] == '頂級王者 (Champions)'])}")
# print(
#     f"2. 流失的鯨魚人數: {len(df[df['Segment_Name'] == '流失的鯨魚 (Hibernating Whales)'])}")
# print(f"3. 潛力新手人數: {len(df[df['Segment_Name'] == '潛力新手 (New Users)'])}")


# 圖表 2：含金量分析 (各族群總營收)

# 算出每個族群「總共」花了多少錢
# segment_revenue = df.groupby('Segment_Name')[
#     'Monetary'].sum().sort_values(ascending=False)

# # 畫圖
# ax_revenue = sns.barplot(y=segment_revenue.index,
#                          x=segment_revenue.values, palette="pastel")

# # 標上金額 (加上 $ 和逗號)
# for i, v in enumerate(segment_revenue.values):
#     ax_revenue.text(v, i, f' ${v/10000:,.0f} 萬',
#                     color='black', va='center', fontweight='bold')

# plt.title('各族群營收貢獻 (Total Revenue by Segment)', fontsize=18, fontweight='bold')
# plt.xlabel('總營收金額 (Total Monetary)', fontsize=14)
# plt.ylabel('', fontsize=14)

# plt.tight_layout()
# plt.savefig("RFM_Revenue_Chart.png", dpi=300)
# print("💾 營收圖已存檔：RFM_Revenue_Chart.png")
# plt.show()


# plt.figure(figsize=(10, 8))

# # 因為數據點太多 (100萬)，畫散佈圖會變成一團黑
# # 我們隨機抽樣 5000 點來代表就好，不然電腦會跑不動且圖很醜
# df_sample = df.sample(n=5000, random_state=42)

# sns.scatterplot(
#     data=df_sample,
#     x='Recency',
#     y='Frequency',
#     hue='Segment_Name',  # 不同族群不同顏色
#     size='Monetary',    # 錢花越多的點越大
#     sizes=(20, 200),
#     alpha=0.6,          # 透明度
#     palette='deep'
# )

# plt.title('用戶分佈矩陣 (Recency vs Frequency)', fontsize=16)
# plt.xlabel('R: 幾天沒來 (Recency)', fontsize=12)
# plt.ylabel('F: 活躍天數 (Frequency)', fontsize=12)
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)  # 把圖例移到外面

# plt.tight_layout()
# plt.savefig("RFM_Scatter_Plot.png", dpi=300)
# print("💾 散佈圖已存檔：RFM_Scatter_Plot.png")
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import json
import os

# 设置 matplotlib 字体支持中文（如果标签包含中文）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 确保输出目录存在
os.makedirs('plots', exist_ok=True)

# 加载数据
df = pd.read_csv('./grok/video_data.csv')

# 将 timestamp 转换为 datetime 对象
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# 按 aid 和 timestamp 排序，确保时间顺序
df = df.sort_values(['aid', 'timestamp'])

# 计算每个视频连续快照之间的观看数增量
df['view_diff'] = df.groupby('aid')['stat_view'].diff().fillna(0)

# 定义函数：将观看增量分配到小时
def distribute_views(row):
    if row.name == 0 or row['view_diff'] == 0:
        return []
    start_time = df.loc[row.name - 1, 'timestamp']
    end_time = row['timestamp']
    view_diff = row['view_diff']
    time_diff = (end_time - start_time).total_seconds() / 3600  # 时间差（小时）
    if time_diff == 0:
        return []
    view_rate = view_diff / time_diff
    hours_covered = pd.date_range(start=start_time.floor('H'), end=end_time.ceil('H'), freq='H')
    views_per_hour = []
    for hour in hours_covered:
        overlap_start = max(start_time, hour)
        overlap_end = min(end_time, hour + pd.Timedelta(hours=1))
        if overlap_end > overlap_start:
            overlap_hours = (overlap_end - overlap_start).total_seconds() / 3600
            views = view_rate * overlap_hours
            views_per_hour.append((hour, views))
    return views_per_hour

# 应用函数分配观看增量
view_distributions = df.apply(distribute_views, axis=1)

# 展平列表并创建 DataFrame
view_list = [item for sublist in view_distributions for item in sublist]
view_df = pd.DataFrame(view_list, columns=['hour', 'views'])
hourly_views = view_df.groupby(view_df['hour'].dt.hour)['views'].sum()

# 图表 1：用户活跃时段（每小时观看量）
plt.figure(figsize=(10, 6))
sns.barplot(x=hourly_views.index, y=hourly_views.values, color='teal')
plt.title('用户按小时的活跃度')
plt.xlabel('一天中的小时')
plt.ylabel('总观看量')
plt.xticks(range(24))
plt.tight_layout()
plt.savefig('plots/hourly_views.png')
plt.close()

# 保存到 JSON 文件（供其他用途）
hours = list(range(24))
views = [hourly_views.get(hour, 0) for hour in hours]
with open('hourly_views.json', 'w', encoding='utf-8') as f:
    json.dump({'hours': hours, 'views': views}, f, ensure_ascii=False)

# 获取每个视频的最新快照
latest_df = df.groupby('aid').last().reset_index()

# 图表 2：按类别平均观看量
category_views = latest_df.groupby('tname')['stat_view'].mean().sort_values(ascending=False)
plt.figure(figsize=(12, 6))
sns.barplot(x=category_views.values, y=category_views.index, color='purple')
plt.title('按视频类别的平均观看量')
plt.xlabel('平均观看量')
plt.ylabel('视频类别')
plt.tight_layout()
plt.savefig('plots/category_views.png')
plt.close()

# 保存类别数据到 JSON 文件
with open('category_views.json', 'w', encoding='utf-8') as f:
    json.dump({'categories': category_views.index.tolist(), 'avg_views': category_views.values.tolist()}, f, ensure_ascii=False)

# 获取观看数前 100 的视频
top_videos = latest_df.nlargest(100, 'stat_view')

# 统计高频标签
all_tags = []
for tags in top_videos['tags']:
    all_tags.extend(tags.split(','))
tag_counts = Counter(all_tags)
top_tags = tag_counts.most_common(20)  # 取前 20 个标签
tags = [tag for tag, count in top_tags]
counts = [count for tag, count in top_tags]

# 图表 3：热门标签频率
plt.figure(figsize=(12, 6))
sns.barplot(x=counts, y=tags, color='orange')
plt.title('最受欢迎视频中的热门标签')
plt.xlabel('出现次数')
plt.ylabel('标签')
plt.tight_layout()
plt.savefig('plots/top_tags.png')
plt.close()

# 保存标签数据到 JSON 文件
with open('top_tags.json', 'w', encoding='utf-8') as f:
    json.dump({'tags': tags, 'counts': counts}, f, ensure_ascii=False)

print("数据处理和图表生成完成！")
print("图表已保存至 plots/ 目录：hourly_views.png, category_views.png, top_tags.png")
print("JSON 文件已生成：hourly_views.json, category_views.json, top_tags.json")
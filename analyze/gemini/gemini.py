import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from collections import Counter
import csv
import numpy as np

# --- 1. 数据加载与预处理 ---
def load_and_preprocess_data(filepath):
    """
    加载数据，并将所有需要的统计字段转换为数值类型。
    """
    try:
        data_as_list_of_dicts = []
        with open(filepath, mode='r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_as_list_of_dicts.append(row)
        
        if not data_as_list_of_dicts:
            print(f"错误: 文件 '{filepath}' 为空或只有表头。")
            return None

        df = pd.DataFrame(data_as_list_of_dicts)
        print("使用csv.DictReader成功加载数据，列名已从文件自动获取。")

    except FileNotFoundError:
        print(f"错误：找不到数据文件 '{filepath}'。请确保文件路径正确。")
        return None
    except Exception as e:
        print(f"读取或处理文件时发生错误: {e}")
        return None

    # --- 数据类型转换 ---
    df['timestamp_dt'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # 【关键改动】将 real_time_all 和 real_time_web 添加到数值转换列表
    stat_cols = [
        'stat_view', 'stat_danmaku', 'stat_reply', 'stat_favorite', 
        'stat_coin', 'stat_share', 'stat_like', 'duration',
        'real_time_all', 'real_time_web' # 添加在线人数字段
    ]
    for col in stat_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df.fillna({'tags': ''}, inplace=True)
    df.dropna(subset=stat_cols, inplace=True)

    print("数据预处理完成。")
    return df

# --- 2. 分析模块 (已全面更新) ---

def analyze_total_online_viewers(df):
    """
    图 1: 分析总在线人数时段
    直接统计所有热门视频的在线人数之和，按小时聚合。
    """
    print("\n--- 1. 开始分析总在线人数时段 ---")
    df['activity_hour'] = df['timestamp_dt'].dt.hour
    
    # 按小时对 real_time_all 求和
    online_viewers_by_hour = df.groupby('activity_hour')['real_time_all'].sum()
    
    # 保存数据
    output_data = {'hours': online_viewers_by_hour.index.tolist(), 'total_online_viewers': online_viewers_by_hour.values.tolist()}
    with open('total_online_viewers_by_hour.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    print("总在线人数时段数据已保存到 total_online_viewers_by_hour.json")

    # 可视化
    plt.figure(figsize=(12, 7))
    sns.barplot(x=online_viewers_by_hour.index, y=online_viewers_by_hour.values, palette='plasma')
    plt.title('B站热门视频总在线人数时段分布', fontsize=16, pad=20)
    plt.xlabel('小时 (Hour of Day)', fontsize=12)
    plt.ylabel('总在线人数 (所有热门视频合计)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('1_total_online_viewers_by_hour.png', dpi=300)
    plt.close()
    print("图表 '1_total_online_viewers_by_hour.png' 已生成。")

def analyze_tags_performance(df):
    """
    图 2 & 3: 分析标签的表现 (频率 vs 平均在线人数)
    """
    print("\n--- 2. 开始分析标签表现 ---")
    latest_videos = df.sort_values('timestamp').drop_duplicates('aid', keep='last').copy()
    
    latest_videos['tags'] = latest_videos['tags'].str.split(',')
    tags_df = latest_videos.explode('tags')
    tags_df = tags_df[tags_df['tags'] != '']

    # 【关键改动】聚合指标改为 real_time_all
    tag_analysis = tags_df.groupby('tags').agg(
        frequency=('aid', 'count'),
        average_online_viewers=('real_time_all', 'mean')
    ).astype({'average_online_viewers': int})

    # --- 图 2: 按频率最高的Top 15标签 (逻辑不变) ---
    top_tags_by_freq = tag_analysis.sort_values(by='frequency', ascending=False).head(15)
    top_tags_by_freq.to_json('tags_by_frequency.json', orient='index', indent=4, force_ascii=False)
    print("高频标签数据已保存到 tags_by_frequency.json")

    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_tags_by_freq['frequency'], y=top_tags_by_freq.index, palette='crest', orient='h')
    plt.title('Top 15 热门视频高频标签', fontsize=16, pad=20)
    plt.xlabel('出现频次', fontsize=12)
    plt.ylabel('标签', fontsize=12)
    plt.tight_layout()
    plt.savefig('2_top_tags_by_frequency.png', dpi=300)
    plt.close()
    print("图表 '2_top_tags_by_frequency.png' 已生成。")
    
    # --- 图 3: 按平均在线人数最高的Top 15标签 ---
    top_tags_by_online = tag_analysis.sort_values(by='average_online_viewers', ascending=False).head(15)
    top_tags_by_online.to_json('tags_by_avg_online.json', orient='index', indent=4, force_ascii=False)
    print("高在线人数标签数据已保存到 tags_by_avg_online.json")

    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_tags_by_online['average_online_viewers'], y=top_tags_by_online.index, palette='magma', orient='h')
    plt.title('Top 15 高平均在线人数标签', fontsize=16, pad=20)
    plt.xlabel('平均实时在线人数', fontsize=12)
    plt.ylabel('标签', fontsize=12)
    plt.tight_layout()
    plt.savefig('3_top_tags_by_avg_online.png', dpi=300)
    plt.close()
    print("图表 '3_top_tags_by_avg_online.png' 已生成。")

def analyze_category_performance(df):
    """
    图 4 & 5: 分析视频分区的表现 (平均在线人数 & 在线人数分布)
    """
    print("\n--- 3. 开始分析视频分区表现 ---")
    latest_videos = df.sort_values('timestamp').drop_duplicates('aid', keep='last').copy()
    
    # --- 图 4: 各分区平均在线人数 ---
    # 【关键改动】指标改为 real_time_all
    category_avg_online = latest_videos.groupby('tname')['real_time_all'].mean().sort_values(ascending=False).astype(int)
    category_avg_online.to_json('category_avg_online.json', orient='index', indent=4, force_ascii=False)
    print("各分区平均在线人数数据已保存到 category_avg_online.json")

    plt.figure(figsize=(12, 8))
    sns.barplot(x=category_avg_online.values, y=category_avg_online.index, palette='viridis', orient='h')
    plt.title('各视频分区的平均在线人数', fontsize=16, pad=20)
    plt.xlabel('平均实时在线人数', fontsize=12)
    plt.ylabel('视频分区', fontsize=12)
    plt.tight_layout()
    plt.savefig('4_category_average_online.png', dpi=300)
    plt.close()
    print("图表 '4_category_average_online.png' 已生成。")

    # --- 图 5: 各分区在线人数分布 (箱形图) ---
    top_categories = latest_videos['tname'].value_counts().nlargest(10).index
    online_dist_df = latest_videos[latest_videos['tname'].isin(top_categories)]
    
    plt.figure(figsize=(14, 8))
    # 【关键改动】绘图数据改为 real_time_all
    sns.boxplot(x='real_time_all', y='tname', data=online_dist_df, palette='coolwarm', orient='h')
    plt.xscale('log')
    plt.title('Top 10 热门分区的在线人数分布 (对数坐标)', fontsize=16, pad=20)
    plt.xlabel('实时在线人数 (Log Scale)', fontsize=12)
    plt.ylabel('视频分区', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('5_online_distribution_by_category.png', dpi=300)
    plt.close()
    print("图表 '5_online_distribution_by_category.png' 已生成。")

def analyze_duration_vs_online_viewers(df):
    """
    图 6: 视频时长与在线人数的关系 (六边形箱图)
    """
    print("\n--- 4. 开始分析视频时长与在线人数的关系 ---")
    latest_videos = df.sort_values('timestamp').drop_duplicates('aid', keep='last').copy()
    filtered_df = latest_videos[(latest_videos['duration'] > 10) & (latest_videos['duration'] < 3600)]

    # 【关键改动】Y轴改为 real_time_all
    grid = sns.jointplot(
        x=filtered_df['duration'], 
        y=filtered_df['real_time_all'], 
        kind="hex", 
        height=10, 
        color="#41DAA7",
        joint_kws={'gridsize': 40, 'xscale': 'log', 'yscale': 'log'}
    )
    grid.set_axis_labels('视频时长 (秒, 对数坐标)', '实时在线人数 (对数坐标)', fontsize=12)
    grid.fig.suptitle('视频时长 vs 实时在线人数关系图', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig('6_duration_vs_online_viewers_hexbin.png', dpi=300)
    plt.close()
    print("图表 '6_duration_vs_online_viewers_hexbin.png' 已生成。")

# --- 主函数 ---
if __name__ == '__main__':
    data_file = 'bilibili_hot_videos_server.csv'
    
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    bili_df = load_and_preprocess_data(data_file)
    
    if bili_df is not None:
        analyze_total_online_viewers(bili_df)
        analyze_tags_performance(bili_df)
        analyze_category_performance(bili_df)
        analyze_duration_vs_online_viewers(bili_df)
        
        print("\n所有分析任务完成！已生成6个基于'在线人数'的全新分析图表。")
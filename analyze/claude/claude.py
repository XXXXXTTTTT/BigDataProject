import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import csv  # 添加csv库
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

class BilibiliVideoAnalyzer:
    
    def __init__(self, csv_file_path=None):
        """
        初始化分析器
        """
        self.df = None
        self.processed_data = {}
        
        if csv_file_path:
            self.load_data(csv_file_path)
        else:
            # 使用测试数据
            self.create_test_data()
    
    def load_data(self, file_path):
        """
        使用csv库加载CSV数据
        """
        try:
            data_list = []
            with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
                # 尝试自动检测分隔符
                sample = csvfile.read(1024)
                csvfile.seek(0)
                
                # 检测分隔符
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                # 如果检测失败，默认使用制表符（根据原代码）
                if delimiter not in [',', '\t', ';', '|']:
                    delimiter = '\t'
                
                # 读取CSV文件
                csv_reader = csv.DictReader(csvfile, delimiter=delimiter)
                
                for row in csv_reader:
                    # 处理数值字段，将字符串转换为适当的数据类型
                    processed_row = {}
                    for key, value in row.items():
                        if value == '' or value is None:
                            processed_row[key] = None
                        else:
                            # 尝试转换数值字段
                            if key in ['timestamp', 'aid', 'videos', 'tid', 'copyright', 'pubdate', 'ctime', 
                                     'state', 'duration', 'stat_view', 'stat_danmaku', 'stat_reply', 
                                     'stat_favorite', 'stat_coin', 'stat_share', 'stat_now_rank', 
                                     'stat_his_rank', 'stat_like', 'stat_dislike', 'stat_vt', 
                                     'stat_vv', 'stat_fav_g', 'stat_like_g', 'owner_mid']:
                                try:
                                    processed_row[key] = int(float(value))
                                except (ValueError, TypeError):
                                    processed_row[key] = value
                            else:
                                processed_row[key] = value
                    
                    data_list.append(processed_row)
            
            # 转换为DataFrame
            self.df = pd.DataFrame(data_list)
            print(f"成功使用csv库加载数据，共 {len(self.df)} 条记录")
            
            # 显示数据基本信息
            print(f"数据列数: {len(self.df.columns)}")
            print(f"主要列名: {list(self.df.columns[:10])}")
            
        except FileNotFoundError:
            print(f"文件 {file_path} 未找到，使用测试数据")
            self.create_test_data()
        except UnicodeDecodeError:
            print("文件编码错误，尝试使用其他编码格式...")
            try:
                # 尝试使用其他编码
                self.load_data_with_encoding(file_path, 'gbk')
            except:
                print("编码转换失败，使用测试数据")
                self.create_test_data()
        except Exception as e:
            print(f"数据加载失败: {e}")
            print("使用测试数据继续分析")
            self.create_test_data()
    
    def load_data_with_encoding(self, file_path, encoding):
        """
        使用指定编码加载数据
        """
        data_list = []
        with open(file_path, 'r', encoding=encoding, newline='') as csvfile:
            # 检测分隔符
            sample = csvfile.read(1024)
            csvfile.seek(0)
            
            sniffer = csv.Sniffer()
            try:
                delimiter = sniffer.sniff(sample).delimiter
            except:
                delimiter = '\t'  # 默认使用制表符
            
            csv_reader = csv.DictReader(csvfile, delimiter=delimiter)
            
            for row in csv_reader:
                processed_row = {}
                for key, value in row.items():
                    if value == '' or value is None:
                        processed_row[key] = None
                    else:
                        # 数值字段转换
                        if key in ['timestamp', 'aid', 'videos', 'tid', 'copyright', 'pubdate', 'ctime', 
                                 'state', 'duration', 'stat_view', 'stat_danmaku', 'stat_reply', 
                                 'stat_favorite', 'stat_coin', 'stat_share', 'stat_now_rank', 
                                 'stat_his_rank', 'stat_like', 'stat_dislike', 'stat_vt', 
                                 'stat_vv', 'stat_fav_g', 'stat_like_g', 'owner_mid']:
                            try:
                                processed_row[key] = int(float(value))
                            except (ValueError, TypeError):
                                processed_row[key] = value
                        else:
                            processed_row[key] = value
                
                data_list.append(processed_row)
        
        self.df = pd.DataFrame(data_list)
        print(f"成功使用 {encoding} 编码加载数据，共 {len(self.df)} 条记录")
    
    def preprocess_data(self):
        """
        数据预处理
        """
        print("开始数据预处理...")
        
        # 转换时间戳
        self.df['datetime'] = pd.to_datetime(self.df['timestamp'], unit='s')
        self.df['pubdate_dt'] = pd.to_datetime(self.df['pubdate'], unit='s')
        self.df['hour'] = self.df['datetime'].dt.hour
        self.df['day_of_week'] = self.df['datetime'].dt.dayofweek
        self.df['date'] = self.df['datetime'].dt.date
        
        # 处理标签
        self.df['tags_list'] = self.df['tags'].str.split(',')
        self.df['tags_count'] = self.df['tags_list'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        
        # 计算互动率
        self.df['engagement_rate'] = (
            self.df['stat_like'] + self.df['stat_coin'] + self.df['stat_favorite'] + 
            self.df['stat_share'] + self.df['stat_reply']
        ) / self.df['stat_view']
        
        # 计算视频质量分数（综合指标）
        self.df['quality_score'] = (
            self.df['stat_like'] * 0.3 + 
            self.df['stat_coin'] * 0.2 + 
            self.df['stat_favorite'] * 0.2 + 
            self.df['stat_share'] * 0.15 + 
            self.df['stat_reply'] * 0.15
        ) / self.df['stat_view']
        
        # 时长分类
        self.df['duration_category'] = pd.cut(
            self.df['duration'], 
            bins=[0, 60, 300, 600, 1800, float('inf')], 
            labels=['短视频(<1min)', '短中视频(1-5min)', '中等视频(5-10min)', '长视频(10-30min)', '超长视频(>30min)']
        )
        
        print("数据预处理完成")
    
    def analyze_time_activity(self):
        """
        分析用户活跃时段
        """
        print("分析用户活跃时段...")
        
        # 按小时统计观看量
        hourly_views = self.df.groupby('hour').agg({
            'stat_view': ['sum', 'mean', 'count'],
            'stat_like': 'sum',
            'stat_reply': 'sum',
            'stat_share': 'sum'
        }).round(2)
        
        # 按星期几统计
        weekday_views = self.df.groupby('day_of_week').agg({
            'stat_view': ['sum', 'mean', 'count'],
            'stat_like': 'sum',
            'engagement_rate': 'mean'
        }).round(2)
        
        # 按日期统计（趋势分析）
        daily_views = self.df.groupby('date').agg({
            'stat_view': 'sum',
            'aid': 'nunique',  # 每日热门视频数量
            'engagement_rate': 'mean'
        }).round(2)
        
        self.processed_data['hourly_activity'] = hourly_views
        self.processed_data['weekday_activity'] = weekday_views
        self.processed_data['daily_trends'] = daily_views
        
        return hourly_views, weekday_views, daily_views
    
    def analyze_video_characteristics(self):
        """
        分析视频特征
        """
        print("分析视频特征...")
        
        # 按分区分析
        category_analysis = self.df.groupby('tnamev2').agg({
            'stat_view': ['mean', 'sum', 'count'],
            'stat_like': 'mean',
            'engagement_rate': 'mean',
            'duration': 'mean',
            'quality_score': 'mean'
        }).round(2)
        
        # 按时长分析
        duration_analysis = self.df.groupby('duration_category').agg({
            'stat_view': ['mean', 'count'],
            'engagement_rate': 'mean',
            'quality_score': 'mean'
        }).round(2)
        
        # UP主分析
        owner_analysis = self.df.groupby('owner_name').agg({
            'stat_view': ['sum', 'mean', 'count'],
            'engagement_rate': 'mean',
            'quality_score': 'mean'
        }).round(2)
        
        # 标签分析
        all_tags = []
        for tags_list in self.df['tags_list'].dropna():
            if isinstance(tags_list, list):
                all_tags.extend([tag.strip() for tag in tags_list if tag.strip()])
        
        tag_counts = pd.Series(all_tags).value_counts().head(20)
        
        self.processed_data['category_analysis'] = category_analysis
        self.processed_data['duration_analysis'] = duration_analysis
        self.processed_data['owner_analysis'] = owner_analysis
        self.processed_data['popular_tags'] = tag_counts
        
        return category_analysis, duration_analysis, owner_analysis, tag_counts
    
    def create_visualizations(self):
        print("创建可视化图表...")
        
        # 设置全局样式
        plt.rcParams['font.size'] = 12
        
        # 1. 24小时活跃度分析
        plt.figure(figsize=(12, 6))
        hourly_data = self.processed_data['hourly_activity']['stat_view']['sum']
        full_hourly = pd.Series(0, index=range(24))
        full_hourly.update(hourly_data)
        
        bars1 = plt.bar(range(24), full_hourly.values, color='skyblue', alpha=0.8)
        plt.title('24小时用户活跃度分布', fontsize=16, fontweight='bold')
        plt.xlabel('小时', fontsize=12)
        plt.ylabel('总观看量', fontsize=12)
        plt.xticks(range(0, 24, 2))
        plt.grid(True, alpha=0.3)
        
        for bar in bars1:
            height = bar.get_height()
            if not pd.isna(height) and height > 0:
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height/1000)}K' if height > 1000 else f'{int(height)}',
                        ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig('01_24小时活跃度分布.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. 一周活跃度分析
        plt.figure(figsize=(10, 6))
        weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        weekday_data = self.processed_data['weekday_activity']['stat_view']['sum']
        full_weekday = pd.Series(0, index=range(7))
        full_weekday.update(weekday_data)
        
        bars2 = plt.bar(weekday_names, full_weekday.values, color='lightcoral', alpha=0.8)
        plt.title('一周用户活跃度分布', fontsize=16, fontweight='bold')
        plt.xlabel('星期', fontsize=12)
        plt.ylabel('总观看量', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        for bar in bars2:
            height = bar.get_height()
            if not pd.isna(height) and height > 0:
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height/1000)}K' if height > 1000 else f'{int(height)}',
                        ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig('02_一周活跃度分布.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. 视频分区对比
        plt.figure(figsize=(12, 8))
        category_data = self.processed_data['category_analysis']['stat_view']['mean'].head(10)
        if len(category_data) > 0:
            bars3 = plt.barh(range(len(category_data)), category_data.values, color='lightgreen', alpha=0.8)
            plt.title('各分区平均观看量对比', fontsize=16, fontweight='bold')
            plt.xlabel('平均观看量', fontsize=12)
            plt.yticks(range(len(category_data)), category_data.index)
            plt.grid(True, alpha=0.3, axis='x')
            
            for i, bar in enumerate(bars3):
                width = bar.get_width()
                if not pd.isna(width) and width > 0:
                    plt.text(width, bar.get_y() + bar.get_height()/2.,
                            f'{int(width/1000)}K' if width > 1000 else f'{int(width)}',
                            ha='left', va='center', fontsize=10)
        else:
            plt.text(0.5, 0.5, '数据不足', ha='center', va='center', transform=plt.gca().transAxes, fontsize=14)
            plt.title('各分区平均观看量对比', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('03_各分区平均观看量对比.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. 互动率vs观看量散点图
        plt.figure(figsize=(10, 8))
        if len(self.df) > 0:
            scatter = plt.scatter(self.df['stat_view'], self.df['engagement_rate'], 
                                c=self.df['duration'], cmap='viridis', alpha=0.6, s=50)
            plt.title('观看量vs互动率关系', fontsize=16, fontweight='bold')
            plt.xlabel('观看量', fontsize=12)
            plt.ylabel('互动率', fontsize=12)
            plt.colorbar(scatter, label='视频时长(秒)')
            plt.grid(True, alpha=0.3)
            if self.df['stat_view'].min() > 0:
                plt.xscale('log')
        
        plt.tight_layout()
        plt.savefig('04_观看量vs互动率关系.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. 视频时长分布
        plt.figure(figsize=(12, 6))
        duration_data = self.processed_data['duration_analysis']['stat_view']['mean']
        if len(duration_data) > 0:
            bars5 = plt.bar(range(len(duration_data)), duration_data.values, color='orange', alpha=0.8)
            plt.title('不同时长视频平均观看量', fontsize=16, fontweight='bold')
            plt.xlabel('视频时长分类', fontsize=12)
            plt.ylabel('平均观看量', fontsize=12)
            plt.xticks(range(len(duration_data)), duration_data.index, rotation=45)
            plt.grid(True, alpha=0.3)
            
            for bar in bars5:
                height = bar.get_height()
                if not pd.isna(height) and height > 0:
                    plt.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height/1000)}K' if height > 1000 else f'{int(height)}',
                            ha='center', va='bottom', fontsize=10)
        else:
            plt.text(0.5, 0.5, '数据不足', ha='center', va='center', transform=plt.gca().transAxes, fontsize=14)
            plt.title('不同时长视频平均观看量', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('05_不同时长视频平均观看量.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 6. 热门标签TOP15
        plt.figure(figsize=(12, 8))
        top_tags = self.processed_data['popular_tags'].head(15)
        if len(top_tags) > 0:
            bars6 = plt.barh(range(len(top_tags)), top_tags.values, color='purple', alpha=0.7)
            plt.title('热门标签TOP15', fontsize=16, fontweight='bold')
            plt.xlabel('出现次数', fontsize=12)
            plt.yticks(range(len(top_tags)), top_tags.index)
            plt.grid(True, alpha=0.3, axis='x')
            
            for i, bar in enumerate(bars6):
                width = bar.get_width()
                if not pd.isna(width) and width > 0:
                    plt.text(width, bar.get_y() + bar.get_height()/2.,
                            f'{int(width)}', ha='left', va='center', fontsize=10)
        else:
            plt.text(0.5, 0.5, '标签数据不足', ha='center', va='center', transform=plt.gca().transAxes, fontsize=14)
            plt.title('热门标签TOP15', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('06_热门标签TOP15.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 7. 质量分数分布
        plt.figure(figsize=(10, 6))
        if len(self.df) > 0 and not self.df['quality_score'].isna().all():
            plt.hist(self.df['quality_score'].dropna(), bins=min(30, len(self.df)), 
                    color='teal', alpha=0.7, edgecolor='black')
            plt.title('视频质量分数分布', fontsize=16, fontweight='bold')
            plt.xlabel('质量分数', fontsize=12)
            plt.ylabel('视频数量', fontsize=12)
            plt.grid(True, alpha=0.3)
        else:
            plt.text(0.5, 0.5, '质量分数数据不足', ha='center', va='center', transform=plt.gca().transAxes, fontsize=14)
            plt.title('视频质量分数分布', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('07_视频质量分数分布.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 8. 时长vs互动率箱线图
        plt.figure(figsize=(12, 6))
        if len(self.df) > 0 and not self.df['duration_category'].isna().all():
            try:
                sns.boxplot(data=self.df, x='duration_category', y='engagement_rate')
                plt.title('不同时长视频互动率分布', fontsize=16, fontweight='bold')
                plt.xlabel('视频时长分类', fontsize=12)
                plt.ylabel('互动率', fontsize=12)
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3)
            except:
                plt.text(0.5, 0.5, '数据不足绘制箱线图', ha='center', va='center', transform=plt.gca().transAxes, fontsize=14)
                plt.title('不同时长视频互动率分布', fontsize=16, fontweight='bold')
        else:
            plt.text(0.5, 0.5, '时长分类数据不足', ha='center', va='center', transform=plt.gca().transAxes, fontsize=14)
            plt.title('不同时长视频互动率分布', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('08_不同时长视频互动率分布.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 9. 观看量vs点赞量关系
        plt.figure(figsize=(10, 8))
        if len(self.df) > 0:
            plt.scatter(self.df['stat_view'], self.df['stat_like'], alpha=0.6, color='red', s=30)
            plt.title('观看量vs点赞量关系', fontsize=16, fontweight='bold')
            plt.xlabel('观看量', fontsize=12)
            plt.ylabel('点赞量', fontsize=12)
            plt.grid(True, alpha=0.3)
            
            if self.df['stat_view'].min() > 0 and self.df['stat_like'].min() > 0:
                plt.xscale('log')
                plt.yscale('log')
                
                # 添加趋势线
                try:
                    z = np.polyfit(np.log(self.df['stat_view']), np.log(self.df['stat_like']), 1)
                    p = np.poly1d(z)
                    plt.plot(self.df['stat_view'], np.exp(p(np.log(self.df['stat_view']))), 
                            "orange", alpha=0.8, linewidth=2, label='趋势线')
                    plt.legend()
                except:
                    pass
        
        plt.tight_layout()
        plt.savefig('09_观看量vs点赞量关系.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 10. 每小时平均互动率
        plt.figure(figsize=(12, 6))
        hourly_engagement = self.df.groupby('hour')['engagement_rate'].mean()
        full_hourly_engagement = pd.Series(0, index=range(24))
        full_hourly_engagement.update(hourly_engagement)
        
        plt.plot(range(24), full_hourly_engagement.values, marker='o', linewidth=2, 
                markersize=8, color='green', markerfacecolor='lightgreen', markeredgecolor='darkgreen')
        plt.title('24小时平均互动率变化', fontsize=16, fontweight='bold')
        plt.xlabel('小时', fontsize=12)
        plt.ylabel('平均互动率', fontsize=12)
        plt.xticks(range(0, 24, 2))
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('10_24小时平均互动率变化.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 11. UP主视频数量vs质量
        plt.figure(figsize=(10, 8))
        if len(self.df) > 0:
            owner_stats = self.df.groupby('owner_name').agg({
                'aid': 'count',
                'quality_score': 'mean'
            })
            if len(owner_stats) > 0:
                plt.scatter(owner_stats['aid'], owner_stats['quality_score'], 
                        alpha=0.7, s=80, color='brown')
                plt.title('UP主视频数量vs平均质量', fontsize=16, fontweight='bold')
                plt.xlabel('视频数量', fontsize=12)
                plt.ylabel('平均质量分数', fontsize=12)
                plt.grid(True, alpha=0.3)
            else:
                plt.text(0.5, 0.5, 'UP主数据不足', ha='center', va='center', transform=plt.gca().transAxes, fontsize=14)
                plt.title('UP主视频数量vs平均质量', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('11_UP主视频数量vs平均质量.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 12. 分区互动率对比
        plt.figure(figsize=(12, 8))
        category_engagement = self.processed_data['category_analysis']['engagement_rate']['mean'].head(8)
        if len(category_engagement) > 0:
            bars12 = plt.bar(range(len(category_engagement)), category_engagement.values, 
                            color='navy', alpha=0.8)
            plt.title('各分区平均互动率对比', fontsize=16, fontweight='bold')
            plt.xlabel('分区', fontsize=12)
            plt.ylabel('平均互动率', fontsize=12)
            plt.xticks(range(len(category_engagement)), category_engagement.index, rotation=45)
            plt.grid(True, alpha=0.3)
            
            for bar in bars12:
                height = bar.get_height()
                if not pd.isna(height) and height > 0:
                    plt.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:.3f}', ha='center', va='bottom', fontsize=10)
        else:
            plt.text(0.5, 0.5, '分区数据不足', ha='center', va='center', transform=plt.gca().transAxes, fontsize=14)
            plt.title('各分区平均互动率对比', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('12_各分区平均互动率对比.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("所有图表已单独保存完成！")
        print("生成的图表文件：")
        for i in range(1, 13):
            filename_map = {
                1: "01_24小时活跃度分布.png",
                2: "02_一周活跃度分布.png", 
                3: "03_各分区平均观看量对比.png",
                4: "04_观看量vs互动率关系.png",
                5: "05_不同时长视频平均观看量.png",
                6: "06_热门标签TOP15.png",
                7: "07_视频质量分数分布.png",
                8: "08_不同时长视频互动率分布.png",
                9: "09_观看量vs点赞量关系.png",
                10: "10_24小时平均互动率变化.png",
                11: "11_UP主视频数量vs平均质量.png",
                12: "12_各分区平均互动率对比.png"
            }
            print(f"- {filename_map[i]}")
    
    def export_analysis_results(self):
        """
        导出分析结果到文件
        """
        print("导出分析结果...")
        
        # 导出到Excel
        # with pd.ExcelWriter('bilibili_analysis_results.xlsx', engine='openpyxl') as writer:
            # 原始数据
            # self.df.to_excel(writer, sheet_name='原始数据', index=False)
            
            # # 时间活跃度分析
            # self.processed_data['hourly_activity'].to_excel(writer, sheet_name='24小时活跃度')
            # self.processed_data['weekday_activity'].to_excel(writer, sheet_name='一周活跃度')
            
            # # 视频特征分析
            # self.processed_data['category_analysis'].to_excel(writer, sheet_name='分区分析')
            # self.processed_data['duration_analysis'].to_excel(writer, sheet_name='时长分析')
            # self.processed_data['owner_analysis'].to_excel(writer, sheet_name='UP主分析')
            
            # # 热门标签
            # self.processed_data['popular_tags'].to_excel(writer, sheet_name='热门标签')
        
        # 导出JSON格式（用于前端图表）
        json_data = {
            'hourly_activity': {
                'hours': list(range(24)),
                'views': self.processed_data['hourly_activity']['stat_view']['sum'].tolist(),
                'engagement': self.df.groupby('hour')['engagement_rate'].mean().tolist()
            },
            'weekday_activity': {
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                'views': self.processed_data['weekday_activity']['stat_view']['sum'].tolist(),
                'engagement': self.processed_data['weekday_activity']['engagement_rate']['mean'].tolist()
            },
            'category_stats': {
                'categories': self.processed_data['category_analysis']['stat_view']['mean'].head(10).index.tolist(),
                'avg_views': self.processed_data['category_analysis']['stat_view']['mean'].head(10).tolist(),
                'engagement_rates': self.processed_data['category_analysis']['engagement_rate']['mean'].head(10).tolist()
            },
            'duration_stats': {
                'categories': self.processed_data['duration_analysis']['stat_view']['mean'].index.tolist(),
                'avg_views': self.processed_data['duration_analysis']['stat_view']['mean'].tolist(),
                'engagement_rates': self.processed_data['duration_analysis']['engagement_rate']['mean'].tolist()
            },
            'popular_tags': {
                'tags': self.processed_data['popular_tags'].head(20).index.tolist(),
                'counts': self.processed_data['popular_tags'].head(20).tolist()
            },
            'summary_stats': {
                'total_videos': len(self.df),
                'total_views': int(self.df['stat_view'].sum()),
                'avg_engagement': float(self.df['engagement_rate'].mean()),
                'peak_hour': int(self.processed_data['hourly_activity']['stat_view']['sum'].idxmax()),
                'most_active_day': int(self.processed_data['weekday_activity']['stat_view']['sum'].idxmax()),
                'top_category': self.processed_data['category_analysis']['stat_view']['sum'].idxmax()
            }
        }
        
        with open('bilibili_analysis_data.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print("结果已导出到:")
        print("- bilibili_analysis_results.xlsx (详细数据)")
        print("- bilibili_analysis_data.json (前端图表数据)")
    
    def generate_insights_report(self):
        """
        生成洞察报告
        """
        print("\n=== B站热门视频数据分析报告 ===")
        
        # 基础统计
        total_videos = len(self.df)
        total_views = self.df['stat_view'].sum()
        avg_engagement = self.df['engagement_rate'].mean()
        
        print(f"\n📊 基础统计:")
        print(f"• 分析视频总数: {total_videos:,}")
        print(f"• 总观看量: {total_views:,}")
        print(f"• 平均互动率: {avg_engagement:.4f}")
        
        # 时间活跃度洞察
        peak_hour = self.processed_data['hourly_activity']['stat_view']['sum'].idxmax()
        peak_views = self.processed_data['hourly_activity']['stat_view']['sum'].max()
        
        most_active_day = self.processed_data['weekday_activity']['stat_view']['sum'].idxmax()
        weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        
        print(f"\n⏰ 用户活跃时段分析:")
        print(f"• 最活跃时段: {peak_hour}:00 (观看量: {peak_views:,})")
        print(f"• 最活跃日期: {weekday_names[most_active_day]}")
        
        # 视频特征洞察
        top_category = self.processed_data['category_analysis']['stat_view']['mean'].idxmax()
        top_category_views = self.processed_data['category_analysis']['stat_view']['mean'].max()
        
        best_duration = self.processed_data['duration_analysis']['engagement_rate']['mean'].idxmax()
        
        print(f"\n🎬 视频特征分析:")
        print(f"• 最受欢迎分区: {top_category} (平均观看量: {top_category_views:,.0f})")
        print(f"• 最佳视频时长: {best_duration}")
        
        # 热门标签
        top_3_tags = self.processed_data['popular_tags'].head(3)
        print(f"\n🏷️ 热门标签TOP3:")
        for i, (tag, count) in enumerate(top_3_tags.items(), 1):
            print(f"• {i}. {tag} ({count}次)")
        
        # 质量分析
        high_quality_threshold = self.df['quality_score'].quantile(0.8)
        high_quality_videos = self.df[self.df['quality_score'] >= high_quality_threshold]
        
        print(f"\n⭐ 高质量视频特征:")
        print(f"• 高质量视频数量: {len(high_quality_videos)} ({len(high_quality_videos)/total_videos*100:.1f}%)")
        print(f"• 高质量视频平均时长: {high_quality_videos['duration'].mean():.0f}秒")
        print(f"• 高质量视频主要分区: {high_quality_videos['tnamev2'].mode().iloc[0]}")
        
        print("\n" + "="*50)
    
    def run_complete_analysis(self):
        """
        运行完整分析流程
        """
        print("开始B站热门视频数据分析...")
        
        # 数据预处理
        self.preprocess_data()
        
        # 执行分析
        self.analyze_time_activity()
        self.analyze_video_characteristics()
        
        # 创建可视化
        self.create_visualizations()
        
        # 导出结果
        self.export_analysis_results()
        
        # 生成报告
        self.generate_insights_report()
        
        print("\n✅ 分析完成！所有文件已生成。")

# 使用示例
if __name__ == "__main__":

    # 如果有CSV文件，可以这样加载：
    analyzer = BilibiliVideoAnalyzer('video_data.csv')
    
    # 运行完整分析
    analyzer.run_complete_analysis()
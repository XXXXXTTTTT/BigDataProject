import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from dataset import FEATURES, norm_data
import joblib

def cluster():
    # 加载处理好的数据
    df = pd.read_csv("cluster_ready.csv")
    print(df.head())


    X_scaled, scaler = norm_data(df=df)

    # 初始化 KMeans 聚类器，设置簇数为 4
    # kmeans = KMeans(n_clusters=4)
    kmeans = KMeans(n_clusters=3, init='k-means++')
    # 训练 KMeans 聚类模型
    kmeans.fit(X_scaled)

    # 获取每个样本的聚类标签
    df['cluster'] = kmeans.labels_

    # 标准化特征数据
    
    # 查看每个类的中心点
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    cluster_centers_df = pd.DataFrame(cluster_centers, columns=FEATURES)
    print("聚类中心：\n", cluster_centers_df)
    
    
#可视化

    # 使用 PCA 降维到 2D 以便可视化
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(X_scaled)

    # 创建一个散点图，按照聚类标签绘制每个 UP 主
    plt.figure(figsize=(8, 6))
    plt.scatter(pca_components[:, 0], pca_components[:, 1], c=df['cluster'], cmap='viridis', alpha=0.6)
    plt.title("KMeans")
    plt.xlabel('PCA1')
    plt.ylabel('PCA2')
    plt.colorbar(label='Cluster')
    plt.show()

    # 聚类结果统计，查看每个类的成员分布
    cluster_summary = df.groupby('cluster').agg({
        'log_followers': 'mean',
        'log_view': 'mean',
        'like_rate': 'mean',
        'engagement_rate': 'mean',
        'duration_engagement': 'mean'
    }).reset_index()
    
    # 'followers', 'total_view', 'like_rate', 'engagement_rate', 'duration_engagement'

    # cluster_summary = df.groupby('cluster').agg({
    #     'followers': 'mean',
    #     'total_view': 'mean',
    #     'like_rate': 'mean',
    #     'engagement_rate': 'mean',
    #     'duration_engagement': 'mean'
    # }).reset_index()
    # print(cluster_summary)



    joblib.dump(kmeans, 'kmeans_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    
    # 计算聚类的轮廓系数
    silhouette_avg = silhouette_score(X_scaled, kmeans.labels_)
    print(f"聚类的轮廓系数: {silhouette_avg}")

#测试脚本
if __name__ == '__main__':
    cluster()
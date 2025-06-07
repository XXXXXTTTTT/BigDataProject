import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

# 加载处理好的数据
df = pd.read_csv("cluster_ready.csv")
print(df.head())


# 提取聚类特征列
features = ['log_followers', 'log_view', 'like_rate', 'engagement_rate', 'duration_engagement']
X = df[features]

# 标准化特征数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(X_scaled[:5])  # 查看标准化后的数据前五行

# 存储不同 K 值的 SSE
sse = []

# 尝试不同的 K 值（例如从 1 到 10）
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300, random_state=42)
    kmeans.fit(X_scaled)
    sse.append(kmeans.inertia_)  # KMeans 的总平方误差（inertia_）

# 绘制 K 与 SSE 的关系图
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), sse, marker='o')
plt.title('K\SSE')
plt.xlabel('K')
plt.ylabel('SSE')
plt.show()

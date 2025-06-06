import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
from dataset import compute_features


"""
预测新数据的聚类标签

参数:
    new_data (list or np.array): 新数据，包含待预测的样本
    model_path (str): 训练好的 KMeans 模型路径，默认为 'kmeans_model.pkl'
    
返回:
    cluster_label (int): 新数据所属的聚类标签
"""
    
def predict_new_data(new_data, model_path='kmeans_model.pkl'):

    
    # 加载保存的 KMeans 模型
    kmeans = joblib.load(model_path)
    
    # 1. 预处理新数据：标准化


    new_data_scaled = compute_features(new_data) 

    # 2. 使用训练好的模型预测新数据的类别标签
    cluster_label = kmeans.predict(new_data_scaled)  # 预测聚类标签
    
    return cluster_label
#测试脚本
if __name__ == '__main__':
    # 示例：假设新数据是单个样本
    # new_sample = np.array([[1318997, 1572091, 528, 168685339, 2577582, 695764, 304477, 349603, 1435380, 572710, 0, 560]])  # 假设是一个包含5个特征的样本
    new_sample =     {
    "uid": 400482416,
    "followers": 32, #粉丝数
    "total_videos": 2, #投稿视频数
    "total_view": 15954, #总播放量
    "total_like": 101, #总点赞
    "total_coin": 25, #总硬币
    "total_favorite": 30, #所有收藏
    "total_share": 42, #所有分享
    "total_comment": 37, #评论数
    "total_danmaku": 41, #弹幕
    "total_duration": 5311, #视频总时长
    "total_chargers": 0, #充电数
    "total_videos_count": 2, #总水平数
    "errors": []
    }
    cluster = predict_new_data(new_sample)    
    print(f"新数据的聚类标签是: {cluster}")


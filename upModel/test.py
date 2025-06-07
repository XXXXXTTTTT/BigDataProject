import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from dataset import FEATURES,NUMERCIAL_FEATURES,get_data_from_db, compute_features, norm_data, load_data_from_db, get_showInfo_from_db
from sklearn.preprocessing import StandardScaler
import mplcursors
import requests
from io import BytesIO
from PIL import Image
import concurrent.futures

"""
预测新数据的聚类标签

参数:
    new_data (list or np.array): 新数据，包含待预测的样本
    model_path (str): 训练好的 KMeans 模型路径，默认为 'kmeans_model.pkl'
    
返回:
    cluster_label (int): 新数据所属的聚类标签
"""

    
def predict_new_data(new_data, model_path='kmeans_model.pkl', scaler_path='scaler.pkl'):

    
    # 加载保存的 KMeans 模型
    kmeans = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    # 1. 预处理新数据：标准化
    
    if isinstance(new_data, dict):  # 如果是字典类型，转换为 DataFrame
       new_data = pd.DataFrame([new_data])  # 每个 UP 主数据为一行

    # 提取并计算特征
    features = compute_features(new_data)
    features = features[FEATURES]
    # 使用训练时的 scaler 进行标准化
    X_scaled = scaler.transform(features)

    # 聚类预测
    cluster_label = kmeans.predict(X_scaled)
    
    return cluster_label

#根据UID进行预测
def predict_new_data_via_uid(uid, model_path='kmeans_model.pkl'):

    data = get_data_from_db(uid=uid)
        
    
    return predict_new_data(data)

# 获取所有UP主的数据并进行预测
def predict_all_up(model_path='kmeans_model.pkl'):
    df = load_data_from_db()  # 获取所有UP主数据
    
    # 将 DataFrame 转换为字典，key 为 uid，value 为数据行
    up_data = df.set_index('uid').to_dict(orient='index')
    
    # 用于存储每个UP主的预测结果
    results = []
    
    for uid, data in up_data.items():
        
        
        
        if isinstance(data, dict):  # 如果是字典类型，转换为 DataFrame
            data = pd.DataFrame([data])  # 每个 UP 主数据为一行
        data['uid'] = uid
        print(data)
        # data = data[NUMERCIAL_FEATURES]    
        # new_data_scaled = compute_features(data) 
        # X_scaled, scaler = norm_data(new_data_scaled)
        cluster_label = predict_new_data(data, model_path=model_path)
        
        # 获取UP主的名字和头像URL
        df = get_showInfo_from_db(uid)
        # name, avatar_url
        # 存储预测结果
        results.append({
            'uid': uid,
            'name': df['name'],
            'avatar_url': df['avatar_url'],
            'cluster_label': cluster_label[0]  # 预测标签
        })
    
    return results

# 可视化展示每个UP主的聚类结果（头像和名字）
def visualize_up_clusters(results):
      # 设置图形
    plt.figure(figsize=(12, 8))

    cluster_colors = ['red', 'green', 'blue', 'purple']
    x_coords = []
    y_coords = []
    hover_info = []
    avatar_images = []
    
    # 遍历每个UP主，获取头像URL
    for result in results:
        cluster_label = result['cluster_label']
        name = result['name']
        
        avatar_url = result['avatar_url'].values[0] 
        print(f"{name} : {cluster_label}")
        # print(f"Fetching avatar for {name}: {avatar_url}")

        x_coords.append(np.random.rand())  # 随机生成坐标
        y_coords.append(np.random.rand())
        hover_info.append(f"{name}\n{avatar_url}")
        avatar_images.append(avatar_url)
        
    print(f"num : {len(results)}")
    scatter = plt.scatter(x_coords, y_coords, c=[cluster_colors[label] for label in [result['cluster_label'] for result in results]], s=200)

    # 绑定点击事件，点击后显示名字和头像
    # mplcursors.cursor(scatter, hover=False).connect("add", lambda sel: on_click(sel, hover_info, x_coords, y_coords, avatar_images))

    plt.title('UP 主聚类结果展示')
    plt.xlabel('PCA 组件 1')
    plt.ylabel('PCA 组件 2')

    # 在图上显示头像（只是放置标记，不做任何交互）
    # for i, avatar_url in enumerate(avatar_images):
    #     try:
    #         response = requests.get(avatar_url, timeout=5)  # 设置请求超时5秒
    #         if response.status_code != 200:
    #             print(f"Failed to download {avatar_url}")
    #             continue  # 跳过当前头像URL
            
    #         img = Image.open(BytesIO(response.content))  # 使用PIL加载图像内容
            
    #         # 将PIL图像转换为matplotlib可用的格式
    #         imagebox = OffsetImage(img, zoom=0.1)  # 设置头像显示大小
    #         ab = AnnotationBbox(imagebox, (x_coords[i], y_coords[i]), frameon=False)
    #         plt.gca().add_artist(ab)

    #     except Exception as e:
    #         print(f"Error with image {avatar_url}: {e}")

    plt.show()


def on_click(sel, hover_info, x_coords, y_coords, avatar_images):
    """点击时显示相应的名字和头像"""
    idx = sel.index  # 获取点击的点的索引
    name, avatar_url = hover_info[idx].split("\n")

    # 创建文本框显示名字
    sel.annotation.set_text(f"{name}\n{avatar_url}")
    
    # 获取对应的头像并显示
    try:
        response = requests.get(avatar_url, timeout=5)  # 设置请求超时5秒
        if response.status_code != 200:
            print(f"Failed to download {avatar_url}")
            return  # 如果下载失败，返回
        
        img = Image.open(BytesIO(response.content))  # 使用PIL加载图像内容
        
        # 将PIL图像转换为matplotlib可用的格式
        imagebox = OffsetImage(img, zoom=0.1)  # 设置头像显示大小
        ab = AnnotationBbox(imagebox, (x_coords[idx], y_coords[idx]), frameon=False)
        plt.gca().add_artist(ab)
        
    except Exception as e:
        print(f"Error with image {avatar_url}: {e}")

    

#测试脚本
if __name__ == '__main__':
    
    new_sample = {
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
    
    # cluster = predict_new_data(new_sample) 
    
    # cluster = predict_new_data_via_uid(1318997) #0 大V
    
    # cluster = predict_new_data_via_uid(171844704) #0 粘
    
    # cluster = predict_new_data_via_uid(502937705) 
       
    # cluster = predict_new_data_via_uid(1453964802)
    
    # print(f"新数据的聚类标签是: {cluster}")
    
    # 获取所有UP主的聚类结果
    results = predict_all_up(model_path='kmeans_model.pkl')
    
    # 可视化聚类结果
    visualize_up_clusters(results)


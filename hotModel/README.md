
# 热门视频预测模块



运行前需要下载的库



#py从数据库中获取数据

`pip install pymysql`



#py数据处理库

`pip install pandas`

`pip install numpy`





数据处理:

原始数据:

"""

  {

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

"""



用于聚类的特征：



  \# 构造新特征

  log_followers = log10(followers] + 1)  #粉丝数对数

  log_view = log10(total_view + 1) #播放量对数

  like_rate = total_like/ total_view.replace(0, np.nan) #点赞率  

  engagement_rate= (total_like + total_coin * 2 + total_favorite +

total_share+ total_comment + total_danmaku) / total_view.replace(0, np.nan)   #综合互动率

  avg_duration= df['total_duration'] / df['total_videos'].replace(0, np.nan)





根据(粉丝数,播放量)等数据的长尾分布(大多数UP粉丝少, 少部分UP粉丝多的很), 我们对这类数据进行+1对数处理, (加1防止零值) 作为特征













=======
## 📌 `README.md` 

```markdown
# 🎬 Bilibili 热门视频预测与UP主分析平台

本项目基于B站热门视频数据，结合机器学习建模、数据分析与可视化，构建了一个集预测、平台概览、UP主洞察于一体的分析平台，支持前后端联动部署。

---

## 🧠 项目功能模块

### 1️⃣ 平台概览与核心指标
- ✅ DAU（日活跃 UP主数）
- ✅ 平均每日播放量
- ✅ 平均使用时长
- ✅ 项目目标说明

### 2️⃣ UP主分析模块
- 🔍 条件筛选（UID / 昵称 / 粉丝量）
- 📈 潜力UP主互动率分析（散点图、箱线图）
- 👤 单个UP主详情卡片 + 最新视频表格
- 📉 历史趋势数据：粉丝数、播放量、互动率

### 3️⃣ 热门视频分析模块
- 🔥 播放热度热力图（小时 × 星期）
- ☁️ 视频关键词词云（基于弹幕）
- 📊 分区热度排行榜（视频数 + 平均播放）
- 🤖 热度预测接口（等级 + 置信度 + 预测播放量区间）
- 📈 模型性能指标：准确率、召回率

---

## 📁 项目结构

```

hot\_video\_prediction/
├── scripts/
│   ├── data\_preprocessing.py     # 数据提取与预处理
│   ├── model\_training.py         # 模型训练与保存
│   ├── api\_service\_extended.py   # 完整后端服务接口（FastAPI）
├── requirements.txt              # 所有依赖库
├── X.csv, y.csv                  # 模型输入特征数据
├── hot\_video\_model.pkl           # 训练好的模型文件
└── metrics.json                  # 模型评估指标（准确率/召回率）

````

---

## 🚀 快速开始（本地运行）

### 1. 克隆项目并进入目录

```bash
git clone https://github.com/yourname/hot_video_prediction.git
cd hot_video_prediction
````

### 2. 创建并激活虚拟环境

```bash
python -m venv venv
venv\\Scripts\\activate  # Windows
# 或 source venv/bin/activate  # macOS/Linux
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
pip install scikit-learn cryptography
```

### 4. 修改数据库连接（在 `data_preprocessing.py` 中）

```python
engine = create_engine("mysql+pymysql://remote:123456@114.116.251.42:3306/bilibili")
```

### 5. 执行数据与模型构建

```bash
python scripts/data_preprocessing.py
python scripts/model_training.py
```

### 6. 启动后端 API 服务

```bash
uvicorn scripts.api_service_extended:app --reload
```

### 7. 访问接口文档

浏览器打开： [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📊 示例 API：热门预测

```json
POST /predict

{
  "点赞率": 0.06,
  "弹幕率": 0.01,
  "评论率": 0.02,
  "投币率": 0.03,
  "hour": 15,
  "weekday": 3,
  "duration": 300
}
```

返回：

```json
{
  "prediction": 1,
  "confidence": 0.84,
  "level": "高热",
  "play_range": "10w+"
}
```

---

## 📌 数据说明（部分字段）

| 字段             | 含义         |
| -------------- | ---------- |
| stat\_view     | 播放量        |
| stat\_like     | 点赞数        |
| stat\_reply    | 评论数        |
| stat\_coin     | 投币数        |
| stat\_favorite | 收藏数        |
| duration       | 视频时长（秒）    |
| tags           | 视频标签，用逗号分隔 |

---
这个是mysql里bilibili的表结构+--------------------+
| Tables_in_bilibili |
+--------------------+
| bilibili_videos    |
| hot_videos         |
| up_profile         |
+--------------------+

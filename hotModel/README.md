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














"""
    这个是对外暴露的接口
    返回数据格式如下:
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

uid =  400482416,
followers = 32,
total_videos = 2,
total_view = 15954,
total_like = 101,
total_coin = 25,
total_favorite = 30,
total_share = 42,
total_comment = 37,
total_danmaku = 41,
total_duration = 5311,
total_chargers = 0,
total_videos_count = 2,
    

#一些初步量化指标

#播放/粉丝比

View_Follower_Ratio =  total_view/followers


# 数据爬取模块

## 热门视频分析数据

请先在数据库中自行创建一个名为`bilibili`的数据库.然后在这个数据库下去导入`hot_videos.sql`然后就能获得数据了.

为了简化数据库.这个表存了所有视频的数据信息.这个表的主键是`timestamp(时间戳) + aid(视频的av号)`.

爬虫会不断地爬取热门视频的数据,会记录爬取的时间戳和热门视频的相关信息,存到这个表中,所以需要使用`timestamp(时间戳) + aid(视频的av号)`作为主键.

### 字段含义

```
timestamp : 时间戳可以转换成标准时间
formatted_time : 格式化的时间
aid : 视频的av号
videos : 视频的数量
tid : 标签的编号
tname : 标签的名称
copyright : 版权状态
pic : 视频封面图片的URL
title : 视频标题
ctime : 创建时间戳
desc : 视频描述
state : 视频状态
duration : 视频时长（秒）
mission_id : 关联任务或活动的ID
pub_location : 发布地点
tnamev2 : 第二标签名称
pid_name_v2 : 父级分类名称
short_link_v2 : 视频短链接
dynamic : 动态或简介内容
stat_view : 视频播放量
stat_danmaku : 弹幕数量
stat_reply : 评论数量
stat_favorite : 收藏数量
stat_coin : 投币数量
stat_share : 分享数量
stat_now_rank : 当前排名
stat_his_rank : 历史最高排名
stat_like : 点赞数量
stat_dislike : 点踩数量
stat_vt : 未知统计指标
stat_vv : 视频播放量（重复字段）
stat_fav_g : 未知收藏统计
stat_like_g : 未知点赞统计
owner_mid : 视频作者的ID
owner_name : 视频作者名称
owner_face : 作者头像的URL
tags : 视频标签   (如果需要使用,请自行提取.所有标签蹦整合为一个字符串,不同标签之间用","分隔)
```

---

当前的.sql文件,只是一个预览版的(主要用于确定格式),后续数据量还会增加.

数据爬取的内容,只涉及到`fetch_hot.py`这个文件

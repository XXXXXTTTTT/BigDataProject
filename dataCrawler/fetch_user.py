from bilibili_api import user
import asyncio
import json
from typing import List, Dict
import asyncio
from bilibili_api import video, Credential
from typing import List, Dict, Union

async def fetch_all_videos(u:user.User)->List[str]:
    page = 1
    videos = []
    while True:
        result = await u.get_videos(pn=page, ps=50, order=user.VideoOrder.PUBDATE)
        video_list = result.get('list', {}).get('vlist', [])
        if not video_list:
            break
        videos.extend(video_list)
        page += 1
    
    bvids = []
    for v in videos:
        bv = v.get("bvid","")
        bvids.append(bv)
    
    return bvids

async def get_video_stats(video_ids: List[Union[str, int]], credential: Credential = None) -> Dict:
    """
    统计视频列表的播放量、点赞数、投币数、收藏数、转发数、评论数、弹幕数量等信息。

    Args:
        video_ids (List[Union[str, int]]): 视频的 BV 号或 AID 列表。
        credential (Credential, optional): Bilibili API 凭据。默认为 None。

    Returns:
        Dict: 包含视频总数和每个视频的统计数据的字典。
    """
    stats = {
        "total_videos": len(video_ids),
        "total_view": 0,  # 总播放量
        "total_like": 0,  # 总点赞数
        "total_coin": 0,  # 总投币数
        "total_favorite": 0,  # 总收藏数
        "total_share": 0,  # 总转发数
        "total_comment": 0,  # 总评论数
        "total_danmaku": 0,  # 总弹幕数
        "total_duration": 0,  # 总视频时长（秒）
        "total_chargers": 0,  # 总充电人数
        "total_videos_count": 0,  # 总分P数
        "errors":[]
    }

    for vid in video_ids:
        try:
            # 初始化 Video 对象
            v = video.Video(bvid=vid if isinstance(vid, str) else None,
                           aid=vid if isinstance(vid, int) else None,
                           credential=credential)
            
            # 获取视频信息
            info = await v.get_info()
            
            # 获取充电信息
            chargers = await v.get_chargers()
            
            # 获取标签
            tags = await v.get_tags()
            
            # 获取视频统计数据
            stat = info.get('stat', {})
            video_stat = {
                "bvid": info.get('bvid', ''),
                "aid": info.get('aid', 0),
                "title": info.get('title', ''),
                "view": stat.get('view', 0),  # 播放量
                "like": stat.get('like', 0),  # 点赞数
                "coin": stat.get('coin', 0),  # 投币数
                "favorite": stat.get('favorite', 0),  # 收藏数
                "share": stat.get('share', 0),  # 转发数
                "comment": stat.get('reply', 0),  # 评论数
                "danmaku": stat.get('danmaku', 0),  # 弹幕数（直接从 info 获取）
                "duration": info.get('duration', 0),  # 视频时长（秒）
                "videos_count": info.get('videos', 0),  # 分P数
                "upload_time": info.get('pubdate', 0),  # 上传时间（时间戳）
                "create_time": info.get('ctime', 0),  # 创建时间（时间戳）
                "uploader_mid": info.get('owner', {}).get('mid', 0),  # UP主 MID
                "uploader_name": info.get('owner', {}).get('name', ''),  # UP主名字
                "category": info.get('tname', ''),  # 分区
                "category_id": info.get('tid', 0),  # 分区ID
                "category_v2": info.get('tname_v2', ''),  # 二级分区
                "category_id_v2": info.get('tid_v2', 0),  # 二级分区ID
            }

            # 更新总统计
            stats["total_view"] += video_stat["view"]
            stats["total_like"] += video_stat["like"]
            stats["total_coin"] += video_stat["coin"]
            stats["total_favorite"] += video_stat["favorite"]
            stats["total_share"] += video_stat["share"]
            stats["total_comment"] += video_stat["comment"]
            stats["total_danmaku"] += video_stat["danmaku"]
            stats["total_duration"] += video_stat["duration"]
            stats["total_videos_count"] += video_stat["videos_count"]

            # stats["videos"].append(video_stat)

        except Exception as e:
            # 记录错误但继续处理其他视频
            stats["errors"].append({
                "bvid": vid if isinstance(vid, str) else '',
                "aid": vid if isinstance(vid, int) else 0,
                "error": str(e)
            })

    return stats


async def fetch_user_info(uid:str):
    """
    这个是对外暴露的接口
    返回数据格式如下:
    {
    "uid": 400482416,
    "followers": 32,
    "total_videos": 2,
    "total_view": 15954,
    "total_like": 101,
    "total_coin": 25,
    "total_favorite": 30,
    "total_share": 42,
    "total_comment": 37,
    "total_danmaku": 41,
    "total_duration": 5311,
    "total_chargers": 0,
    "total_videos_count": 2,
    "errors": []
    }
    """
    res = {}
    u = user.User(uid=uid)
    realation = await u.get_relation_info()
    res["uid"] = uid
    res["followers"] = realation["follower"]
    
    bvids = await fetch_all_videos(u)
    video_statistic = await get_video_stats(bvids)
    res.update(video_statistic)
    return res
    

if __name__ == '__main__':
    async def main():
        uid = 400482416
        res = await fetch_user_info(uid=uid)
        print(json.dumps(res,indent=2))
    asyncio.run(main())
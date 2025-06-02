import asyncio
from bilibili_api import video, Credential
from typing import List, Dict, Union
from uuid import uuid4

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
        "videos": [],
        "summary": {
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
        }
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
            stats["summary"]["total_view"] += video_stat["view"]
            stats["summary"]["total_like"] += video_stat["like"]
            stats["summary"]["total_coin"] += video_stat["coin"]
            stats["summary"]["total_favorite"] += video_stat["favorite"]
            stats["summary"]["total_share"] += video_stat["share"]
            stats["summary"]["total_comment"] += video_stat["comment"]
            stats["summary"]["total_danmaku"] += video_stat["danmaku"]
            stats["summary"]["total_duration"] += video_stat["duration"]
            stats["summary"]["total_videos_count"] += video_stat["videos_count"]

            # stats["videos"].append(video_stat)

        except Exception as e:
            # 记录错误但继续处理其他视频
            stats["videos"].append({
                "bvid": vid if isinstance(vid, str) else '',
                "aid": vid if isinstance(vid, int) else 0,
                "error": str(e)
            })

    return stats

# 示例使用
async def main():
    # 示例视频列表（可以是 BV 号或 AID）
    video_ids = ["BV1Vf4y1V7ra", "BV1gy4y1L7qf"]
    # 可选：提供凭据以访问更多数据
    credential = Credential(
        sessdata="",
        bili_jct="",
        buvid3=""
    )
    result = await get_video_stats(video_ids,credential)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())






example = {
  "total_videos": int,  # 视频总数
  "videos": [
    {
      "bvid": str,  # BV 号
      "aid": int,  # AID
      "title": str,  # 视频标题
      "view": int,  # 播放量
      "like": int,  # 点赞数
      "coin": int,  # 投币数
      "favorite": int,  # 收藏数
      "share": int,  # 转发数
      "comment": int,  # 评论数
      "danmaku": int,  # 弹幕数
      "duration": int,  # 视频时长（秒）
      "videos_count": int,  # 分P数
      "upload_time": int,  # 上传时间（时间戳）
      "create_time": int,  # 创建时间（时间戳）
      "uploader_mid": int,  # UP主 MID
      "uploader_name": str,  # UP主名字
      "category": str,  # 分区
      "category_id": int,  # 分区ID
      "category_v2": str,  # 二级分区
      "category_id_v2": int,  # 二级分区ID
      "copyright": int,  # 版权类型（1: 自制, 2: 转载）
      "description": str,  # 视频描述
      "tags": List[str],  # 标签列表
      "cover_url": str,  # 封面URL
      "dimension": Dict,  # 分辨率信息
      "is_favored": bool,  # 是否已收藏
      "is_liked": bool,  # 是否已点赞
      "chargers_count": int,  # 充电人数
      "rights": Dict,  # 权限设置
      "is_episode": bool,  # 是否为番剧
      "is_forbid_note": bool,  # 是否禁止笔记
      "error": str  # 如果获取失败，记录错误信息
    },
    ...
  ],
  "summary": {
    "total_view": int,  # 总播放量
    "total_like": int,  # 总点赞数
    "total_coin": int,  # 总投币数
    "total_favorite": int,  # 总收藏数
    "total_share": int,  # 总转发数
    "total_comment": int,  # 总评论数
    "total_danmaku": int,  # 总弹幕数
    "total_duration": int,  # 总视频时长（秒）
    "total_chargers": int,  # 总充电人数
    "total_videos_count": int  # 总分P数
  }
}
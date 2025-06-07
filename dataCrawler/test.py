import time
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
    
    print(json.dumps(videos,indent=2))
    bvids = []
    for v in videos:
        bv = v.get("bvid","")
        bvids.append(bv)
        
    return bvids

u = user.User(uid="546195")
asyncio.run(fetch_all_videos(u))
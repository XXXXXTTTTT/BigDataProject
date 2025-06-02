import asyncio
import json
from bilibili_api import video


async def main() -> None:
    # 实例化 Video 类
    v = video.Video(bvid="BV1uv411q7Mv")
    # 获取信息
    info = await v.get_info()
    # 打印信息
    print(json.dumps(info,indent=4))


if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import aiohttp
import json
from typing import List, Dict, Any
import time
import logging
import ssl

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CommentCrawler:
    def __init__(self, max_concurrent: int = 5, request_delay: float = 1.0):
        """
        初始化爬虫
        :param max_concurrent: 最大并发数
        :param request_delay: 请求间隔时间（秒）
        """
        self.max_concurrent = max_concurrent
        self.request_delay = request_delay
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session = None
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        # 创建SSL上下文，跳过证书验证
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        connector = aiohttp.TCPConnector(
            limit=100, 
            limit_per_host=30,
            ssl=ssl_context,  # 使用自定义SSL上下文
            force_close=True,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(
            total=30,
            connect=10,
            sock_read=10
        )
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=self.headers,
            trust_env=True  # 信任环境变量中的代理设置
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    async def fetch_user_comments(self, uid: str, pn: int = 1, ps: int = 100) -> Dict[str, Any]:
        """
        获取单个用户的评论信息
        :param uid: 用户ID
        :param pn: 页码
        :param ps: 每页数量
        :return: 评论数据
        """
        async with self.semaphore:  # 控制并发数
            try:
                url = f"https://api.aicu.cc/api/v3/search/getreply?uid={uid}&pn={pn}&ps={ps}&mode=0&keyword="
                
                logger.info(f"正在请求用户 {uid} 的评论数据...")
                
                # 添加重试机制
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        async with self.session.get(
                            url,
                            ssl=False,  # 跳过SSL验证
                            allow_redirects=True
                        ) as response:
                            if response.status == 200:
                                # 尝试解析JSON
                                try:
                                    data = await response.json()
                                except json.JSONDecodeError:
                                    # 如果JSON解析失败，获取原始文本
                                    text = await response.text()
                                    logger.warning(f"用户 {uid} JSON解析失败，原始响应: {text[:200]}...")
                                    return {
                                        'uid': uid,
                                        'success': False,
                                        'data': None,
                                        'error': 'JSON解析失败'
                                    }
                                
                                comment_count = data.get('data', {}).get('cursor', {}).get('all_count', 0)
                                logger.info(f"用户 {uid} 评论获取成功，共 {comment_count} 条评论")
                                return {
                                    'uid': uid,
                                    'success': True,
                                    'data': data,
                                    'error': None
                                }
                            else:
                                logger.warning(f"用户 {uid} 请求失败，状态码: {response.status}")
                                if attempt < max_retries - 1:
                                    await asyncio.sleep(2 ** attempt)  # 指数退避
                                    continue
                                return {
                                    'uid': uid,
                                    'success': False,
                                    'data': None,
                                    'error': f"HTTP {response.status}"
                                }
                    except aiohttp.ClientError as e:
                        logger.warning(f"用户 {uid} 连接错误 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                        if attempt < max_retries - 1:
                            await asyncio.sleep(2 ** attempt)  # 指数退避
                            continue
                        return {
                            'uid': uid,
                            'success': False,
                            'data': None,
                            'error': f"连接失败: {str(e)}"
                        }
                        
            except Exception as e:
                logger.error(f"用户 {uid} 请求异常: {str(e)}")
                return {
                    'uid': uid,
                    'success': False,
                    'data': None,
                    'error': str(e)
                }
            finally:
                # 请求间隔
                await asyncio.sleep(self.request_delay)
    
    async def crawl_multiple_users(self, uid_list: List[str]) -> List[Dict[str, Any]]:
        """
        批量爬取多个用户的评论信息
        :param uid_list: 用户ID列表
        :return: 所有用户的评论数据列表
        """
        logger.info(f"开始爬取 {len(uid_list)} 个用户的评论数据，最大并发数: {self.max_concurrent}")
        
        # 分批处理，避免一次性创建太多任务
        batch_size = 10
        all_results = []
        
        for i in range(0, len(uid_list), batch_size):
            batch = uid_list[i:i + batch_size]
            logger.info(f"处理批次 {i//batch_size + 1}，用户数: {len(batch)}")
            
            # 创建当前批次的任务
            tasks = [self.fetch_user_comments(uid) for uid in batch]
            
            # 执行当前批次
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 处理异常结果
            for j, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    all_results.append({
                        'uid': batch[j],
                        'success': False,
                        'data': None,
                        'error': str(result)
                    })
                else:
                    all_results.append(result)
            
            # 批次间休息
            if i + batch_size < len(uid_list):
                await asyncio.sleep(2)
        
        # 统计结果
        success_count = sum(1 for r in all_results if r['success'])
        logger.info(f"爬取完成，成功: {success_count}/{len(uid_list)}")
        
        return all_results
    
    def save_results(self, results: List[Dict[str, Any]], filename: str = "comments_data.json"):
        """
        保存结果到文件
        :param results: 爬取结果
        :param filename: 保存文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            logger.info(f"结果已保存到 {filename}")
        except Exception as e:
            logger.error(f"保存文件失败: {str(e)}")

async def main():
    """主函数示例"""
    # 示例用户ID列表
    uid_list = [
        "400482416",
        "123456789",
        "987654321",
        # 添加更多用户ID...
    ]
    
    # 使用爬虫
    async with CommentCrawler(max_concurrent=5, request_delay=1.0) as crawler:
        results = await crawler.crawl_multiple_users(uid_list)
        
        # 保存结果
        crawler.save_results(results)
        
        # 打印统计信息
        success_results = [r for r in results if r['success']]
        failed_results = [r for r in results if not r['success']]
        
        print(f"\n=== 爬取结果统计 ===")
        print(f"总用户数: {len(uid_list)}")
        print(f"成功: {len(success_results)}")
        print(f"失败: {len(failed_results)}")
        
        if success_results:
            print(f"\n=== 成功的用户 ===")
            for result in success_results:
                comment_count = result['data'].get('data', {}).get('cursor', {}).get('all_count', 0)
                print(f"用户 {result['uid']}: {comment_count} 条评论")
        
        if failed_results:
            print(f"\n=== 失败的用户 ===")
            for result in failed_results:
                print(f"用户 {result['uid']}: {result['error']}")

if __name__ == "__main__":
    # 运行爬虫
    asyncio.run(main())
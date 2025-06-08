import asyncio
import time

async def func():
    await asyncio.sleep(1)
    
async def main():
    cnt = 10
    start = time.time()
    while cnt > 0:
        await func()
        print(f"--cnt--{cnt}")
        cnt -= 1
    print(f'--cost--{time.time() - start}')
    
asyncio.run(main())
import json

import aiofiles as aiofiles
import requests
import asyncio
import aiohttp

"""

"""


async def aioDownload(cid, b_id, title):
    data = {
        "book_id": b_id,
        "cid": f"{b_id}|{cid}",
        "need_bookinfo": 1
    }
    data = json.dumps(data)
    url = f"http://dushu.baidu.com/api/pc/getChapterContent?data={data}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            dic = await resp.json()

            async with aiofiles.open("txt/" + title + ".txt", mode="w", encoding="utf-8") as f:
                await f.write(dic['data']['novel']['content'])  # 把小说内容写出


async def getCatalog(url):
    resp = requests.get(url)
    items = resp.json()["data"]["novel"]["items"]
    tasks = []
    for item in items:
        title = item["title"]
        cid = item["cid"]
        # 准备异步任务
        print(title, cid)
        task = asyncio.create_task(aioDownload(cid, b_id, title))
        tasks.append(task)
    await asyncio.wait(tasks)


if __name__ == '__main__':
    # b_id = "4306063500"
    b_id = "4295084047"
    url = 'http://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"' + b_id + '"}'
    asyncio.run(getCatalog(url))
# https://dushu.baidu.com/api/pc/getDetail?data={%22book_id%22:%224295084047%22}

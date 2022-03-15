# 部分弹幕功能代码来自项目：https://github.com/IsoaSFlus/danmaku，感谢大佬
# 快手弹幕代码来源及思路：https://github.com/py-wuhao/ks_barrage，感谢大佬
# 仅抓取用户弹幕，不包括入场提醒、礼物赠送等。

import asyncio
import json

import danmaku
import websockets
import time

async def printer(q):
    while True:
        m = await q.get()
        if m['msg_type'] == 'danmaku':
            print(f'{m["name"]}：{m["content"]}')


async def wsPrinter(websocket, q):
    while True:
        m = await q.get()
        if m['msg_type'] == 'danmaku':
            print(f'用户{m["name"]}弹幕：{m["content"]} {time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())}')
            dumped = json.dumps(m, separators=(',', ':'), ensure_ascii=False)
            await websocket.send(dumped)


async def main(url):
    q = asyncio.Queue()
    dmc = danmaku.DanmakuClient(url, q)
    asyncio.create_task(printer(q))
    await dmc.start()


async def ws_handler(websocket, path):
    while True:
        """
        直播间地址
        """
        room_path = path[1:]
        q = asyncio.Queue()
        dmc = danmaku.DanmakuClient(room_path, q)
        asyncio.create_task(wsPrinter(websocket, q))
        await dmc.start()


start_server = websockets.serve(ws_handler, 'localhost', 7852)
print("listen on localhost:7852")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

# a = input('请输入直播间地址：\n')
# asyncio.run(main(a))

# 虎牙直播：https://www.huya.com/11352915
# 斗鱼直播：https://www.douyu.com/85894
# B站直播：https://live.bilibili.com/70155
# 快手直播：https://live.kuaishou.com/u/jjworld126
# 火猫直播：
# 企鹅电竞：https://egame.qq.com/383204988
# 花椒直播：https://www.huajiao.com/l/303344861?qd=hu
# 映客直播：https://www.inke.cn/liveroom/index.html?uid=87493223&id=1593906372018299
# CC直播：https://cc.163.com/363936598/
# 酷狗直播：https://fanxing.kugou.com/1676290
# 战旗直播：
# 龙珠直播：http://star.longzhu.com/wsde135864219
# PPS奇秀直播：https://x.pps.tv/room/208337
# 搜狐千帆直播：https://qf.56.com/520208a
# 来疯直播：https://v.laifeng.com/656428
# LOOK直播：https://look.163.com/live?id=196257915
# AcFun直播：https://live.acfun.cn/live/23682490
# 艺气山直播：http://www.173.com/96

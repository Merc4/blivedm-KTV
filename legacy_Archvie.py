import sys
import time
import asyncio
import aiohttp
import zlib

from aiowebsocket.converses import AioWebSocket
import json

remote = 'ws://broadcastlv.chat.bilibili.com:2244/sub'
roomid = '2171056'

data_raw = '000000{headerLen}0010000100000007000000017b22726f6f6d6964223a{roomid}7d'
data_raw = data_raw.format(headerLen=hex(27 + len(roomid))[2:],
                           roomid=''.join(map(lambda x: hex(ord(x))[2:], list(roomid))))

async def startup():
    async with AioWebSocket(remote) as aws:
        converse = aws.manipulator
        await converse.send(bytes.fromhex(data_raw))
        tasks = [receDM(converse), sendHeartBeat(converse)]
        await asyncio.wait(tasks)

hb='00 00 00 10 00 10 00 01  00 00 00 02 00 00 00 01'
async def sendHeartBeat(websocket):
    while True:
        await asyncio.sleep(30)
        await websocket.send(bytes.fromhex(hb))
        print('[Notice] Sent HeartBeat.')

async def receDM(websocket):
    while True:
        recv_text = await websocket.receive()

        if recv_text == None:
            recv_text = b'\x00\x00\x00\x1a\x00\x10\x00\x01\x00\x00\x00\x08\x00\x00\x00\x01{"code":0}'

        printDM(recv_text)


# 数据包传入：
def printDM(data):
    # 获取数据包的长度，版本和操作类型
    packetLen = int(data[:4].hex(), 16)
    ver = int(data[6:8].hex(), 16)
    op = int(data[8:12].hex(), 16)

    if (len(data) > packetLen):
        printDM(data[packetLen:])
        data = data[:packetLen]

    if (ver == 2):
        data = zlib.decompress(data[16:])
        printDM(data)
        return

    if (op == 5):
        try:
            jd = json.loads(data[16:].decode('utf-8', errors='ignore'))
            if (jd['cmd'] == 'DANMU_MSG' and '点歌' in jd['info'][1]):
                print('[点歌] ', jd['info'][2][1], ': ', jd['info'][1])
            elif (jd['cmd'] == 'SEND_GIFT'):
                print('[GITT]', jd['data']['uname'], ' ', jd['data']['action'], ' ', jd['data']['num'], 'x',
                      jd['data']['giftName'])
            elif (jd['cmd'] == 'LIVE'):
                print('[Notice] LIVE Start!')
            elif (jd['cmd'] == 'PREPARING'):
                print('[Notice] LIVE Ended!')
                
        except Exception as e:
            pass
if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(startup())
    except Exception as e:
        print('退出')
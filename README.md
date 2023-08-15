# blivedm
本项目fork自xfgryujk，在其基础上增加了一条筛选语句。

```python
    # # 仅Print带有‘点歌’字样的弹幕
    async def _on_danmaku(self, client: blivedm.BLiveClient, message: blivedm.DanmakuMessage):
     if "点歌" in message.msg:
        print(f'[{client.room_id}] {message.uname}：{message.msg}')
```
----------------------

关于使用blivedm的使用，协议解释，请参考xfgryujk的博客。

Python获取bilibili直播弹幕的库，使用WebSocket协议

[协议解释](https://blog.csdn.net/xfgryujk/article/details/80306776)（有点过时了，总体是没错的）

基于本库开发的一个应用：[blivechat](https://github.com/xfgryujk/blivechat)

## 使用说明

1. 需要Python 3.8及以上版本
2. 安装依赖

    ```sh
    pip install -r requirements.txt
    ```

3. 例程看[sample.py](./sample.py)

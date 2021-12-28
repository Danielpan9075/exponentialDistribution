from refreshRate import refresh
from aiohttp import web


async def postRefresh(request):
    try:
        try:
            data = await request.json()
        except:
            data = {}

        fieldsList = ['douyin_user_id', 'likes_count', 'comment_count', 'download_count', 'share_count', 'collect_count', 'create_time']
        if False in map(lambda x: x in data and len(str(data[x]).strip()) > 0 and isinstance(data[x], int), fieldsList):
            return web.json_response({
                "code": -1,
                "message": "失败",
                "data": "参数错误"
            })

        if not data:
            return web.json_response({
                "code": -1,
                "message": "失败",
                "data": "参数不全"
            })
        getInterval = refresh(data)
        rsp = {
            "code": 1,
            "message": "成功",
            "douyinUserId": getInterval.uid,
            "nextUpdateTime": getInterval.nextUpdateTime
        }
        return web.json_response(rsp)

    except Exception as e:
        rsp = {
            "code": -1,
            "message": "失败",
            "data": str(e),
        }
        print('postRefresh error ==> {} {}'.format(
            request.transport.get_extra_info('peername'), str(e)))
        return web.json_response(rsp)


app = web.Application()
app.router.add_post('/dyOpusRefresh', postRefresh)


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5050)

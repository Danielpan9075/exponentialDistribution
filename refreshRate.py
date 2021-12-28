import time
import numpy as np
# import matplotlib.pyplot as plt

"""
设计一个算法，现在需要根据抖音作品的参数，来设定作品的更新频率，抖音作品有以下参数
1.点赞 2.评论 3.下载 4.分享 5.收藏 6.发布时间
暂定最快的更新频率为10分钟，最慢的更新频率为24小时，以10分钟为步长，当每次更新抖音作品信息时，算法需要给出下次更新的间隔
"""


class refresh(object):
    def __init__(self, sourceDate):
        self.uid = sourceDate['douyin_user_id']
        self.likesCount = sourceDate['likes_count']
        self.commentCount = sourceDate['comment_count']
        self.downloadCount = sourceDate['download_count']
        self.shareCount = sourceDate['share_count']
        self.collectCount = sourceDate['collect_count']
        self.minDuration = 10
        self.maxDuration = 1450
        self.createTime = sourceDate['create_time']
        self.currentTime = int(time.time())
        self.calcIncterval()

    def calcIncterval(self):
        # 发布时间大于90天，24小时更新
        if self.createTime < int(time.time()) - 7776000:
            print(self.createTime, '<', int(time.time()) - 7776000)
            self.nextUpdateTime = 1440
            return
        # 指数分布系数
        lambd = 0.005
        x = np.arange(self.minDuration, self.maxDuration, 10)
        y = lambd * np.exp(-lambd * x)
        # arrayy = list(map(lambda x: float('{:.10f}'.format(x)), y))
        # print(arrayy)
        # plt.plot(x, y)
        # plt.show()

        # 每分钟互动次数
        interaction = sum(
            [self.likesCount, self.commentCount, self.downloadCount, self.shareCount, self.collectCount]) / \
                      ((self.currentTime - self.createTime) / 60) / 100000

        idy = self.closest(y, interaction)
        ind = np.where(y == idy)
        self.nextUpdateTime = int(x[ind][0])

    # 返回mylist中最接近Number的值
    def closest(self, mylist, Number):
        answer = []
        for i in mylist:
            answer.append(abs(Number - i))
        return mylist[answer.index(min(answer))]

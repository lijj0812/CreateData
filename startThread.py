import threading
#from createProfile import createPro
from createAccCon2 import createAccAndContact
# -*- coding: utf-8 -*-


class Test(threading.Thread):

    # TODO 初始化参数
    def __init__(self, times):
        threading.Thread.__init__(self)
        self.times = times

    # TODO 逻辑代码
    def run(self):
        # 创建设备档案***
        #createPro()
        # 创建设备联系人
        createAccAndContact()

    # TODO 资源回收
    def __del__(self):
        pass


def run():
    mythreads = []
    # 线程数设置
    lites = 30
    # 创建多线程
    for item in range(lites):
        try:
            task_item = Test(item)
            task_item.start()
            mythreads.append(task_item)
        except BaseException:
            raise

    for thread in mythreads:
        thread.join()


if __name__ == '__main__':
    run()

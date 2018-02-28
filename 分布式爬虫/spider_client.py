# coding:utf-8
import os
import random, time  # 随机数，时间
import queue  # 队列
import re
import multiprocessing  # 分布式进程
import multiprocessing.managers  # 分布式进程管理器

from sun.base_unit import *


class QueueManager(multiprocessing.managers.BaseManager):
    ''' 继承进程管理共享数据 '''
    pass

if __name__ == '__main__':
    QueueManager.register('get_task')   # 1. 注册函数，调用服务器
    QueueManager.register('get_result')
    manager = QueueManager(address=("10.36.137.37", 8848), authkey='123456')
    manager.connect()   # 2. 链接服务器

    task = manager.get_task()
    result = manager.get_result()

    for i in range(1000):
        time.sleep(1)
        try:
            url = task.get()
            print('client get', url)
            data_list = get_data_from_url(url)
            for data in data_list:
                result.put(data)
        except:
            pass
    print('main over')
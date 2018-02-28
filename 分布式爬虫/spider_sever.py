# coding:utf-8
import os
import random, time  # 随机数，时间
import queue  # 队列
import re
import multiprocessing  # 分布式进程
import multiprocessing.managers  # 分布式进程管理器

from sun.base_unit import *

task_queue = queue.Queue()  # 任务
result_queue = queue.Queue()  # 结果


def return_task():
    ''' 返回任务队列 '''
    return task_queue


def return_result():
    ''' 返回结果队列 '''


class QueueManager(multiprocessing.managers.BaseManager):
    ''' 继承进程管理共享数据 '''
    pass


if __name__ == '__main__':
    url = "http://wz.sun0769.com/html/top/report.shtml"
    TN = 10

    url_num = get_url_numbers(url)  # 获取页码数，页码会变化
    urllist = make_urllist(url_num)  # 制作url列表

    multiprocessing.freeze_support()  # 1. 开启分布式支持
    QueueManager.register('get_task', callable=return_task())  # 2. 注册函数给客户端调用
    QueueManager.register('get_result', callable=return_result())
    manager = QueueManager(address=("10.36.137.37", 8848), authkey='123456')  # 3. 创建一个管理器，设置地址与密码
    manager.start()

    task, result = manager.get_task(), manager.get_result()  # 4. 任务，结果

    # 5. 分发任务
    for url in urllist:
        print('task add data', url)
        task.put(url)

    print('=' * 25 + '=' * 25)

    filepath = "./data/cr_data.txt"
    if os.path.exists(filepath):
        os.remove(filepath)
    file = open(filepath, 'ab')

    # 6. 获取结果数据，写入文件
    while True:
        res = result.get(timeout=100)
        print('get data', res)
        if res:
            file.write(res.encode('utf-8', 'ignore'))
            file.flush()
        else:
            break

    file.close()
    manager.shutdown()  # 7. 关闭服务器

# encoding = utf-8
import time
from sun.base_unit import *
import gevent
import gevent.monkey


def coroutine(urllist,file):
    for url in urllist:
        data_list = get_data_from_url(url)
        for data in data_list:
            file.write(data.encode('utf-8','ignore'))
        time.sleep(1)

if __name__ == '__main__':
    url = "http://wz.sun0769.com/html/top/report.shtml"
    TN = 10

    url_num = get_url_numbers(url)  # 获取页码数，页码会变化
    urllist = make_urllist(url_num)  # 制作url列表
    urllist_task = division_urllist(urllist, TN)  # 分解任务

    filepath = "./data/cr_data.txt"
    if os.path.exists(filepath):
        os.remove(filepath)
    file = open(filepath,'ab')

    task_list = []
    for i in range(TN):
        task = gevent.spawn(coroutine, urllist_task[i][:10],file)
        task_list.append(task)
    gevent.joinall(task_list)    #
    gevent.monkey.patch_all()   # 自动切换

    file.close()

    print('main over')
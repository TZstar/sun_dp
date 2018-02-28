# encoding = utf-8
import time
from sun.base_unit import *
import multiprocessing


def download(urllist,queue):
    for url in urllist:
        data_list = get_data_from_url(url)
        print(os.getpid(),'get data')
        for data in data_list:
            queue.put(data)   # 压入数据
        print(os.getpid(),'put data')
        time.sleep(1)

if __name__ == '__main__':
    url = "http://wz.sun0769.com/html/top/report.shtml"
    TN = 10

    url_num = get_url_numbers(url)  # 获取页码数，页码会变化
    urllist = make_urllist(url_num)  # 制作url列表
    urllist_task = division_urllist(urllist, TN)  # 分解任务

    filepath = "./data/mp_data.txt"
    if os.path.exists(filepath):
        os.remove(filepath)
    file = open(filepath,'ab')

    process_list = []
    queue = multiprocessing.Manager().Queue()  # 多进程队列

    for i in range(TN):
        process = multiprocessing.Process(target=download, args=(urllist_task[i][:3], queue))
        process.start()
        process_list.append(process)

    for p in process_list:
        p.join()   # 等待所有进程退出

    while not queue.empty():
        data = queue.get()
        file.write(data.encode('utf-8','ignore'))
        print('get',data)

    file.close()

    print('main over')
# encoding = utf-8
import time
import threading

from sun.base_unit import *

'''
多线程，线程锁式写入文件
'''

def single_threading(urllist):
    for url in urllist:
        date_list = get_data_from_url(url)  # 下载页面，存入数据到txt
        # with rlock:
        write_txt(date_list, filepath)  # 写入txt文件中
        time.sleep(1)


def single_threading_pro(urllist,file):
    for url in urllist:
        data_list = get_data_from_url(url)  # 下载页面，存入数据到txt
        with rlock:
                for data in data_list:
                    file.write(data.encode('utf-8', 'ignore'))
        time.sleep(1)


def mt1():
    global rlock, filepath
    url = "http://wz.sun0769.com/html/top/report.shtml"
    TN = 10

    rlock = threading.RLock()  # 线程锁，避免冲突
    url_num = get_url_numbers(url)  # 获取页码数，页码会变化
    urllist = make_urllist(url_num)  # 制作url列表
    urllist_task = division_urllist(urllist, TN)  # 任务分割

    filepath = "./data/mt_data.txt"

    threadlist = []
    for i in range(TN):
        mythread = threading.Thread(target=single_threading,
                                    args=(urllist_task[i][:10],))
        mythread.start()
        threadlist.append(mythread)
    for thd in threadlist:
        thd.join()


def mt2():
    global rlock, filepath
    url = "http://wz.sun0769.com/html/top/report.shtml"
    TN = 10

    rlock = threading.RLock()  # 线程锁，避免冲突
    url_num = get_url_numbers(url)  # 获取页码数，页码会变化
    urllist = make_urllist(url_num)  # 制作url列表
    urllist_task = division_urllist(urllist, TN)  # 任务分割

    filepath = "./data/mt_data.txt"
    if os.path.exists(filepath):
        os.remove(filepath)   # 如果文件存在则删除文件
    file = open(filepath, 'ab')

    threadlist = []
    for i in range(TN):
        mythread = threading.Thread(target=single_threading_pro,
                                    args=(urllist_task[i],file))
        mythread.start()
        threadlist.append(mythread)
    for thd in threadlist:
        thd.join()

    file.close()

if __name__ == '__main__':

    # mt1()  # 写入后关闭文件，相当于自带文件锁
    mt2()   # 带文件锁写入txt

    print('main over')

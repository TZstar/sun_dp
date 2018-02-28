# encoding = utf-8
import time
from sun.base_unit import *

if __name__ == '__main__':
    url = "http://wz.sun0769.com/html/top/report.shtml"
    filepath = "./data/st_data.txt"

    url_num = get_url_numbers(url)  # 获取页码数，页码会变化
    urllist = make_urllist(url_num)  # 制作url列表

    for url in urllist[:10]:
        date_list = get_data_from_url(url)  # 下载页面，存入数据到txt
        write_txt(date_list,filepath) # 写入txt文件中
        time.sleep(1)
    print('main over')
# encoding = utf-8
import os
import requests
import re
import lxml
import lxml.etree


def get_url_numbers(url):
    ''' 获取url的数量 '''

    # pagetxt = requests.get(url).text
    # print(pagetxt)  # 字符串不能正常显示，可能有故障
    pagetxt = requests.get(url).content
    # print(pagetxt.decode('GB2312',errors='ignore'))
    myxml = lxml.etree.HTML(pagetxt.decode('GB2312', errors='ignore'))

    # 获取总页码数
    url_num_text = myxml.xpath("//div[@class='pagination']/text()")[-1]
    urlre = re.compile('\d+', re.IGNORECASE)
    url_num = urlre.findall(url_num_text)[0]
    print(url_num)

    return eval(url_num)


def make_urllist(url_num):
    ''' 将页码和帖子数量，转换为对应url的格式 '''

    urllist = []
    if url_num % 30 == 0:
        for i in range(url_num // 30):
            url = 'http://wz.sun0769.com/index.php/question/report?page=' + str(i * 30)
            urllist.append(url)
    else:
        for i in range(url_num // 30 + 1):
            url = 'http://wz.sun0769.com/index.php/question/report?page=' + str(i * 30)
            urllist.append(url)
    print(len(urllist))
    # print(urllist[-1])

    return urllist


def division_urllist(urllist, n):
    ''' 将url列表分解成n个子列表'''
    url_task = [[] for i in range(n)]
    # print(url_task)

    for i in range(len(urllist)):
        url_task[i % n].append(urllist[i % n])

    # print(len(url_task[0]), url_task[0][0])
    return url_task


def get_data_from_url(url):
    ''' 获取单页面数据 '''

    print(url)
    pagetxt = requests.get(url).content
    myxml = lxml.etree.HTML(pagetxt.decode('GB2312', errors='ignore'))

    tr_list = myxml.xpath("//table[@cellpadding='0']//table[@cellpadding='1']//tr")
    # print(len(tr_list))
    # print(tr_list)

    data_list = []
    for tr in tr_list:
        try:
            id = tr.xpath('./td[1]/text()')[0]
            type = tr.xpath('./td[2]/a[1]/text()')[0]
            title = tr.xpath('./td[2]/a[2]/text()')[0]
            about = tr.xpath('./td[2]/a[3]/text()')[0]
            status = tr.xpath('./td[3]/span/text()')[0]
            name = tr.xpath('./td[4]/text()')[0]
            time = tr.xpath('./td[5]/text()')[0]
        except:
            print('error')

        print(id, type, title, about, status, name, time)
        row = ' # '.join([str(id), type, title, about, status, name, str(time),'\r\n'])
        data_list.append(row)

    # print(len(data_list))
    # print(data_list[0])
    return data_list


def write_txt(data_list, filepath):
    '''
    将数据写入到txt文件中；
    如果文件存在，则添加模式写入；如果不存在，覆写模式写入。
    '''

    if not os.path.exists(filepath):
        write_type = 'wb'
    else:
        write_type = 'ab'

    with open(filepath,write_type) as f:
        for data in data_list:
            f.write(data.encode('utf-8','ignore'))


if __name__ == '__main__':
    url = "http://wz.sun0769.com/html/top/report.shtml"
    filepath = "./data/test_data.txt"

    # url_num = get_url_numbers(url)  # 获取页码数，页码会变化
    # urllist = make_urllist(url_num)  # 制作url列表
    data_list = get_data_from_url(url)  # 下载页面，存入数据到txt
    # division_urllist(urllist, 10)   # 任务分割
    write_txt(data_list, filepath)

    print('main over')

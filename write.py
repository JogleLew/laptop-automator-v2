# -*- coding: utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup

def writeToForum(fid, tid, pid, page, cookies, msg):
    url = "http://bbs.pcbeta.com/forum.php?mod=post&action=edit&fid=" + str(fid) + "&tid=" + str(tid) + "&pid=" + str(pid) + "&page=" + str(page)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko)'}
    response = requests.get(url=url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text)
    form_hash = soup.find_all('input', attrs={'name':'formhash'})[0]['value']
    post_time = soup.find_all('input', attrs={'name':'posttime'})[0]['value']

    url2 = "http://bbs.pcbeta.com/forum.php?mod=post&action=edit&extra=&editsubmit=yes"
    headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko)', 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryqVqtFrpj2wyX6aOR'}
    data = postStr(form_hash, post_time, fid, tid, pid, page, msg).encode('gbk')
    response = requests.post(url=url2, headers=headers2, cookies=cookies, data=data)
    if response.text.find('审核') > 0:
        print('checking')
    else:
        print('pass')

def postStr(formhash, posttime, fid, tid, pid, page, msg):
    string = ""
    boundary = "------WebKitFormBoundaryqVqtFrpj2wyX6aOR\r\n"
    items = {
            "formhash": formhash,
            "posttime": posttime,
            "delattachop": "0",
            "wysiwyg": "1",
            "fid": fid,
            "tid": tid,
            "pid": pid,
            "page": page,
            "subject": "",
            "message": msg,
            "editsubmit": "true",
            "save": "0",
            "uploadalbum": "2043",
            "newalbum": "",
            "usesig": "1"
    }
    for key in items:
        string = string + boundary
        string = string + "Content-Disposition: form-data; name=\"" + key + "\"\r\n\r\n" + str(items[key]) + "\r\n"
    return string

def forumStr(datalist):
    s = ''
    for item in datalist:
        s = s + "[url=http://bbs.pcbeta.com/viewthread-" + item['tid'] + "-1-1.html]" + item['title'] + "[/url]\r\n" + "作者: [url=http://i.pcbeta.com/?" + item['uid'] + "]" + item['author'] + "[/url] | " + item['createTime'] + "\r\n\r\n"
    return s

def writeData(data, threads, cookies):
    info = threads[0].split(',')
    msg = '[align=center][color=#ff00][size=7]更新日期：' + data['lastUpdateTime'] + '[/size][/color][/align]\r\n[align=center][color=#9932cc]由Laptop Automator生成[/color][/align]'
    # print(msg)
    writeToForum(info[0], info[1], info[2], info[3], cookies, msg)
    time.sleep(3)

    keys = ['Acer', 'Asus', 'Dell', 'Hasee', 'HP', 'Lenovo']
    for i in range(len(keys)):
        key = keys[i]
        msg = "[size=5][color=#ff0000]" + key + "[/color][/size]\r\n" + forumStr(data['data'][key])
        # print(msg)
        info = threads[i + 1].split(',')
        writeToForum(info[0], info[1], info[2], info[3], cookies, msg)
        time.sleep(3)

    msg = ''
    keys = ['MSI', 'Samsung', 'Sony', 'Toshiba']
    for key in keys:
        msg = msg + "[size=5][color=#ff0000]" + key + "[/color][/size]\r\n" + forumStr(data['data'][key])
    # print(msg)
    info = threads[7].split(',')
    writeToForum(info[0], info[1], info[2], info[3], cookies, msg)
    time.sleep(3)

    key = 'Others'
    msg = "[size=5][color=#ff0000]" + key + "[/color][/size]\r\n" + forumStr(data['data'][key])
    # print(msg)
    info = threads[8].split(',')
    writeToForum(info[0], info[1], info[2], info[3], cookies, msg)



import requests
from bs4 import BeautifulSoup

def getForumPage(cookies, fid, page):
    url = "http://bbs.pcbeta.com/forum.php?mod=forumdisplay&fid=" + str(fid) + "&orderby=dateline&filter=author&orderby=dateline&page=" + str(page)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko)'}
    response = requests.get(url=url, headers=headers, cookies=cookies)
    return response.text

def handlePage(r, lastdate, end):
    result = []
    soup = BeautifulSoup(r)
    segments = soup.find_all('tbody')
    for seg in segments:
        try:
            thread_link = seg.find(class_='xst')['href']
            thread_name = seg.em.text + seg.find(class_='xst').text
            user_link = seg.cite.a['href']
            user_name = seg.cite.a.text
            thread_time = seg.find_all('em')[-1].text
            obj = {}
            obj['author'] = user_name
            obj['createTime'] = thread_time.split(' ')[0]
            if compareDate(obj['createTime'], lastdate) < 0:
                continue
            k = thread_link.split('&')
            for kk in k:
                kkk = kk.split('=')
                if len(kkk) == 2 and kkk[0] == 'tid':
                    obj['tid'] = kkk[1]
                    break
            obj['title'] = thread_name
            uid = user_link.split('-')[-1].split('.')[0]
            obj['uid'] = uid
            if obj['tid'] > end:
                result.append(obj)
        except:
            pass
    return (result, True)

def compareDate(date1, date2):
	if date1 == date2:
		return 0
	y1 = int(date1.split('-')[0])
	m1 = int(date1.split('-')[1])
	d1 = int(date1.split('-')[2])
	y2 = int(date2.split('-')[0])
	m2 = int(date2.split('-')[1])
	d2 = int(date2.split('-')[2])
	if y1 > y2 or (y1 == y2 and m1 > m2) or (y1 == y2 and m1 == m2 and d1 > d2):
		return 1
	return -1

def crawl(fid, cookies, last_date, last_tid):
    flag = True
    page = 1
    res = []
    while flag:
        r = getForumPage(cookies, fid, page)
        result, flag = handlePage(r, last_date, last_tid)
        if len(result) == 0:
            flag = False
        res = res + result
        page = page + 1
    return res

def getThreadPage(cookies, tid):
    url = "http://bbs.pcbeta.com/viewthread-" + tid + "-1-1.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko)'}
    response = requests.get(url=url, headers=headers, cookies=cookies)
    return response.text

def getThreadObj(cookies, tid):
    page = getThreadPage(cookies, tid)
    soup = BeautifulSoup(page)
    thread_link = soup.h1.find_all('a')[1]['href']
    thread_name = soup.h1.find_all('a')[0].text + soup.h1.find_all('a')[1].text
    user_link = soup.find_all('div', attrs={'class': 'authi'})[0].a['href']
    user_name = soup.find_all('div', attrs={'class': 'authi'})[0].a.text
    thread_time = soup.find_all('div', attrs={'class': 'authi'})[1].text.split(' ')[1]
    obj = {}
    obj['author'] = user_name
    obj['createTime'] = thread_time
    obj['tid'] = thread_link.split('-')[1]
    obj['title'] = thread_name
    uid = user_link.split('-')[-1].split('.')[0]
    obj['uid'] = uid
    return obj

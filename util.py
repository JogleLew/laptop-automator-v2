import json
import re

def read_fid():    
    """read fid from config/fid.txt"""
    fid = '-1'
    with open('config/fid.txt', 'r', encoding="utf-8") as f:
        r = f.read()
        fid = r
    return int(fid)

def read_cookies():
    """read cookies from config/session.txt"""
    cookies = {}
    with open('config/session.txt', 'r', encoding='utf-8') as f:
        while 1:
            line = f.readline()
            parts = line.split('=')
            if len(parts) == 2:
                cookies[parts[0].strip()] = parts[1].strip()
            if not line:
                break
    return cookies

def read_threads():
    """read threads from config/threads.txt"""
    threads = []
    with open('config/threads.txt', 'r', encoding='utf-8') as f:
        while 1:
            line = f.readline()
            threads.append(line.strip())
            if not line:
                break
    return threads

def read_value():
    """read regex and value from config/value.txt"""
    regex = {}
    with open('config/value.txt', 'r', encoding='utf-8') as f:
        while 1:
            line = f.readline()
            parts = line.split('=')
            if len(parts) == 2:
                regex[parts[0].strip()] = int(parts[1].strip())
            if not line:
                break
    return regex

def read_data():
    """read thread data from config/data.txt"""
    data = {}
    with open('config/data.txt', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    return data

def write_data(data):
    """write thread data to config/data.txt"""
    data_str = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    with open('config/data.txt', 'w', encoding='utf-8') as f:
        f.write(data_str)

def filter(all_list, regex):
    new_list = []
    for item in all_list[::-1]:
        title = item['title'].lower()
        score = 0
        for regex_exp in regex:
            count = regex[regex_exp]
            pattern = re.compile('.*?' + regex_exp + '.*?')
            match = pattern.match(title)
            if match:
                score = score + count
        if score > 0:
            new_list.append(item)
    return new_list



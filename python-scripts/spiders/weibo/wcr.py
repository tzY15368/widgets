# -*- coding: utf-8 -*-
import requests
requests.packages.urllib3.disable_warnings()

from lxml import etree

from datetime import datetime, timedelta
from wb_cookies import cookies
from threading import Thread

import csv
from queue import Queue
from math import ceil
import json
import os
import time
import re
from time import sleep
from random import randint

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie':''
}
def get_header(cookie:str):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie':cookie
    }
    return headers
def write_to_log(worker_id:int,err:str):
        with open('error_log.csv','a',encoding='utf-8-sig',newline='') as fi:
            csv_writer = csv.writer(fi)
            csv_writer.writerow([str(time.strftime("%Y-%m-%d %H:%M:%S")), worker_id,err])
            fi.close()
def write_to_csv(worker_id:int,result:list):
        with open('result.csv','a',encoding='utf-8-sig',newline='') as fi:
            csv_writer = csv.writer(fi)
            for re in result:
                csv_writer.writerow([worker_id,re])
            fi.close()
user_headers_all = []
for i in range(0,len(cookies)):
    user_headers_all.append(get_header(cookies[i]))
for u in user_headers_all:
    pass
    #print(u)
init_url = 'https://m.weibo.cn/comments/hotflow?id=4467107636950632&mid=4467107636950632&max_id_type=0'
base_url = 'https://m.weibo.cn/comments/hotflow?id=4467107636950632&mid=4467107636950632&max_id={}&max_id_type=1'
i=0
'''
try:
    r = requests.get(init_url,headers=user_headers_all[4],verify=False)
    data = json.loads(r.text)
    max_id = data['data']['max_id']
    comments = data['data']['data']
    #print(type(comments),len(comments))
    #print(comments[0])
    print('initial max id:',max_id)
    write_to_csv(4,comments)
except Exception as e:
    print('Initialization error:',repr(e))
    exit(-4)
#exit(-4)
'''
max_id_queue = Queue(maxsize=3)
max_id = '4481962490243023'
while True:
    try:
        time.sleep(1)
        worker_id = i%len(cookies)
        print('worker {} requesting url:{}'.format(worker_id,base_url.format(max_id)))
        #print(user_headers_all[worker_id])
        i = i+1
        r = requests.get(base_url.format(max_id),headers=user_headers_all[worker_id],verify=False)
        #print(r.content)
        #print(r.text)
        if r.text=='':
            print('Error: empty response. Sleeping.',end='',flush=True)
            for i in range(0,60):
                if i%10==0:
                    print('-',end='',flush=True)
                time.sleep(1)
            continue
        data = json.loads(r.text)
        if data.get('data')==None:
            print(max_id_queue.full())
            if max_id_queue.full():
                max_id = max_id_queue.get()
                time.sleep(60)
                continue
            else:
                raise ValueError('failed: ok=0 response')
        comments = data['data']['data']
        print('received {} comments'.format(len(comments)))
        write_to_csv(worker_id,comments)
        max_id = data['data']['max_id']
        if max_id_queue.full():
            max_id_queue.get()
        max_id_queue.put(max_id)
    except json.JSONDecodeError as e:
        if r.text.find('请求超时')!=-1 or r.text.find('出错了，请稍后重试')!=-1:
            continue
        else:
            print(e)
            print(r.text)
            print('previous max_id:',max_id)
            break
    except Exception as e:
        print('error:',repr(e))
        print('previous max_id:',max_id)
        print('end time: ',datetime.now().strftime('%Y-%m-%d %H:%M'))
        break    
# -*- coding: utf-8 -*-
import requests
requests.packages.urllib3.disable_warnings()

from lxml import etree

from datetime import datetime, timedelta

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
cookies = [
#r'''_ga=GA1.2.1276643117.1575426942; _T_WM=76888205938; ALF=1594780582; SCF=AsxpvoeU-pm1Zp6o1myLPVbdjnkIKBLlSzBVJtshLLmqEfPQ1v2wMGOv2E1XckB83Cw1ZFlZjjltavofGXJeYro.; SUB=_2A25z4pH5DeRhGeFN4lER8irKyD6IHXVRLD-xrDV6PUJbktANLXX7kW1NQ6N8Hy7A2IaJDr4wRjg_26OYzoTtmDd-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW5xOK.VJrbpyexEIZv-g5i5JpX5K-hUgL.FoM01Ke7eoBce0z2dJLoI7pewg4V-JHV9sHE9gBt; SUHB=0QS5J4EMH8LAGY; SSOLoginState=1592189353''',
r'''_T_WM=08f78267b3c8b3e81c5694bd749d0c72; SUB=_2A25z4pcxDeRhGeBL6VQV9S7LwjyIHXVRLDl5rDV6PUJbkdAKLUPgkW1NRzu3llWd9x3VWbQ9as4YwzSkEF4dFzBy; SUHB=0HThyw0vmdoET-; SCF=AuFHAYWcr5N7MVvhRYFgAAXIgqOt23a7o9xLpBJbIJUwPTSkSo47ZzEQf4qcLBCp-RP2ZssFXSBu-P-VVVbS5So.; SSOLoginState=1592190817''',
r'''SSOLoginState=1592190975; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803; SCF=AlJWCUzhtBahGwPw1-Ld0XoCpr2_afMRDbWuxGGs2AJhFSNZX0OwNOAbAib2Q48ivlQSm7UF_JrIz_zXMAyn3gM.; SUHB=0HTRywznSdNbb2; _T_WM=59182846185; SUB=_2A25z4pevDeRhGeBL6VQW9CbPzDmIHXVRLDnnrDV6PUJbkdANLRmlkW1NRzurGyMaFi1rMxWpkcF4fo2FCf04pXa4; MLOGIN=0''',
r'''_T_WM=0fc358d6de2b169b49cba779c156be20; SUB=_2A25z4pgyDeRhGeBL6VQV9CzMyzSIHXVRLDh6rDV6PUJbkdANLXfekW1NRzupHVs14cdDcKvUEbzDBs9qWqU_a0g7; SUHB=0tKqdVfp1t9Ki9; SCF=ApOHqsywZ4KV37HTOTydFVFRrsTEpKOOO3bB8gEZz-3wLLzlIXgPRXeLYuZtAeCSJBnWxWX4O-CwF73ViXHDo9I.; SSOLoginState=1592191074''',
r'''_T_WM=cfd63a6ea056ffc64049dd6a13f84df4; SUB=_2A25z4pj0DeRhGeBL6VQW9CvJwzSIHXVRLDi8rDV6PUJbkdANLRDHkW1NRzupXTuLdQAqp6vNSWRj0ehdJkvIW3y3; SUHB=0sqxgRgmqJ8LFw; SCF=Ak_xlUZColY07f0BqHEuXfjKD1bxebujP_TfPGjVBJlHz6wiu2hFP6ux1nVIj2RHKYR5c1c64ojgtWP_bY4V0uU.; SSOLoginState=1592191140''',
r'''_T_WM=b5f5f1cea8af590b0cc950ffd4a9abf9; SUB=_2A25z4pihDeRhGeBL6VQV8ybEzDmIHXVRLDjprDV6PUJbkdAKLU7SkW1NRzuusgS0dua4NdphPIxs_mwMJAoVW8Fv; SUHB=0oUoosUwsYVVsl;SCF=AkkkLfVwaGsPIdkMij8SP5Ci_p4yMk288fJhRsFyFQTZECR1Hn3Q-xEYwSfnaBaIJ-Gcjk4QD7hUQYsu68ng75I.; SSOLoginState=1592191217''',

]
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
max_id = '4485793948706354'
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
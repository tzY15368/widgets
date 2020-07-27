import redis
import requests
import pymysql,random,time,hashlib,csv
import Queue
from datetime import datetime, timedelta
import json
import os
import time
import re
from time import sleep
from random import randint
import threading

db = pymysql.connect("localhost","root","****")
r = redis.Redis(host='localhost',port=6379,decode_responses=True,password='****')
cursor = db.cursor()

uid = "4467107636950632"
max_id_type=0
i=0
init_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type={}'
base_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=1'
user_url = 'https://m.weibo.cn/api/container/getIndex?\
containerid=230283{}-_INFO'
cookies = ['*']
proxies = ['*']
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie':''
}
sql = "CREATE DATABASE "+uid
try:
    cursor.execute(sql)
except Exception as e:
    print(repr(e))
sql = """CREATE TABLE `comments` (
  `id` int NOT NULL,
  `er_id` bigint DEFAULT NULL,
  `acc_age_x` int DEFAULT NULL,
  `age_x` int DEFAULT NULL,
  `location` varchar(3) DEFAULT NULL,
  `floor_nuumber` int DEFAULT NULL,
  `created_at` varchar(30) DEFAULT NULL,
  `text` varchar(728) DEFAULT NULL,
  `user_name` varchar(19) DEFAULT NULL,
  `user_gender` varchar(1) DEFAULT NULL,
  `user_avt` varchar(138) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
try:
    cursor.execute(sql)
except Exception as e:
    print(repr(e))
max_id_queue = Queue(maxsize=3)

def get_header(cookie:str):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie':cookie
    }
    return headers
def get_proxy(i:int):
    return {'https':"http://"+proxies[i]}
async def write_to_log(worker_id:int,err:str):
        with open('error_log.csv','a',encoding='utf-8-sig',newline='') as fi:
            csv_writer = csv.writer(fi)
            await csv_writer.writerow([str(time.strftime("%Y-%m-%d %H:%M:%S")), worker_id,err])
            fi.close()
async def write_to_csv(fname:str,worker_id:int,result:list):
        with open(fname+'.csv','a',encoding='utf-8-sig',newline='') as fi:
            csv_writer = csv.writer(fi)
            if fname=='comments':
                for re in result:
                    await csv_writer.writerow([worker_id,re])
            else:
                await csv_writer.writerow([worker_id,result])
            fi.close()
async def write_to_mysql(worker_id:int,op_type:str,result_list:list):
    sql = "INSERT INTO %s.comments (craeted_at,floor_number,text,user_id,profile_img_url,user_gender)\
        VALUES (%s,%s,%s,%s,%s%s)"
    try:
        if op_type=='comment':
            await cursor.executemany(sql,result_list)
        else:
            sql = "UPDATE TABLE comments set er_id=%s,acc_age_x=%s,age_x=%s,location=%s) where user_id=%s"
            await cursor.execute(sql,result_list)
        db.commit()
    except Exception as e:
        print(repr(e))
async def redispop():
    mid =  await r.rpop('task-list')
    return json.loads(mid)
async def redispush(_type,_id):
    val = json.dumps({'type':_type,'id':_id})
    await r.lpush('task-list',val)
def age_parser(s:str):
    age = -1
    try:
        s = s.split(' ')[0]
        if len(s)>6:
            #d = parse(s.split(' ')[0]).date().strftime('%Y-%m-%d')
            d = datetime.datetime.strptime(s,'%Y-%m-%d')
            age = 2020-d.year
    except Exception as e:
        pass
        #print(e)
    return age
def parse_info(input_txt):
    data = json.loads(input_txt)
    cards = data['data']['cards']
    account_info = {}
    person_info = {}
    for c11 in cards:
        if str(c11).find('账号信息')!=-1:
            account_info = c11
        elif str(c11).find('个人信息')!=-1:
            person_info = c11
    uid,reg_time,age,location = None,None,None,None
    for c41 in account_info['card_group']:
        if c41.get('item_name')=='注册时间':
            reg_time = c41['item_content']
    for c41 in person_info['card_group']:
        if c41.get('item_name')=='生日':
            age = c41['item_content']
        if c41.get('item_name')=='所在地':
            location=c41['item_content']
    return [uid,age_parser(reg_time),age_parser(age),location]

try:
    r = requests.get(init_url.format(uid,uid,0),headers=get_header(i),verify=False,proxies=get_proxy(i))
    if r.status_code!=200:
        raise ValueError('initialization failed.')
    data = json.loads(r.text)
    max_id = data['data']['max_id']
    comments = data['data']['data']
    result_list = []
    for j in comments:
        #craeted_at,floor_number,text,user_id,profile_img_url,user_gender = 
        result_list.append(comments['created_at'],comments['floor_number'],comments['text']\
                           ,comments['user']['id'],comments['user']['profile_img_url']\
                           ,comments['user']['gender'])
    write_to_log(i,'initial max id:'+str(max_id))
    write_to_csv('comments',i,comments)
    write_to_mysql(i,result_list)
    redispush('comment',max_id)
    redispush('user',comments['user']['id'])
    i = i+1
except Exception as e:
    print(e)
    write_to_log(i,str(e))

while True:
    time.sleep(0.8)
    mid = redispop()
    if mid['type']=='comment':
        max_id_queue.put(mid['id'])
    url = base_url.format(uid,uid,mid['id']) if mid['type']=='comment' else \
        user_url.format(mid['id'])
    try:
        r = requests.get(url,headers=get_header(i),proxies=get_proxy(i))
        if r.status_code==418:
            time.sleep(60)
            continue
        elif r.status_code!=200:
            continue
        if mid['type']=='comment':
            if r.text=='':
                print('Error: empty response. Sleeping.',end='',flush=True)
                for i in range(0,60):
                    if i%10==0:
                        print('-',end='',flush=True)
                time.sleep(1)
                continue
            data = json.loads(r.text)
            if data.get('data')=None:
                if max_id_queue.full():
                    max_id = max_id_queue.get()
                    time.sleep(300)
                    print('ok=0 response')
                    redispush('comment',max_id)
                    continue
            max_id = data['data']['max_id']
            comments = data['data']['data']
            result_list = []
            for j in comments:
                #craeted_at,floor_number,text,user_id,profile_img_url,user_gender = 
                result_list.append(j['created_at'],j['floor_number'],j['text']\
                           ,j['user']['id'],j['user']['profile_img_url']\
                           ,j['user']['gender'])
                redispush('user',j['user']['id'])
            write_to_csv('comments',i,comments)
            write_to_mysql(i,result_list)
            redispush('comment',max_id)
            i = i+1
        else:
            info = parse_info(r.text)
            info.append(info[0])
            write_to_csv('users',i,info)
            write_to_mysql(i,info)
    except Exception as e:
        print(e)
        write_to_log(i,str(e))
        time.sleep(60)
        continue    
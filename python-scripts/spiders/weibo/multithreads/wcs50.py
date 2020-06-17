# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_time:      2019/8/16 16:10
# file_name:        WeiboCommentScrapy.py
# github            https://github.com/inspurer
# qq邮箱            2391527690@qq.com
# 微信公众号         月小水长(ID: inspurer)

import requests

requests.packages.urllib3.disable_warnings()

from lxml import etree

from datetime import datetime, timedelta

from threading import Thread

import csv

from math import ceil

import os
import time
import re
from time import sleep
from random import randint
cookies = [
r'''_ga=GA1.2.1276643117.1575426942; _T_WM=76888205938; ALF=1594780582; SCF=AsxpvoeU-pm1Zp6o1myLPVbdjnkIKBLlSzBVJtshLLmqEfPQ1v2wMGOv2E1XckB83Cw1ZFlZjjltavofGXJeYro.; SUB=_2A25z4pH5DeRhGeFN4lER8irKyD6IHXVRLD-xrDV6PUJbktANLXX7kW1NQ6N8Hy7A2IaJDr4wRjg_26OYzoTtmDd-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW5xOK.VJrbpyexEIZv-g5i5JpX5K-hUgL.FoM01Ke7eoBce0z2dJLoI7pewg4V-JHV9sHE9gBt; SUHB=0QS5J4EMH8LAGY; SSOLoginState=1592189353''',
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

user_headers_all = []
for i in range(0,len(cookies)):
    user_headers_all.append(get_header(cookies[i]))
for u in user_headers_all:
    print(u)
#exit()
class WeiboCommentScrapy(Thread):

    def __init__(self,wid,user_headers,worker_id):
        Thread.__init__(self)
        self.headers = user_headers
        self.worker_id = worker_id
        self.result_headers = [
            '评论者主页',
            '评论者昵称',
            '评论者性别',
            '评论者所在地',
            '评论者微博数',
            '评论者关注数',
            '评论者粉丝数',
            '评论内容',
            '评论获赞数',
            '评论发布时间',
        ]
        print('received:',wid,user_headers,worker_id)
        if not os.path.exists('comment'):
            os.mkdir('comment')
        self.wid = wid
        self.start()

    def parse_time(self,publish_time):
        publish_time = publish_time.split('来自')[0]
        if '刚刚' in publish_time:
            publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        elif '分钟' in publish_time:
            minute = publish_time[:publish_time.find('分钟')]
            minute = timedelta(minutes=int(minute))
            publish_time = (datetime.now() -
                            minute).strftime('%Y-%m-%d %H:%M')
        elif '今天' in publish_time:
            today = datetime.now().strftime('%Y-%m-%d')
            time = publish_time[3:]
            publish_time = today + ' ' + time
        elif '月' in publish_time:
            year = datetime.now().strftime('%Y')
            month = publish_time[0:2]
            day = publish_time[3:5]
            time = publish_time[7:12]
            publish_time = year + '-' + month + '-' + day + ' ' + time
        else:
            publish_time = publish_time[:16]
        return publish_time

    def getPublisherInfo(self,url):
        res = requests.get(url=url,headers=self.headers,verify=False)
        html = etree.HTML(res.text.encode('utf-8'))
        head = html.xpath("//div[@class='ut']/span[1]")[0]
        head = head.xpath('string(.)')[:-3].strip()
        keyIndex = head.index("/")
        nickName = head[0:keyIndex-2]
        sex = head[keyIndex-1:keyIndex]
        location = head[keyIndex+1:]

        footer = html.xpath("//div[@class='tip2']")[0]
        weiboNum = footer.xpath("./span[1]/text()")[0]
        weiboNum = weiboNum[3:-1]
        followingNum = footer.xpath("./a[1]/text()")[0]
        followingNum = followingNum[3:-1]
        followsNum = footer.xpath("./a[2]/text()")[0]
        followsNum = followsNum[3:-1]
        print(nickName,sex,location,weiboNum,followingNum,followsNum)
        return nickName,sex,location,weiboNum,followingNum,followsNum

    def get_one_comment_struct(self,comment):
        # xpath 中下标从 1 开始
        userURL = "https://weibo.cn/{}".format(comment.xpath(".//a[1]/@href")[0])

        content = comment.xpath(".//span[@class='ctt']/text()")
        # '回复' 或者只 @ 人
        if '回复' in content or len(content)==0:
            test = comment.xpath(".//span[@class='ctt']")
            content = test[0].xpath('string(.)').strip()

            # 以表情包开头造成的 content == 0,文字没有被子标签包裹
            if len(content)==0:
                content = comment.xpath('string(.)').strip()
                content = content[content.index(':')+1:]
        else:
            content = content[0]

        praisedNum = comment.xpath(".//span[@class='cc'][1]/a/text()")[0]
        praisedNum = praisedNum[2:praisedNum.rindex(']')]

        publish_time = comment.xpath(".//span[@class='ct']/text()")[0]

        publish_time = self.parse_time(publish_time)
        nickName,sex,location,weiboNum,followingNum,followsNum = self.getPublisherInfo(url=userURL)

        return [userURL,nickName,sex,location,weiboNum,followingNum,followsNum,content,praisedNum,publish_time]

    def write_to_csv(self,result,isHeader=False):
        with open('comment/' + self.wid + '---'+str(self.worker_id)+'.csv', 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            if isHeader == True:
                writer.writerows([self.result_headers])
            writer.writerows(result)
        print('已成功将{}条评论写入{}中'.format(len(result),'comment/' + self.wid + '----'+str(self.worker_id)+'.csv'))
    def write_to_log(self,err):
        with open('logs/error_log.csv','a',encoding='utf-8-sig') as fi:
            csv_writer = csv.writer(fi)
            csv_writer.writerow([str(time.strftime("%Y-%m-%d %H:%M:%S")), self.worker_id,err])
            fi.close()
    def run(self):
        res = requests.get('https://weibo.cn/comment/{}'.format(self.wid),headers=self.headers,verify=False)
        try:
            commentNum = re.findall("评论\[.*?\]",res.text)[0]
            commentNum = int(commentNum[3:len(commentNum)-1])
        except:
            exit(-3)
        print(commentNum)
        pageNum = ceil(commentNum/10)
        print(pageNum)
        for page in range(pageNum):
            if page<47:
                continue
            if page%len(user_headers_all)!=self.worker_id:
                continue
            try:
                result = []
                data = {'mp':100000,'page':page}
                res = requests.post('https://weibo.cn/comment/{}?uid=1139098205&rl=0'.format(self.wid), data=data,headers=self.headers,verify=False)
                #res = requests.get('https://weibo.cn/comment/{}?page={}'.format(self.wid,page+1), headers=self.headers,verify=False)
                
                html = etree.HTML(res.text.encode('utf-8'))

                comments = html.xpath("/html/body/div[starts-with(@id,'C')]")

                print('第{}/{}页'.format(page+1,pageNum))

                for i in range(len(comments)):
                    result.append(self.get_one_comment_struct(comments[i]))

                if page==0:
                    self.write_to_csv(result,isHeader=True)
                else:
                    self.write_to_csv(result,isHeader=False)
            except Exception as e:
                self.write_to_log(repr(e))
            sleep(randint(1,3))

if __name__ =="__main__":
    import threading
    worker_threads = []
    print(user_headers_all[0])
    def start_worker(id:int):
        WeiboCommentScrapy(wid='Is9M7taaY',user_headers=user_headers_all[id],worker_id=id)
    for i in range(0,len(user_headers_all)):
        t = threading.Thread(target=start_worker,args=[i])
        t.daemon=False
        t.start()
        worker_threads.append(t)
    print(len(worker_threads))
    sleep(10)
    #WeiboCommentScrapy(wid='Is9M7taaY',user_headers=user_headers_all[0],worker_id=0)


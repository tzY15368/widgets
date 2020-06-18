import requests,json,threading,csv,time
import pandas as pd

from wb_cookies import cookies
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
def write_to_csv(result:list):
        with open('result-personal-info.csv','a',encoding='utf-8-sig',newline='') as fi:
            csv_writer = csv.writer(fi)
            csv_writer.writerow(result)
            fi.close()
def fetchinfo(worker_id,id_list:list):
    print('----> worker {} received {} jobs'.format(worker_id,len(id_list)))
    covered_id = []
    i=0
    while len(id_list)!=0:
        time.sleep(0.5)
        i = i+1
        this_id = id_list.pop()
        covered_id.append(this_id)
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=230283'+str(this_id)+'_-_INFO'
        r = requests.get(url,headers=user_headers_all[worker_id])
        print('worker {}:{},{}'.format(worker_id,this_id,r.status_code))
        if str(r.status_code)=='200':
            write_to_csv([1,worker_id,this_id,r.text])
            #big_result.append([1,worker_id,this_id,r.text])
        else:
            print('--------------',r.status_code)
            write_to_csv([0,worker_id,this_id,r.text])
            #big_result.append([0,worker_id,this_id,r.text])
        if i%1000==0:
            print('worker {} progress: {}'.format(worker_id,i/len(id_list)))
    print('worker {} done.'.format(worker_id))
user_headers_all = []
for i in range(0,len(cookies)):
    user_headers_all.append(get_header(cookies[i]))
df = pd.read_csv('load_result_200k_with_id.csv')
print(df['user_id'].shape)
df_out = df['user_id'].drop_duplicates(keep='first')
print(df_out.shape)
df.to_csv('./only_ids_200k.csv',index=False,encoding="utf_8_sig")
exit(0)
id_list = list(df_out)
big_result = []
worker_threads = []
print('len of id list:{}'.format(len(id_list)))
for i in range(0,len(cookies)):
    t = threading.Thread(target=fetchinfo,args=( i%len(cookies) ,id_list[0 + i * (int(len(id_list)/len(cookies))):(0+(i+1)*(int(len(id_list)/len(cookies))) if i!=len(cookies)-1 else len(id_list))]))
    t.start()
    print('thread {} started,assigned: {} : {}'.format(i,0 + i * (int(len(id_list)/len(cookies))),(0+(i+1)*(int(len(id_list)/len(cookies))) if i!=len(cookies)-1 else len(id_list))))
    worker_threads.append(t)
print(len(big_result))

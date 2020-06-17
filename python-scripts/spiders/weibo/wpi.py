import requests,json,threading,csv,time
import pandas as pd
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

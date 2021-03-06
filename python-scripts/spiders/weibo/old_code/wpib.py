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
user_headers_all = []
for i in range(0,len(cookies)):
    user_headers_all.append(get_header(cookies[i]))
df = pd.read_csv('load_result_200k_with_id.csv')
print(df['user_id'].shape)
df_out = df['user_id'].drop_duplicates(keep='first')
print(df_out.shape)
print(df_out.iloc[0])
last_id = '1627996681'
r_start = 0
while str(df_out.iloc[r_start])!=last_id:
    r_start = r_start+1
for i in range(r_start,df.shape[0]):
    time.sleep(0.5)
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=230283'+str(df.iloc[0])+'_-_INFO'
    worker_id = i%len(cookies)
    r = requests.get(url,headers=user_headers_all[worker_id])
    if str(r.status_code)=='200':
        print('user {} done'.format(df_out.iloc[i]))
        write_to_csv([worker_id,r.text])
    else:
        print(r.status_code)
        print(r.text)
        print('---->last id: {}, termination time: {}'.format(df_out.iloc[i],str(time.strftime("%Y-%m-%d %H:%M:%S"))))
        break


    
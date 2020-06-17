import requests,json
cookie = r'''_T_WM=0fc358d6de2b169b49cba779c156be20; SUB=_2A25z4pgyDeRhGeBL6VQV9CzMyzSIHXVRLDh6rDV6PUJbkdANLXfekW1NRzupHVs14cdDcKvUEbzDBs9qWqU_a0g7; SUHB=0tKqdVfp1t9Ki9; SCF=ApOHqsywZ4KV37HTOTydFVFRrsTEpKOOO3bB8gEZz-3wLLzlIXgPRXeLYuZtAeCSJBnWxWX4O-CwF73ViXHDo9I.; SSOLoginState=1592191074'''
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie':cookie
}
id = '2704763507'
url = 'https://m.weibo.cn/api/container/getIndex?containerid=230283'+id+'_-_INFO'
r = requests.get(url,headers=headers)
print(r.text)
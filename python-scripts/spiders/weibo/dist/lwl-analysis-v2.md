```python
import pandas as pd
import json
import datetime
from dateutil.parser import parse
import re
import time
from matplotlib import pyplot as plt
import wordcloud,jieba
from PIL import Image
import collections
import numpy as np
from datetime import timezone,timedelta
```

# 数据预处理


```python
comp = re.compile('</?\w+[^>]*>')
def strip_html(s:str):
    return comp.sub('',s)
```


```python
df = pd.read_csv('lwl_raw.csv')
floor_number_list = []
created_at_list = []
text_list = []
user_name_list = []
user_gender_list = []
user_avt_list = []
user_id_list = []
for i in range(0,df.shape[0]):
    s_dict = json.loads(json.dumps(eval(df.iloc[i][1])))
    floor_number_list.append(s_dict['floor_number'])
    if i%1000==0:
        print('{}/{}'.format(i+1,df.shape[0]))
        '''
    df['floor_number'][i]=s_dict['floor_number']
    df['created_at'][i]=s_dict['created_at']
    df['text'][i] = s_dict['text']
    df['user_name'][i] = s_dict['user']['screen_name']
    df['user_gender'][i] = s_dict['user']['gender']
    df['user_avt'][i] = s_dict['user']['profile_image_url']
    df['user_id'][i] = s_dict['user']['profile_url'].split('=')[-1]
    if i%1000==0:
        print('1-{}/{}'.format(i+1,df.shape[0]))
        '''
df['floor_nuumber']=floor_number_list
del floor_number_list


for i in range(0,df.shape[0]):
    s_dict = json.loads(json.dumps(eval(df.iloc[i][1])))
    created_at_list.append(s_dict['created_at'])
    if i%1000==0:
        print('2-{}/{}'.format(i+1,df.shape[0]))
df['created_at'] = created_at_list
del created_at_list


for i in range(0,df.shape[0]):
    s_dict = json.loads(json.dumps(eval(df.iloc[i][1])))
    text_list.append(s_dict['text'])
    if i%1000==0:
        print('3-{}/{}'.format(i+1,df.shape[0]))
df['text'] = text_list
del text_list


for i in range(0,df.shape[0]):
    s_dict = json.loads(json.dumps(eval(df.iloc[i][1])))
    user_name_list.append(s_dict['user']['screen_name'])
    if i%1000==0:
        print('4-{}/{}'.format(i+1,df.shape[0]))
df['user_name'] = user_name_list
del user_name_list


for i in range(0,df.shape[0]):
    s_dict = json.loads(json.dumps(eval(df.iloc[i][1])))
    user_gender_list.append(s_dict['user']['gender'])
    if i%1000==0:
        print('5-{}/{}'.format(i+1,df.shape[0]))
df['user_gender'] = user_gender_list
del user_gender_list


for i in range(0,df.shape[0]):
    s_dict = json.loads(json.dumps(eval(df.iloc[i][1])))
    user_avt_list.append(s_dict['user']['profile_image_url'])
    if i%1000==0:
        print('6-{}/{}'.format(i+1,df.shape[0]))
df['user_avt'] = user_avt_list
del user_avt_list


for i in range(0,df.shape[0]):
    s_dict = json.loads(json.dumps(eval(df.iloc[i][1])))
    user_id_list.append(s_dict['user']['profile_url'].split('=')[-1])
    if i%1000==0:
        print('7-{}/{}'.format(i+1,df.shape[0]))
df['user_id'] = user_id_list
del user_id_list
```


```python
df_raw = pd.read_csv('lwl_raw.csv')
```


```python
df_raw.columns[0]
df = df_raw.drop(df_raw.columns[[0,1,2]],axis=1)
```


```python
df.sort_values(by="floor_nuumber",ascending=True,inplace=True)
```


```python
print(df.shape)
df_drop = df.drop_duplicates(subset=['floor_nuumber'],keep='first',inplace=False)
print(df_drop.shape)
```

    (899988, 7)
    (836689, 7)
    


```python
df_drop.head()
df_drop.drop(index=(df_drop.loc[(df_drop['floor_nuumber']==0)].index),inplace=True)
```


```python
df_drop.head()
df_drop.tail()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>floor_nuumber</th>
      <th>created_at</th>
      <th>text</th>
      <th>user_name</th>
      <th>user_gender</th>
      <th>user_avt</th>
      <th>user_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>858829</td>
      <td>953461</td>
      <td>Sun Jun 21 12:23:22 +0800 2020</td>
      <td>亮亮，节日快乐</td>
      <td>网个红</td>
      <td>m</td>
      <td>https://tvax4.sinaimg.cn/crop.0.0.996.996.180/...</td>
      <td>6036716472</td>
    </tr>
    <tr>
      <td>858828</td>
      <td>953462</td>
      <td>Sun Jun 21 12:23:27 +0800 2020</td>
      <td>李医生父亲节快乐🎉</td>
      <td>人生不过是一个轮回</td>
      <td>f</td>
      <td>https://tvax4.sinaimg.cn/crop.0.0.512.512.180/...</td>
      <td>5106420671</td>
    </tr>
    <tr>
      <td>858827</td>
      <td>953463</td>
      <td>Sun Jun 21 12:23:31 +0800 2020</td>
      <td>以前的评论看不见了？哎……消灭吐槽的声音就＝消灭了负能量。</td>
      <td>天津地产老炮</td>
      <td>m</td>
      <td>https://tvax1.sinaimg.cn/default/images/defaul...</td>
      <td>1681365414</td>
    </tr>
    <tr>
      <td>858826</td>
      <td>953464</td>
      <td>Sun Jun 21 12:23:44 +0800 2020</td>
      <td>宋木山：你体内负能量太多啦</td>
      <td>蓝玛飞蓬</td>
      <td>f</td>
      <td>https://tvax1.sinaimg.cn/default/images/defaul...</td>
      <td>7056348723</td>
    </tr>
    <tr>
      <td>858825</td>
      <td>953465</td>
      <td>Sun Jun 21 12:24:30 +0800 2020</td>
      <td>父亲节快乐！</td>
      <td>哈哈陈</td>
      <td>m</td>
      <td>https://tva3.sinaimg.cn/crop.0.0.180.180.180/5...</td>
      <td>1416936310</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_drop.to_csv('lwl-clean.csv',index=False,encoding="utf_8_sig")
```


```python
del df
df = df_drop
```

# 数据分析
--- 

## 概览
----

### 男女比


```python
m = df.loc[(df['user_gender']=='m')].shape[0]
f = df.loc[(df['user_gender']=='f')].shape[0]
print(m,f)
```

    310782 525905
    


```python
plt.rcParams['font.sans-serif']=['Microsoft YaHei'] #用来正常显示中文标签
labels = ['男','女']
sizes = (m,f)
explode = (0,0)
plt.pie(sizes,explode=explode,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150)
plt.title('800k male-to-female ratio (Feb 01 to Jun 21)')
plt.savefig('./img/mf-ratio-'+str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))+'.png',dpi=80,bbox_inches='tight')
plt.show()
```


![png](output_16_0.png)


----
### 词频与词云


```python
text_col = df['text']
print(text_col.shape)
cut_text = []
for i,text in enumerate(text_col):
    if i%100000==0:
        print('-',end='')
    cut_text.append(jieba.lcut(strip_html(text)))
print(cut_text[2])
```

    (836687,)
    ---------[]
    


```python
cut_col_list = [i for j in cut_text for i in j]
punctuation_marks = ['，',',','!','！','。','.','、','~','[',']','【','】',' ']
stop_words = open('stopwords.words','r',encoding='utf-8').read().split('\n')
cut_col_list_stripped = list(filter(lambda x:x not in punctuation_marks,cut_col_list))
cut_col_list_stripped_stopped = list(filter(lambda x:x not in stop_words,cut_col_list_stripped))
all_txt = " ".join(cut_col_list_stripped_stopped)

len(all_txt)
```




    13467446



#### 词频


```python
words_count = collections.Counter(cut_col_list_stripped_stopped)
words_count_top = words_count.most_common(20)
print(words_count_top)
print(len(cut_col_list_stripped_stopped))
```

    [('好', 193393), ('蜡烛', 174030), ('李医生', 154063), ('走', 128026), ('🙏', 117412), ('一路', 86701), ('加油', 71668), ('都', 57842), ('早日康复', 56781), ('希望', 51391), ('？', 45452), ('不', 43294), ('英雄', 42028), ('人', 41093), ('会', 40369), ('…', 38515), ('晚安', 37079), ('还', 30526), ('很', 29640), ('说', 28134)]
    4757136
    


```python
plt.figure(figsize=(20,8),dpi=80)
words = []
count = []
for (w,c) in words_count_top:
    words.append(w)
    count.append(c)
x = range(len(words))
plt.bar(x,count,width=0.5)
plt.rcParams['font.sans-serif']=['Microsoft YaHei']
plt.xticks(x,words)
plt.tick_params(labelsize=20)
plt.savefig('./img/words-freq-'+str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))+'.png',dpi=80,bbox_inches='tight')
plt.show()
```

    c:\users\nathany\appdata\local\programs\python\python37\lib\site-packages\matplotlib\backends\backend_agg.py:211: RuntimeWarning: Glyph 55357 missing from current font.
      font.set_text(s, 0.0, flags=flags)
    c:\users\nathany\appdata\local\programs\python\python37\lib\site-packages\matplotlib\backends\backend_agg.py:211: RuntimeWarning: Glyph 56911 missing from current font.
      font.set_text(s, 0.0, flags=flags)
    c:\users\nathany\appdata\local\programs\python\python37\lib\site-packages\matplotlib\backends\backend_agg.py:176: RuntimeWarning: Glyph 128591 missing from current font.
      font.load_char(ord(s), flags=flags)
    


![png](output_22_1.png)


#### 词云


```python
w = wordcloud.WordCloud(\
    width = 1000, height = 700,\
    background_color = "white",     font_path = "msyh.ttc",scale=16,collocations=False
)


w.generate_from_text(all_txt)
```




    <wordcloud.wordcloud.WordCloud at 0x2a909fcfe80>




```python
w.to_file('./img/cloud-'+str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))+'.png')
```




    <wordcloud.wordcloud.WordCloud at 0x2a909fcfe80>




```python
plt.imshow(w)
plt.axis("off")
plt.figure()
plt.show()
```


![png](output_26_0.png)



    <Figure size 432x288 with 0 Axes>


----
## 详细内容

----
### 时间序列分析

#### 评论量——日期


```python
dates = {}
for i in range(0,df.shape[0]):
    if i%100000==0:
        print('->',end='')
    d = parse(df.iloc[i]['created_at']).date().strftime('%m-%d')
    if dates.get(d)==None:
        dates[d]=1
    else:
        dates[d]+=1
```

    ->->->->->->->->->


```python
x_data = []
y_data = []
for k in dates:
    x_data.append(k)
    y_data.append(dates[k])
plt.figure(figsize=(24,8),dpi=160)
plt.plot(x_data,y_data)
plt.title('评论量')
plt.xticks(rotation=60)
plt.tick_params(labelsize=5)
plt.savefig('./img/comment-count-daily-'+str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))+'.png',dpi=160,bbox_inches='tight')
plt.show()
```


![png](output_31_0.png)


#### 评论男女比日期变化


```python
dates = {}
m_total = 1
f_total = 1
for i in range(0,df.shape[0]):
    if i%100000==0:
        print('->',end='')
    d = parse(df.iloc[i]['created_at']).date().strftime('%m-%d')
    if df.iloc[i]['user_gender']=='f':
        f_total +=1
    else:
        m_total+=1
    dates[d]=m_total/f_total
```

    ->->->->->->->->->


```python
x_data = []
y_data = []
for k in dates:
    x_data.append(k)
    y_data.append(dates[k])
plt.figure(figsize=(24,8),dpi=160)
plt.plot(x_data,y_data)
plt.title('男女比')
plt.xticks(rotation=60)
plt.tick_params(labelsize=5)
plt.savefig('./img/mf-ratio-daily-'+str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))+'.png',dpi=160,bbox_inches='tight')
plt.show()
```


![png](output_34_0.png)


#### 评论&男女比小时变化


```python
hours = {}
for i in range(0,df.shape[0]):
    if i%100000==0:
        print('->',end='')
    d = parse(df.iloc[i]['created_at'])
    d = d +timedelta(hours=8)
    h_str = d.astimezone(timezone.utc).strftime('%H')
    if hours.get(h_str)==None:
        hours[h_str]={'m':1,'f':1,'m_total':1,'f_total':1}
    else:
        hours[h_str][df.iloc[i]['user_gender']]+=1
        hours[h_str][df.iloc[i]['user_gender']+'_total']+=1
```

    ->->->->->->->->->


```python
x_data = []
y_data = []
m_data = []
f_data = []
for k in hours:
    x_data.append(k)
    y_data.append(hours[k]['m']/hours[k]['f'])
    m_data.append(hours[k]['m_total'])
    f_data.append(hours[k]['f_total'])
'''
x_data.reverse()
y_data.reverse()
f_data.reverse()
m_data.reverse()
'''
index_0 = x_data.index('00')
x_data = x_data[index_0:]+x_data[0:index_0]
y_data = y_data[index_0:]+y_data[0:index_0]
f_data = f_data[index_0:]+f_data[0:index_0]
m_data = m_data[index_0:]+m_data[0:index_0]


plt.plot(x_data,y_data)
plt.title('男女比-小时')
plt.xticks(rotation=60)
plt.tick_params(labelsize=5)
plt.savefig('./mf-ratio-hour-'+str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))+'.png',dpi=160,bbox_inches='tight')
plt.show()

width=0.25
index = np.arange(len(x_data))
plt.bar(index,m_data,width=width,label='评论数-男',color='darkorange')
plt.bar(index+width,f_data,width=width,label='评论数-女',color='green',tick_label=x_data)
plt.xticks()
plt.xlabel('时间（小时）')
plt.ylabel('评论数（条）')
plt.title('评论数-小时')
plt.legend()
plt.savefig('./img/mf-count-hour-'+str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))+'.png',dpi=160,bbox_inches='tight')
plt.show()
```


![png](output_37_0.png)



![png](output_37_1.png)


### 多次评论


```python
id_list = list(df['user_id'])
cnt = collections.Counter()
for id in id_list:
    cnt[id]+=1
#id_count = collections.Counter(id_list)
b50,b25,b5 = 0,0,0
for id in cnt:
    if cnt[id]>50:
        b50+=1
    elif cnt[id]>25:
        b25+=1
    elif cnt[id]>5:
        b5+=1
print(b50,b25,b5)

print(len(id_list),"->",len(cnt))
```

    479 788 8918
    836687 -> 561497
    


```python

```


```python
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
    return (uid,reg_time,age,location)
```


```python
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType

```


```python
udf = pd.read_csv('ids-result.csv')
```


```python
df = pd.read_csv('lwl-clean.csv')
```


```python
udf.shape
df.shape
```




    (836687, 10)




```python
udf.drop_duplicates(keep='first',inplace=True)
```


```python
udf.shape
```




    (178515, 2)




```python
df.loc[df['user_id']==6912893061,'age']=3
```


```python
udf['acc_age'] = -1
udf['age']=-1
udf['loc']=''
udf['user_id']=udf.iloc[0]
print(udf.shape)
print(udf.head())
```

    (178515, 6)
       5694902542  \
    0  1587194582   
    1  6912893061   
    2  6526702684   
    3  6221311844   
    4  5316214557   
    
      {"ok":1,"data":{"cards":[{"card_type":11,"card_group":[{"card_type":42,"display_arrow":0,"desc":"\u8d26\u53f7\u4fe1\u606f"},{"card_type":41,"item_name":"\u6635\u79f0","item_content":"\u6674\u5929\u53c2\u52a0\u56ed\u6e38\u4f1a"},{"card_type":41,"item_name":"\u7b80\u4ecb","item_content":"\u6682\u65e0\u7b80\u4ecb"},{"card_type":41,"item_name":"\u6ce8\u518c\u65f6\u95f4","item_content":"2015-09-05"},{"item_name":"\u9633\u5149\u4fe1\u7528","display_arrow":1,"card_type":41,"item_content":"\u4fe1\u7528\u8f83\u597d","actionlog":{"act_code":"594","ext":"uid:6526450790|ouid:5694902542|verified_type:-1|ptype:0|load_read_level:","oid":"https:\/\/service.account.weibo.com\/sunshine\/guize?sinainternalbrowser=topnav","fid":"2302835694902542_-_INFO","cardid":"230283_-_WEIBO_INDEX_USERINFO_CREDIT","uicode":"10000198"},"scheme":"https:\/\/service.account.weibo.com\/sunshine\/guize?sinainternalbrowser=topnav&luicode=10000011&lfid=2302835694902542_-_INFO"}]},{"card_type":11,"card_group":[{"card_type":42,"display_arrow":0,"desc":"\u4e2a\u4eba\u4fe1\u606f"},{"card_type":41,"item_name":"\u6027\u522b","item_content":"\u5973"},{"card_type":41,"item_name":"\u751f\u65e5","item_content":"\u72ee\u5b50\u5ea7"},{"card_type":41,"item_name":"\u6240\u5728\u5730","item_content":"\u5409\u6797"}]},{"card_type":11,"is_asyn":1,"card_group":[],"itemid":"2306185694902542_-_3861","async_api":"\/api\/container\/getItem?itemid=2306185694902542_-_3861&download="},{"card_type":11,"is_asyn":1,"card_group":[],"itemid":"2306185694902542_-_profileinterest","async_api":"\/api\/container\/getItem?itemid=2306185694902542_-_profileinterest&download="},{"card_type":11,"is_asyn":0,"card_group":[{"display_arrow":1,"title_extra_text":"\u66f4\u591a","card_type":42,"scheme":"https:\/\/m.weibo.cn\/p\/index?containerid=2316145694902542_-_SUGGEST&title=%E5%A5%B9%E6%8E%A8%E8%8D%90%E7%9A%84%E5%88%86%E7%BB%84&luicode=10000011&lfid=2302835694902542_-_INFO","desc":"\u5979\u63a8\u8350\u7684\u5206\u7ec4","actionlog":{"act_code":"594","ext":"uid:6526450790|ouid:5694902542|verified_type:-1","oid":"2302835694902542_-_SUGGROUPINFO","fid":"2302835694902542_-_INFO","cardid":"230283_-_WEIBO_INDEX_USERINFO_SUGGROUPINFO","uicode":"10000198"}},{"card_type":3,"scheme":"https:\/\/m.weibo.cn\/p\/index?containerid=2316145694902542_-_SUGGEST&title=%E5%A5%B9%E6%8E%A8%E8%8D%90%E7%9A%84%E5%88%86%E7%BB%84&luicode=10000011&lfid=2302835694902542_-_INFO","pics":[{"desc1":"\u641e\u7b11\u5e7d\u9ed8","pic":"https:\/\/tvax1.sinaimg.cn\/crop.0.0.1080.1080.1024\/b1072857ly8gdi7rzpc6dj20u00u0acu.jpg?KID=imgbed,tva&Expires=1593022164&ssig=osh5UpliQY","count":1,"desc2":"\u51717\u4eba","name":"\u5979\u63a8\u8350\u7684\u5206\u7ec4","scheme":"https:\/\/m.weibo.cn\/p\/index?containerid=2316145694902542_-_SUGGMEMBER_3883763391760388&luicode=10000011&lfid=2302835694902542_-_INFO","pic_small":"","pic_big":"","pic_middle":""}],"roundedcorner":1}]},{"card_type":11,"is_asyn":1,"card_group":[],"itemid":"2306185694902542_-_likes","async_api":"\/api\/container\/getItem?itemid=2306185694902542_-_likes&download="}],"cardlistInfo":{"show_style":1,"button":null,"can_shared":0,"cardlist_menus":[{"name":"\u5237\u65b0","type":"button_menus_refresh"},{"name":"\u8fd4\u56de\u9996\u9875","params":{"scheme":"sinaweibo:\/\/gotohome"},"type":"gohome"}],"v_p":"42","cardlist_title":"","desc":"","containerid":"2302835694902542_-_INFO","page":null},"banners":null,"scheme":"sinaweibo:\/\/cardlist?containerid=2302835694902542_-_INFO&_T_WM=80686514775&v_p=42&luicode=10000011&lfid=2302835694902542_-_INFO"}}  \
    0  {"ok":1,"data":{"cards":[{"card_type":11,"card...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    1  {"ok":0,"msg":"\u8fd9\u91cc\u8fd8\u6ca1\u6709\...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    2  {"ok":1,"data":{"cards":[{"card_type":11,"card...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    3  {"ok":1,"data":{"cards":[{"card_type":11,"card...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    4  {"ok":1,"data":{"cards":[{"card_type":11,"card...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    
       acc_age  age loc user_id  
    0       -1   -1         NaN  
    1       -1   -1         NaN  
    2       -1   -1         NaN  
    3       -1   -1         NaN  
    4       -1   -1         NaN  
    


```python
for i in range(0,udf.shape[0]):
    udf.loc
```


```python
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
print(age_parser('10-27 天蝎座'))
print(age_parser('2014-05-27'))
print(age_parser(None))
print(age_parser('2018-03-11  双鱼座'))
print(age_parser(' '))
```

    -1
    6
    -1
    2
    -1
    


```python
geo = (
        Geo()
        .add_schema(maptype="china")
        .add("geo", [list(z) for z in zip(["上海徐汇区"], [888])])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title="Geo-基本示例"),
        )
    )
geo.render_notebook()
```

    c:\users\nathany\appdata\local\programs\python\python37\lib\site-packages\pyecharts\charts\chart.py:14: PendingDeprecationWarning: pyecharts 所有图表类型将在 v1.9.0 版本开始强制使用 ChartItem 进行数据项配置 :)
      super().__init__(init_opts=init_opts)
    





<script>
    require.config({
        paths: {
            'echarts':'https://assets.pyecharts.org/assets/echarts.min', 'china':'https://assets.pyecharts.org/assets/maps/china'
        }
    });
</script>

        <div id="df4027e95b30492a90b24ed27456bc39" style="width:900px; height:500px;"></div>

<script>
        require(['echarts', 'china'], function(echarts) {
                var chart_df4027e95b30492a90b24ed27456bc39 = echarts.init(
                    document.getElementById('df4027e95b30492a90b24ed27456bc39'), 'white', {renderer: 'canvas'});
                var option_df4027e95b30492a90b24ed27456bc39 = {
    "animation": true,
    "animationThreshold": 2000,
    "animationDuration": 1000,
    "animationEasing": "cubicOut",
    "animationDelay": 0,
    "animationDurationUpdate": 300,
    "animationEasingUpdate": "cubicOut",
    "animationDelayUpdate": 0,
    "color": [
        "#c23531",
        "#2f4554",
        "#61a0a8",
        "#d48265",
        "#749f83",
        "#ca8622",
        "#bda29a",
        "#6e7074",
        "#546570",
        "#c4ccd3",
        "#f05b72",
        "#ef5b9c",
        "#f47920",
        "#905a3d",
        "#fab27b",
        "#2a5caa",
        "#444693",
        "#726930",
        "#b2d235",
        "#6d8346",
        "#ac6767",
        "#1d953f",
        "#6950a1",
        "#918597"
    ],
    "series": [
        {
            "type": "scatter",
            "name": "geo",
            "coordinateSystem": "geo",
            "symbolSize": 12,
            "data": [
                {
                    "name": "\u4e0a\u6d77\u5f90\u6c47\u533a",
                    "value": [
                        121.43,
                        31.18,
                        888
                    ]
                }
            ],
            "label": {
                "show": false,
                "position": "top",
                "margin": 8
            },
            "rippleEffect": {
                "show": true,
                "brushType": "stroke",
                "scale": 2.5,
                "period": 4
            }
        }
    ],
    "legend": [
        {
            "data": [
                "geo"
            ],
            "selected": {
                "geo": true
            },
            "show": true,
            "padding": 5,
            "itemGap": 10,
            "itemWidth": 25,
            "itemHeight": 14
        }
    ],
    "tooltip": {
        "show": true,
        "trigger": "item",
        "triggerOn": "mousemove|click",
        "axisPointer": {
            "type": "line"
        },
        "showContent": true,
        "alwaysShowContent": false,
        "showDelay": 0,
        "hideDelay": 100,
        "formatter": function (params) {        return params.name + ' : ' + params.value[2];    },
        "textStyle": {
            "fontSize": 14
        },
        "borderWidth": 0,
        "padding": 5
    },
    "title": [
        {
            "text": "Geo-\u57fa\u672c\u793a\u4f8b",
            "padding": 5,
            "itemGap": 10
        }
    ],
    "visualMap": {
        "show": true,
        "type": "continuous",
        "min": 0,
        "max": 100,
        "inRange": {
            "color": [
                "#50a3ba",
                "#eac763",
                "#d94e5d"
            ]
        },
        "calculable": true,
        "inverse": false,
        "splitNumber": 5,
        "orient": "vertical",
        "showLabel": true,
        "itemWidth": 20,
        "itemHeight": 140,
        "borderWidth": 0
    },
    "geo": {
        "map": "china",
        "roam": true,
        "emphasis": {}
    }
};
                chart_df4027e95b30492a90b24ed27456bc39.setOption(option_df4027e95b30492a90b24ed27456bc39);
        });
    </script>





```python
user_df = pd.read_csv('ids-result.csv')
```


```python
rdf = pd.DataFrame(columns=['user_id','acc_age','age','location'])
```


```python
user_df.drop_duplicates(inplace=True,keep='first')
```


```python
user_df.shape
```




    (178515, 2)




```python
for i in range(user_df.shape[0]):
    if i%10000==0:
        print('-> ',end='')
    try:
        info = parse_info(user_df.iloc[i][1])
        rdf.loc[i]=(user_df.iloc[i][0],age_parser(info[1]),age_parser(info[2]),str(info[3]).replace(" ",''))
    except:
        pass
```

    -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> 


```python
rdf
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>acc_age</th>
      <th>age</th>
      <th>location</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>1587194582</td>
      <td>8</td>
      <td>-1</td>
      <td>上海徐汇区</td>
    </tr>
    <tr>
      <td>2</td>
      <td>6526702684</td>
      <td>2</td>
      <td>21</td>
      <td>其他</td>
    </tr>
    <tr>
      <td>3</td>
      <td>6221311844</td>
      <td>3</td>
      <td>-1</td>
      <td>北京</td>
    </tr>
    <tr>
      <td>4</td>
      <td>5316214557</td>
      <td>6</td>
      <td>-1</td>
      <td>其他</td>
    </tr>
    <tr>
      <td>5</td>
      <td>5156326275</td>
      <td>6</td>
      <td>32</td>
      <td>上海</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>178510</td>
      <td>2114527213</td>
      <td>9</td>
      <td>120</td>
      <td>其他</td>
    </tr>
    <tr>
      <td>178511</td>
      <td>1792764054</td>
      <td>10</td>
      <td>-1</td>
      <td>湖北武汉</td>
    </tr>
    <tr>
      <td>178512</td>
      <td>3944727782</td>
      <td>6</td>
      <td>23</td>
      <td>其他</td>
    </tr>
    <tr>
      <td>178513</td>
      <td>5726128709</td>
      <td>5</td>
      <td>-1</td>
      <td>天津</td>
    </tr>
    <tr>
      <td>178514</td>
      <td>2929149160</td>
      <td>8</td>
      <td>-1</td>
      <td>海外</td>
    </tr>
  </tbody>
</table>
<p>178072 rows × 4 columns</p>
</div>




```python
rdf.to_csv('user-clean.csv',index=False,encoding="utf_8_sig")
```


```python
udf = pd.read_csv('user-clean.csv')
df = pd.read_csv('lwl-clean.csv')
```


```python
mdf = pd.merge(udf,df,on='user_id',how='right')
```


```python
mdf.to_csv('lwl-user-clean-1.csv',index=False,encoding="utf_8_sig")
```


```python
mdf['acc_age_x'].isna()
```




    0         False
    1         False
    2         False
    3         False
    4         False
              ...  
    852806     True
    852807     True
    852808     True
    852809     True
    852810     True
    Name: acc_age_x, Length: 852811, dtype: bool




```python
udf = pd.read_csv('user-clean.csv')
udf.shape
```




    (178072, 4)




```python
age_clean_df = udf[udf['age']!=-1]
```


```python
age_clean_df['age'].plot(kind='bar')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x21d8992ea58>




```python
plt.show()
```


```python
plt.figure(figsize=(20,8),dpi=80)
words = []
count = []
for (w,c) in words_count_top:
    words.append(w)
    count.append(c)
x = range(len(words))
plt.bar(x,count,width=0.5)
plt.rcParams['font.sans-serif']=['Microsoft YaHei']
plt.xticks(x,words)
plt.tick_params(labelsize=20)
plt.savefig('./img/words-freq-'+str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))+'.png',dpi=80,bbox_inches='tight')
plt.show()
```

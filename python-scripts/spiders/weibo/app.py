from fastapi import FastAPI,Query,Request,Cookie,Response,Header,Form,status
from typing import Optional
from starlette.responses import RedirectResponse
import pymysql,random,time,hashlib

app = FastAPI()


db = pymysql.connect("localhost","root","Bit_root_123","lwl")
cursor = db.cursor()

MAXLEN = 277
QLEN = 10

def min(a,b):
    return a if a<=b else b
def max(a,b):
    return a if a>b else b
def md5(input:str):
    return hashlib.md5(input.encode(encoding='UTF-8')).hexdigest()
def wok(ip:str):
    return md5(md5(ip)+str(time.time()))[8:16]
@app.get('/status')
async def getstatus():
    sql = "SELECT COUNT(*) FROM %s;"
    try:
        cursor.executemany(sql,['comments','users'])
    except Exception as e:
        print(e)
    result = curosr.fetchall()
    return {'success':result!=None,'comments':result[0],'users':result[1]}
@app.get('/random')
async def getrandom():
    rand = random.randint(1,MAXLEN-QLEN)
    sql_rand = "SELECT acc_age_x,location,created_at,text FROM comments WHERE id >= (SELECT floor(RAND() * (SELECT MAX(id) FROM comments))) LIMIT %s"
    sql = "SELECT * FROM comments where id between %s and %s limit %s"
    try:
        cursor.execute(sql_rand,QLEN)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    results = cursor.fetchall()
    return {'success':results!=None,'result':results}
 
@app.get('/comment')
async def getcomment(page:int,per_page:int):
    per_page = min(per_page,20)
    page = max(page,1)
    results = []
    print(page,per_page)
    
    sql = "SELECT cookie,created_at,text from discussions ORDER BY created_at DESC  limit %s, %s"
    print(sql%((page-1)*per_page,per_page)) 
    try:
        cursor.execute(sql,[(page-1)*per_page,per_page]) 
        results = cursor.fetchall()
    except Exception as e:
        db.rollback()
        print(e)
    return {'success':results!=None,'result':results}
@app.post('/comment')
async def setcomment(
    *,
    response: Response,
    content:str=Form(...),
    is_head:int=1,
    head:int=0,
    parent:int=0,
    uid:str=Cookie(None), 
    X_Real_Ip:str=Header(None)
    ):
    if not uid:
        uid = wok(X_Real_Ip) 
        response.set_cookie(key='uid',value=uid)
    sql = "INSERT INTO discussions (cookie, text, created_at,\
            ip, upvotes, pinned, is_head, head_update, head, parent, bodies)\
            VALUES (%s, %s, %s, %s, 0, 0, %s, %s, %s, %s, %s)"
    
    now = int(time.time())
    input_list = [uid,content,now,X_Real_Ip,is_head,now,head,parent,'']

    if is_head==0:
        sql += ""
    try:
        cursor.execute(sql,input_list)
        if is_head==0:
            sql = "UPDATE TABLE " 
        print(db.insert_id())
        db.commit()
        return RedirectResponse(status_code=status.HTTP_302_FOUND,url='https://www.dutbit.com/lwl/index.html')
    except Exception as e:
        db.rollback()
        print(e)
        return {'success':False,'details':repr(e)}
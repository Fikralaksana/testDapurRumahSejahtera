from fastapi import FastAPI,Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from functools import wraps
import uvicorn,sqlite3,requests
from datetime import datetime

app = FastAPI()

con = sqlite3.connect("./sql.db")
con.row_factory = sqlite3.Row 
cur = con.cursor()
################################################### Soal 2
def auth_required(func):
    @wraps(func)
    async def wrapper(request,*args, **kwargs):
        auth=request.headers.get('Authorization')
        print(auth)
        if auth=="codenih":
            return await func(request,*args, **kwargs)
        else :
            return "auth failed"

    return wrapper


@app.get("/perjam")
@auth_required
async def perjam(request:Request):
    date=request.query_params.get('date')
    sensor_id=request.query_params.get('sensor_id')
    sensorQuery="sensor_id="+sensor_id
    dateQuery=""
    if date!=None:
        start="waktu>'"+date+" 00:00'"
        end="waktu<'"+date+" 24:00'"
        dateQuery="AND "+start+" and "+end
    command= """SELECT strftime('%H',waktu)as jam,sum(total) as total
FROM t
WHERE """+sensorQuery+" "+dateQuery+"""
GROUP BY strftime('%H',waktu)"""
    print(command)
    h=cur.execute(command)
    data=h.fetchall()
    resp=jsonable_encoder(data)
    return JSONResponse(resp)

@app.get("/perhari")
@auth_required
async def perhari(request:Request):
    today=datetime.today().strftime('%Y-%m-%d')
    sensor_id=request.query_params.get('sensor_id')
    start=request.query_params.get('start',default="2000-01-01")
    end=request.query_params.get('end',default=today)
    sensorQuery="sensor_id="+sensor_id
    start="waktu> '"+start+"'"
    end="waktu< '"+end+"'"
    dateQuery="AND "+start+" and "+end
    command= """SELECT sum(total),waktu
FROM t
WHERE """+sensorQuery+" "+dateQuery+"""
GROUP BY strftime('%d',waktu)"""
    print(command)
    h=cur.execute(command)
    data=h.fetchall()
    resp=jsonable_encoder(data)
    return JSONResponse(resp)

############################################################# Soal 3
@app.post('/short')
@auth_required
async def shortUrl(request:Request):
    form= await request.form()
    url=form['url']
    username = "o_2mei75399c"
    password = "1234qweasd"
    auth_res = requests.post("https://api-ssl.bitly.com/oauth/access_token", auth=(username, password))
    access_token = auth_res.content.decode()
    headers = {"Authorization": f"Bearer {access_token}"}
    groups_res = requests.get("https://api-ssl.bitly.com/v4/groups", headers=headers)
    groups_data = groups_res.json()['groups'][0]
    guid = groups_data['guid']
    shorten_res = requests.post("https://api-ssl.bitly.com/v4/shorten", json={"group_guid": guid, "long_url": url}, headers=headers)
    print("token", shorten_res)
    link = shorten_res.json().get('link')
    return link



if __name__=='__main__':
    uvicorn.run(app)
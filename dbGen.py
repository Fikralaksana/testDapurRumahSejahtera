import csv, sqlite3
from datetime import datetime

con = sqlite3.connect("./sql.db") 
cur = con.cursor()
cur.execute("CREATE TABLE t (id INTEGER PRIMARY KEY,waktu DATETIME,sensor_id TEXT NOT NULL,total INTEGER);") 

with open('data.csv','r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], datetime.strptime(i['timestamp'], '%m/%d/%Y %H:%M'), i['sensor_id'], i['total']) for i in dr]
cur.executemany("INSERT INTO t (id,waktu,sensor_id,total) VALUES (?, ?,?,?);", to_db)
con.commit()
con.close()

#
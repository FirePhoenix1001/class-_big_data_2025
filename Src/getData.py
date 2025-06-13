import requests
import psycopg2
from datetime import datetime

url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
response = requests.get(url)
data = response.json()  # 解析 JSON 格式的資料
# print (data)
# data = data["result"]["records"]  # 提取 "records" 這個部分

conn = psycopg2.connect(
    dbname="nutn",  # 替換為你的資料庫名稱
    user="nutn",    # 替換為你的資料庫使用者
    password="nutn@password",  # 替換為你的資料庫密碼
    host="192.168.56.101",       # 可以根據你的需求修改
    port="5432"             # 預設 PostgreSQL 埠號
)
cur = conn.cursor()



# 3. 插入資料
insert_query = """
    INSERT INTO youbike_stations (
        sno, sna, sarea, mday, ar, 
        srcUpdateTime, infoTime, total, 
        available_rent_bikes, available_return_bikes
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# 4. 提取並插入每一筆資料
for station in data:
    # 提取需要的欄位
    sno = station["sno"]
    sna = station["sna"]
    sarea = station["sarea"]
    mday = datetime.strptime(station["mday"], "%Y-%m-%d %H:%M:%S")  # 資料更新時間轉換為時間格式
    ar = station["ar"]
    srcUpdateTime = datetime.strptime(station["srcUpdateTime"], "%Y-%m-%d %H:%M:%S")  # 原始資料更新時間
    infoTime = datetime.strptime(station["infoTime"], "%Y-%m-%d %H:%M:%S")  # 資訊時間
    total = int(station["total"])
    available_rent_bikes = int(station["available_rent_bikes"])
    available_return_bikes = int(station["available_return_bikes"])

    # 將資料插入 PostgreSQL
    values = (
        sno, sna, sarea, mday, ar, 
        srcUpdateTime, infoTime, total, 
        available_rent_bikes, available_return_bikes
    )
    cur.execute(insert_query, values)

# 提交變更
conn.commit()

# 關閉連接
cur.close()
conn.close()

print("資料成功插入 PostgreSQL 資料庫！")
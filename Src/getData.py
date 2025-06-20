import requests
import psycopg2
from datetime import datetime

# 1. 抓取資料
url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"抓取資料失敗: {e}")
    exit(1)

# 2. 資料庫連線
try:
    conn = psycopg2.connect(
        dbname="nutn",
        user="nutn",
        password="nutn@password",
        host="192.168.56.101",
        port="5432"
    )
    conn.autocommit = False  # 禁用 autocommit，讓 rollback 有效
    cur = conn.cursor()
except Exception as e:
    print(f"資料庫連線失敗: {e}")
    exit(1)

# 3. 插入語句（避免重複）
insert_query = """
    INSERT INTO youbike_stations (
        sno, sna, sarea, mday, ar,
        srcUpdateTime, infoTime, total,
        available_rent_bikes, available_return_bikes
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (sno, mday) DO NOTHING
"""  # 確保資料表有 UNIQUE(sno, mday)

# 4. 插入資料
for station in data:
    try:
        values = (
            station["sno"],
            station["sna"],
            station["sarea"],
            datetime.strptime(station["mday"], "%Y-%m-%d %H:%M:%S"),
            station["ar"],
            datetime.strptime(station["srcUpdateTime"], "%Y-%m-%d %H:%M:%S"),
            datetime.strptime(station["infoTime"], "%Y-%m-%d %H:%M:%S"),
            int(station["total"]),
            int(station["available_rent_bikes"]),
            int(station["available_return_bikes"]),
        )
        cur.execute(insert_query, values)
    except Exception as e:
        print(f"資料插入失敗（站點 {station.get('sno')}）: {e}")
        conn.rollback()  # 這一步很關鍵
        continue

# 5. 結束
try:
    conn.commit()
except Exception as e:
    print(f"提交失敗: {e}")
finally:
    cur.close()
    conn.close()

print("本次資料成功處理完畢")

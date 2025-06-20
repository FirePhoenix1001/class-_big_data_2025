import requests
import psycopg2

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
    conn.autocommit = False
    cur = conn.cursor()
except Exception as e:
    print(f"資料庫連線失敗: {e}")
    exit(1)

# 3. 建立資料表 map（若已存在就刪除）
try:
    cur.execute("DROP TABLE IF EXISTS youbike_map")
    cur.execute("""
        CREATE TABLE youbike_map (
            sna TEXT,
            sarea TEXT,
            ar TEXT,
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION
        )
    """)
except Exception as e:
    print(f"建立資料表失敗: {e}")
    conn.rollback()
    cur.close()
    conn.close()
    exit(1)

# 4. 插入資料
insert_query = """
    INSERT INTO youbike_map (sna, sarea, ar, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
"""

for station in data:
    try:
        values = (
            station["sna"],
            station["sarea"],
            station["ar"],
            float(station["latitude"]),
            float(station["longitude"]),
        )
        cur.execute(insert_query, values)
    except Exception as e:
        print(f"插入失敗（站點 {station.get('sno')}）: {e}")
        conn.rollback()
        continue

# 5. 結束
try:
    conn.commit()
    print("map 資料表寫入完成 ✅")
except Exception as e:
    print(f"提交失敗: {e}")
finally:
    cur.close()
    conn.close()

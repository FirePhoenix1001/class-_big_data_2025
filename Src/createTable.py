import psycopg2

conn = psycopg2.connect(
    dbname="nutn",
    user="nutn",
    password="nutn@password",
    host="192.168.56.101",
    port="5432"
)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS youbike_stations")

# 重新建立 youbike_stations 資料表，並使用 sno + mday 作為唯一鍵
cur.execute("""
    CREATE TABLE youbike_stations (
        id SERIAL PRIMARY KEY,  -- 建議加入流水號主鍵
        sno VARCHAR(20),
        sna VARCHAR(100),
        sarea VARCHAR(50),
        mday TIMESTAMP,
        ar VARCHAR(255),
        srcUpdateTime TIMESTAMP,
        infoTime TIMESTAMP,
        total INT,
        available_rent_bikes INT,
        available_return_bikes INT,
        UNIQUE(sno, mday)  -- 加入複合唯一鍵
    );
""")

conn.commit()
cur.close()
conn.close()

print("資料表創建成功！")

import psycopg2

conn = psycopg2.connect(
    dbname="nutn",  # 替換為你的資料庫名稱
    user="nutn",    # 替換為你的資料庫使用者
    password="nutn@password",  # 替換為你的資料庫密碼
    host="192.168.56.101",       # 可以根據你的需求修改
    port="5432"             # 預設 PostgreSQL 埠號
)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS stations")

# 創建新資料表
cur.execute("""
    CREATE TABLE youbike_stations (
        sno VARCHAR(20) PRIMARY KEY,
        sna VARCHAR(100),
        sarea VARCHAR(50),
        mday TIMESTAMP,
        ar VARCHAR(255),
        srcUpdateTime TIMESTAMP,
        infoTime TIMESTAMP,
        total INT,
        available_rent_bikes INT,
        available_return_bikes INT
    );
""")

    # 提交變更並關閉資料庫連線
conn.commit()
cur.close()
conn.close()

print("資料表創建成功！")
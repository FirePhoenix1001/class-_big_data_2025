from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import pandas as pd

# --- 資料庫連線設定 ---
username = "nutn"
password = quote_plus("nutn@password")  # %40 = @
host = "192.168.56.101"
port = "5432"
dbname = "nutn"
db_url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
engine = create_engine(db_url)

# --- 從原始資料表讀資料 ---
query = """
SELECT ar, mday, srcUpdateTime, infoTime, total, available_rent_bikes, available_return_bikes
FROM youbike_stations
"""
df = pd.read_sql(query, engine)

# --- 去除重複資料 ---
df_clean = df.drop_duplicates()

# --- 建立新表 youbike_cleaned（如果不存在） ---
create_table_sql = """
CREATE TABLE IF NOT EXISTS youbike_cleaned (
    ar VARCHAR,
    mday TIMESTAMP,
    srcUpdateTime TIMESTAMP,
    infoTime TIMESTAMP,
    total INT,
    available_rent_bikes INT,
    available_return_bikes INT
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_sql))
    conn.execute(text("DELETE FROM youbike_cleaned"))  # 清空乾淨資料表

# --- 插入乾淨資料 ---
insert_query = """
INSERT INTO youbike_cleaned (
    ar, mday, srcUpdateTime, infoTime, total,
    available_rent_bikes, available_return_bikes
) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

raw_conn = engine.raw_connection()
try:
    cur = raw_conn.cursor()

    # 確保資料表存在
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS youbike_cleaned (
        ar VARCHAR,
        mday TIMESTAMP,
        srcUpdateTime TIMESTAMP,
        infoTime TIMESTAMP,
        total INT,
        available_rent_bikes INT,
        available_return_bikes INT
    );
    """
    cur.execute(create_table_sql)

    # 清空乾淨資料表
    cur.execute("DELETE FROM youbike_cleaned")

    # 批量插入乾淨資料
    insert_query = """
    INSERT INTO youbike_cleaned (
        ar, mday, srcUpdateTime, infoTime, total,
        available_rent_bikes, available_return_bikes
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cur.executemany(insert_query, list(df_clean.itertuples(index=False)))

    raw_conn.commit()
    cur.close()
finally:
    raw_conn.close()

print("✅ 成功建立 youbike_cleaned，已存入去重後的資料。原始資料未更動。")


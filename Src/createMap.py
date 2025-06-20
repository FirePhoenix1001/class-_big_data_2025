from datetime import datetime
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm
from sqlalchemy import create_engine

# 中文字型設定
if os.name == "nt":
    matplotlib.rcParams['font.family'] = 'Microsoft JhengHei'
else:
    font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    font_prop = fm.FontProperties(fname=font_path)
    matplotlib.rcParams['font.family'] = font_prop.get_name()
matplotlib.rcParams['axes.unicode_minus'] = False

# 資料庫連線
engine = create_engine("postgresql+psycopg2://nutn:nutn%40password@192.168.56.101:5432/nutn")

# 查詢最新時間
latest_time = pd.read_sql("""
    SELECT MAX(srcupdatetime) as latest FROM youbike_stations
""", engine).iloc[0, 0]
timestamp = pd.to_datetime(latest_time).strftime("%Y%m%d_%H%M")
filename = f"youbike_map_{timestamp}.png"

# JOIN youbike_stations 與 youbike_map 取得位置與數量
# 修正後 SQL 查詢
df = pd.read_sql(f"""
    SELECT m.latitude, m.longitude, s.available_rent_bikes, s.total
    FROM youbike_stations s
    JOIN youbike_map m ON s.sna = m.sna
    WHERE s.srcupdatetime = '{latest_time}'
""", engine)


# 經緯度範圍
min_lat, max_lat = df['latitude'].min(), df['latitude'].max()
min_lon, max_lon = df['longitude'].min(), df['longitude'].max()

# 建立格點矩陣
scale = 1000
lat_range = int((max_lat - min_lat) * scale) + 1
lon_range = int((max_lon - min_lon) * scale) + 1
grid = np.zeros((lat_range, lon_range), dtype=int)

# 對應資料至格點
for _, row in df.iterrows():
    lat_idx = int((row['latitude'] - min_lat) * scale)
    lon_idx = int((row['longitude'] - min_lon) * scale)
    grid[lat_idx, lon_idx] += float(row['available_rent_bikes'])


# 繪製圖像
plt.figure(figsize=(10, 8))
plt.imshow(
    grid,
    cmap='hot',
    origin='lower',
    extent=[min_lon, max_lon, min_lat, max_lat],
)

plt.title("YouBike 可租借車輛分布圖")
plt.xlabel("經度")
plt.ylabel("緯度")
plt.colorbar(label="可租借數量")
plt.tight_layout()

# 存檔
# output_dir = "/home/vincent0999200/nutn/Youbike/Src/picture"
# os.makedirs(output_dir, exist_ok=True)
# full_path = os.path.join(output_dir, filename)
full_path = filename
plt.savefig(full_path, dpi=300)
print(f"✅ 熱點圖已儲存為 {full_path}")


import requests
import pandas as pd
import numpy as np

# 下載資料
url = "https://2384.tainan.gov.tw/IMP/jsp/rwd_api/ajax_routeinfo_pathattr.jsp?id=1100&Lang=cht"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)

# 解析 JSON
data = response.json()

# 取出站牌資料
stop_data = data['data']

# 只取需要的欄位
df = pd.DataFrame(stop_data)[['id', 'stopInfo', 'carNo']]

# 整理資料
df['stopInfo'] = df['stopInfo'].replace('即將進站', '0分鐘')
df['carNo'] = df['carNo'].replace('', '無車輛')

# 轉成 list
records = df.values.tolist()

# 中文站名清單
stop_names = [
    "臺南轉運站", "臺南火車站(北站)", "臺南公園(北門路)", "成大醫院(勝利路)", "勝利北路", "中樓", "開元", "崑山中學",
    "南工宿舍", "南工社區", "中興", "康福新城", "二王", "南大附中", "永康農會", "永康", "龍潭口", "德芳社區",
    "西勢", "西勢東", "南光藥廠", "保生大帝宮", "唪口", "清水寺", "新化站", "新化區公所", "新化保養廠",
    "養護之家", "仁愛之家", "深坑子", "畜試所", "台南醫院新化分院", "接天寺", "那拔林", "千鳥橋", "隙子口",
    "豐德", "大立窯業", "頂店", "光和里", "光和活動中心", "下菜寮", "頂菜寮", "左鎮化石園區", "龍溝", "邦寮",
    "橄欖山", "左鎮分駐所", "左鎮果菜市場", "左鎮", "東屏厝", "睦光里", "竹坑", "刺桐腳", "後坑", "九層林",
    "愛文山", "松腳", "玉井懷恩堂", "倒松", "劉陳", "望明口", "玉山新城", "新庄", "玉井工商", "玉井站"
]

# 處理每一筆資料
final_records = []
last_car = None

for idx, record in enumerate(records):
    stop_id, stop_info, car_no = record
    stop_name = stop_names[idx]

    if car_no != '無車輛':
        last_car = car_no
        final_records.append([stop_name, stop_info, car_no])
    else:
        if last_car is not None:
            final_records.append([stop_name, stop_info, last_car])
        else:
            final_records.append([stop_name, stop_info, '無車輛'])

# 轉成三維陣列
array_3d = np.array(final_records).reshape((len(final_records), 1, 3))

# # 顯示結果
# print(array_3d)
# 只顯示「臺南火車站(北站)」
target_stop = "臺南火車站(北站)"

# 過濾 array_3d 中符合的資料
filtered = [row for row in array_3d if row[0][0] == target_stop]

# 顯示
print(np.array(filtered))

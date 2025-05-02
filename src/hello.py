import requests
from bs4 import BeautifulSoup

# 抓 HTML 頁面
url_html = "https://2384.tainan.gov.tw/IMP/jsp/rwd_api/ajax_routeinfo.jsp?id=1100&Lang=cht"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response_html = requests.get(url_html, headers=headers)

# 印出抓到的 HTML文字
print(response_html.text)


ehhhheeeee
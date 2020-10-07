import requests
from bs4 import BeautifulSoup


header = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}


search_str = "c언어"

encode_str = str(search_str.encode('euc-kr')).replace("\\x","%")[2:-1]

# print(encode_str)


url = "http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&query="+encode_str

# str(search_str.encode('euc-kr')).replace("\\x","%")

res = requests.get(url, headers = header)

bs = BeautifulSoup(res.text, "lxml")

lists = bs.select("div.goodsList_list tr")

print(lists)

for li in lists:
    pass
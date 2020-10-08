import requests
from bs4 import BeautifulSoup

USER_SHOP_URL = "UsedShop"

def search_book(search_str, page=1):
    header = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}

    encode_str = str(search_str.encode('euc-kr')).replace("\\x","%")[2:-1]

    url = "http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&query="+encode_str+"&domain=BOOK&PageNumber="+str(page)

    # str(search_str.encode('euc-kr')).replace("\\x","%")

    res = requests.get(url, headers = header)

    bs = BeautifulSoup(res.text, "lxml")

    lists = bs.select("div.goodsList_list tr")

    # print(lists)

    alt_list = list()
    src_list = list()
    url_list = list()

    for li in lists[::2]:
        
        img = li.select_one("td.goods_img a img")
        url = li.select_one("td.goods_img a").get("href")
        alt = img.get('alt')
        src = img.get('src')
        
        if alt is not None and alt != "":
            if str(url).find(USER_SHOP_URL) == -1:
                # print(alt)
                # print(img.get('src'))
                url_list.append(url[15:])
                alt_list.append(alt)
                src_list.append(src)
    

    print(url_list)
    return {
        "alt_list":alt_list,
        "src_list":src_list,
        "url_list":url_list
    }
import requests
from bs4 import BeautifulSoup

USER_SHOP_URL = "UsedShop"
BOOK_DETAIL_URL = "http://www.yes24.com/Product/Goods/"
IMAGE_URL = "http://image.yes24.com/goods/"
IMAGE_SIZE_URL = "/L"


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


def crwal_index(book_num):
    header = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
    url = BOOK_DETAIL_URL + str(book_num)
    res = requests.get(url, headers = header)

    bs = BeautifulSoup(res.text, "lxml")

    indexes = bs.select_one("#infoset_toc .txtContentText")
    # indexs = bs.find("div", ("gd_infoSet", "gd_infoSetCrop", "infoMoreOn"))

    # print(indexs.contents)

    # 책 제목, 지은이 등등 정보 추가 가져오기

    # 나중에.. 관리자가 사람들이 등록한 책 보고 목차 설된것 중에 좋은거 있으면 그 책의 베이스 테이블로 선택해서 
    # 나중에 등록한 사용자가 뎁스 설정같은거 안해도 되는 시스템


    index_list = list()
    
    if indexes is None:
        return None

    for content in indexes.contents:
        if str(content).find("<br/>") == -1:
            index_list.append(str(content).strip())

    image = IMAGE_URL + str(book_num) + IMAGE_SIZE_URL
    name = bs.select_one(".gd_titArea .gd_name").text
    auth = bs.select_one(".gd_pubArea .gd_auth").text.strip()
    publisher = bs.select_one(".gd_pubArea .gd_pub").text.strip()
    date = bs.select_one(".gd_pubArea .gd_date").text.strip()

    result = {
        "indexes":index_list,
        "image":image,
        "name":name,
        "auth":auth,
        "publisher":publisher,
        "date":date
    }

    return result



# print(crwal_index(74269921231231))
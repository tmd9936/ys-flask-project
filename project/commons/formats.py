from project import app
from datetime import timedelta, datetime
import time

@app.template_filter("datetime_format")
def datetime_format(value):
    if value is None:
        return ""
    
    now_timestamp = time.time()

    # 클라이언트의 local 타임을 datetime형식으로 출력
    local_datetime = datetime.fromtimestamp(now_timestamp)
    # print(local_datetime)

    # utcgromtimestamp는 UTC datetime을 리턴
    utc_datetiem = datetime.utcfromtimestamp(now_timestamp)
    # print(utc_datetiem)

    offset_time = local_datetime - utc_datetiem
    print("offset_time : ", offset_time)
    

    value = datetime.fromtimestamp((int(value) / 1000)) + offset_time

    return value.strftime("%Y-%m-%d %H:%M:%S")

# @app.template_filter("length")
# def length(value):
    
#     if value is None :
#         return ""

#     return 

    

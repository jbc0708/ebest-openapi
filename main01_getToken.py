
import requests
import json

APP_KEY = "발급받은 APP_KEY"
SECRET_KEY = "발급받은 SECRET_KEY"
BASE_URL = "https://openapi.ebestsec.co.kr:8080"

def get_Token():
    PATH = "/oauth2/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    body = {
        "appkey": APP_KEY,
        "appsecretkey": SECRET_KEY,
        "grant_type": "client_credentials",
        "scope": "oob"
    }
    result = requests.post(BASE_URL+PATH, headers=headers, data=body)

    return result

def get_DayInfo(token, code, tr_cont, tr_cont_key, startday, cnt):
    PATH = "/stock/market-data"
    headers = {
        "content-type": "application/json; charset=utf-8", 
        "authorization": "Bearer "+token,
        "tr_cd": "t1305",         #요청하는 tr의 이름
        "tr_cont": tr_cont,      #연속조회 여부  ('Y' or 'N')
        "tr_cont_key": tr_cont_key # 처음 조회라면 "" or "0", 연속조회라면 마지막 수신한 응답의 header에 있는 tr_cont_key 사용
    }
    body = {
        "t1305InBlock":  { 
                "shcode": code, #요청하는 종목코드
                "dwmcode": 1,   #일봉=1, 주봉=2, 월봉=3
                "date": startday,       # 처음조회시 빈칸("")으로 하면 가장 최근 거래일을 기준으로 함
                                                # 연속조회시 마지막 수신한 응답의 body의 t1305OutBlock 키의 date 값을 입력하면됨
                 "cnt": cnt        #호출시 요청할 데이터의 건수 
             } 
     }
    result = requests.post(BASE_URL+PATH, headers=headers, data=json.dumps(body))
    return result

temp = get_Token()

token = temp.json()["access_token"]

data = get_DayInfo(token, "122630", "N", "0", "", 5) 
data_header = data.headers
data_body = data.json()
info = data_body["t1305OutBlock1"]
for i in info:
    print(i)
    print("-"*20)
time.sleep(1.1)
# 아래는 연속 조회를 위한 추가 코드입니다.
data2 = get_DayInfo(token, "122630","Y", data_header["tr_cont_key"], data_body["t1305OutBlock"]["date"], 5),
data2_header = data2.headers
data2_body = data2.json()
info2 = data2_body["t1305OutBlock1"]
for i in info2:
    print(i)
    print("-"*20) 
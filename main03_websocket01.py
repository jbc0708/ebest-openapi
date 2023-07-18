# pip install websocket-client 로 모듈을 우선 설치 후 실행하셔야 됩니다.
# 설치는 websocket-client 라고 하였지만 실제 코드에서는 websocket이라고 입력합니다.
import websocket
import requests

APP_KEY = "발급받은 APP_KEY"
SECRET_KEY = "발급받은 SECRET_KEY"
BASE_URL = "https://openapi.ebestsec.co.kr:8080"

def get_token():
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

result = get_token()
token = result.json()["access_token"]

url = "wss://openapi.ebestsec.co.kr:9443/websocket"
ws = websocket.WebSocket()
ws.connect(url=url)
codes = ['122630', '252670', '069500'] # 실시간 수신팓을 코스피 종목코드
for code in codes:
    sendMsg = '{"header":{"token" : "%s" ,"tr_type" : "3"}, "body" : {"tr_cd" : "S3_" , "tr_key" : "%s"}}'%(token,code)
    ws.send(sendMsg)
while True:
    data=ws.recv()
    print(data)
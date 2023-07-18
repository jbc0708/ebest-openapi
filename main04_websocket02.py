# pip install websockets로 모듈을 우선 설치 후 실행하셔야 됩니다.

import websockets
import requests
import asyncio

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


url = "wss://openapi.ebestsec.co.kr:9443/websocket"

result = get_token()
token = result.json()["access_token"]

async def connect():
    async with websockets.connect(url, ping_interval=60) as websocket:
        codes = ['122630', '252670', '069500']
        for code in codes:
            sendMsg = '{"header" : {"token" : "%s" , "tr_type" : "3"} , "body" : {"tr_cd" : "S3_" , "tr_key" : "%s"}}'%(token,code)
            await websocket.send(sendMsg)

        while True:
            data = await websocket.recv()
            print(data)

asyncio.get_event_loop().run_until_complete(connect())
asyncio.get_event_loop().close()
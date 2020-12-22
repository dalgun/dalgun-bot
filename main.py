# -*- coding: utf-8 -*-

import requests
import json
import logging
import time
from random import randint

URL = "https://m.land.naver.com/complex/getComplexArticleList"
# 시간 표시 형식
tType = "%Y-%m-%d %H:%M:%S"


param = {
    'page' : 1,
    'hscpNo': '159',
    'tradTpCd': 'B2',
    'order': 'date_',
    'showR0': 'N',
    'title' : '가산 두산 위브'
}

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
    'Referer': 'https://m.land.naver.com/'
}

logging.basicConfig(level=logging.INFO)


# 텔레그램 봇에게 요청하는 sendTelegramMsg() 이라는 함수를 생성
def sendTelegramMsg(APIKey, chatID, text):
    r = requests.get("https://api.telegram.org/bot"
                     + APIKey + "/sendMessage?chat_id="
                     + chatID + "&text="
                     + text + "&parse_mode=Markdown")
    return r
# 텔레그램 설정
TelAPI = "1415596817:AAG8cajcOA_G_KyIFq04GICQCBmw-_6PZEY" # 텔레그램 봇의 KEY. 텔레그램 @BotFather가 알려준 키를 입력.
TelChan = "1308384308" # 숫자값 또는 @AWESOMEBOT 과 같은 형식으로 입력.

# 로그에 출력될 내용 (텔레그램에는 전송되지 않습니다)
print ("========내 설정========")
print ("Telegram 채널ID: " + TelChan)
print ("==============================")


def getNaverInfo(param):

    tempStrList = ""
    resp = requests.get(URL, params=param, headers=header)

    if resp.status_code != 200:
        logging.error('invalid status: %d' % resp.status_code)
        tempStrList = "["+param['title']+"]"+"조회시 오류가 발생하였습니다. HTTP STATUS CODE: " + resp.status_code
        return tempStrList


    data = json.loads(resp.text)
    result = data['result']
    if result['totAtclCnt'] is 0:
        tempStrList = "["+param['title']+"]-월세 조회 결과가 없습니다."
        return tempStrList

    for item in result['list']:
        # logging.info('[%s-%s] %s %s층 %s만원' % (item['atclNm'], item['tradTpNm'], item['bildNm'], item['flrInfo'], item['prcInfo']))
        tempStr = "[{}-{}] {} {} 층 {} 만원".format(item['atclNm'], item['tradTpNm'], item['bildNm'], item['flrInfo'], item['prcInfo'])
        tempStrList += tempStr+"\n"

    return tempStrList

    # if result['moreDataYn'] == 'N':

while(1):
    try:
        sendTelegramMsg(TelAPI, TelChan, getNaverInfo(param))
    # 오류발생시 무시하고 반복 (오류 내용 출력)
    except Exception as ex:
        print("[" + time.strftime(tType) + "] 오류 발생 - 재시도합니다.", ex)

    print("[" + time.strftime(tType) + "] 대기합니다...")
    time.sleep(randint(1800,1810))

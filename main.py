# -*- coding: utf-8 -*-

import requests
import json
import logging

URL = "https://m.land.naver.com/complex/getComplexArticleList"

param = {
    'hscpNo': '3359',
    'tradTpCd': 'B2',
    'order': 'date_',
    'showR0': 'N',
}

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
    'Referer': 'https://m.land.naver.com/'
}

logging.basicConfig(level=logging.INFO)
page = 0


# 텔레그램 봇에게 요청하는 sendTelegramMsg() 이라는 함수를 생성
def sendTelegramMsg(APIKey, chatID, text):
    r = requests.get("https://api.telegram.org/bot"
                     + APIKey + "/sendMessage?chat_id="
                     + chatID + "&text="
                     + text + "&parse_mode=Markdown")
    return r
tempStrList = ''
# 텔레그램 설정
TelAPI = "1415596817:AAG8cajcOA_G_KyIFq04GICQCBmw-_6PZEY" # 텔레그램 봇의 KEY. 텔레그램 @BotFather가 알려준 키를 입력.
TelChan = "1308384308" # 숫자값 또는 @AWESOMEBOT 과 같은 형식으로 입력.

# 로그에 출력될 내용 (텔레그램에는 전송되지 않습니다)
print ("========내 설정========")
print ("Telegram 채널ID: " + TelChan)
print ("==============================")

while True:
    page += 1
    param['page'] = page

    resp = requests.get(URL, params=param, headers=header)
    if resp.status_code != 200:
        logging.error('invalid status: %d' % resp.status_code)
        break

    data = json.loads(resp.text)
    result = data['result']
    if result is None:
        logging.error('no result')
        break

    for item in result['list']:
        if float(item['spc2']) < 80 or float(item['spc2']) > 85:
            continue
        logging.info('[%s-%s] %s %s층 %s만원' % (item['atclNm'], item['tradTpNm'], item['bildNm'], item['flrInfo'], item['prcInfo']))
        tempStr = "[{}-{}] {} {} 층 {} 만원".format(item['atclNm'], item['tradTpNm'], item['bildNm'], item['flrInfo'], item['prcInfo'])
        tempStrList = tempStrList.join(tempStr)
        print(tempStrList)

    if result['moreDataYn'] == 'N':

        break


sendTelegramMsg(TelAPI, TelChan, tempStrList)


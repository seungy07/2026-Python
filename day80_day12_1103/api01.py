# py -m pip install xmltodict  # py -m pip install httpx
# httpx란 외부 api 통신하는 라이브러리, axios/client/httpx 공공자료 API연동/SPRING API
# xmltodict  xml -> dict 파싱 라이브러리

import httpx
import pandas as pd
# 1] 공공데이터에 json 형식의 자료 요청 

service_key = "3f12958d4a3d304a9e3f30fef163ec8020c6aec9c35ad05e206caa977355eaa2"
def test1():
    
    # https://api.odcloud.kr/api/15052602/v1/uddi:855807e2-fe8a-4e47-8a5a-ce1894e410d7_201909031553?page=1&perPage=10&serviceKey=3f12958d4a3d304a9e3f30fef163ec8020c6aec9c35ad05e206caa977355eaa2
    # 2] 신청한 Api의 주소 및 파라미터 분석 , page 현재 페이지, perPage=페이지당 자료수 , serviceKey
    url = "https://api.odcloud.kr/api/15052602/v1/uddi:855807e2-fe8a-4e47-8a5a-ce1894e410d7_201909031553"
    url += "?page=1"
    url += "&perPage=147"
    url += f"&serviceKey={service_key}"
    
    # 3] httpx 이용하여 통신하기 , import httpx
    # httpx.HTTP메소드명( 통신할 주소 ), 통신 결과 반환
    response = httpx.get(url)  #print(response)
    # 4] 응답결과 JSON 변환 .json()
    response_json = response.json() # print(response_json)
    # 5] 판다스에 저장하기, import pandas as pd
    df = pd.DataFrame( response_json['data'] ) # { "currentCount" : 10, "data:[실질자료]"}
    df.info()

test1()

# 2] 공공데이터포털 xml 형식의 자료 요청,
import xmltodict # xml 변환 라이브러리
# https://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyFullDown?serviceKey=3f12958d4a3d304a9e3f30fef163ec8020c6aec9c35ad05e206caa977355eaa2&pageNo=1&numOfRows=10
def test2():
    url = "https://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyFullDown"
    url += f"?serviceKey={service_key}"
    url += "&pageNo=1&numOfRows=100"

    # 2] https 이용한 api 요청
    response = httpx.get(url)

    # 3] 요청 응답 자료를 문자열로 반환하여 파이썬 dict 형식으로 변환
    response_dict = xmltodict.parse(response.text) # print(response_dict)
    # 4] <response> -> <body> -> <items> -> <item>
    df = pd.DataFrame( response_dict['response']['body']['items']['item'] )
    df.info()
    
#     <response>
        # <header>
            # <resultCode>00</resultCode>
            # <resultMsg>NORMAL SERVICE.</resultMsg>
        # </header>
        # <body>
            # <items>
                # <item>

test2()
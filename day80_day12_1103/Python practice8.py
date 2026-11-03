# Practice8: API 데이터 수집
# 1. 개요 및 대상 API 정보
# API 이름: 행정안전부_착한가격업소 현황
# API URL: https://www.data.go.kr/data/3045247/fileData.do 

# 목표: httpx를 통해 공공데이터 API를 호출하고, pandas를 활용해 업소명, 주소, 가격 데이터를 구조화한 뒤 통계 분석을 수행합니다.
# 2. 상세 요구사항
# 2-1 (API 호출 및 파라미터 설정):
# 지정된 API URL에 인증키(serviceKey)를 포함하여 요청합니다.
# 임의의 100건의 데이터를 수집

# 2-2 (데이터프레임 적재):
# 응답받은 JSON 데이터 중 실제 행 목록인 data 배열을 추출하여 pandas.DataFrame으로 변환합니다.

# 2-3 (데이터 전처리 및 분석):
# 가격1 컬럼의 데이터를 숫자형(pd.to_numeric)으로 변환합니다.
# 수집된 100건 데이터 기준 가격1의 평균값을 산출하여 출력합니다.

# 2-4 (업종별 평균 가격 집계 및 시각화):
# groupby('업종')을 사용하여 업종별 가격1의 평균 가격을 계산합니다.
# seaborn의 barplot 활용하여 업종별 평균 가격 비교 막대그래프를 시각화합니다.

import httpx
import pandas as pd
import xmltodict
import seaborn as sns 
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

service_key ="3f12958d4a3d304a9e3f30fef163ec8020c6aec9c35ad05e206caa977355eaa2"

def run():
    # 2-1 
    url = "https://api.odcloud.kr/api/3045247/v1/uddi:0d236000-b33f-41ad-9227-ee0efa3ec6c8"
    url += "?page=1&perPage=100"
    url += f"&serviceKey={service_key}"

    # 2-2
    response = httpx.get(url)
    response_json = response.json() #print(response_json)
    data = pd.DataFrame(response_json['data'])
    data.info()

    # 2-3
    data['가격1'] = pd.to_numeric( data['가격1'].fillna(0) )
    print(f"수집건수: {len(data)}건")
    print(f"가격1 평균: {data['가격1'].mean()}원")

    # 2-4
    group_mean = data.groupby('업종')['가격1'].mean()
    sns.barplot(x=group_mean.values ,y=group_mean.index)
    plt.xlabel('가격1 평균 금액')
    plt.title('업종별 평균 금액')
    plt.show()

run()
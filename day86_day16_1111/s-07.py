import pandas as pd
fish = pd.read_csv("./day86_day16_1111/Fish.csv")

# 1) 다중 분류 실습하기 윈한 특성 / 타긱(여러개 어종) 구분
x = fish.drop(columns=['Species']) # 어종을 제외한 모든 열
y = fish['Species'] # 어종 열

# 2) 분리,  stratify=y  정답지에 학습용과 테스트용 비율 유지(분류 모델 권장)
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42,stratify=y)

# 3) 스켈링
from sklearn.preprocessing import StandardScaler
ss = StandardScaler() 
x_train_scaled = ss.fit_transform(x_train) # fit + transform
x_test_scaled = ss.transform(x_test)

# 4) 로지스틱 회귀 = 이진분류(시그모이드) / 다중분류(소프트맥스) 중 자동 선택
# L2 규제(릿지) 자동 적용. 손실(오차)함수 계산 함. C = 1.0 기본값 / 강도 설정 가능 (하이퍼파라미터)
# 계산 반복수(경사 하강법) : 최적의 가중치/기울기 찾기 위한 계산 반복수, 기본값 100, **권장 1000~3000 최적 찾으면 자동 중단
# 경사하강법: 기울기(규제) 변경 하면서 최적의 오차 찾는 과정
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(C=1.0, max_iter=1000, random_state=42) #  ( C = 규제강도 ) 설정가능, ( max_iter=100 )
model.fit(x_train_scaled,y_train)
y_perd = model.predict(x_test_scaled)
print(y_perd)
# ['Bream' 'Perch' 'Smelt' 'Perch' 'Perch' 'Perch' 'Bream' 'Pike' 'Smelt'
#  'Perch' 'Perch' 'Perch' 'Parkki' 'Perch' 'Pike' 'Perch' 'Bream' 'Perch'
#  'Perch' 'Pike' 'Perch' 'Bream' 'Smelt' 'Perch' 'Bream' 'Bream' 'Parkki'
#  'Perch' 'Smelt' 'Perch' 'Pike' 'Bream']

# y 값의 클래스를 보고 이진 / 다중 분류 판단

import numpy as np
print( np.round(model.predict_proba(x_test_scaled[:3]), 3) ) # 지수값 표현, # np.round(리스트, 자릿수)
print( model.classes_) # ['Bream' 'Parkki' 'Perch' 'Pike' 'Roach' 'Smelt' 'Whitefish'] 정답지 종류


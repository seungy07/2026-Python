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


# 평가지표
# average="macro" : 클래스마다 개수 다 다르므로 산술평균 값으로 계산
from sklearn.metrics import accuracy_score, precision_score, recall_score,f1_score
# 1) 정확도 : 전체 예측 건수 중 맞힌 정답의 비율 , (TP+TN) / (TP+TN+FP+FN)
# 클래스내 개수들이 불균형이면 점수 왜곡 발생
print( accuracy_score(y_test, y_perd))  # 0.8125
# 2) 정밀도 : 예측 한 것 중 실제로 맞힌 비율 , TP / (TP+FP)
print(precision_score(y_test, y_perd, average="macro"))  # 0.6309523809523808
# 3) 재현율 : 실제 정답인 것 중, 모델이 놓치지 않고 찾아낸 비율, TP / (TP+FN)
print(recall_score(y_test,y_perd,average="macro")) # 0.7012987012987013
# 4) f1 점수/표준 : 정밀도와 재현율 간의 조화 조정하기 위한 조화평균, 2 * 정밀도*재현율 / (정밀도+재현율)
print( f1_score(y_test,y_perd,average="macro")) # 0.6609105180533751

## 4대 평가지표는 혼동행렬 이용하여 계산
# 혼동행렬 시각화
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, classification_report

ConfusionMatrixDisplay.from_predictions(y_test,y_perd)
plt.title('Confusion Matrix')
plt.show()

## 리포트(평가 지표 보고서)  classification_report
print(classification_report(y_test,y_perd)) 

# 파이프라인 구성
from sklearn.pipeline import Pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(max_iter=1000,random_state=42))
])
# 하이퍼 파라미터 후보군 , 식별자_ _매개변수명 : [후보값, 후보값]
param_grid = {'model__C':[0.01, 0.1,1.0,10.0,100.0]}
# k폴드 이용한 교차 검증(표준) =>  다중 분류시 StratifiedKFold(계층분류) 사용 <= 이진분류를 하더라도 권장
from sklearn.model_selection import GridSearchCV,KFold,StratifiedKFold
SFold = StratifiedKFold(n_splits=5, shuffle=True,random_state=42)
grid = GridSearchCV(pipe, param_grid,cv=SFold, scoring='f1_macro', n_jobs=-1)
grid.fit(x_train,y_train)

print(grid.best_params_) # 최적의 파라미터 # {'model__C': 100.0}
print(grid.best_score_) # 최적 f1 score # 0.8288862211551287

best_model = grid.best_estimator_
pred = best_model.predict(x_test)

print( classification_report(y_test,pred)) 

# 추후 joblib로 최적 모델 저장 사용
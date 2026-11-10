# 로지스틱 회귀 : 범주형을 예측하는 분류 알고리즘 
import pandas as pd
df = pd.read_csv("./day85_day15_1110/Fish.csv")

# 1) 이진분류 실습을 위한 정답지 2개 사용
df = df[ (df['Species'] == 'Bream' ) | (df['Species'] == 'Smelt') ]

x = df[['Weight','Length1','Length2','Length3','Height','Width']]
y = df['Species'] # Bream or Smelt

# 2) 분리, 분류 학습 모델 사용시( 타깃의 분리 비율 일정하게 만들기 stratify=타깃 )
# 무작위 ㅂㄴ리 한 경우 타깃의 클래스(값) 비율 일정 유지, 분류모델

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=42, stratify=y) # stratify

# 3) 특성 스케일링
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
ss.fit(x_train)
x_train_scaled = ss.transform(x_train)
x_test_scaled = ss.transform(x_test)

# 4) 로지스틱 회귀 모델 학습
from sklearn.linear_model import LogisticRegression
logistic = LogisticRegression()
logistic.fit(x_train_scaled,y_train)
y_pred = logistic.predict(x_test_scaled)
print(y_pred) # ['Bream' 'Bream' 'Smelt' 'Bream' 'Bream' 'Smelt' 'Smelt' 'Bream' 'Bream' 'Bream']

# 5) 결과 속성
print( logistic.classes_ ) # 정답지 종류
print( logistic.predict_proba( x_test_scaled[:3] ) ) # 확률 반환
# [[0.99255987 0.00744013]      Bream(0)열 Smelt(1)열
#  [0.99568698 0.00431302]
#  [0.04598467 0.95401533]]

# ) 모델 평가: 분류 정확도(Accuracy) 확인
from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test,y_pred) # (테스트정답지, 테스트예측)
print(acc) # 1.0 => 100% 현재 실습은 데이터가 적다.


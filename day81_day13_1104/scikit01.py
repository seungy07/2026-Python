# [사이킷런 scikit-learn] 방대한 머신러닝 알고리즘 모델 제공
# pip install scikit-learn

# 머신러닝 목표: 추론/예측 과정
# 특성(feature): 모델이 학습하는 자료 정보 , 
# 타깃(target): 모델이 맞춰야하는 정답 정보

# 지도학습: 특성과 다깃을 모두 제공하여 학습(정답O) , 회귀/분류
# 비지도 학스비 타깃없이 특성만으로 제공하는 학습 (정답X) 군집/텍스트마이닝(분석) 토픽/주성분분석(PCA)

# (회귀모델)
# 1) 다순 선형 회귀 , [물고기 길이를 이용해서 무게 예측]
import pandas as pd
df = pd.read_csv('./day81_day13_1104/Fish.csv')
df.info()

# 2) 모델 학습에 사용할 데이터 추출 (수치형)
# 특성 : Length2 (물고기 대각선 cm)    ,  # 타깃 : Weight(물고기 무게 g)
feature = ['Length2']  
target = 'Weight'
# 3) x독립변수/입력변수/특성변수,  y종속변수/목표변수/target 구조화
x = df[feature] # 2차원 # 사이킷런 모델 구조상 학습할 특성은 2차원으로
y = df[target]  # 1차원

# 4) 데이터 분리, 학습용/테스트 분리
from sklearn.model_selection import train_test_split 
# 특성학습자료, 특성테스트자료, 타깃학습자료, 타깃테스트자료 = train_test_split(특성, 타깃, test_size=비율, random_state=난수시드값) (시드번호 고정)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
# 훈련세트 : 모델에서 규칙을 찾는 자료
# 테스트세트: 모델학습 후 모델 평가/예측성능 점수/지표

# 5) 모델 학습 및 예측, 단순(특성값1개) 선형 회귀모델
from sklearn.linear_model import LinearRegression
model = LinearRegression() # 파이썬 객체 생성 방법 new 없음, 변수명 = 클래스명 ()
# 6) 모델 학습, model.fit(특성자료, 타깃 자료)
model.fit(x_train, y_train)

# 7) 모델 가중치(기울기), model.coef
print( model.coef_ ) # [30.43452394]
# 8) 모델 편향(y절편) 확인 
print( model.intercept_ ) #  -477.306349
# 9) 학습한 모델의 예측, 새로운 x값을 넣어서 y값을 구하기
y_pred = model.predict(x_test)  # model.predict( 2차원 특성자료 )
print(y_pred)
# *) 단순회귀모델: y = ax + b , [30.43452394]*[x] + [-477.306349]
# *) 문제점: 직선관계는

# 10) 시각화  
import matplotlib.pyplot as plt
plt.scatter(x_train, y_train) # 학습자료둘
plt.scatter([30], model.predict([[30]]), color='red' )
plt.plot([0,100], model.predict([[0],[100]])) # 회귀선: 임의의 최솟값/최댓값
plt.show()
# 11) 문제점
# x,y 직선 관계이며 실 자료들은 꼭 비례 증가가 아닐 수 있다.
# 해결: 다항 회귀
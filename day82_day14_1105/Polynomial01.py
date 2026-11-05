
# 1] 항 추가하는 함수
from sklearn.preprocessing import PolynomialFeatures 
poly = PolynomialFeatures() # 객체 생성
poly.fit([[2]])         #  특성 규칙
print(poly.transform([[22]])) # [[1. 2. 4.]] # 기본절편, 원래갓, 제곱값
# 2] 절편 제외
poly = PolynomialFeatures(include_bias=False) # include_bias=False 기본절편 제외 
poly.fit([[2]])
print(poly.transform([[2]])) # [[2. 4.]]

# 3] 특성 2개인 경우 
poly = PolynomialFeatures(include_bias=False)
poly.fit([[2,3]])               # 특성 규칙 (2,3)
print(poly.transform([[2,3]])) # [[2. 3. 4. 6. 9.]] # 두항의 곱셈까지 

# *] 특성 3개인 경우 9개?
poly = PolynomialFeatures(include_bias=False)
poly.fit([[2,3,4]])               # 2^특성수 + 1 
print(poly.transform([[2,3,4]])) # [[ 2.  3.  4.  4.  6.  8.  9. 12. 16.]]
# 수동으로 특성의 제곱항을 만들지 않고 자동(PolynomialFeatures) 으로 다항 추가
# *문제점: 과대적합이 생길 수 있다.  (사용: 과소적합을 피하기위해 사용한다)

# 2] 다항 회귀 모델
import pandas as pd
df = pd.read_csv("./day82_day14_1105/Fish.csv")
# 1) 특성과 타깃 구성
x = df[ ['Length2', 'Height','Width']] # 특성 3개
y = df['Weight'] # 타깃 1개
# 2) 테스트/훈련용 분리
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

# 3) 과소적합을 방지하고자 다항 만들기 PolynomialFeatures
poly = PolynomialFeatures(include_bias=False)
poly.fit(x_train) # 학습할 특성들을 규칙(제곱/곱셈)
# print(poly.transform( x_train ))
x_train_poly = poly.transform(x_train)
x_test_poly = poly.transform(x_test)
print( x_train.shape ); print(x_train_poly.shape) # 3열 -> 9열(항이 추가 됨)  ,행 127 동일

# 4) 모델 학습 
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(x_train_poly, y_train) # 항이 추가된 특성으로 학습
# 5) 결정계쑤
from sklearn.metrics import r2_score
y_perd = model.predict(x_test_poly) # 테스트용 다항 특성으로 예측
print("다항 회귀 결정계수" , r2_score(y_test, y_perd)) # 0.9719372415762594

# 3] 다항의 차수 늘리기   # degree=n, n의 제곱까지 하여 항 수 추가
poly = PolynomialFeatures(include_bias=False, degree=10)  # 생략시 2(기본값)
poly.fit(x_train)
x_train_poly2 = poly.transform(x_train)
# print(x_train_poly2.shape) # (127,285)  차수2->차수10 증가에 따른 (127,9)
x_test_poly2 = poly.transform(x_test)

model = LinearRegression()
model.fit(x_train_poly2, y_train) 
y_perd2 = model.predict(x_test_poly2) # 테스트용 다항 특성으로 예측
print("다항 회귀 결정계수" , r2_score(y_test, y_perd2)) # 0.07276663213888512

# *] 모델 구현에서 다양한 속성값( degree = N ) 들을 테스트 하여 설계/구현 한다
# *] 특성이 너무 많아지면 훈련 데이터가 과하게 집학 하여 과대적합이 발생하여 점수 낮아질수 있다

# 4] 특성 수 증가함에 따라 특성간의 단위 표준화(0 ~ 1)
from sklearn.preprocessing import StandardScaler # 표준화 제공 라이브러리
ss = StandardScaler()
ss.fit(x_train_poly) # 다항 추가된 학습 자료
x_train_scaled = ss.transform(x_train_poly)
x_test_scaled = ss.transform(x_test_poly)
print(x_train_scaled[0]) # [-1.14878727 -1.06273398 ....
print(x_train_poly[0])  # [ 16.2          4.5924  ...
# 평균보다 작으면 음수, 평균+1 편준 보다 크면 1이상

# 5] 규제: 기울기(가중치) 크기에 패널티를 부여 하여 특성 오차/손실 확인하여 특성을 제외
# 릿지(0에 가깝게 축소) (Ridge, L2 규제) ,  라쏘 (제외) (Lasso, L1 규제)
# 1) 릿지
from sklearn.linear_model import Ridge
# 2) alpha(규제강도) : 값이 커질수록 가중치/기울기를 0에 가깝게 규제한다 -> 완만
# 반복하여 최적의 규제 강도 찾기
alpha_list = [0.001, 0.01, 0.1, 1, 10, 100]
for alpha in alpha_list:
    model = Ridge(alpha= alpha) # 6가자 강도 설정 하여 릿지 모델 생성
    model.fit( x_train_scaled, y_train) # 학습
    # 학습데이터 점수와 테스트용 점수 격차 적은 alpha 찾기
    print( alpha, "-- 훈련용 학습 데이터 점수 vs 테스트용 학습 데이터 점수 --")
    print("Train r2: ", model.score(x_train_scaled, y_train))
    print("test R2: " , model.score(x_test_scaled, y_test))

# 3) 라쏘 모델
from sklearn.linear_model import Lasso
lasso = Lasso(alpha= 10 ) # 임의의 강도 지정 라쏘 객체 생성
lasso.fit(x_train_scaled, y_train)
print( lasso.score(x_train_scaled, y_train)) # 0.9587575172401576
print(lasso.score(x_test_scaled, y_test)) # 0.9609557543588229
# 제외된 특성
import numpy as pd
zero_features = pd.sum( lasso.coef_ == 0)
print(zero_features) # 기울기 0으로 제거된 특성 수
# 훈령용이랑 테스트용 격차 확인

# 다항에서는 스케일링(표준화) 필수 , StandardScaler() 
# 특성이 적으면(과소적합/모델 단순) --> 항 추가(PolynomialFeatures) , degree 차수 
# 특성이 많으면(과대적합/모델 복잡) --> 규제 Ridge(L2), Lasso(L1) , alpha 규제강도
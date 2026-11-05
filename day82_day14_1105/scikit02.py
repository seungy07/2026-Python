import pandas as pd
df = pd.read_csv("./day82_day14_1105/Fish.csv")

# [day13 단순 선형 회귀]
# 1. 특성, 타깃 분류
x = df[['Length2']]
y = df['Weight']
# 2. 훈련용/테스트용 분리
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)
# 3. 단순회귀 모델
from sklearn.linear_model import LinearRegression
model = LinearRegression()
# 4. 학습
model.fit(x_train,y_train)
# 5. 모델 결정계수
y_pred = model.predict(x_test)
from sklearn.metrics import r2_score
print("결정계수 r2: ", r2_score(y_test,y_pred) ) # 0.8199897860284712

# [day14 다항 회귀]
# 1] 특성[x]에 제곱하여 항 추가
import numpy as np
x_train_poly = np.column_stack( (x_train**2, x_train) ) # np.column_stack((배열1, 배열2)) : 배열 합치기
print(x_train_poly) # [16.2] -> [262.44 16.2]

# 2] 제곱된 특성으로 모델 학습
model = LinearRegression()
model.fit(x_train_poly, y_train)
# 3] 예측
print( model.predict( [[30**2, 30]] )) # [405.27748848]

# 4] 시각화
point = np.arange(0,101) # 0~100까지 회귀선을 만들기 위한 배열
# 특성과 동일하게 제곱항 추가
point_poly = np.column_stack((point**2,point))
import matplotlib.pyplot as plt
plt.scatter(x_train,y_train) # 특성자료
plt.plot(point, model.predict(point_poly), color='red') # (제곱항이 추가된 ) 회귀선
plt.show() 

# 5] 결정계수
x_test_poly = np.column_stack( (x_test**2, x_test) )# 테스트용도 제곱항 추가
y_pred = model.predict(x_test_poly)
print( r2_score(y_test, y_pred))  # 0.8249869834428712  => day13 보다 0.005정도 높아짐
# 직선 공식(1차 방정식): y = Wx + b  # 곡선 공식(2차) y = Wx^2 + Wx + b

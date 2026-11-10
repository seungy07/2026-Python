import pandas as pd
df = pd.read_csv("./day85_day15_1110/Fish.csv")  # 1) 자료 수집
# 2) *예측*할 특성과 타깃(정답) 선정/구성
x = df[['Length2','Height','Width']] # 2) 특성
y = df['Weight'] # 2) 타깃(정답) 선정/구성

# 3) 훈련/테스트 분리
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,train_size=0.2,random_state=42)

# 4) 과소적합 방지 => 항 추가 PolynomialFeautures # 제곱/곱셈
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2, include_bias=False) # degree=2기본값 # include_bias=False 편향값 1제외
poly.fit(x_train) 
x_train_poly = poly.transform(x_train)
x_test_poly = poly.transform(x_test)

# 5) 항이 많아지면 / 특성간에 표준화 / 스케일링
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
ss.fit(x_train_poly)
x_train_scaled = ss.transform(x_train_poly)
x_test_scaled = ss.transform(x_test_poly)

# 6) 모델 선택, 규제(릿지/라쏘)  없을시 단순 선형회귀 alpha=규제강도
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(x_train_scaled,y_train)
#7) 결정 계수
print('r2: ', model.score(x_train_scaled, y_train))
print('r2: ', model.score(x_test_scaled, y_test))
# r2:  0.9907782821219157
# r2:  0.96970686305412 # 학습 데이터와  테스트 데이터 결정계수 차이


# ============================ (4) ~ (6) 과정 묶음
from sklearn.pipeline import Pipeline
# pipe_model = Pipeline( [ ('식별자', 클래스명() ) ] )
pipe_model = Pipeline( [ ('poly', PolynomialFeatures(degree=2, include_bias=False) ),
                        ('scaler', StandardScaler()),
                        ('regressor', LinearRegression()) ] )
pipe_model.fit(x_train,y_train)
train_r2 = pipe_model.score(x_train,y_train); print('train_r2: ', train_r2); # train_r2:  0.9907782821219157
test_r2 = pipe_model.score(x_test, y_test); print('test_r2: ', test_r2); # test_r2:  0.9697068630541217




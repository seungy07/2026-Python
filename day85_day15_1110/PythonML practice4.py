# PythonML Practice4: 로지스틱 이진 분류 (Logistic Regression)
# 데이터 출처: https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# [단계 1] 데이터 로드 및 전처리, 독립/종속 변수 추출
# 파일명: ./data.csv
df = pd.read_csv('./day85_day15_1110/data.csv')
df.info()
# 1. 식별자('id') 및 결측 열('Unnamed: 32')이 존재한다면 제외합니다.
df = df.drop(columns=['id', 'Unnamed: 32'], errors='ignore')
# 2. 'diagnosis' 열을 종속 변수 y로 추출하고, 악성(M)은 1, 양성(B)은 0으로 매핑(변환)하세요.
df['diagnosis'] = df['diagnosis'].mask(df['diagnosis'] == 'M', 1)
df['diagnosis'] = df['diagnosis'].mask(df['diagnosis'] == 'B', 0)
df['diagnosis'] = df['diagnosis'].astype(float)
y = df['diagnosis'] 
print(df['diagnosis'])
# 3. 'diagnosis'를 제외한 30개의 수치형 피처를 독립 변수 X로 추출하세요.
x = df.drop(columns=['diagnosis']).select_dtypes(include='number')
# df = pd.read_csv('./data.csv')
# # id 컬럼 드롭 및 전체가 결측치(NaN)인 열 자동 제거
# df = df.drop(columns=['id'])
# df = df.dropna(axis=1, how='all') # Unnamed: 32 등 모든 값이 NaN인 열을 자동으로 날립니다.
# # 종속 변수(문자열 'M', 'B' 유지) 및 독립 변수 분리
# Y = df['diagnosis']
# X = df.drop(columns=['diagnosis'])

# [단계 2] 훈련용 / 테스트용 데이터 분리
# train_test_split을 사용하여 8:2 비율(test_size=0.2)로 분리하고,
# 재현성을 위해 random_state=42, 클래스 비율 유지를 위해 stratify=y로 설정하세요.
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42,stratify=y)

# [단계 3] 데이터 표준화 (Standardization)
# StandardScaler를 활용하여 훈련 데이터(X_train) 기준으로 스케일러를 학습(fit)시키고,
# X_train과 X_test를 각각 표준화(transform) 변환하세요.
ss = StandardScaler()
ss.fit(x_train)
x_train_scaled = ss.transform(x_train)
x_test_scaled = ss.transform(x_test)

# [단계 4] 로지스틱 회귀 모델 학습 (Logistic Regression)
# LogisticRegression(random_state=42) 모델을 생성하고 훈련 세트(X_train_scaled, y_train)로 학습시키세요.
logistic = LogisticRegression()
logistic.fit(x_train_scaled, y_train)

# [단계 5] 모델 평가 및 분류 정확도(Accuracy) 확인
# 테스트 세트에 대한 예측을 수행하고 정확도(accuracy_score)를 출력하세요.
y_pred = logistic.predict(x_test_scaled)
acc = accuracy_score(y_test,y_pred)
print('정확도: ', acc)

# [단계 6] 샘플 데이터 예측 및 예측 확률 확인
# 테스트 세트의 앞선 3개 샘플 데이터에 대해: x_test_scaled[:3]
# 1. 모델이 예측한 클래스(0 또는 1)를 출력하세요.
# 2. 각 샘플별 양성(0)/악성(1) 클래스에 대한 예측 확률(predict_proba)을 출력하세요.
sample = x_test_scaled[:3]
print("예측결과: ", logistic.predict(sample)) # [0. 1. 0.]
print(logistic.classes_)
print(logistic.predict_proba(sample))

proba = logistic.predict_proba(x_test_scaled[:3])
pred = logistic.predict(x_test_scaled[:3])

for i in range(len(proba)):
    print(
        f"샘플 {i+1} | 예측: {int(pred[i])} | "
        f"양성: {proba[i][0]:.2%} | 악성: {proba[i][1]:.2%}"
    )
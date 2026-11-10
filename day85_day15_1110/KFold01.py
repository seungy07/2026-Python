import pandas as pd
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression,Ridge

df = pd.read_csv("./day85_day15_1110/Fish.csv") 
x = df[['Length2','Height','Width']] 
y = df['Weight']
x_train,x_test,y_train,y_test=train_test_split(x,y,train_size=0.2,random_state=42)

# 10) 최적(성능좋은/오차적은)의 파라미터(매개변수/대입값) 찾기
# degree=2, alpha=0.01

# 1. 파이프라인 만들기
pipe_model = Pipeline([
    ('poly', PolynomialFeatures(include_bias=False)),
    ('scaler', StandardScaler()),
    ('ridge', Ridge()) # alpha 튜닝
])
# 2. 후보군 파라미터 만들기, {'식별자_파라미터명' : [후보값, 후보값 ]}
param_grid = {'poly__degree' : [2,3], 'ridge__alpha': [0.001, 0.01 ,0.1 , 1, 10, 100] }

# 3. K-Fold 교차 검증 , import KFold,GridSearchCV
kf = KFold(n_splits=5, shuffle=True, random_state=42) # KFold(K개의 동일한 폴드로 분할, 섞을지, 시드값)
# 학습데이터들을 5개로 나누고 4개학습하고 1개 검증, => 5번 반복 교차 검증 => 평균 오차/손실 성능 사용

# 4. 그리드서치CV : 교차검증과 다양한 파라미터 자동으로 실행하고 최적 찾기
grid = GridSearchCV( estimator=pipe_model, param_grid= param_grid, scoring='r2', cv= kf, n_jobs= -1 )
# GridSearchCV( estimator= 진행할 모델/파이프라인, param_grid= {파라미터 후보군}, scoring='평가지표명', cv= 교차검증, n_jobs= 작업을 병렬로 실행할지 )
# n_jobs= -1 (CPU 사용가능하 코어의 최대 병렬 사용) *거의 고정값으로 사용

# 5. 그리드서치로 학습
grid.fit(x_train,y_train)

# 6. 주요 속성
best_model = grid.best_estimator_ # 가장 성능 좋은 모델 반환
print(best_model) # Pipeline(steps=[('poly', PolynomialFeatures(degree=3, include_bias=False)),('scaler', StandardScaler()), ('ridge', Ridge(alpha=1))])
print(grid.best_params_) # 가장 성능 좋은 조합  # {'poly__degree': 3, 'ridge__alpha': 1}
print(grid.best_score_) # 교차검증에서 평균 점수(최고)  # 0.9791809880885332
# 7. 최적 모델로 평가
print(best_model.score(x_train,y_train)) # 0.9910724145806052
print(best_model.score(x_test,y_test)) #  0.9716495825855089

# 11) 서빙(학습된 모델 재사용), 학습된 모델 저장하고 다른곳에서 호출
# 연구/학습 : 코랩(고사양GPU)에서 학습 --> 실제 서버(FAST API)에서 호출
# 실무: GPU서버 학습 --> 실제 서버에서 호출
import joblib
# 1) 모델 저장 # joblib.dump( 저장할 모델, 경로.pkl )
joblib.dump( best_model, './day85_day15_1110/fish_model.pkl' )

# 12) 다른 파이썬 파일에서 저장된 모델 불러오기
# PythonML Practice5: 다중 분류
# 데이터셋: seaborn diamonds dataset (다이아몬드 세공 품질 'cut' 다중 분류)
import seaborn as sns
from sklearn.model_selection import train_test_split,StratifiedKFold,GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import joblib
import pandas as pd
import numpy as np

# [단계 1] 데이터 로드 및 전처리, 독립/종속 변수 분리
# 1. seaborn의 'diamonds' 데이터셋을 로드하세요. (sns.load_dataset('diamonds'))
df = sns.load_dataset('diamonds')
df.info()
# 2. 실습 연산 효율성을 위해 5,000개 샘플을 무작위 추출하세요. (df = df.sample(n=5000, random_state=42).reset_index(drop=True))
df = df.sample(n=5000, random_state=42).reset_index(drop=True)
# 3. 다이아몬드 커팅 품질('cut': Fair, Good, Very Good, Premium, Ideal)을 종속 변수 Y로, 나머지 컬럼을 독립 변수 X로 분리하세요.
x = df.drop(columns=['cut'])
y = df['cut']

# [단계 2] 훈련용 / 테스트용 데이터 분리
# train_test_split을 사용하여 8:2 비율(test_size=0.2)로 분리하고, 5개 클래스 비율 유지를 위해 stratify=Y, 재현성을 위해 random_state=42로 설정하세요.
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42,stratify=y)

# [단계 3] ColumnTransformer를 활용한 복합 전처리 구성
# 1. 수치형 피처: ['carat', 'depth', 'table', 'price', 'x', 'y', 'z'] -> StandardScaler를 적용하세요.
# 2. 범주형 피처: ['color', 'clarity'] -> OneHotEncoder(drop='first', sparse_output=False )를 적용하세요.
# 3. 위 두 변환기를 ColumnTransformer로 묶어 'preprocessor' 객체를 정의하세요.
num_features = ['carat', 'depth', 'table', 'price', 'x', 'y', 'z']
cat_features = ['color', 'clarity']
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_features)
    ]
)

# [단계 4] 파이프라인(Pipeline) 구축 및 기본 모델 학습
# 1. Pipeline을 생성하여 [단계 3]의 'preprocessor'와 LogisticRegression(max_iter=1000, random_state=42)을 단일 워크플로우로 연결하세요.
# 2. X_train 원본(DataFrame)과 Y_train을 파이프라인에 직접 투입하여 모델을 학습(fit)시키세요.
pipe = Pipeline([
    ('perprocessor', preprocessor), ('model', LogisticRegression(max_iter=1000,random_state=42))
])
pipe.fit(x_train,y_train)

# [단계 5] 모델 다중 분류 지표 산출 및 혼동 행렬 시각화
# 1. 테스트 세트(X_test)에 대한 예측 레이블(Y_pred) 및 예측 확률(Y_pred_proba)을 생성하세요.
y_pred = pipe.predict(x_test)
y_pred_proba = pipe.predict_proba(x_test)
# 2. 파이프라인 내부 분류기의 클래스 순서(classes_)를 확인하고, 다중 분류 4대 평가 지표를 산출하세요:
#    - 정확도 (accuracy_score) 정밀도 (precision_score, average='macro') 재현율 (recall_score, average='macro') F1 점수 (f1_score, average='macro')
print( pipe.classes_) # ['Fair' 'Good' 'Ideal' 'Premium' 'Very Good']
print( classification_report(y_test, y_pred))

# 3. ConfusionMatrixDisplay.from_predictions를 활용해 혼동 행렬을 시각화하세요.
ConfusionMatrixDisplay.from_predictions(y_test,y_pred)
plt.title('ConfusionMartix')
plt.show()

# [단계 6] GridSearchCV 기반 하이퍼파라미터 튜닝
# 1. 규제 강도 탐색 그리드를 정의하세요: {'model__C': [0.01, 0.1, 1.0, 10.0]}
param_grid = {'model__C': [0.01, 0.1, 1.0, 10.0]}
# 2. StratifiedKFold(n_splits=5, shuffle=True, random_state=42) 교차 검증 객체를 생성하세요.
sf =StratifiedKFold(n_splits=5,shuffle=True,random_state=42 )
# 3. scoring='f1_macro'를 기준으로 GridSearchCV를 수행하여 최적 파라미터와 최고 점수를 출력하세요.
grid = GridSearchCV(pipe, param_grid, cv=sf, scoring='f1_macro', n_jobs=-1)
grid.fit(x_train,y_train)
# 4. 최적 추정기(best_estimator_)로 X_test를 평가하고 classification_report를 출력하세요.
best_model = grid.best_estimator_
best_model_pred = best_model.predict(x_test)
print( classification_report(y_test, best_model_pred) )

# [단계 7] 파이프라인 직렬화(저장/불러오기) 및 신규 원본 데이터 실시간 추론
# 1. joblib.dump를 사용하여 최적화된 파이프라인 전체를 './diamond_pipeline.pkl'로 저장하세요.
joblib.dump(best_model, './day86_day16_1111/diamond_pipeline.pkl')
# 2. joblib.load로 저장된 파이프라인을 다시 불러오세요.
load_model=joblib.load('./day86_day16_1111/diamond_pipeline.pkl')
# 3. 스케일링/인코딩을 거치지 않은 원본 형태의 임의 다이아몬드 샘플(DataFrame)을 생성하세요: (예: carat=0.7, color='E', clarity='SI1', depth=61.5, table=55.0, price=3000, x=5.7, y=5.75, z=3.5)
sample = pd.DataFrame({ 'carat':[0.7], 'color':['E'], 'clarity':['SI1'], 'depth':[61.5], 'table':[55.0], 'price':[3000], 'x':[5.7], 'y':[5.75], 'z':[3.5] })
# 4. 불러온 파이프라인의 predict() 및 predict_proba()에 직접 전달하여 예측 커팅 등급(cut)과 가장 높은 확신도(최대 확률 %)를 출력하세요.
print("예측 커팅 등급: " ,load_model.predict(sample) ) # ['Ideal']
print("가장 높은 확신도: ",load_model.predict_proba(sample),"%") # [[2.46175180e-04 2.16673854e-02 8.03355179e-01 3.09884831e-02 1.43742777e-01]] %
print( np.round(load_model.predict_proba(sample),3 ) ) # [[0.    0.022 0.803 0.031 0.144]]
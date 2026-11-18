# PythonML Practice6: LightGBM과 Optuna를 활용한 회귀 모델 해석
# 데이터셋: 개인 특성 및 생활 습관에 따른 연간 의료비 'charges' 예측
url = 'https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv'

# [단계 1] 데이터 로드, 범주형 타입 변환 및 독립/종속 변수 분리
# 1. pandas.read_csv()를 사용하여 위 URL에서 보험 의료비 데이터셋을 로드하세요.
import pandas as pd
df = pd.read_csv(url)

# 2. 결측치나 이상치 방지를 위해 의료비('charges')가 0보다 큰 데이터만 필터링하세요. df = df[df['charges'] > 0]
df = df[ df['charges'] > 0 ]

# 3. 수치형 피처( num_cols = ['age', 'bmi', 'childre '] )와 범주형 피처( cat_cols = ['sex', 'smoker', 'region'] )를 정의하세요.
num_cols = ['age', 'bmi', 'children'] # 수치형
cat_cols = ['sex', 'smoker', 'region'] # 범위형

# 4. LightGBM의 네이티브 범주형 피처 처리를 위해 cat_cols에 해당하는 컬럼들의 데이터 타입을 'category'로 변환하세요. .astype('category')
for col in cat_cols:
    df[col] = df[col].astype('category')

# 5. 수치형 및 범주형 피처를 결합하여 독립 변수 X로, 연간 의료비('charges')를 종속 변수 Y로 분리하세요.
X = df[num_cols+cat_cols]
Y = df['charges']

# [단계 2] 훈련용 / 테스트용 데이터 분리
# train_test_split을 사용하여 8:2 비율(test_size=0.2)로 분리하고, 재현성을 위해 random_state=42로 설정하세요.
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2, random_state=42)

# [단계 3] Optuna 목적 함수(Objective) 및 K-Fold 교차 검증 기반 조기 종료 설계
# 1. Optuna의 불필요한 상세 로그를 숨기기 위해 로그 레벨을 WARNING으로 설정하세요. optuna.logging.set_verbosity(optuna.logging.WARNING)
import optuna
from lightgbm import LGBMRegressor,early_stopping
import numpy as np
optuna.logging.set_verbosity( optuna.logging.WARNING )

# 2. objective(trial) 함수를 정의하고, 내부에서 KFold(n_splits=5, shuffle=True, random_state=42) 교차 검증 객체를 생성하세요.
def objecctive(trial):
    from sklearn.model_selection import KFold
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_r2_scores = []
    best_itreations = []

    for train_idx, val_idx in cv.split(X_train,Y_train):
        X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
        Y_tr, Y_val = Y_train.iloc[train_idx], Y_train.iloc[val_idx]
# 3. 최종 테스트 R2 점수가 85%(0.85) 이상 달성되도록 LGBMRegressor의 주요 하이퍼파라미터 탐색 공간을 자유롭게 설계하세요. n_estimators=1000, random_state=42, verbose=-1, n_jobs=-1 고정
        model = LGBMRegressor(
            n_estimators=1000, random_state=42, verbose=-1, n_jobs=-1,
            learning_rate=trial.suggest_float('learning_rate', 0.01,0.1),
            num_leaves=trial.suggest_int('num_leaves', 10,30),
            max_depth=trial.suggest_int('max_depth', 3,10),
            min_child_samples=trial.suggest_int('min_child_samples', 10,50),
            subsample=trial.suggest_float('subsample', 0.6,1.0), subsample_freq=1,
            colsample_bytree=trial.suggest_float('colsample_bytree', 0.6,1.0)
        )        
# 4. 검증 세트(eval_set=[(X_val, Y_val)])와 callbacks=[early_stopping(stopping_rounds=30, verbose=False)]를 적용해 학습하세요.
        model.fit(X_tr,Y_tr, eval_set=[(X_val,Y_val)], callbacks=[early_stopping(stopping_rounds=30, verbose=False)] ) 
        r2 = model.score( X_val,Y_val)
        cv_r2_scores.append(r2)
        best_itreations.append(model.best_iteration_)

# 5. 각 폴드의 검증 R2 점수(model.score)와 최적 반복 횟수(model.best_iteration_)를 기록한 뒤, 평균 최적 트리 개수를 trial.set_user_attr('best_n_estimators', int(np.mean(best_iterations)))로 저장하고 평균 R2 점수를 반환하세요.
    trial.set_user_attr( 'best_n_estimators', int(np.mean(best_itreations)) )
    return np.mean(cv_r2_scores)

# [단계 4] 베이지안 최적화(TPE) 수행 및 최적 하이퍼파라미터 도출
# 1. optuna.samplers.TPESampler(seed=42)를 적용해 direction='maximize' 기준의 study 객체를 생성하세요.
study = optuna.create_study(direction='maximize', sampler= optuna.samplers.TPESampler(seed=42) )

# 2. study.optimize()를 실행하여 목표 성능(R2 85% 이상)에 도달할 수 있도록 적절한 시도 횟수(n_trials)만큼 튜닝을 수행하세요.
study.optimize(objecctive, n_trials=10)

# 목표 달성 여부와 관계없이 최종 결과 출력
print('최고 교차검증 평균 R²:', study.best_value) # 최고 교차검증 평균 R²: 0.859096908159119

# 3. 도출된 최적 하이퍼파라미터(study.best_params)와 사용자 속성에서 추출한 자동 산출 최적 트리 개수(study.best_trial.user_attrs['best_n_estimators'])를 출력하세요.
print( '최적 하이퍼파라미터: ', study.best_params ) #최적 하이퍼파라미터:  {'learning_rate': 0.08029218200897703, 'num_leaves': 10, 'max_depth': 3, 'min_child_samples': 30, 'subsample': 0.9109447544977591, 'colsample_bytree': 0.9901774165289148}
optimal_model = study.best_trial.user_attrs['best_n_estimators']
print('최적 트리 수: ', optimal_model) # 최적 트리 수:  51

# [단계 5] 최종 모델 학습 및 회귀 성능·특성 중요도 평가
# 1. 도출된 최적 파라미터(study.best_params)와 n_estimators=optimal_n_estimators를 적용한 최종 LGBMRegressor를 생성하고 전체 X_train, Y_train으로 학습(fit)시키세요.
final_model = LGBMRegressor(random_state=42, verbose=-1, n_jobs=-1,
                            **study.best_params, n_estimators=optimal_model)
final_model.fit(X_train,Y_train)

# 2. Train R2 점수와 Test R2 점수를 각각 산출하여 출력하고, Test R2 점수가 0.85 이상인지 확인하세요.
print('Train r2: ', final_model.score(X_train,Y_train)) # Train r2:  0.8731899607717326
print('Test r2: ', final_model.score(X_test,Y_test)) # Test r2:  0.881962508898816

# 3. 최종 모델이 학습한 특성 이름(feature_names_in_)과 특성 중요도(feature_importances_)를 출력하여 주요 영향 변수를 확인하세요.
print( final_model.feature_name_ ) # ['age', 'bmi', 'children', 'sex', 'smoker', 'region']
print(final_model.feature_importances_) # [141  88  37   9  47  15]

# [단계 6] 모델 직렬화(저장/불러오기) 및 신규 고객 데이터 실시간 추론
# 1. joblib.dump를 사용하여 최적화된 최종 모델을 './lgbm_insurance_model.pkl'로 저장하고, joblib.load로 다시 불러오세요.
import joblib
joblib.dump(final_model, './day89_day19_1116/lgbm_insurance_model.pkl')
model = joblib.load('./day89_day19_1116/lgbm_insurance_model.pkl')

# 2. 신규 고객 2명의 원본 데이터(DataFrame)를 생성하세요:
sample = pd.DataFrame([{'age': 28, 'bmi': 23.5, 'children': 0, 'sex': 'female', 'smoker': 'no', 'region': 'southwest'},{'age': 52, 'bmi': 34.2, 'children': 2, 'sex': 'male', 'smoker': 'yes', 'region': 'southeast'}])

# 3. 범주형 카테고리 매핑 일치를 위해 신규 데이터의 cat_cols 컬럼 타입을 X_train[col].dtype과 동일하게 변환하세요.
for col in cat_cols:
    sample[col] = sample[col].astype('category')

# 4. 불러온 모델의 predict()에 전달하여 1번 고객과 2번 고객의 예측 연간 의료비를 출력하세요.
pred = model.predict(sample)
print( pred[0] ) # 4500.920403241691
print( pred[1] ) # 
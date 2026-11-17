import pandas as pd
import numpy as np
import optuna
import joblib

from lightgbm import LGBMRegressor,early_stopping
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

df = pd.read_csv('./python/train.csv')
print('원본 데이터 수:', len(df))

# 문자열 공백 및 결측값 정리
for col in df.select_dtypes(include=['object', 'string']).columns:
    df[col] = df[col].str.strip()
df = df.replace(['NaN', 'conditions NaN', ''], np.nan)

# 타깃을 숫자로 변환  "(min) 24" → 24
df['Time_taken(min)'] = pd.to_numeric(
    df['Time_taken(min)'].astype('string').str.replace('(min)', '', regex=False).str.strip(),errors='coerce')

# 정답이 없거나 0 이하인 행 제외
df = df.loc[df['Time_taken(min)'].notna()& (df['Time_taken(min)'] > 0)].copy()

# 수치형 컬럼 변환
coordinate_cols = [
    'Restaurant_latitude',
    'Restaurant_longitude',
    'Delivery_location_latitude',
    'Delivery_location_longitude'
]
number_cols = [
    'Delivery_person_Age',
    'Delivery_person_Ratings',
    'multiple_deliveries'
] + coordinate_cols
for col in number_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)

# 학습용 거리 계산
# 서비스에서는 거리를 직접 입력받지만,
# 원본 학습 데이터에는 좌표만 있으므로 거리로 변환
valid_coordinates = (
    df['Restaurant_latitude'].between(-90, 90)
    & df['Delivery_location_latitude'].between(-90, 90)
    & df['Restaurant_longitude'].between(-180, 180)
    & df['Delivery_location_longitude'].between(-180, 180)
    & df[coordinate_cols].notna().all(axis=1)
    & df[coordinate_cols].ne(0).all(axis=1)
)
lat1 = np.radians(df['Restaurant_latitude'])
lon1 = np.radians(df['Restaurant_longitude'])
lat2 = np.radians(df['Delivery_location_latitude'])
lon2 = np.radians(df['Delivery_location_longitude'])
a = (np.sin((lat2 - lat1) / 2) ** 2+ np.cos(lat1) * np.cos(lat2)* np.sin((lon2 - lon1) / 2) ** 2)
df['distance_km'] = 6371 * 2 * np.arcsin(np.sqrt(a.clip(0, 1)))
df.loc[~valid_coordinates, 'distance_km'] = np.nan

# 거리 결측값 및 100km 초과 행 제외
df = df.loc[df['distance_km'].between(0, 100)].copy()

# 평점 이상치 제거
invalid_rating = (df['Delivery_person_Ratings'].notna()& ~df['Delivery_person_Ratings'].between(1, 5))
df = df.loc[~invalid_rating].copy()

# 주문 시각에서 시간대 추출 # 원본의 "18:30:00"과 "18:30" 형식을 모두 처리 --> 시간만 사용
time_text = df['Time_Orderd'].astype('string')
order_time = pd.to_datetime(time_text,format='%H:%M:%S',errors='coerce')
order_time = order_time.fillna(pd.to_datetime(time_text,format='%H:%M',errors='coerce'))
df['order_hour'] = order_time.dt.hour

# 도시명 오타 통일
df['City'] = df['City'].replace('Metropolitian','Metropolitan')
df = df.reset_index(drop=True)
print('정제 후 데이터 수:', len(df)) 

#  8. 특성 및 타깃 구성
num_cols = [
    'distance_km',
    'order_hour',
    'Delivery_person_Age',
    'Delivery_person_Ratings',
    'multiple_deliveries'
]
cat_cols = [
    'Weatherconditions',
    'Road_traffic_density',
    'Festival',
    'City',
    'Type_of_vehicle'
]
feature_cols = num_cols + cat_cols

# 학습에 사용할 특성 + 정답
required_cols = feature_cols + ['Time_taken(min)']
before_count = len(df)

# 해당 컬럼 중 하나라도 결측값이면 행 제거
df = df.dropna(subset=required_cols).reset_index(drop=True)
print('제거 전:', before_count)
print('제거한 행:', before_count - len(df))
print('남은 행:', len(df))

# 수치형
for col in num_cols:
    df[col] = df[col].astype(float)
# 범주형: LightGBM의 범주형 처리 사용
for col in cat_cols:
    df[col] = df[col].astype('category')

X = df[feature_cols]
Y = df['Time_taken(min)']

print('\n사용할 특성:', feature_cols)
print('\n특성별 결측값 수:')
print(X.isna().sum())

# 훈련 / 테스트 분리
X_train, X_test, Y_train, Y_test = train_test_split(X, Y,test_size=0.2,random_state=42)

# 모델 
# 1) 목적함수
def objective(trial):
    cv = KFold(n_splits=5,shuffle=True,random_state=42)
    cv_r2_scores= [ ]       # 각 폴더별 검증 점수 저장 
    best_iterations = [ ]   # 각 폴더별 최적 트리 번호 저장 
    for train_idx, val_idx in cv.split(X_train, Y_train): # K번째 폴드의 훈련용/검증용 인덱스 반환 
        # 훈련 데이터 세트 내부에서 훈련용/검증용 분할 수행 , K=5 , 5개 폴드, 각각 한번씩 검증용
        X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
        Y_tr, Y_val = Y_train.iloc[train_idx], Y_train.iloc[val_idx]

        # 탐색할 파라미터로 모델 생성
        model = LGBMRegressor(
            n_estimators=1000,
            learning_rate=trial.suggest_float( 'learning_rate' , 0.01 , 0.1 ),
            num_leaves=trial.suggest_int('num_leaves', 10, 30),
            max_depth=trial.suggest_int( 'max_depth' , 3 , 10 ),
            min_child_samples=trial.suggest_int( 'min_child_samples', 10 , 50 ),
            subsample=trial.suggest_float( 'subsample' , 0.6 , 1.0 ), 
            subsample_freq=1, verbose=-1,random_state=42, n_jobs=-1, 
            colsample_bytree=trial.suggest_float('colsample_bytree',0.6,1.0)
        )

        # 학습 + 조기 종료
        model.fit(X_tr, Y_tr, eval_set=[(X_val, Y_val)], callbacks=[early_stopping(stopping_rounds=50,verbose=False)])

        # 폴드별 검증 R²와 최적 트리 수 저장
        cv_r2_scores.append(model.score(X_val, Y_val))
        best_iterations.append(model.best_iteration_)

    # 최적 트리 수의 평균 저장
    trial.set_user_attr('best_n_estimators',int(np.mean(best_iterations)))
    return np.mean(cv_r2_scores)

# 2) Optuna 탐색
sampler = optuna.samplers.TPESampler(seed=42)
study = optuna.create_study(direction='maximize',sampler=sampler)

study.optimize(objective, n_trials=20)

# 3) 최적 파라미터 확인
print('최적 파라미터:', study.best_params)
best_count = study.best_trial.user_attrs['best_n_estimators']
print('최적 트리 수:', best_count)
print('교차검증 평균 R²:', study.best_value)

# 4) 최적 파라미터로 최종 Pipeline 생성
final_model = Pipeline([
    ('model', LGBMRegressor(**study.best_params,n_estimators=best_count,subsample_freq=1,random_state=42,verbose=-1,n_jobs=-1))
])
final_model.fit(X_train, Y_train)

# 5) 최종 평가
Y_pred = final_model.predict(X_test)

train_r2 = final_model.score(X_train, Y_train)
test_r2 = final_model.score(X_test, Y_test)
mae = mean_absolute_error(Y_test, Y_pred)
rmse = np.sqrt(mean_squared_error(Y_test, Y_pred))

print('Train R²:', train_r2)
print('Test R²:', test_r2)
print('MAE:', mae, '분')
print('RMSE:', rmse, '분')

# Pipeline 내부 모델의 속성 확인
print(final_model.named_steps['model'].feature_name_)
print(final_model.named_steps['model'].feature_importances_)

# 최적 파라미터: {'learning_rate': 0.06724618801451224, 'num_leaves': 30, 'max_depth': 9, 'min_child_samples': 16, 'subsample': 0.8448777555981579, 'colsample_bytree': 0.9166672626440991}
# 최적 트리 수: 142
# 교차검증 평균 R²: 0.7908356335856417  ``
# Train R²: 0.8051556646638649
# Test R²: 0.7922646662176822
# MAE: 3.3548935308462196 분
# RMSE: 4.24283782293311 분
# ['distance_km', 'order_hour', 'Delivery_person_Age', 'Delivery_person_Ratings', 'multiple_deliveries', 'Weatherconditions', 'Road_traffic_density', 'Festival', 'City', 'Type_of_vehicle']
# [977 295 581 598 295 463 274 110 155 370]

# 6) 모델 및 평가 지표 저장
metrics = {'r2': float(test_r2),'mae': float(mae),'rmse': float(rmse),'cv_r2': float(study.best_value)}

joblib.dump(final_model, './python/delivery_model.pkl')
joblib.dump(metrics, './python/delivery_metrics.pkl')


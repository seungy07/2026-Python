import pandas as pd
import numpy as np
import optuna
import joblib

from lightgbm import LGBMRegressor,early_stopping
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

model = joblib.load('./python/delivery_model.pkl')
received_data = {
    'distance_km': 7.5,
    'order_hour': 18,
    'Delivery_person_Age': 28,
    'Delivery_person_Ratings': 4.5,
    'multiple_deliveries': 1,
    'Weatherconditions': 'conditions Sunny',
    'Road_traffic_density': 'Low',
    'Festival': 'No',
    'City': 'Urban',
    'Type_of_vehicle': 'motorcycle'
}

# 받은 값을 하나의 행으로 만들기
sample = pd.DataFrame([received_data])
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

# Python에서 학습 때와 같은 컬럼 순서·타입으로 맞추기
sample = sample[num_cols + cat_cols]

for col in num_cols:
    sample[col] = sample[col].astype(float)

for col in cat_cols:
    sample[col] = sample[col].astype('category')

pred = model.predict(sample)

print(f'예상 배달 소요 시간: {pred[0]:.2f}분')
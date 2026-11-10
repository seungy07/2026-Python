import joblib
import pandas as pd

# 1. 모델 불러오기, joblib.load(모델경로)
loaded_model = joblib.load('./day85_day15_1110/fish_model.pkl')

# 2. 불러온 모델로 예측 테스트
sample = pd.DataFrame({'Length2':[32,40], 'Height':[10,60], 'Width':[4,2]}) # 특성명은 같이 : 임의값

pred = loaded_model.predict(sample) 
print('예측값/무게: ', pred) # 예측값/무게:  [335.20056114]


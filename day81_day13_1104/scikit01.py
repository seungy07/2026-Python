# [사이킷런 scikit-learn] 방대한 머신러닝 알고리즘 모델 제공
# pip install scikit-learn

# 머신러닝 목표: 추론/예측 과정
# 특성(feature): 모델이 학습하는 자료 정보 , 
# 타깃(target): 모델이 맞춰야하는 정답 정보

# 지도학습: 특성과 다깃을 모두 제공하여 학습(정답O) , 회귀/분류
# 비지도 학스비 타깃없이 특성만으로 제공하는 학습 (정답X) 군집/텍스트마이닝(분석) 토픽/주성분분석(PCA)

# (회귀모델)
# 1) 다순 선형 회귀
import pandas as pd
df = pd.read_csv('./day81_day13_1104/Fish.csv')
df.info()

# 2) 모델 학습에 사용할 데이터 추출 (수치형)
# 특성 : Length2 (물고기 대각선 cm)    ,  # 타깃 : Weight(물고기 무게 g)

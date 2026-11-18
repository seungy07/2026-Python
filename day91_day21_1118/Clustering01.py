# 지도학습 : 특성(독립변수)과 타깃(종속변수) 모델에 학습하여 예측, 회귀 r2 분류 f1-score 평가지도
# 비지도 학습 : 특성 모델을 이용하여 거리/밀도 계산 -> 군집/클러스터/그룹   , 최적의 K (SSE, 실루엣)

import pandas as pd
url = "https://raw.githubusercontent.com/arunk13/MSDA-Assignments/master/IS607Fall2015/Assignment3/student-mat.csv"
df = pd.read_csv(url, sep=';')

X = df[['studytime', 'absences', 'G1', 'G2', 'G3']] # 공부시간, 결석일수, 1~3학기 성적 
# 타깃/종속 없음. -> 비지도 학습

from sklearn.model_selection import train_test_split # 학습 98% / 검증 2% (중요도 떨어짐)
X_train, X_test = train_test_split(X, test_size=0.02, random_state=42) # 

# 1) 스케일링/단위 표준화 , 
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
X_train_scaled = ss.fit_transform(X_train)
X_test_scaled = ss.transform(X_test)

# 2) 군집 = 그룹만들기 = 클러스터, K개의 군집을 찾는 Kmeans 모델
from sklearn.cluster import KMeans # n_clusters= 군집수
model = KMeans(n_clusters=3, random_state=42) # 모델 생성 , 주의할점 : 만역에 최대학생 10일떄 클러스터 수 10명은 의미 없다.
model.fit(X_train_scaled) # 군집 학습
train_labels = model.predict( X_train_scaled ) # 군집 추론
print('앞에서 10명 그룹 확인: ', train_labels[:10])  # 앞에서 10명 그룹 확인:  [0 1 1 0 1 2 1 2 0 2]

print('테스트 학생 군집 예측 결과: ' ,model.predict(X_test_scaled)) # [2 1 0 2 2 1 1 2]

# 3) 시각화 : 특성 여러개 이므로 2D 시각화 한계
import matplotlib.pyplot as plt
plt.scatter( X_train_scaled[:,4], X_train_scaled[:,1], c=train_labels )
plt.scatter(X_test_scaled[:,4], X_test_scaled[:,1], marker='*', c='red')
plt.title('k-means Clustering')
plt.xlabel('scaled G3')
plt.ylabel('scaled absences')
plt.show()

# pandas 복습
# import pandas as pd
# list = [ [2,3],[4,5]]
# list_2 = pd.DataFrame(list)
# print( list_2.iloc[:,1])

# 4) 최적의 k(군집/그룹) 수 찾기 vs 지도학습(F1 분류/R2 회귀)
from sklearn.metrics import silhouette_score
sse_list = []
sil_list = []

for k in range(2,20): # range(시작값, 끝값 -1)
    k_temp = KMeans(n_clusters= k, random_state=42) # k 반복마다 학습 모델 생성
    preds = k_temp.fit_predict(X_train_scaled) # 모델 학습/추론 동시에, fit + predict
    sse_list.append( k_temp.inertia_ ) # 군집 결과에 각 샘플과 중심점 거리 제곱의 합 저장
    sil_list.append( silhouette_score(X_train_scaled, preds) ) # 실루엣 점수를 저장
plt.plot(range(2,20), sse_list, marker='o') # sse
plt.show()
 
plt.plot(range(2,20), sil_list, marker='o') # 실루엣
plt.show()

# SSE : 엘보우 지점(기울기가 완만하게 꺽이는 변곡점)  
# 실루엣 :  높은 값 일수록 이상적        
# 두 차트 해석하여 최적의 K 해석 
# 최적 K 군집하기
best_model = KMeans( n_clusters=5, random_state=42 )
pred = best_model.fit_predict(X_train_scaled)
print(pred[:10]) # [3 4 1 3 2 4 1 4 4 4]

# 5) HDBSCAN   # k-means 다르게 *밀도 기반으로 군집, 이상치(-1) 자동 탐지
from sklearn.cluster import HDBSCAN
# HDBSCAN(min_cluster_size= 군집을하기위한 최소데이터수(기본값5), min_samples=군집 판별할 떄 계산되는 이웃 수)
hdb = HDBSCAN(min_cluster_size=15, min_samples=5)
pred = hdb.fit_predict(X_train_scaled)
print(pred) # 군집4개  # 이상치 -1 


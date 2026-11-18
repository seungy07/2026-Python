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
# min_cluster_size : 클수록 군집수 적어짐. min_samples : 클수록 이상치 많아짐.
hdb = HDBSCAN(min_cluster_size=30, min_samples=5)
pred = hdb.fit_predict(X_train_scaled)
print(pred) # 군집4개  # 이상치 -1 

X_train['hdb_cluster'] = pred
print( X_train['hdb_cluster'].value_counts() ) # (min_cluster_size=18, min_samples=3) 변환으로 바뀜
# 0 194 , 1 85 , 2 56 , -1 32 , 3 20   -> 15 , 5
# 1 183, 2 88 , 0 81 , -1 35   - > 30 , 3

# 시각화: 이상치 * 와 군집데이터 O 표시
nosie_mask = (X_train['hdb_cluster'] == -1)
plt.scatter(X_train.loc[~nosie_mask, 'G3'], X_train.loc[~nosie_mask, 'absences'], c=X_train.loc[~nosie_mask, 'hdb_cluster'])
plt.scatter(X_train.loc[nosie_mask, 'G3'], X_train.loc[nosie_mask, 'absences'], c='red', marker='*')
plt.show()

# 6) PCA(주성분 분석) : 고차원 데이터의 분산을 저차원으로 축소하여 주성분/특성
# 고차원이란? 다수의 특성들의 가중치/기울기 표현, 상관계수 : 두 특성이 어느 방향으로 어느 정도로 변하는지 나타내는 숫자
# 1차 -> 다차 방정식 
from sklearn.decomposition import PCA
# PCA( n_components=차원수 )
pca = PCA( n_components=2 , random_state=42) # 시각화를 하기 위한 2차원 축소
# 딥러닝( 이미지 3차원 -> R(1)G(2)B(3)이미지수(4)--> 흑백 --> G(1)장수(2) )
# 사진에 고양이가 있어 없어? 칼라사진 -> 흑백으로 차원 축소
X_train_pca = pca.fit_transform(X_train_scaled)
print(X_train_pca)        # 행 마다의 가중치
print(pca.components_.T) # 주 특성별 가중치
#      주성분1     주성분2
# [[ 0.13219328 -0.61408979]    공부시간 
#  [-0.00599139  0.78051288]    결석일수
#  [ 0.56213 845  0.00343157]    1학기 성적
#  [ 0.58342273  0.03443535]    2학기 성적
#  [ 0.57105808  0.11178463]]   3학기 성적
# 주성분1 에서 강한(+)? 1학기/2학기/3학기 성적들 
pca_hdb = HDBSCAN( min_cluster_size=30, min_samples=5 )
pca_pred = pca_hdb.fit_predict( X_train_pca ) # 5차원에서 2차원으로 축소
X_train['PC1'] = X_train_pca[:, 0]
X_train['PC2'] = X_train_pca[:, 1]
X_train['PCA_cluster'] = pca_pred
print( X_train.loc[X_train['PCA_cluster'] != -1,['PC1', 'PC2', 'PCA_cluster']].head(5) )
#          PC1       PC2  PCA_cluster
# 116  0.808827 -0.220407            2
# 9    1.758814 -0.368879            2
# 393  0.000504  0.206730            0
# 155 -0.714701 -0.412403            1
# 272  0.124762 -0.311819            1
# 클러스터2는 상 (PC1에서 강한 양수)
# 클러스터1는 하 (PC1에서 음의 양수)
# 클러스터0는 중 (PC1에서 0에가까운 평균이므로)

# 7) 이상치 제외한 G3 평균 계산 
noraml_clusters = X_train[ X_train['PCA_cluster'] != -1 ] # 이상치 제외  
cluster_means = noraml_clusters.groupby('PCA_cluster')['G3'].mean() # 2 1 0
sorted_cluster = cluster_means.sort_values( ascending = True ) # T오 / F내 
print(sorted_cluster) # 클러스터별 G3 평균 점수  와  PC1 예측 비교
# PCA_cluster
# 1     9.873239
# 0    12.500000
# 2    13.641509
# 클러스터 2가 상위권이다 라는 라벨링 근거

# 8) 라벨링
labels = {}
for idx, cluter_id in enumerate( sorted_cluster.index):
    labels[ cluter_id ] = f'Level{idx}'

labels[-1] = 'Outlier' # 이상치는 리스트 가장 뒤에
print(labels) # {1: 'Level1', 0: 'Level2', 2: 'Level3', -1: 'Outlier'}

X_train['pca_cluster_label'] = X_train['PCA_cluster'].replace(labels)
print(X_train) # 군집화한 결과 가지고 추후에 지도학습
# 지도 학습에서 성능 향상 하기 위한 방법 -> 0) 전처리  1) 하이퍼파라미터 설정   2) 파생변수
# # 특성이 다양할 수록 성능 up 
 
# 9) PCA 시각화
for lbl in list(labels.values()):
    sub = X_train[X_train['pca_cluster_label']== lbl]
    if lbl == 'Outlier':
        plt.scatter(sub['PC1'], sub['PC2'], c='red', marker='*', label=lbl)
    else : 
        plt.scatter(sub['PC1'], sub['PC2'], marker='o', label = lbl)
plt.legend()
plt.show()

# PCA 시각화하게 되면 특성들을 2가지(2D) 형태 표현 가능함.
# 현재 주성분 PC1(G1 G2 G3) , PC2(공부시간, 결석일수)

import numpy as np

# 1차원 배열 통계 함수
x = np.array( [1,2,3,4,5] )
print( np.min(x), np.max(x) ) # 최솟값, 최댓값
print( np.argmin(x), np.argmax(x)) # 최솟값 위치, 최댓값 위치
print( np.sum(x), np.mean(x), np.median(x)) # 합계, 평균, 중앙값
print( np.var(x), np.std(x), np.sqrt(x)) # 분산, 표준편차, 각 요소의 양의 제곱근

# 2차원 배열 통계
# np.통계함수( 2차원 배열, axis 생략시 ) => 1차원 평탄화,  0 열기준 , 1 행 기준
y = np.array( [[1,2,3],[4,5,6]] )
# 배열의 축 (axis) 0: 가로(열)) , 1 세로(행)
print( np.min(y), np.max(y) ) # 1 6 , 2차원 => 1차원 평탄화 후 요소 통계갑 계산
print( np.min(y ,axis = 0), np.max(y, axis = 1) ) # [1 2 3] [3 6] 
print( np.argmin(y, axis=0) , np.argmax(y, axis=1)) # [2 2]
print( np.sum(y, axis = 0), np.mean(y, axis=0), np.median(y, axis=1))
print( np.var(y), np.std(y), np.sqrt(y))


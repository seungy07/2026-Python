import numpy as np

# 1] 병합, vstack( [배열1,배열2] ), hstack([배열1,배열2])
x = np.array([[1,2],[3,4]]) # 2차원 배열
y = np.array([[5,6],[7,8]])
z = np.vstack( [x,y] ) # .array 일때는 왜 한칸 떨어져서 나오는 거지? => 3차원
print(z) # 세로

z = np.hstack( [x,y] ) # 가로
print(z)

# 2] 병합2, concatenate( (배열1,배열2) )
z = np.concatenate( (x,y), axis=0 ) # axios = 0 세로방향, = 1 가로방형
print(z)
z = np.concatenate( (x,y), axis=1 )
print(z)

# 3] 정렬, .sort(배열): 오름차순 , [ : : -1] 내림차순
x = np.array( [3,1,4,2,5] )
print( np.sort( x ) ) # 오름차순
print( np.sort(x)[ : : -1 ] ) # 내림차순
print(x) # 원본은 안바뀜

x.sort() # 원본 자체가 변경
print(x)
# 2차원 정렬은 판다스 에서 pandas

# 4] 값 자체를 정렬하지 않고 배열을 정렬 위치 순번 반환
score = np.array( [75,95,60,88] )
z = np.argsort( score )  # 오름차순 기준. 정렬을 하지는 않음 
print(z)  # [2 0 3 1] 현재 리스트의 인덱스 기준으로, 정렬시 순번을 알려줌
print( z[-1] )

# 5] 필터링/조건식, *개발자 for 사용안함(장점): 공학/AI 라이브러리 => C언어 *
x = np.array( [10,20,30,40,50] )
print( x > 30 ) # 요소마다 연산, # [False False False  True  True]
print( x[ x > 30 ]) # 인덱싱 안에서 조건식 사용하면 True 값 추출, # [40 50]

y = np.array( [ [1,2,3],[4,5,6],[7,8,9] ])
print( y % 2 == 0 )
# [[False  True False]
#  [ True False  True]
#  [False  True False]]
print( y[ y % 2 == 0] ) # 차원 축소, 유지는 선택 
# [2 4 6 8]

# 6] 삼항연산자, np.where( 조건, 참, 거짓 )
print( np.where( x > 30, x, 0) )
print( np.where( y % 2 == 0, 1 ,0 ) ) # 학습은 0과 1로 학습, 라벨링 => 라이브러리 있ㄷ

# 7] 다수 조건, & | ~(not)
# 조건이 2개 이상이면 () 또는 변수,  a= y%2==0
a = y%2==0 
print( y[ (y%2== 0) & (y%4 == 0)] ) # () & () , [4 8]
print( y[ a | (y%4 == 0) ] ) # [2 4 6 8]
print( y[ ~a ] ) # [1 3 5 7 9] ,부정문 ~ 
# 주의할점 : C?JAVA에서 & 비트(0/1) 연산자, numpy에서는 &논리연산자 
# 넘파이는 파이썬에서 실행되는 구조( 중복에 따른 오버라이딩 제한 ) bool vs bool_


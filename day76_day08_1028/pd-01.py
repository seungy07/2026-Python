# 판다스 : 데이터 조작 및 분석(표형태) 라이브러리
# 설치 : pip install pandas, py -m pip install pandas
# 호출
import pandas as pd
print(pd.__version__) # pandas 버전 확인

# 1] 데이터프레임: 2차원(표) , pd.DataFrame( 리스트 )
data_list = [ [ 'ant' , 25 , 'seoul'] , ['bee' , 30 , 'busan'] , ['cat' , 35 , 'incheon'] ] # 2차원 리스트 

# pd.DataFrame( 2차원리스트 , columns = [ 열이름 ] , index = [ 행이름 ] )
x = pd.DataFrame( data_list , columns= ['name' , 'age' , 'city'] )
print(x) # 행과 열 -> 표형식

# 2] 데이터프레임2 , pd.DataFrame( 딕셔너리 ), 키(열)
data_dict = { 'name' : ['ant','bee','cat'] , 'age' : [25,30,35] , 'city' : ['seoul','busan','incheon'] } # 딕셔너리 
y = pd.DataFrame(data_dict)
print(x)

# 3] 컬럼 값 추출, df[ '열이름' ]
ages = y['age'] # 나이추출
print( ages ) # Name: age, dtype: int64  # Series(1차원)
print( type(ages) ) # <class 'pandas.Series'>
print( type(ages.values) ) # <class 'numpy.ndarray'>

# 4] 데이터프레임3 : 넘파이,
import numpy as np
data_np = np.array( data_list ) # numpy 자료
df = pd.DataFrame(data_np, columns= ['name' , 'age' , 'city'], index=['a','b','c'])  # numpy -> pandas 호환
print(df)

# 5] 주요 속성
print( df.shape ) # 행/열 크기 # (3, 3) 
print( df.columns ) # 컬럼 목록 Index(['name', 'age', 'city'], dtype='str')
print(df.index) # 인덱스 목록 Index(['a', 'b', 'c'], dtype='str')
print( df.values ) # 값만 2차원 리스트로 추출
print( df.head(2) ) # 상위 n개만 반환
print( df.tail(2) ) # 하위 n개만 반환

# 컬럼이름, 결측치, 타입확인
df.info() # print 내장,  컬럼 정보(타입확인), 결측치에 대한 정보도 포함
# <class 'pandas.DataFrame'>
# Index: 3 entries, a to c
# Data columns (total 3 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   name    3 non-null      str  
#  1   age     3 non-null      str  
#  2   city    3 non-null      str  
# dtypes: str(3)
# memory usage: 96.0+ bytes

# 6] 인덱싱
print( df.iloc[1] )  # df.iloc[인덱스] , 인덱스 행 반환
print( df.iloc[1 , 2]) # [행 인덱스, 열 인덱스]  # 인덱스 행에 인덱스 번째 요소 

print( df.loc[ 'b' ] ) # .loc[ 인덱스명 ] # 지정한 인덱스 이름 번째 행 반환
print( df.loc['b' , 'city'] ) # loc[행명, 컬러명]  

# 7] 슬라이싱
print( df.iloc[ 0:2, 0:1 ]) # [행슬라이싱, 열슬라이싱]
print( df.loc['a':'b' , 'name':'city'] ) # 시작 , 끝 모두 포함
 
# 8] 열 추가, df[ '새로운열' ] = 새로운 값
df['score'] = [100,200, 95]  # 개수가 맞않으면 오류, 공백 혹은 0으로 채워야함
print(df)

# 9] 값 수정 , df['수정열'] =  새로운 값
df['age'] = [ 1, 2, 3]
print(df)

df.loc['b', 'age'] = 20 # b행 age 열
print(df)
df.iloc[0 , 0] = 'ap'
print(df)

# 10] 여러개 수정, 
df.loc[ ['a','b'] , 'score'] = [100,300]
print(df)

# 11] 필터링(조건)
print( df['score'] > 70 ) # 조건 True/False 만 나옴
# a    True
# b    True
# c    True
print( df[ df['score'] > 70 ] ) # 조건에 참인 것만 원본에서 추출 
print( df[ (df['score'] > 70)  & (df['age'] >= 20) ] )
print( df[ (df['score'] > 70)  | (df['age'] >= 20) ] )

# 필터링 이용하여 새로운 열 **
df.loc[ df['score'] > 100, 'passed' ] = True
print( df ) 

# 12] 컬러명 변경, df.rename( columns= { '기존열이름' : '새로운컬러명' } )
df = df.rename( columns= { 'city' : '도시', 'age' : '나이' })
print(df)

# 13] 집계, .describe() : 수치 자료들 집계요약,  df['열이름'].집계함수()
print( df.describe() ) 
print( df['나이'].sum())
print( df['passed'].value_counts() ) # 자료 빈도 수

# 14] 합치기 / 병합
df1 = pd.DataFrame({'ID': [1, 2, 3], 'Score': [90, 80, 85]})
df2 = pd.DataFrame({'ID': [4, 5, 6], 'Score': [75, 95, 88]})

# 세로 연결 pd.concat( [df1,df2] , axis = 0, ignore_index = True ) 
new_df = pd.concat( [df1,df2], axis=0 , ignore_index = True)
print(new_df)

new_df2 = pd.concat([df1,df2], axis=1)
print(new_df2)

# 병합 : 교집합(공통 컬럼)
df_info = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['Ant', 'Bee', 'Cat']})
df_score = pd.DataFrame({'ID': [2, 3, 4], 'Score': [88, 92, 85]})

# pd.merge( df1, df2, on="공통컬럼명", how=방향) 방향: inner / outer
new_df = pd.merge( df_info, df_score, on='ID' , how='inner')
print(new_df)
new_df = pd.merge( df_info, df_score, on='ID' , how='outer') # 정의가 없는 자료는 NaN 으로
print(new_df) 

# 15] 정렬, df.sort_values( by='컬럼명', ascending=True(오름차순/기본값) False (내림차순) )
df = pd.DataFrame({
  'name': ['Ant', 'Bee', 'Cat', 'Dog'],
  'age': [27, 27, 22, 32],
  'score': [88, 95, 85, 90]
})

new_df = df.sort_values( by='age', ascending=False )
print(new_df)

# 다중 정렬, [ ] 사용, ** age기준으로 1차 정렬 후 동일한 age끼리 2차정렬 (중복 없으면 무의미)
new_df = df.sort_values( by=['age', 'score'], ascending=[True,False])
print(new_df)

# 컬럼명 정렬 axis=1,  axis=0 행 정렬
new_df = df.sort_index( axis=0, ascending=False)
print(new_df)


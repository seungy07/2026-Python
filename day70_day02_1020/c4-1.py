# p.192
# 리스트란? 대괄호[]에 자료를 쉼표로 구분하여 여러 자료들을 저장
# [요소,요소,요소] , 요소 = element 
# 인덱스란? 리스트내 요소들이 저장된 순서, 0번시작 ~

list_a = [273,32,103, "문자열", True, False ] # 리스트 선언
print( list_a[2] ) # 인덱스
print(list_a[1:3]) # 1~2  [32,103] 슬라이싱

list_a[2] = 7 # 요소 값 수정/변경
print(list_a)
print(list_a[-2]) # # 파이썬에서는 인덱싱 음수로 가능 
print(list_a[3][1]) # 자 #문자열도 리스트/배열 # 문자 한개는 리터럴
# print(list_a[1][1]) # 오류 # 리터럴/ 1차원값
# 고차원 배열 = 판다스/데이터프레임워크 = 사진/ RGB   
list_1 = [ 1,2,3] # 1차원
list_2 = [ [1,2], [3,4], [5,6]] # 2차원
print(list_2[1][0])  # 3  #[행][열] => 판다스/데이터

# p.196  # 값 추가
list_a = [1,2,3]
list_b = [4,5,6]
print(list_a + list_b)
print(list_a * 3)
print(len(list_a)) # 3 길이 
list_a.append(4)     # append(값)  
print(list_a)
list_a.insert(1,10) # insert(삽입할 위치, 값)  (인덱스,값)
print(list_a)

list_aa = [ [1],[2],[3] ]
print(list_a + list_aa) # [1, 10, 2, 3, 4, [1], [2], [3]]

list_a.extend( list_b ) # [1, 10, 2, 3, 4, 4, 5, 6]
print(list_a) 

# 주의할점
list_c = [1,2]
list_c + [3]    # 방법1]   새로운 리스트 생성 (주소값 변경) ,  list_c 변화 없다
list_c.append(3) # 방법2] 기존 리스트 포함  list_c 변화 있다
print(list_c)

# 삭제하기
list_a = [1,2,3,4,5]
del list_a[2] # 반환하지 않고 삭제만    [인덱스]
print(list_a)   
list_a.pop(0) # 1  반환 후 삭제  (인덱스)
print(list_a)
del list_a[1:3] # del 키워드를 이용한 슬라이싱 삭제
print(list_a) 

list_a.remove(2)  # .remove(값) 값으로 삭제
print(list_a) # [ ]

list_a.clear() # 리스트명.clear() 전체 삭제
 
# 리스트 정렬 p.205
list_a = [ 4,7,2,3,2,0,1]
list_a.sort(reverse=True)  # .sort() 오름차순(기본값),  (reverse=True) 내림차순
print(list_a)

# p.204 슬라이싱, [시작인덱스 : 끝인덱스 : 단계 ]
print(list_a[::-1])

# p.206, 리스트 내부 있는지 확인 in / not in 연산자
list_a = [273,32,103,57,52]
273 in list_a  # True
99 in list_a    # False 
273 not in list_a   # False
99 not in list_a    # True

# p.208 리스트와 반복문, 리스트내 요소들이 순차적인 인덱스 구조
# for 반복변수 in 반복가능한자료:
#          실행 코드
for i in list_a:
    print(i) 
for i in "안녕하세요": # 문자열도 문자 리스트이기 때문에 
    print(i)

# 중첩 리스트와 중첩 반복문 p.210
list_a = [[1,2,3],[4,5,6,7],[8,9]]
for i in list_a:
    print(i)

# 구구단 작성
for i in range(2,10,1):
    for k in range(1,10,1):
        print( f"{i} * {k} = {i*k} ")

# 전개 연산자 p.211
a = [1,2,3,4]
print(*a) # 1 2 3 4
print(a) # [1,2,3,4]
b = [ *a, *a]; print(b) # [1, 2, 3, 4, 1, 2, 3, 4]
c = [*a,5]  # [1, 2, 3, 4, 5]
print(c)

# p.216 딕셔너리   
# 딕셔너리란? { } 중괄호 선언하고 키 : 값 형태로 쉼표로 연결
# { key : value, key : value, key : value }
# key 중복x / value 중복O
# JS:JSON , JAVA: MAP/DTO , DB: RECORD

# 1. 선언 
dict_a = { 'name' : '언벤져스 엔득임', 'type':'히어로 무비'}
# 2. 값 호출  , 딕셔너리명['key] => value
print(dict_a['name'])

# 딕셔너리 값 추가 p.221
# 딕셔너리명['새로운 키'] = 새로운 값
dict_a['price'] = 20
print(dict_a)
dict_a['type'] = "호러" # 이미 존재하는 키는 값 수정

# 삭제  , del 딕셔너리명['키'] 
del dict_a['name'] # {'type': '호러', 'price': 20}

# p.224  딕셔너리 내 키 존재 여부 in
'type' in dict_a  # true
'type' not in dict_a # False
# .get('key') 키 접근 
print( dict_a.get('name') ) # name 없기 때문에 None 출력
print( dict_a.get('price'))

# 속성값 호출, 방법1: 딕셔너리명['key'], 방법2: 딕셔너리명.get(key)
# 차이점 : 반환 차이 , 방법1) 존재하지않으면 예외 발생 , 방법2) 존재하지 않으면 None 반환

# for 키변수 in 딕셔너리, 
for key in dict_a:
    print(key, ":", dict_a[key]) # 방법 1
    print( dict_a.get(key))       # 방법 2


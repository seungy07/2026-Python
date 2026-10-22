# p.317 
# 튜플이란? 여러 자료들을 저장하는 리스트와 비슷한 자료형
# 특징 : 초기화 이후 수정 불가(불변)
# 장점 : VO (불변성, 읽기 전용), 수정 없는 자료(리스트보다 성능 좋음) = 메모리효율 좋음
# (요소,요소,요소)

# 1. 튜플선언
tuple_test = (10,20,30)
# 2. 요소값 호출
print( tuple_test[0], tuple_test[2] )
# 3. 요소값 수정
tuple_test[0] = 40 # 'tuple' object does not support item assignment , 수정불가 오류
# 4. 요소가 하나인 경우
tuple_test2 = (273,) # (237) , 없이 선언시 값 취급으로 인덱스를 사용못함
print(tuple_test2[0])
# 5. 튜플은 소괄호 생략해도 된다.
(a, b ) = (10,20)
print(a,b)

a,b = 10,20
print(a,b)  #10 20  괄호 없이 줌 ,range() 도 

# p.320
# - 스왑
a,b = b,a  # a에 b 값 대입, b에 a값 대입
# -리액트(JS)에서 비슷한 문법존재 => 구조분해 (useState, props)
# name, age = { name:유재석, age:1}
c , d = [ 30,40]
print(c,d)

# enumerate(리스트) => [(인덱스,값),(인덱스,값)]  딕셔너리.items() => (키,값) , (키,값) 

# 6. 함수/연산 결과는 항상 1개 (return) 
def test():
    return 10,20 # 결과는 1개 (10과 20 튜플로 묶은 1개)

# p.322
# 7. 콜백함수 : 함수 그 자체를 매개변수 전달하여 전달받은 곳에서 함수 호출
# 리액트 : onClick( 회원가입() ) [x]  --> onClick( 회원가입 ) [o]
def call_10_items( func ):
    func()
def print_hello():
    print("안녕")
call_10_items(print_hello()) # print_hello() 결과값 전달 
call_10_items(print_hello) # print_hello 함수 (그 자체) 정보 전달

# p.323 
# java : 리스트.stream.forEach() , 리스트.stream.map() or . filter()
# react : 리스트.forEach() , 리스트.map() , 리스트.filter()
# python : for x in 리스트, map(코드, 리스트), filter(코드,리스트)
# forEach 단순반복(return X), map 반복+반환(return O), filter 반복+(참이면) 반환

#예제, map
def power( item ):
    return item*item
def under_3( item ):
    return item < 3
list_a = [ 1,2,3,4,5 ]
print( list( map( power, list_a ) ) )  # map( power, list_a ) => <map object at 0x00000223FE93F100>
# JS : list_a.map( power )  vs  list_a.map( x-> return x*x )

# filter
print( list( filter( under_3 , list_a) ) ) # 리스트로 변환 <filter object at 0x00000223FCFAAE60>
# Js filter : list_a.filter( under_3 ) , list_a.filter( x -> return x < 3)

# p.324 람다? 코드 줄이기
# lambda 매개변수 : 리턴값
power = lambda item : item*item
under_3 = lambda item : item <3
list_a = [ 1,2,3,4,5 ]
print( list( map(power, list_a) ))

# p.326, 인라인 람다
output = map( lambda item : item*item, list_a )

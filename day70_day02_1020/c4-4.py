# p.251
numbers = [103,52,273,32,77]
print(min(numbers))
print(max(numbers))
print(sum(numbers))

# p. 252 revered(리스트)
numbers_revered = reversed(numbers) # 리스트 뒤집기
print( list(numbers_revered))
# int( ) float() str() list() : 특정 타입으로 변환 함수
# p.264 이터레이터
print(next(numbers_revered))
# 이터러블 : 요소들을 하나씩 차례로 꺼내기 가능한 객체 의미
# 이터레이터 : 이터러블 중에서 하나씩 차례로 꺼낼 수 있는 요소
# 가능 타입 : 리스트, 딕셔너리, 문자열, 튜플
# 이터레이터 하나씩 꺼내는 함수 = next() 함수 ---> 이터러블

del list
# p.254 enumerate(리스트) , [(인덱스,값),(인덱스,값)]
numbers = [103,52,273,32,77]
print(enumerate(numbers)) #<enumerate object at 0x00000260607831F0> 이터레이터 객체
print(list( enumerate(numbers))) # [(0, 103), (1, 52), (2, 273), (3, 32), (4, 77)]

# p.256  딕셔너리.items(), [ (key,value), (key, value)]
dict_a = {"name":"유잭석", "age":20}
for key,value in dict_a.items():
    print(key,":",value)

# p.258 리스트 내포, 인덱스 자리에 반복문 사용가능
# 0부터 20까지 2씩 증가한 자료들을 리스트에 저장
# 방법 1)
array = []
for i in range(0,21,2):
    array.append(i)
# 방법 2)
array = [ i for i in range(0,21,2) if i != 10 ] # 참인것만 리스트에 즐어감
print(array)
# 표현식 for 반복자 in 반복할 수 있는 것 if 조건문 

# p.263 , .join()
# 방법 1] """여러줄"""
print("""
    안녕1
    안녕2
""")
# 방법 2) \n 제어문자
print("안녕1\n안녕2")
# 방법 3) ("문자열" "문자열" "문자열") 튜플
print( ("안녕1\n" "안녕2"))
# 방법 4) 사이문자열.join(리스트), 리스트 요소 사이마다 특정문자열 삽입
print( "\n".join(["안녕1","안녕2","안녕3"]))
print("-".join("유재석")) # 유-재-석   # 문자열도 리스트,

"{:b}".format(10)

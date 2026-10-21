# p.274 ~
# 함수란? 코드의 집합 
    # 값 저장 = 변수 , 실행코드저장 = 함수 
    # 값 여러개 저장 = 리스트/딕셔너리/튜플
# 매개변수란? 함수를 호출할 때는 괄호 내부에 여러 가지를 넣는 변수
# 리턴값? 함수를 호출해서 최종적으로 나오는 결과

# def 함수명( 매개변수명 ) :
#       실행문

# 값 재사용 = 변수 , 코드 재사용 = 반복문/함수
# "안녕하세요" 3번 출력 반복 -> 반복문(반복 패턴 존재) or 함수(입력/출력)
#  반복패턴 : 리스트(인덱스)  /  회원가입 함수 , 회원목록에서 중복아이디 찾기 => 반복문 

# 1. 기본적인 함수
def print_3_times():  # 함수 정의/만들기
    print("안녕!")
    print("안녕!")
    print("안녕!")
print_3_times()  # 함수 사용/호출
# vs , 식별자란?  p.71 변수/함수명
for i in range(0,3,):
    print("안녕!")

# 2. 매개변수란? 매개(중매-서로 다른 곳에서 연결), 인수/인자값 -> 매개변수
# 파이썬 { }가 아닌 탭(들여쓰기) 이용하여 구역 구분
def print_3_times(value, n):
    for i in range(n):
        print(value)
print_3_times("반갑",2)
# print_3_times("qks") # 매개변수를 하나만 넣으면 혹은 더 넣어도 오류 , 지정 수 만큼 넣어야함

# 가변 매개변수  p.278  p.211 전개연산자 *
# def 함수명(매개변수, 매개변수, *가변매개변수):
def print_n_times(n, *values):
    for i in range(n):
        for value in values:
            print(value)
        print() # 줄바꿈 용
# print_n_times("HI","b","A", 3) # 어디까지가 가변 매개변수인지 몰라 오류, 가변매개변수 뒤로는 X 
print_n_times(3,"HI","b","A")
# 조건 1: 가변매개변수가 가장 뒤로 정의.
# 조건 2: 1번만 사용

# p.279, 기본 매개변수, 매개변수에 기본값 대입 형태, 인수/인자 값 생략시 적용
# 매개변수=값  형태 => 기본 매개변수
def print_n_times2(value , n=2): # 기본 매개변수 뒤에는 일반 매개변수가 올 수 없다
    for i in range(n):
        print(value)
print_n_times2("반갑")  # 기본매개변수 생략시 초기 정해진 값이 들어가짐
print_n_times2("반갑",1)    

#p.280 키워드 매개변수
def print_n_times1(n=2, *values): # 기본 매개변수가 가변 매개변수보다 앞에 오는 경우
    for i in range(n):
        for value in values:
            print(value)
        print()
print_n_times1("HI","b","A") # TypeError: 'str' object cannot be interpreted as an integer

def print_n_times3(*values, n=2): # 기본 매개변수가 가변 매개변수보다 뒤에 오는 경우
    for i in range(n):
        for value in values:
            print(value)
        print()
print_n_times3("HI","b","A")  # n번 출력 
# 기본 매개변수가 가변 매개변수보다 앞에 올 때, 오류
# 가변 매개변수가 기본 매개변수보다 앞에 올떄, 기본 매개변수 인자값 없다
# 해결 방안 : 키워드 매개변수    

print("안녕하세요1", end="\n") # end매개변수는 출력 후 무엇을 할지 # \n 기본값 = 기본 매개변수
print("안녕하세요2", end="") # 키워드 매개변수란? 인수 대입시 매개변수명 지정
print("안녕하세요3")  # 안녕하세요2안녕하세요3
# (가변매개변수, 키워드 매개변수)

def print_n_times4(*values, n=2):
    # *매개변수 -> 가변매개변수  # 매개변수명=기본값 -> 기본매개변수
    for i in range(n):
        for value in values:
            print(value)
        print()
print_n_times4("안녕","파이써","즐겁?", n=3) # 3번반복  n=3 키워드 매개변수
print_n_times4("안녕","파이써","즐겁?", 3) # 키워드로 지정하지않아서 3까지 가변매개변수로 인식..


# p.285 리턴이란? 함수가 종료되면서 반환 되는 값
def return_test():
    print("A")
    return   # 함수를 실행했던 위치로 돌아가 함수를 끝낸다는 의미. 함수종료/함수끝
    print("B")  # => 함수 포함안됨
return_test() # A 출력 

def return_test1(): 
    return
print(return_test1())  # None # 아무것도 리턴하지 않는 함수의 값을 할당하고있다는 경고문 뜸

# p.287
def sum_all(start, end):
    output = 0
    for i in range(start,end+1):
        output += i
    return output
print("0 to 100: ", sum_all(0,100))
print("0 to 1000: ", sum_all(0,1000))
print("50 to 100: ", sum_all(50,100))
print("500 to 1000: ", sum_all(500,1000))

def sum_all1(start=0, end=100, step=1):
    output = 0
    for i in range(start,end+1,step):
        output += i
    return output
print("A.", sum_all1(0,100,10))
print("B.", sum_all1(end=100))
print("C.", sum_all1(end=100, step=2))


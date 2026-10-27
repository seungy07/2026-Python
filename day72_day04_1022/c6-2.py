# p.382
# try:
#   예외가 발생할 가능성 있는 구문
# except 예외의 종류 as 예외객체를 활용할 변수명 :
#   예외가 발생했을 때 실행할 구문

# [예외 객체란] 발생한 예외 정보 갖는 객체
# 예외 클래스 : Exception(예외 최상위 클래스)
# except 예외 클래스명 as 변수명 :
# as 키워드 : 클래스의 객체변수 생성
# 그 외 모든 예외 처리 : 여러개 except에서 Exception 항상 마지막 위치
# 주의할점 : Exception 앞에 위치하면 아래 예외가 작동 안함 -> 상속 개념(예외 클래스 업캐스팅)
# p.388
# p.391 
# raise : 강제로 예외 발생, 주로 CRUD 실패 의미
# raise 예외 객체

# p.383
list_number = [52,279,32,72,100]
try:
    number_input = int( input("정수입력: ") )
    print( list_number[ number_input ] )
    raise NotImplementedError # 강제 예외 발생
    # JAVA : throws new 예외 클래스()

except ValueError as e:
    print(e)
except IndexError as e:
    print(e)
except Exception as e:
    print(e)

a = 10
def s(b):
    b = b + 1
    print(b)
    print(a)
s(a)

output = [i for i in range(1,101) if "{:b}".format(i).count("0") == 1]
print(output)


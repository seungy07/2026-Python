# p.360
# 구문 오류 : 실행 전 오류, 실행 자체 불가능
# 런타임 오류 : 실행 중 오류, 예외
# 예외 처리 : 예외를 해결하는 모든 것을 

# 조건문 또는 try
# 조건문)
input_a = input("정수입력: ")  
if input_a.isdigit():  #  문자열.isdigit() : 문자열 타입의 값이 숫자이면 True
    number_input = int(input_a)  # 문자열시 ValueError
    print(number_input)
else:
    print("정수 입력")

# try except )
try:
    number = int( input("정수 입력 try: ") )
    print(number)
except: # 아무것도 없을 시 구문 오류 발생
    # print("다시")   
    pass
else:
    print("예외 발생안함")
finally:
    print("마지막에 무조건 실행")
# try:
#   예외가 발생할 코드
# except:
#   예외 발생시 실행 코드
#   pass # 통과 키워드
# else:
#   예외가 발생하지 않았을 때 실행 코드
# finally:  # 활용) 파일 실행 후 파일 닫기/종료 용도
#   무조건 실행할 코드

# p.374  closed 속성   , finallt 활용 예
try:
    file = open("info.txt", "w")
    # open(파일명, 옵션) 파일 불렁기 함수 # W 옵션: 파일이 없으면 생성
    예외.발생() # 일부러 예외 발생 부분
    # file.close()  # 파일 닫기
except:
    print("예외.발생 부분")
finally:
    file.close()
print(file.closed)
# try 에서 예외발생시 발생 코드 이후는 실행이 안됨. 

# finally 사용 : return 함수 종료시 무조건 실행 할 코드로 사용.
# break 키워드 사용시 반복문 종료 + finally 무조건 실행 코드  + 추가 적인 코드 작성가능(반복문 밖)


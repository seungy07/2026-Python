# p.293 재귀함수, 재귀란 자기 자신을 호출하는 것
# 팩토리얼 구현  1) 반복문  2)재귀함수
# 1) 반복문
def factorial(n):
    output = 1
    for i  in range(1,n+1):
        output *= i 
    return output
factorial(3)

# 2) 재귀함수
def factorial(n):
    if n == 0:  # 무한 재귀를 막기 위한, 방지가 있어야함
        return 1
    else:
        return n * factorial(n-1)
factorial(3)

# * 구구단 예시
for 단 in range(2,10):
    for 곱 in range(1,10):
        print(단*곱)

# 구구단 재귀
def 구구단( 단=2, 곱=1):
    if 단 > 9 : # 재귀끝
        return 
    if 곱 > 9 :
        구구단(단+1, 1) # 단 올리기
        return
    print(단*곱)
    구구단(단, 곱+1) # 곱 올리기
구구단()

# # p.296 파보나치 수열
# def fibonacci(n):
#     if n == 1:
#         return 1
#     if n == 2:
#         return 1
#     else:
#         return fibonacci(n-1) + fibonacci(n-2)

# p.297 재귀 함수 피보나치 수열
counter = 0
def fibonacci(n):
    print("fibonacci({})를 구합니다.".format(n))
    global counter
    counter += 1
    if n == 1:
        return 1
    if n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
print(fibonacci(5))
print("----")
print("fibonacci(5) 계산할 때 함수를 호출한 횟수는 {}번 입니다.".format(counter))
# f(5) = f(4) + f(3) = 3 + 2 = 5
# f(4) = f(3) + f(2) = f(2) + f(1) + 1 = 1 + 1 + 1 = 3
# f(3) = f(2) + f(1) = 1 + 1 = 2
# 카운트 발생지점n  5, 4, 3, 2, 1, 2, 3, 2, 1 => 9번

# p.301 딕셔너리 재귀함수
dictionary = {1:1, 2:1}
def fibonacci(n):
    if n in dictionary:
        return dictionary[n]
    else:
        output = fibonacci(n-1) + fibonacci(n-2)
        dictionary[n] = output
        return output
print( fibonacci(5) )
print(dictionary)
# f(5) -> output = f(4) + f(3) , d[5] = f(4) + f(3)  추가 5
# f(4) -> output = f(3) + f(2) , d[4] = f(3) + f(2)  추가 3
# f(3) -> output = f(2) + f(1) , d[3] = f(2) + f(1)  추가 2
# f(2) -> return 1
# f(1) -> return 1


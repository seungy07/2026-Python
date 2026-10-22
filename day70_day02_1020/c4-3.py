# p.231 ~
# 범위 함수 : range()
# 1. range(수) , 0 ~ 수 -1 까지 범위(정수)
print( range(5)) # range(0, 5)
print(list(range(5))) # [0 1 2 3 4]
# 2. range( 시작값, 끝값  ) 
print( list(range(3,6)))
# 3. range(시작값, 끝값, 단계)
print(list(range(0,10,2)))

# p. 233
n = 10
a = range(0, n//2) # n / 2 = float타입 으로 *오류
# // 몫 연산자 혹은 int() 로 정수 변환 사용
print(a)

for i in range(10, 0,-1):
    print(i)

for i in range(1,10):
    if i % 2 == 1 :
        print(i)

for i in range(1,10,2):
    print(i)

for i in range(2,10):
    for k in range(1,10):
        print(f"{i} * {k} = {i*k}")


# p.240
# while 반복문
# while 조건식:     조건이 True이면 실행코드 실행, False 반복 종료
#       실행코드 

i = 1
while i < 11:
    print(i)
    i += 1

list = [1,2,1,2]
value = 2
while value in list:
    list.remove(value)
print(list)

a = {}
i = 0
while i < 5 :
    a[i] = 1
    i += 1
print(a)

# p.44 break, continue 키워드 : 반복문에서 사용하는 키워드
for i in range(1,11,1):
    if i == 3:
        break
    print(i)

for i in range(1,11):
    if i == 3:
        continue
    print(i)

x = 10
y = 2

if x > 4:
    if y > 2:
        print(x*y)
else:
    print(x+y)
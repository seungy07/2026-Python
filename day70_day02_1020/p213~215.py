# 교과서 문제 풀기 p.213 ~
numbers = [273, 103, 5, 32, 65, 9, 72, 800, 99]
for number in numbers:
    if number % 2 == 0:
        print(f"{number}는 짝수 입니다.")
    else :
        print(f"{number}는 홀수 입니다.")

for number in numbers:
    if len(str(number)) == 3:
        print(f"{number}는 3 자릿수 입니다.")
    elif len(str(number)) == 2:
        print(f"{number}는 2 자릿수 입니다.")
    else :
        print(f"{number}는 1 자릿수 입니다.")

numbers = [1,2,3,4,5,6,7,8,9]
output = [[],[],[]]
# [ [1,4,7] , [2,5,8] , [3,6,9] ]
for number in numbers:
    output[ (number - 1) % 3 ].append(number)
print(output)

numbers = [1,2,3,4,5,6,7,8,9]
for i in range(0,len(numbers)//2): # 0 , 4   0 1 2 3
    j = i * 2 + 1
    print(f"i = {i}, j = {j}")
    numbers[j] = numbers[j]**2
print(numbers)
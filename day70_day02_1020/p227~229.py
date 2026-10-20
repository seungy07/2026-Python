pets = [
    {'name':'구름', "age":5},
    {'name':'초코', "age":3},
    {'name':'아지', "age":1},
    {'name':'호랑이', "age":1}
]

for i in pets:
    print( i.get('name') , f"{i.get('age')}살" )

for i in pets:
    print( i['name'], f"{i['age']}살")

numbers = [1,2,6,8,4,3,2,1,9,5,4,9,7,2,1,3,5,4,8,9,7,2,3]
counter = {}

for number in numbers:
    if number in counter:
        counter[number] += 1
    else :
        counter[number] = 1
print(counter)

character = {
    "name" : "기사", 'level' : 12,
    'items' : { 'sword': '불꽃의 검', 'armor' : '풀플레이트'},
    'skill' : ["베기", "세게 베게", "아주 세게 베기"]
}
for key in character:
    if type(character[key]) is list:
        for i in character[key]:
            print(key, ":", i)
    elif type(character[key]) is dict:
        for i in character[key]:
            print(i,":",character[key][i])
    else :
        print(key,":", character[key])
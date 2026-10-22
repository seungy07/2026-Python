numbers = [1,2,3,4,5,6]
print( "::".join( str(number) for number in numbers ))

numbers = list(range(1,10+1))
print( list( filter( lambda x : x % 2 == 1 ,numbers) ) )

print( list( filter( lambda x : (x >= 3 and x < 7 ),numbers) ) )

print("hellow py" *3)
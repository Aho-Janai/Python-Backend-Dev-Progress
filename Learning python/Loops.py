#Direct
# total = []
# for i in range(100):
#     if (i%5 ==0 and i%3 ==0):
#         total.append(i)
#     else: print("macaco")
# print(total)

#Use the loop var as index to modify the list (Add 1 to an existing list)
# days = [1,2,3,4,5,6]
# num_days = len(days)
# for i in range(0,num_days):
#     days[i] +=1 # same as days[i] = days[i] +1
# print(days)

# same as before, but with conditions
# days = [1,2,3,4,5,6]
# cool_days = [23,2,8]
# num_days = len(days)
# for i in range(0,num_days):
#     if i in cool_days:
#         days[i] +=5
#     else: days[i] +=1
# print(days)

# multiply the content of a list itself with a loop (factorial calculator)
# the start of the range cannot be 0 because we are suing that
# very range to calculate the factorial, that's way I start with 0 and add 1 to
# the factorial variable
# when multipliyin the content of a list, start at 1, whem adding, start at 0
# factorial_of_five = 5
# store_factorial = 1
# for i in range (1, factorial_of_five+1):
#     store_factorial = i * store_factorial
# print(store_factorial)

#Factorial with i = 1, 10 and exponent 3
# this take i in a range, rise it to cube, then save it in another variable
# sigma = 10
# initial = 1
# store_value = 0
# i_cube = 3

# for i in range (1,11):
#     i_cube = i**3
#     store_value += i_cube
# print(store_value)

#Nested Loop (Major and minor chords combination)

# chords = ["A ","B ","C ","D ","E ","F ","G "]
# types_chord = ["Minor","Major"]
# store_majorminor_chords = []
# for chord in chords:
#     for type_chord in types_chord:
#         store_majorminor_chords.append(chord + type_chord)
# print(store_majorminor_chords)

#A better way to write this would be this, (no storage variable needed)
# chords = ["A ","B ","C ","D ","E ","F ","G "]
# types = ["Minor","Major"]
# all_chords = [f"{chord} {type}" for chord in chords for type in types]
# print(all_chords)

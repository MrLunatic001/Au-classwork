import random

try:
    user_input = int(input("Enter a choice: Rock (0) Paper (1) Scissors (2): "))
except:
    user_input = int(input("Enter an interger please, Rock (0) Paper (1) Scissors (2): "))

rand = random.randint(0,2)
if rand == 0:
    if user_input == 1:
        print("Scissors, you loose")
    elif user_input == 0:
        print("Paper, you loose")
    else:
        print("Rock, you loose")
elif rand == 1:

    if user_input == 1:
        print("Rock, you win")
    elif user_input == 0:
        print("Scissors, you win")
    else:
        print("Paper, you win")
else:
    if user_input == 1:
        print("Paper, draw")
    elif user_input == 0:
        print("Paper, draw")
    else:
        print("Scissors, draw")
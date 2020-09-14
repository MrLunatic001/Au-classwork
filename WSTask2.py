while True:
    try:
        room_width = int(input("Enter the width of the room: "))
        break
    except:
        print("Enter an integer")
while True:
    try:
        room_length = int(input("Enter the length of the room: "))
        break
    except:
        print("Enter an integer")
while True:
    try:
        unpaint_width = int(input("Enter the width of unpaintable areas: "))
        break
    except:
        print("Enter an integer")
while True:
    try:
        unpaint_length = int(input("Enter the length of unpaintable areas: "))
        break
    except:
        print("Enter an integer")
while True:
    try:
        num_coats = int(input("Enter the number of coasts of paint requires: "))
        break
    except:
        print("Enter an integer")
total_paint = ((room_length * room_width - unpaint_length * unpaint_width) * num_coats) / 11
print("The total amount of paint required to paint the room is: " + str(round(total_paint, 2)) + " liters.")

### ACS - As disucssed in class. Don't use break in your code. The loop needs a termination condition you can rely on!
### ACS - Code alos needs annotating. But it all works well.

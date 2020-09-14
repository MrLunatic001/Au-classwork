import math
while True:
    try:
        students = int(input("Input the number of students: "))
        break
    except:
        print("Enter an integer")
while True:
    try:
        books = int(input("Input the number of books: "))
        break
    except:
        print("Enter an integer")
print("The number of books that each student will receive: " + str(round(books/students)))
if round(books/ students) == 0:
    print("The number of books left over: " + str(students))
else:
    print("The number of books left over: " + str(books % students))

name = input("Enter a name: ")
print("The length of the name is: " + str(len(name)))

## ACS - Good. We will look at programming conventions in the lesson

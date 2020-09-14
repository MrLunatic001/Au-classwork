while True:
    try:
        car_mileage_past = float(input("Input the car mileage the last time the car was filed: "))
        break
    except:
        print("Enter a number")
while True:
    try:
        car_mileage_present = float(input("Input the car mileage now"))
        break
    except:
        print("Enter a number")
while True:
    try:
        number_of_liters = float(input("Input the total number of liters taken to fill the tank: "))
        break
    except:
        print("Enter a number: ")
gallon = number_of_liters * 4.546
miles_per_gallon = float(car_mileage_past - car_mileage_present) / gallon
print("The number of miles per gallon for your car is : " + str(round(miles_per_gallon, 2)))


### Is this working. I tried 12700 and 12940 and 70 and got -.075?? Can't see how it is negative. 

import time
import VL53L0X
import RPi.GPIO as GPIO

# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 20
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown = 16

GPIO.setwarnings(False)

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1_shutdown, GPIO.OUT)
GPIO.setup(sensor2_shutdown, GPIO.OUT)

ledPinGreen = 18
GPIO.setup(ledPinGreen, GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L0X
GPIO.output(sensor1_shutdown, GPIO.LOW)
GPIO.output(sensor2_shutdown, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.50)

# Create one object per VL53L0X passing the address to give to
# each.
tof = VL53L0X.VL53L0X(address=0x2B)
tof1 = VL53L0X.VL53L0X(address=0x2D)

# Set shutdown pin high for the first VL53L0X then 
# call to start ranging 
GPIO.output(sensor1_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

# Set shutdown pin high for the second VL53L0X then 
# call to start ranging 
GPIO.output(sensor2_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

timing = tof.get_timing()
if (timing < 20000):
    timing = 20000
print ("Timing %d ms" % (timing/1000))

count_BEST = 0
count_BETTER = 0
count_GOOD = 0

for count in range(1,1000000):
    distance = tof.get_distance()
    if 90 < distance < 100:
        count_BEST+=1
        print ("sensor ", tof.my_object_number, distance, 'cm', "BEST")
        GPIO.output(ledPinGreen, GPIO.HIGH)
        time.sleep(1)
    elif 100 <= distance < 110:
        count_BETTER+=1
        print ("sensor ", tof.my_object_number, distance, 'cm', "BETTER")
        GPIO.output(ledPinGreen, GPIO.HIGH)
        time.sleep(1)
    elif 110 <= distance < 120:
        count_GOOD+=1
        print ("sensor ", tof.my_object_number, distance, 'cm', "GOOD")
        GPIO.output(ledPinGreen, GPIO.HIGH)
        time.sleep(1)
    else:
        print ("sensor ", tof.my_object_number, distance, 'cm', "NOT GOOD")


    distance1 = tof1.get_distance()
    if (distance1 > 0):
         print ("sensor ", tof.my_object_number, distance1, 'cm')
    else:
        print ("%d - Error" % tof1.my_object_number)


    # distance = tof.get_distance()
    # if (distance > 0):
    #     print ("sensor %d - %d mm, %d cm, iteration %d" % (tof.my_object_number, distance, (distance/10), count))
    # else:
    #     print ("%d - Error" % tof.my_object_number)

    # distance1 = tof1.get_distance()
    # if (distance1 > 0):
    #     print ("sensor %d - %d mm, %d cm, iteration %d" % (tof1.my_object_number, distance1, (distance1/10), count))
    # else:
    #     print ("%d - Error" % tof1.my_object_number)

    time.sleep(timing/1000000.00)

tof1.stop_ranging()
GPIO.output(sensor2_shutdown, GPIO.LOW)
tof.stop_ranging()
GPIO.output(sensor1_shutdown, GPIO.LOW)


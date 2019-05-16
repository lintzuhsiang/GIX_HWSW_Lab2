import sys
import logging
import time
import os
import json
from azure-mgmt-eventhub import EventHubClient, Sender, EventData
import time
import VL53L0X
import RPi.GPIO as GPIO

logger = logging.getLogger("azure")

ADDRESS = "amqps://spimo2.servicebus.windows.net/spimo"

# SAS policy and key are not required if they are encoded in the URL
USER = "spimo"
KEY = "GvQXr2EQpDc0t4jBKH3Y+xvqN2HFoz7d1HrHBvbHpc8="
# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 20
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown = 16

GPIO.setwarnings(False)

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1_shutdown, GPIO.OUT)
GPIO.setup(sensor2_shutdown, GPIO.OUT)

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


ledPinGreen = 24
ledPinRed = 23
GPIO.setup(ledPinGreen, GPIO.OUT)
GPIO.setup(ledPinRed, GPIO.OUT)


try:
    if not ADDRESS:
        raise ValueError("No EventHubs URL supplied.")

    ##Create Event Hubs client
    client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
    sender = client.add_sender(partition="0")
    client.run()
    try:
        start_time = time.time()
        #while 1==1:
        for i in range(10000):
            distance = tof.get_distance()
            if 50 < distance < 55:
                count_BEST+=1
                print ("sensor ", tof.my_object_number, distance, 'cm', "BEST")
                GPIO.output(ledPinRed, GPIO.LOW)
                GPIO.output(ledPinGreen, GPIO.HIGH)
            elif 55 <= distance < 60:
                count_BETTER+=1
                print ("sensor ", tof.my_object_number, distance, 'cm', "BETTER")
                GPIO.output(ledPinRed, GPIO.LOW)
                GPIO.output(ledPinGreen, GPIO.HIGH)
            elif 60 <= distance < 65:
                count_GOOD+=1
                print ("sensor ", tof.my_object_number, distance, 'cm', "GOOD")
                GPIO.output(ledPinRed, GPIO.LOW)
                GPIO.output(ledPinGreen, GPIO.HIGH)
            else:
                print ("sensor ", tof.my_object_number, distance, 'cm', "NOT GOOD")
                GPIO.output(ledPinGreen, GPIO.LOW)
                GPIO.output(ledPinRed, GPIO.HIGH)


            distance1 = tof1.get_distance()
            if (distance > 0):
                print ("sensor %d - %d mm, %d cm, iteration %d" % (tof1.my_object_number, distance1, (distance1/10), count))
            else:
                print ("%d - Error" % tof.my_object_number)

            time.sleep(timing/1000000.00)
            device_id = '001'
            patient_id = '001'
            value = distance
            best_count = count_BEST
            eventjson= json.dumps({'device_id': device_id, 'patient_id': patient_id, 'value' : value, 'best_count':best_count})
            sender.send(EventData(str(eventjson)))
        tof1.stop_ranging()
        GPIO.output(sensor2_shutdown, GPIO.LOW)
        tof.stop_ranging()
        GPIO.output(sensor1_shutdown, GPIO.LOW)

    except:
        raise
    finally:
        end_time = time.time()
        client.stop()
        run_time = end_time - start_time
        logger.info("Runtime: {} seconds".format(run_time))

except KeyboardInterrupt:
    pass

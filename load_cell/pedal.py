#! /usr/bin/python

import time
import sys

#EMULATE_HX711=False

#if not EMULATE_HX711:
import RPi.GPIO as GPIO
from hx711 import HX711
#else:
#    from emulated_hx711 import HX711

def cleanAndExit():
    print ("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print ("Bye!")
    sys.exit()

hx = HX711(9,11)  #DT,CLK

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.

#MSB or LSB calibration
def most_common(list_):
	return max(set(list_),key=list_.count)

isMSB = True
if isMSB:
	hx.set_reading_format("MSB", "MSB")
	buf_MSB = []
	for i in range(5):
		raw_data = hx.readRawBytes()
		buf_MSB.append(raw_data[0])
		print raw_data[0]

	if most_common(buf_MSB) == 255 or len(set(buf_MSB))==2:
		print("MSB format")
	else:
		print("Setting to LSB format")
		buf_LSB = []
		hx.set_reading_format("LSB","MSB")   
		for i in range(5):
    			raw_data = hx.readRawBytes()
    			buf_LSB.append(raw_data[0])
			print raw_data[0]
		if most_common(buf_LSB) == 255 or len(set(buf_LSB))==1:
			print("LSB format")
		else: print("Reset again")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.


#calibrate reference weight
refer = 160
hx.set_reference_unit(refer)
#hx.set_reference_unit(10)
hx.reset()
hx.tare()
val = hx.get_weight(3)
while val < -5 or val > 10:
	print("recalibrate...")
	if val < -5:
		refer +=5 
		hx.set_reference_unit(refer)
		hx.reset()
		hx.tare()
	elif val > 10:
		refer -=5
		hx.set_reference_unit(refer)
                hx.reset()
                hx.tare()
	else: print("finish calibration")


print ("Tare done! Add weight now...")

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()


#connect to Azure database by pyodbc
#import pyodbc
#server = 'lung.database.windows.net'
#database = 'lung'
#username = 'pi'
#password = 'R@berry'
#driver= '{ODBC Driver 17 for SQL Server}'
#cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
#cursor = cnxn.cursor()
#cursor.execute("SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName FROM [SalesLT].[ProductCategory] pc JOIN [SalesLT].[Produc$
#row = cursor.fetchone()
#while row:
#    print (str(row[0]) + " " + str(row[1]))
#    row = cursor.fetchone()

while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
        
        #np_arr8_string = hx.get_np_arr8_string()
        #binary_string = hx.get_binary_string()
        #print binary_string + " " + np_arr8_string
	#raw_data = hx.readRawBytes()
	#print raw_data
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = hx.get_weight(3)
        print (val)

        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        hx.power_down()
        hx.power_up()
        time.sleep(0.01)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

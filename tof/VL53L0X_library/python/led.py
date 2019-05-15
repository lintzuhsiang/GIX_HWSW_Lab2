import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ledPin = 23
ledPin2 = 24

GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(ledPin2, GPIO.OUT)

for i in range(5):
	print("LED1 turning on.")
	GPIO.output(ledPin, GPIO.HIGH)
	time.sleep(0.5)
	print("LED1 turning off.")
	GPIO.output(ledPin, GPIO.LOW) 
	time.sleep(0.5)


	print("LED2 turning on.")
	GPIO.output(ledPin2, GPIO.HIGH)
	time.sleep(0.5)
	print("LED2 turning off.")
	GPIO.output(ledPin2, GPIO.LOW) 
	time.sleep(0.5)


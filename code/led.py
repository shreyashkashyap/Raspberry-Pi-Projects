import RPi.GPIO as GPIO
import time

Led_pin1 = 17
Led_pin2 = 27


GPIO.setmode(GPIO.BCM)
GPIO.setup(Led_pin1, GPIO.OUT)  #LED to GPIO17
GPIO.setup(Led_pin2, GPIO.OUT)

GPIO.output(Led_pin2, GPIO.HIGH)
time.sleep(1)
GPIO.output(Led_pin2,GPIO.LOW)
time.sleep(1)
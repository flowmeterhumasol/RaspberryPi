import serial
import RPi.GPIO as GPIO
import time
#import datetime
from datetime import datetime
from datetime import timedelta

ser=serial.Serial("/dev/ttyUSB0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600
def blink(pin):
	GPIO.output(pin,GPIO.HIGH)  
	time.sleep(1)  
	GPIO.output(pin,GPIO.LOW)  
	time.sleep(1)  
	return

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
now= datetime.now()
now_plus_30= now + timedelta(minutes = 30)
#aantal liter voor 4 kranen aangezien nummer 1 de server is
#en dus de krannummers beginnen tellen vanaf 2 komt 2 overeen met index 0 
dataSynced = [0,0,0,0] 
dataStored = [0,0,0,0]

while True:
	read_ser=ser.readline()
	read_ser_array = read_ser.decode().split(":")
	tapNumber = read_ser_array[0]
	totalMilliLiters=read_ser_array[1]
	dataSynced[int(tapNumber)-2] = dataSynced[int(tapNumber)-2] + int(totalMilliLiters)
	print("dataSynced: ", dataSynced)
	
	#Elke 30min checken of ge nog in dezelfde dag zit 
	if(now >= now_plus_30):
            if(now_plus_30.day != now.day):
                    dataStored = dataSynced
                    dataSynced = [0,0,0,0]
            now= datetime.now()
            now_plus_30= now + timedelta(minutes = 30)
        
    
import serial
import RPi.GPIO as GPIO
import time 
from datetime import date 
from datetime import datetime
from datetime import timedelta 
#import mysql.connector 

if __name__=='__main__':
    ser= serial.Serial('/dev/ttyUSB0',9600,timeout=1)
    ser.baudrate=9600
    ser.flush()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)

#mydb = mysql.connector.connect(host="localhost",user="pi", password="PASSWORD", database= "localDB")
#mycursor = mydb.cursor()
#sql="INSERT INTO localDB (date,tap_id,liter) VALUES(%x,%d,%d)"	

time= date.today()
dataSynced = [0.0,0.0,0.0,0.0]
prevIndex = 5 #int begin random getal niet 0

while True:
    if(ser.in_waiting >0):
        read_ser = ser.readline()
        print(read_ser)
        read_ser_index=read_ser.decode().split(".")
        if (prevIndex != read_ser_index[0]):
            ser.write(b"ACK\n")
            print("ACK gestuurd")
            prevIndex = read_ser_index[0]                 
            #Waarden verwerken 
            read_ser_array=read_ser_index[1].split(":")
            tapNumber= read_ser_array[0]
            totalMilliLiters = read_ser_array[1]
            dataSynced[int(tapNumber)-2]=float(dataSynced[int(tapNumber)-2]) +float(totalMilliLiters)
            print("dataSynced: ", dataSynced, "on date: ", time)  

    if(date.today() != time):
        dataStored = dataSynced
        dataSynced = [0,0,0,0]
        print("dataReset: ",dataSynced)
#for x in dataSynced:
#val = (now,x+2, dataSynced[x])
#mycursor.execute(sql, val)
#mydb.commit() 
        time= date.today()
			

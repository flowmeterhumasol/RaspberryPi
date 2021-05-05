import serial
import RPi.GPIO as GPIO
from datetime import date

#Setup serial connection trough USB port 
if __name__=='__main__':
    ser= serial.Serial('/dev/ttyUSB0',9600,timeout=1)
    ser.baudrate=9600
    ser.flush()   
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
 
#prevIndex must be a random number (not zero) since the first incoming index will be 0
prevIndex = 5

#Saving date of this day
#date= date.today()


while True:
    if(ser.in_waiting >0):
        read_ser = ser.readline()
        print(read_ser)
        read_ser_index=read_ser.decode().split(".")
        
        #Checking the index to make sure each message is only processed once
        if (prevIndex != read_ser_index[0]):
            ser.write(b"ACK\n")
            print("ACK gestuurd")
            prevIndex = read_ser_index[0]                 
            #Writing data to file while adding the date of this day
            read_ser_array=read_ser_index[1].split(":")
            with open("localDB_file.txt","a") as file_object:
                file_object.write(str(int(read_ser_array[0])-1)+":"+str(int(read_ser_array[1]))+","+str(date.today())+ "\n")
        

   



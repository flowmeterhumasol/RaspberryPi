import serial
import time 
from datetime import date 
from datetime import datetime
from datetime import timedelta 
import mysql.connector
import logging
import urllib.request

#Checking network connection 
def connect():
    host= 'http://google.com'
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

if (connect()):
    index=0 
    data = [0,0,0,0] 
    day_today= False
    
    #Defining log file 
    logging.basicConfig(filename='uploader.log',filemode='a',format='%(asctime)s-%(message)s',level=logging.INFO)
    logging.info('Start uploading')

    #Connecting to database 
    #mydb = mysql.connector.connect(host="192.168.1.20",user="Sofie",password="Kunting!",database="DBWP")
    #mycursor = mydb.cursor()
    #sql="INSERT INTO hs_tapconsumption_history (tap_id,tap_liter,tap_date) VALUES(%s,%s,%s)"
    mydb = mysql.connector.connect(host="localhost",user="sofie",password="Kunting!",database="localDB")
    mycursor = mydb.cursor()
    sql="INSERT INTO Kunting (tap_id,tap_liter,tap_date) VALUES(%s,%s,%s)"

    #Reading and clearing local database file 
    f=open("localDB_file.txt",'r+')
    alist=f.readlines()
    f.truncate(0)
    f.close()
        
    if (len(alist)>0): 
        #Define oldest date in local database 
        date_index0= alist[0].strip().split(",")
        date_uploaded= date_index0[1]

        #Processing data for each line of the local db
        #For each day the total consumption will be summed and uploaded in the online database
        #The data of the current day will be placed back in the file because the data is not yet complete
        while (index < len(alist) and not day_today ):
            split1= alist[index].strip().split(":")
            split2= split1[1].split(",")
            datum=split2[1]
            
            #When all the data of one day is collected, it will be uploaded in the online database 
            if (datum != date_uploaded) :
                for i in range(len(data)):
                    val = (int(i+1),int(data[i]/1000),date_uploaded)
                    mycursor.execute(sql,val)
                    mydb.commit()
                logging.info('Succesfully uploaded data of day:'+ date_uploaded)
                data =[0,0,0,0] 
                date_uploaded= datum
            
            #When all the data of the previous days is porcessed, the data of the current day
            # is placed back in the local database. 
            if (datum == str(date.today())):
                day_today=True
                f= open("localDB_file.txt",'a')
                while index < len(alist):
                    f.write(alist[index])
                    index +=1
                f.close()
                logging.info('Writing data of the current day back to the file')
            else :
                index +=1
                #Summing total consumption for each tap
                data[int(split1[0])-1]=data[int(split1[0])-1] +int(split2[0])
    else:
        logging.info("No data in localDB file")
    logging.info('Uploading completed')
              

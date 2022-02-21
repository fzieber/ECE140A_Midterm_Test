# Import WSGI ref for importing the serving library
from wsgiref.simple_server import make_server

# Configurator defines all the settings and configs in your web app
from pyramid.config import Configurator

# Response is used to respond to requests to the server
from pyramid.response import FileResponse



# Import NumPy
import numpy as np

import mysql.connector as mysql
from dotenv import load_dotenv
import os




#/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT

DHTPin = 11 #define the pin of DHT11

trigPin = 16
echoPin = 18
MAX_DISTANCE = 220          # define maximum measuring distance, unit: cm
timeOut = MAX_DISTANCE*60   # calculate timeout w.r.t to maximum distance
buzzerPin= 31

id = 1

load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

def pulseIn(pin,level,timeOut): # obtain pulse time of a pin under timeOut
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime
   
def getSonar():            # get measurement of ultrasonic module, unit: cm
    GPIO.output(trigPin, GPIO.HIGH)   # make trigPin output 10us HIGH level
    time.sleep(0.00001)               # 10us
    GPIO.output(trigPin,GPIO.LOW)     # make trigPin output LOW level
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut) # read echoPin pulse time
    distance = pingTime*340.0/2.0/10000.0 # distance w/sound speed @ 340m/s
    return distance
   
def setup():
    GPIO.setmode(GPIO.BOARD)     
    GPIO.setup(trigPin, GPIO.OUT)   # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN)    # set echoPin to INPUT mode
  



def loop():
    global id
    dht = DHT.DHT(DHTPin) #create a DHT class object
    counts = 0 # Measurement counts
    while(True):
        distance = getSonar() # get distance
        print("The distance is : %.2f cm" % (distance))


        counts += 1
        print("Measurement counts: ", counts)
        for i in range(0,15): 
            chk = dht.readDHT11()
            if (chk is dht.DHTLIB_OK):
                print("DHT11,OK!")
                break
            time.sleep(0.1)
        humidity = dht.humidity
        temperature = dht.temperature
        cursor.execute("""INSERT INTO Data_Table VALUES (id, temperature, humidity, distance);""")
        print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))
        time.sleep(2)
       
if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    # connect to the database
    db = mysql.connect(host=db_host, user=db_user,
                       passwd=db_pass, database=db_name)
    cursor = db.cursor()
    try:
        loop()
    except KeyboardInterrupt:  # Press CTRL-C to end the program
        db.close
        GPIO.cleanup()         # release GPIO resources
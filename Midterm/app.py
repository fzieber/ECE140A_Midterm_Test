# Import WSGI ref for importing the serving library
from unittest import result
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

trigPin = 16
echoPin = 18
MAX_DISTANCE = 220          # define maximum measuring distance, unit: cm
timeOut = MAX_DISTANCE*60   # calculate timeout w.r.t to maximum distance
buzzerPin= 31

# GPIO setup
def setup():
    GPIO.setmode(GPIO.BOARD)     

    GPIO.setup(buzzerPin, GPIO.OUT)   

# Set Buzzer when applicable
def Buzzer(alarm):
    if alarm == 'true':
        GPIO.output(buzzerPin,GPIO.HIGH)
    else:
        GPIO.output(buzzerPin,GPIO.LOW)



load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']



def get_data(req):
    # Save boundries from inputs
    minTime = int(req.matchdict['minTime'])
    maxTime = int(req.matchdict['maxTime'])
    if (minTime > maxTime):
       temp = minTime
       minTime = maxTime
       maxTime = temp
    minDist = float(req.matchdict['minDist'])
    maxDist = float(req.matchdict['maxDist'])
    if (minDist > maxDist):
       temp = minDist
       minDist = maxDist
       maxDist = temp
    alarm = str(req.matchdict['alarm'])
    Buzzer(alarm)
    
    if(minTime == maxTime):
       minTime = 0
       maxTime = 100 
    else:
       minTime = minTime - 1
       maxTime = maxTime + 1
    if(minDist == maxDist):
       minDist = 0.0
       maxDist = 220.00 
    else:
       minDist = minDist - 0.01
       maxDist = maxDist + 0.01 

    # connect to the database
    db = mysql.connect(host=db_host, user=db_user,
                       passwd=db_pass, database=db_name)
    cursor = db.cursor()

    
  
    print(minTime)
    print(maxTime)
    print(minDist)
    print (maxDist)

    # query the database with the range constraints
    cursor.execute(
        "SELECT * FROM Data_Table WHERE temperature > -100.0 AND id > '%s' AND id < '%s' AND distance > '%s' AND distance < '%s';" 
                                                               % (minTime, maxTime, minDist, maxDist))
    record = cursor.fetchall()
    db.close()

    response = []

    # if no record found, return error json
    if record is None:
        print("empty table")
        return {
            'error': "No data was found for the given ID",
            'id': "",
            'temperature': "",
            'humidity': "",
            'distance': "",
        }
    else :
       print("saving table")
       print(record)
       for row in record:
          print(row)
          response.append({
             'id': row[0],
             'temperature': row[1],
             'humidity': row[2],
             'distance': row[3]
          })
    return response




# read html file for display
def index_page(req):
   return FileResponse("index.html")

# Main entrypoint
if __name__ == '__main__':

   setup()
   with Configurator() as config:
 
       # Create a route called home
       config.add_route('home', '/')
       # Bind the view (defined by index_page) to the route named ???home???
       config.add_view(index_page, route_name='home')
      
       # Create a route that handles server HTTP requests at: /data/minTime/maxTime/minDist/maxDist/alarm
       config.add_route('data', '/data/{minTime}/{maxTime}/{minDist}/{maxDist}/{alarm}')
      
       
       # Binds the function get_photo to the photos route and returns JSON
       # Note: This is a REST route because we are returning a RESOURCE!
       config.add_view(get_data, route_name='data', renderer='json')
      
       
       
 
       # Add a static view
       # This command maps the folder ???./public??? to the URL ???/???
       config.add_static_view(name='/', path='./public', cache_max_age=3600)
      
       # Create an app with the configuration specified above
       app = config.make_wsgi_app()
   server = make_server('0.0.0.0', 6543, app) # Start the application on port 6543
   server.serve_forever()
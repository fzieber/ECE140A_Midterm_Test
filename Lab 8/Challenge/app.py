# Import WSGI ref for importing the serving library
from wsgiref.simple_server import make_server

# Configurator defines all the settings and configs in your web app
from pyramid.config import Configurator

# Response is used to respond to requests to the server
from pyramid.response import FileResponse

import pytesseract

# Import OpenCV
import cv2

# Import NumPy
import numpy as np

import mysql.connector as mysql


from dotenv import load_dotenv  # only required if using dotenv for creds

import os

import GPS
import Camera



# Store MySql credentials
load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']



# Connect to MySql
db = mysql.connect(user=db_user, password=db_pass,
                   host=db_host)
cursor = db.cursor()


# update found_objects table
def save_data(req):
   
    # clear found_objects table
    cursor.execute("DELETE FROM found_objects;")
    db.commit()
    # Save up-to-date data to found_objects table
    cursor.execute("INSERT INTO found_objects Select * FROM found;")
    db.commit()
    # Print for debugging purposes new content of found_objects table
    cursor.execute("SELECT * FROM found_objects;")
    result = (cursor.fetchall())
    print (result)
    return{}
    
# function to access data
def begin_tracking(req):
   # save object id to newColor
   newColor = req.matchdict['object_id']



   # Find HSV H upper and lower values and name of selected object

   cursor.execute("USE Track_db")
   cursor.execute("SELECT * FROM objects;")
   records = cursor.fetchall()
   print(records)
   cursor.execute("SELECT * FROM objects WHERE color = (%s);", (newColor,) )
   record = cursor.fetchall()
   for row in record:
      lower1 = int(row[1])
      upper1 = int(row[2])
      lower2 = int(row[3])
      upper2 = int(row[4])
      objectName = str(row[5])
   # Save Hsv values as lists and call Camera.followObject function
   low1 = [lower1,50,50]
   up1 = [upper1,255,255]
   low2 = [lower2,50,50]
   up2 = [upper2,255,255]
   print (low1, up1, low2, up2)
   found = Camera.followObject(low1, up1, low2, up2)

   # Pass retrieved boolean into GPS.getCoord 
   Lat, Long, City = GPS.getCoord(found)
   
   if (Lat == 0.0):
       return{}

   # Create new entry for table in HTML depending on number of previous entries of the same object type     
   count = 1
   cursor.execute("SELECT * FROM found WHERE object_name = (%s);", (objectName,) )
   result = (len(cursor.fetchall()))

   if (result > 0):
      count = count + 1
      objectName2 = objectName + str(count)
      cursor.execute("SELECT * FROM found WHERE object_name = (%s);", (objectName2,) )
      result = (len(cursor.fetchall()))
      while(result > 0): 
         count = count + 1
         objectName2 = objectName + str(count)
         cursor.execute("SELECT * FROM found WHERE object_name = (%s);", (objectName2,) )
         result = (len(cursor.fetchall()))
      cursor.execute("INSERT INTO found VALUES (%s, %s, %s, %s);", (objectName2, Lat, Long, City),)
      fName = objectName2
   else:
      cursor.execute("INSERT INTO found VALUES (%s, %s, %s, %s);", (objectName, Lat, Long, City),)
      fName = objectName



   #Send new table data to rest.js for processing, so HTML file can be updated
   cursor.execute("SELECT * FROM found;")
   res = cursor.fetchall()
   response = []
   for row2 in res:
          print(row2)
          response.append({
             'Name': row2[0],
             'Latitude': row2[1],
             'Longitude': row2[2],
             'Address': row2[3]
          })
       
   
   print (response)
   db.commit()
   return response















# read html file for display
def index_page(req):
   return FileResponse("index.html")








# Main entrypoint
if __name__ == '__main__':
   with Configurator() as config:
 
       # Create a route called home
       config.add_route('home', '/')
       # Bind the view (defined by index_page) to the route named ‘home’
       config.add_view(index_page, route_name='home')
      
       # Create a route that handles server HTTP requests at: /track/object_id
       config.add_route('track', '/track/{object_id}')

       # Binds the function begin_Tracking to the track route and returns JSON
       # Note: This is a REST route because we are returning a RESOURCE!
       config.add_view(begin_tracking, route_name='track', renderer='json')
       
       # Create a route that handles server HTTP requests at: /save/object_id
       config.add_route('save', '/save/{object_id}')

       # Binds the function save_data to the save route and returns JSON
       # Note: This is a REST route because we are returning a RESOURCE!
       config.add_view(save_data, route_name='save', renderer='json')




       
       # Add a static view
       
       config.add_static_view(name='/', path='./public', cache_max_age=3600)
      
       # Create an app with the configuration specified above
       app = config.make_wsgi_app()
   server = make_server('0.0.0.0', 6543, app) # Start the application on port 6543
   server.serve_forever()
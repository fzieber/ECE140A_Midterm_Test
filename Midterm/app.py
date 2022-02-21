# Import WSGI ref for importing the serving library
from wsgiref.simple_server import make_server

# Configurator defines all the settings and configs in your web app
from pyramid.config import Configurator

# Response is used to respond to requests to the server
from pyramid.response import FileResponse

# Import OpenCV
import cv2

# Import NumPy
import numpy as np

import mysql.connector as mysql
from dotenv import load_dotenv
import os

load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']



def get_photo(req):
    # Save boundries from age and height range inputs
    ageMin = int(req.matchdict['inAge'])
    if (ageMin == 9):
       ageMax = 70
    else:
       ageMax = ageMin + 11
    heightMin = int(req.matchdict['inHeight'])
    if (heightMin == 139):
       heightMax = 190
    else:
       heightMax = heightMin + 11

    # connect to the database
    db = mysql.connect(host=db_host, user=db_user,
                       passwd=db_pass, database=db_name)
    cursor = db.cursor()

    # query the database with the range constraints
    cursor.execute(
        "SELECT id,name,owner,height,age FROM Gallery_Details WHERE age > '%s' AND age < '%s' AND height > '%s' AND height < '%s';" 
                                                               % (ageMin, ageMax, heightMin, heightMax))
    record = cursor.fetchone()
    db.close()

    # if no record found, return error json
    if record is None:
        return {
            'error': "No data was found for the given ID",
            'id': "",
            'name': "",
            'owner': "",
            'height': "",
            'age':""
        }

    # populate json with relevant values
    response = {"id":record[0], "img_src": record[1], "img_own":record[2]}

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
      
       # Create a route that handles server HTTP requests at: /photos/height/age
       config.add_route('data', '/data/{minTime}/{maxTime}/{minDist}/{maxDist}/{alarm}')
      
       
       # Binds the function get_photo to the photos route and returns JSON
       # Note: This is a REST route because we are returning a RESOURCE!
       config.add_view(get_photo, route_name='data', renderer='json')
      
       
       
 
       # Add a static view
       # This command maps the folder “./public” to the URL “/”
       # So when a user requests img_src with age range 20-30, the server knows to look
       # for it in: “public/geisel_x.jpg” where x is the first image with a
       # corresponding age between 20 and 29
       config.add_static_view(name='/', path='./public', cache_max_age=3600)
      
       # Create an app with the configuration specified above
       app = config.make_wsgi_app()
   server = make_server('0.0.0.0', 6543, app) # Start the application on port 6543
   server.serve_forever()
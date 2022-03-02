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

# JSON which maps photos to ID
plate_photos = [
 {"id":1, "img_src": "Arizona_47.jpg"},
 {"id":2, "img_src": "Delaware_Plate.png"},
 {"id":3, "img_src": "Contrast.jpg"}
]

def detect_plate(img): # TODO
   return img, [[-1,-1],[-1,-1],[-1,-1],[-1,-1]]



def get_text(roi): # TODO
   return "XXXXXXX"

# function to access data
def get_photo(req):
   # post_id retrieves the value that is sent by the client
   # the -1 is needed because arrays are 0-indexed
   idx = int(req.matchdict['photo_id'])-1
   # we return the value at the given index from geisel_photos
   imgJson = plate_photos[idx]
   img = imgJson["img_src"] 
   roi, coord = detect_plate(img)
   text = get_text(roi)
   return {"img_src": roi, "text": text}



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
      
       # Create a route that handles server HTTP requests at: /photos/photo_id
       config.add_route('photos', '/photos/{photo_id}')

       # Binds the function get_photo to the photos route and returns JSON
       # Note: This is a REST route because we are returning a RESOURCE!
       config.add_view(get_photo, route_name='photos', renderer='json')
       
       # Add a static view
       # This command maps the folder “./public” to the URL “/”
       # So when a user requests geisel-1.jpg as img_src, the server knows to look
       # for it in: “public/geisel-1.jpg”
       config.add_static_view(name='/', path='./public', cache_max_age=3600)
      
       # Create an app with the configuration specified above
       app = config.make_wsgi_app()
   server = make_server('0.0.0.0', 6543, app) # Start the application on port 6543
   server.serve_forever()
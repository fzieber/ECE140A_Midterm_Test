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

"""
import os

if os.path.exists("./public/images/CropArizona_47.jpg"):
  os.remove("./public/images/CropArizona_47.jpg")
if os.path.exists("./public/images/CropDelaware_Plate.png"):
  os.remove("./public/images/CropDelaware_Plate.png")
if os.path.exists("./public/images/CropContrast.jpg"):
  os.remove("./public/images/CropContrast.jpg")

if os.path.exists("./public/images/PostArizona_47.jpg"):
  os.remove("./public/images/PostArizona_47.jpg")
if os.path.exists("./public/images/PostDelaware_Plate.png"):
  os.remove("./public/images/PostDelaware_Plate.png")
if os.path.exists("./public/images/PostContrast.jpg"):
  os.remove("./public/images/PostContrast.jpg")
"""

# JSON which maps photos to ID
plate_photos = [
 {"id":1, "img_src": "Arizona_47.jpg"},
 {"id":2, "img_src": "Delaware_Plate.png"},
 {"id":3, "img_src": "Contrast.jpg"}
]

def detect_plate(img): # TODO

   # Read the image
   image_url = "./public/images/" + img
   image = cv2.imread(image_url, 0)
   # 0 is a simple alias for cv2.IMREAD_GRAYSCALE
   # Preprocessing
   """
   # Add a Gaussian Blur to smoothen the noise
   blur = cv2.GaussianBlur(image.copy(), (9, 9), 0)
   
   # Threshold the image to get a binary image
   #_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
   thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

   # Invert the image to swap the foreground and background
   invert = 255 - thresh
   
   # Dilate the image to join disconnected fragments
   kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
   dilated = cv2.dilate(invert, kernel)
   """
   thresh = cv2.bilateralFilter(image.copy(), 13, 15, 15)
   dilated = cv2.Canny(thresh, 30, 200)
   #dilated = cv2.Sobel(image,cv2.CV_64F,1,1,ksize=15)

   # Save Post Processing image
   #cv2.imwrite("./public/images/Post" + img , dilated)

   # Get contours
   contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
   # Find the largest 15 contours
   contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

   # Find best polygon and get location
   location = None

   # Finds rectangular contour
   for contour in contours:
      #approx = cv2.approxPolyDP(contour, 15, True)
      approx =  cv2.minAreaRect(contour) 
      if len(approx) == 4:
         location = approx
         break

   # Handle cases when no quadrilaterals are found        
   if type(location) != type(None):
      print("Corners of the contour are: ",location)
      # cropping image before return
      imgCrop = image[min(location[0][0][1],location[3][0][1]):max(location[1][0][1],location[2][0][1]),min(location[0][0][0],location[1][0][0]):max(location[2][0][0],location[3][0][0])]
      cv2.imwrite("./public/images/Crop" + img , imgCrop)
      return img,location 
   else:
      print("No quadrilaterals found")
      return img, [[-1,-1],[-1,-1],[-1,-1],[-1,-1]]

   



def get_text(roi): 
   # Read the image
   image_url = "./public/images/Crop" + roi
   #imageCrop = cv2.imread(image_url, 0)
   
   #text = pytesseract.image_to_string(image_url, config='--psm 7 --oem 3 ')
   #text = pytesseract.image_to_string(image_url, lang='eng', config='--psm 7 --oem 3 ')
   """
   if (len(text)<7):
      return "XXXXXXX"
   elif (len(text)>7):
      return "XXXXXXX"
   else:
   """
   #return text
   return "XXXXXX"

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
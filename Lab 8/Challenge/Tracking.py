import numpy as np




class Track: 
    Follow = False
    Found = False
    Longitude = 117.2277
    Latitude = 32.8416
    City = "La Jolla"
    lower1 = np.array([0, 50, 50])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([160, 50, 50])
    upper2 = np.array([179, 255, 255])
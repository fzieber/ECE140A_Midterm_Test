import numpy as np
import cv2
import RPi.GPIO as GPIO
import time

# import the motor library
from RpiMotorLib import RpiMotorLib


def followObject(low1, up1, low2, up2):
    #video capture likely to be 0 or 1
    cap=cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    #Stepper Motor Setup
    GpioPins = [18, 23, 24, 25]

    # Declare a named instance of class pass a name and motor type
    mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
    #min time between motor steps (ie max speed)
    step_time = .001

    #PID Gain Values (these are just starter values)
    Kp = 0.003
    Kd = 0.0001
    Ki = 0.0001

    #error values
    d_error = 0
    last_error = 0
    sum_error = 0

    frames = 0
    Found = False
    while(1):
        _,frame=cap.read()
        frames += 1
        #convert to hsv deals better with lighting
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Collect color range inputs 
        lower1 = np.array(low1)
        upper1 = np.array(up1)
        lower2 = np.array(low2)
        upper2 = np.array(up2)
        
        #masks input image with upper and lower color ranges
        red_only1 = cv2.inRange(hsv, lower1, upper1)
        red_only2 = cv2.inRange(hsv, lower2 , upper2)
        
        red_only = red_only1 + red_only2
        
        mask=np.ones((5,5),np.uint8)
        
        
        #run an opening to get rid of any noise
        opening=cv2.morphologyEx(red_only,cv2.MORPH_OPEN,mask)
        cv2.imshow('Masked image', opening)
        

        #run connected components algo to return all objects it sees.        
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opening,4, cv2.CV_32S)
        b=np.matrix(labels)
        if num_labels > 1:
            print(num_labels)
            Found = True
            start = time.time()
            #extracts the label of the largest none background component and displays distance from center and image.
            max_label, max_size = max([(i, stats[i, cv2.CC_STAT_AREA]) for i in range(1, num_labels)], key = lambda x: x[1])
            Obj = b == max_label
            Obj = np.uint8(Obj)
            Obj[Obj > 0] = 255
            cv2.imshow('largest object', Obj)
            
            
            #calculate error from center column of masked image
            error = -1 * (320 - centroids[max_label][0])


    #speed gain calculated from PID gain values
            speed = Kp * error + Ki * sum_error + Kd * d_error
            
            #if negative speed change direction
            if speed < 0:
                direction = False
            else:
                direction = True
            
            #inverse speed set for multiplying step time (lower step time = faster speed)
            speed_inv = abs(1/(speed))
            
            #get delta time between loops
            delta_t = time.time() - start
            #calculate derivative error
            d_error = (error - last_error)/delta_t
            #integrated error
            sum_error += (error * delta_t)
            last_error = error

            
            #buffer of 20 only runs within 20
            if abs(error) > 20:
                mymotortest.motor_run(GpioPins , speed_inv * step_time, 5, direction, False, "full", .05)
            else:
                #run 0 steps if within an error of 20
                mymotortest.motor_run(GpioPins , step_time, 0, direction, False, "full", .05)
            
        else:
            print('no object in view')
            

        k=cv2.waitKey(5)
        if k==27:
            break

    cv2.destroyAllWindows()
    GPIO.cleanup()
    #return if object is found or not
    print(Found)
    return Found

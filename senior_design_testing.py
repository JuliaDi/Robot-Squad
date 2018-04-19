# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 18:05:21 2018

@author: Nike
"""
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import imutils
import cv2
#import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import math
#import imutils

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def get_angle(netPositionX, netPositionY):
    if netPositionX > 0 and netPositionY < 0:
        if abs(netPositionX) >= abs(netPositionY):
            angle1 = math.degrees(math.atan(abs(netPositionY)/abs(netPositionX)))
        elif abs(netPositionX) < abs(netPositionY):
            angle1 = 90 - math.degrees(math.atan(abs(netPositionX)/abs(netPositionY)))
    elif netPositionX < 0 and netPositionY < 0:
        if abs(netPositionX) >= abs(netPositionY):
            angle1 = 180 - math.degrees(math.atan(abs(netPositionY)/abs(netPositionX)))
        elif abs(netPositionX) < abs(netPositionY):
            angle1 = math.degrees(math.atan(abs(netPositionX)/abs(netPositionY))) + 90
    elif netPositionX < 0 and netPositionY > 0:
        if abs(netPositionX) >= netPositionY:
            angle1 = math.degrees(math.atan(netPositionY/abs(netPositionX))) + 180
        elif abs(netPositionX) < netPositionY:
            angle1 = 270 - math.degrees(math.atan(abs(netPositionX)/netPositionY))
    elif netPositionX > 0 and netPositionY > 0:
        if netPositionX >= netPositionY:
            angle1 = 360 - math.degrees(math.atan(netPositionY/netPositionX))
            if angle1 == 360:
                angle1 = 0
        elif netPositionX < netPositionY:
            angle1 = math.degrees(math.atan(netPositionX/netPositionY)) + 270
    elif netPositionX == 0:
        if netPositionY < 0:
            angle1 = 90
        elif netPositionY > 0:
            angle1 = 270
    elif netPositionY == 0:
        if netPositionX > 0:
            angle1 = 0
        elif netPositionX < 0:
            angle1 = 180
    
    return angle1


cap = cv2.VideoCapture(1)
cap.set(3,800)

cap.set(4,800)




#cap.set(5, 1080)
#cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
# =============================================================================
# 
# time.sleep(1)
# 
# cap.set(15, -8.0)
# =============================================================================

# =============================================================================
# currentWB = cap.get(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U)
# cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, currentWB)
# cap.set()
# cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off
# =============================================================================
    
count = 0

initial1 = False
initial2 = False
initial3 = False
initial4 = False

while True:
    
    ret, img = cap.read()
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,200,255,0)
    thresh = cv2.dilate(thresh, None, iterations=1)
    thresh = cv2.erode(thresh, None, iterations=1)
    img2, imgContours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    largest_areas = sorted(imgContours, key=cv2.contourArea)
    
    #top left point of image
    origin = (0,0)
    cv2.circle(img, origin, 25, (255,255,255), -1)
    #cv2.drawContours(img, largest_areas[-10:-1], 0, (255,0,0), 2)
    
    #bottom right point of image
    end = (800,600)
    cv2.circle(img, end, 25, (255,255,255), -1)
    
    #Trying to remove tiny contours
    #mask = np.ones(img.shape[:2], dtype="uint8") * 255
    
    #cv2.drawContours(img, imgContours, -1, (0,255,0), 3)

    
    #if count == 0 and (cv2.waitKey(1) & 0xFF == ord('r')):
    if count == 0:
        savedImage = img2
        savedImageColor = img
        #cv2.drawContours(savedImageColor, imgContours, 0, (0,255,0), 3) #0 argument draws it at outer contour
        
        # draws a circle at the centroid of each child contour
        for i in range(0,len(imgContours)):
            
            #Moment and centroid stuff
            cnt = imgContours[i] #parameter refers to which contour to use
            if cv2.contourArea(cnt) < 100:
               # cv2.drawContours(mask, [i], -1, 0, -1)
                continue
            
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            centroidPoint = (cx, cy)
            cv2.circle(savedImageColor, centroidPoint, 3, (0,0,255), -1)
            print("outside centroid point", centroidPoint)
    
        #cv2.drawContours(savedImage, contours, -1, (255,0,0), 2)
# =============================================================================
#         print("This is what contours prints", contours)
#         print(hierarchy)
#         print("descriptions", hierarchy[0])
#         print("first hierarchy", hierarchy[0][0]) #prints all the properties of the first countour
#         print(hierarchy[0][0][0])   #next contours at same level
#         print(hierarchy[0][0][1])   #prievous contours at same level
#         print(hierarchy[0][0][2])   #first child of contour
#         print(hierarchy[0][0][3])   #parent of contour
# =============================================================================
        maxArea = 0
        
        #Might need to revise for base case(where 0th position of the hierarchy is the parent)
        print(hierarchy[0])
        print(hierarchy[0][0])
        #parent = hierarchy[0][0][0]
        # Might stick with parent equation above, but setting it to 0 solved the base case
        parent = 0
        #if hierarchy[0][0][2] == -1:
        while hierarchy[0][parent][2] == -1:
            cv2.drawContours(savedImageColor, imgContours, hierarchy[0][parent][2],(0,255,0),3) #Only one contour
          #  cv2.drawContours(savedImageColor, hierarchy[0][parent][2], 0, (255,0,0), 3)
            if hierarchy[0][parent][0] > -1:
                #This goes to another contour at the same level if there is one
                parent = hierarchy[0][parent][0]
            elif hierarchy[0][parent][0] == -1:
                break
                
        #elif parent[2] > -1:
        #Need to revise this while statement for case where the only one outer contour since there will be no next
        while hierarchy[0][parent][0] > -1 or hierarchy[0][parent][2] > -1:
            robotNumber = hierarchy[0][0]
            #currentContour = 0   ################ Might not be able to assume initial parent is contour 0!!!
            contourTotal = 1
            childorNext = hierarchy[0][parent][2]
            maxArea = 0
            #This loop draws all the direct children of the parent contour a different color from the parent
            while True:
                #hierarchy[0][child]
                print(hierarchy[0])
                #Finding the biggest child contour in order to determine which contour to use to locate the front
                #of the robot
                currentArea = cv2.contourArea(imgContours[childorNext])
                if currentArea > maxArea:
                    maxArea = currentArea
                    frontContour = childorNext
                
                if contourTotal == 1:
                    # Gets the centroid of the parent (Robot body)
                    if cv2.contourArea(imgContours[hierarchy[0][childorNext][3]]) > 50:
                        M = cv2.moments(imgContours[hierarchy[0][childorNext][3]])
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        centroidPoint = (cx, cy)
                cv2.drawContours(savedImageColor, imgContours, childorNext, (255,0,0), 3)
                #qqqcv2.drawContours(savedImageColor, childorNext, childorNext, (255,0,0), 3)
                #print("current contour", hierarchy[0][childorNext])
                childorNext = hierarchy[0][childorNext][0]

                print("contour Total", contourTotal)
                if childorNext == -1:
                    break
                
                contourTotal += 1
            
            print("contour Total", contourTotal)
            # Finding info to pass to ros for robot 2
            
            if contourTotal == 2:
                #Prints Robot 2 at centroid position of the body
                print("centroid point of robot 1", centroidPoint)
                cv2.putText(savedImageColor, "Robot 1",
        	       (cx-50, cy-50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2)
                #Finds centroid position of the front contour, which will be
                #used to find front of the robot
                FrontM = cv2.moments(imgContours[frontContour])
                Frontcx = int(FrontM['m10']/FrontM['m00'])
                Frontcy = int(FrontM['m01']/FrontM['m00'])
                FrontCentroidPoint = (Frontcx, Frontcy)
# =============================================================================
#                 cv2.putText(savedImageColor, "Front", FrontCentroidPoint, 
#                             cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 150, 0), 2)
# =============================================================================
                #finding the relative coordinates of the front contour with
                #respect to the center of the body
                netPositionX = Frontcx - cx
                netPositionY = Frontcy - cy
                netPosition1 = (netPositionX, netPositionY)
                print("net position of robot 1", netPosition1)
                
                ############################################
                #find and print angle
                #There might need to be if statements based on the x and y values
                #to determine if the x or y term is the opposite side of the angle
                #Not sure how to do this yet, maybe compare lengths of each to hypotenuse
                #also need if statement for fringe case where front is exactly due
                #north, east, west, or south since denominator could have no change which would divide by 0
                #will then need to get angle based on the origin (due east)
                #math.degrees(math.atan(netPositionX/netPositionY))
                ############################################
                
                angle1 = get_angle(netPositionX, netPositionY)
                print("angle of robot 1 is", angle1)
                if initial1 == False:
                     with open("Initial_Output.txt", "a") as text_file:
                         text_file.write("Centroid of robot 1: x position is %d, y position is %d\n" % (cx, cy))
                         text_file.write("Net position of robot 1: x position is %d, y position is %d\n" % (netPositionX, netPositionY))
                         text_file.write("Angle of robot 1: %d\n" % angle1)
                     initial1 = True
# =============================================================================
#                 cv2.putText(savedImageColor, angle1, FrontCentroidPoint, 
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 150, 150), 2)
# =============================================================================
                #First attempt at angle
# =============================================================================
#                 if netPositionX > 0 and netPositionY > 0:
#                     if netPositionX >= netPositionY:
#                         angle1 = math.degrees(math.atan(netPositionY/netPositionX))
#                     elif netPositionX < netPositionY:
#                         angle1 = math.degrees(math.atan(netPositionX/netPositionY))
#                 elif netPositionX < 0 and netPositionY > 0:
#                     if netPositionX >= netPositionY:
#                         angle1 = math.degrees(math.atan(netPositionY/netPositionX)) + 90
#                     elif netPositionX < netPositionY:
#                         angle1 = math.degrees(math.atan(netPositionX/netPositionY)) + 90
#                 elif netPositionX < 0 and netPositionY < 0:
#                     if netPositionX >= netPositionY:
#                         angle1 = math.degrees(math.atan(netPositionY/netPositionX)) + 180
#                     elif netPositionX < netPositionY:
#                         angle1 = math.degrees(math.atan(netPositionX/netPositionY)) + 180
#                 elif netPositionX > 0 and netPositionY < 0:
#                     if netPositionX >= netPositionY:
#                         angle1 = math.degrees(math.atan(netPositionY/netPositionX)) + 270
#                         if angle1 == 360:
#                             angle1 = 0
#                     elif netPositionX < netPositionY:
#                         angle1 = math.degrees(math.atan(netPositionX/netPositionY)) + 270
#                 elif netPositionX == 0:
#                     if netPositionY > 0:
#                         angle1 = 90
#                     elif netPositionY < 0:
#                         angle1 = 270
#                 elif netPositionY == 0:
#                     if netPositionX > 0:
#                         angle1 = 0
#                     elif netPositionX < 0:
#                         angle1 = 180
# =============================================================================
                    
                        
                        
# =============================================================================
#                 if initial1 == False:
#                     with open("Initial_Output.txt", "a") as text_file:
#                         text_file.write("Centroid of robot 1: x position is %d, y position is %d\n" % (cx, cy))
#                         text_file.write("Net position of robot 1: x position is %d, y position is %d\n" % (netPositionX, netPositionY))
#                     initial1 = True
#                     
#                 with open("Output.txt", "w") as text_file:
#                     text_file.write("Centroid of robot 1: x position is %d, y position is %d" % (cx, cy))
#                     text_file.write("Net position of robot 1: x position is %d, y position is %d" % (netPositionX, netPositionY))
# =============================================================================
                    
            
            elif contourTotal == 3:
                #Prints Robot 2 at centroid position of the body
                print("centroid point of robot 2", centroidPoint)
                cv2.putText(savedImageColor, "Robot 2",
        	       (cx-50, cy-50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2)
                #Finds centroid position of the front contour, which will be
                #used to find front of the robot
                FrontM = cv2.moments(imgContours[frontContour])
                Frontcx = int(FrontM['m10']/FrontM['m00'])
                Frontcy = int(FrontM['m01']/FrontM['m00'])
                FrontCentroidPoint = (Frontcx, Frontcy)
# =============================================================================
#                 cv2.putText(savedImageColor, "Front", FrontCentroidPoint, 
#                             cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 150, 0), 2)
# =============================================================================
                #finding the relative coordinates of the front contour with
                #respect to the center of the body
                netPositionX = Frontcx - cx
                netPositionY = Frontcy - cy
                netPosition2 = (netPositionX, netPositionY)
                print("net position of robot 2", netPosition2)
                #if x is pos and y is pos, then front is southeast from body cen
                #if x is pos and y is neg, then front is northeast from body cen
                #if x is neg and y is pos, then front is southwest from body cen
                #if x is neg and y is neg, then front is northwest from body cen
                
                
                angle2 = get_angle(netPositionX, netPositionY)
                print("angle of robot 2 is", angle2)
                if initial2 == False:
                     with open("Initial_Output.txt", "a") as text_file:
                         text_file.write("Centroid of robot 2: x position is %d, y position is %d\n" % (cx, cy))
                         text_file.write("Net position of robot 2: x position is %d, y position is %d\n" % (netPositionX, netPositionY))
                         text_file.write("Angle of robot 2: %d\n" % angle2)
                     initial2 = True
# =============================================================================
#                 cv2.putText(savedImageColor, angle2,
#         	       FrontCentroidPoint, cv2.FONT_HERSHEY_SIMPLEX,
#                 1, (150, 150, 150), 2)
# =============================================================================
# =============================================================================
#                 if netPositionX > 0 and netPositionY > 0:
#                     if netPositionX >= netPositionY:
#                         angle2 = math.degrees(math.atan(netPositionY/netPositionX))
#                     elif netPositionX < netPositionY:
#                         angle2 = math.degrees(math.atan(netPositionX/netPositionY))
#                 elif netPositionX < 0 and netPositionY > 0:
#                     if netPositionX >= netPositionY:
#                         angle2 = math.degrees(math.atan(netPositionY/netPositionX)) + 90
#                     elif netPositionX < netPositionY:
#                         angle2 = math.degrees(math.atan(netPositionX/netPositionY)) + 90
#                 elif netPositionX < 0 and netPositionY < 0:
#                     if netPositionX >= netPositionY:
#                         angle2 = math.degrees(math.atan(netPositionY/netPositionX)) + 180
#                     elif netPositionX < netPositionY:
#                         angle2 = math.degrees(math.atan(netPositionX/netPositionY)) + 180
#                 elif netPositionX > 0 and netPositionY < 0:
#                     if netPositionX >= netPositionY:
#                         angle2 = math.degrees(math.atan(netPositionY/netPositionX)) + 270
#                         if angle2 == 360:
#                             angle2 = 0
#                     elif netPositionX < netPositionY:
#                         angle2 = math.degrees(math.atan(netPositionX/netPositionY)) + 270
#                 elif netPositionX == 0:
#                     if netPositionY > 0:
#                         angle2 = 90
#                     elif netPositionY < 0:
#                         angle2 = 270
#                 elif netPositionY == 0:
#                     if netPositionX > 0:
#                         angle2 = 0
#                     elif netPositionX < 0:
#                         angle2 = 180
# =============================================================================
                
# =============================================================================
#                 if initial2 == False:
#                     with open("Initial_Output.txt", "a") as text_file:
#                         text_file.write("Centroid of robot 2: x position is %d, y position is %d\n" % (cx, cy))
#                         text_file.write("Net position of robot 2: x position is %d, y position is %d\n" % (netPositionX, netPositionY))
#                     initial2 = True
#                 
#                 with open("Output.txt", "w") as text_file:
#                     text_file.write("Centroid of robot 2: x position is %d, y position is %d" % (cx, cy))
#                     text_file.write("Net position of robot 2: x position is %d, y position is %d" % (netPositionX, netPositionY))
# =============================================================================
                    
                #Send centroid point of body and relative direction to ros
            elif contourTotal == 4:
                #Prints Robot 2 at centroid position of the body
                print("centroid point of robot 3", centroidPoint)
                cv2.putText(savedImageColor, "Robot 3",
        	       (cx-50, cy-50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2)
                #Finds centroid position of the front contour, which will be
                #used to find front of the robot
                FrontM = cv2.moments(imgContours[frontContour])
                Frontcx = int(FrontM['m10']/FrontM['m00'])
                Frontcy = int(FrontM['m01']/FrontM['m00'])
                FrontCentroidPoint = (Frontcx, Frontcy)
# =============================================================================
#                 cv2.putText(savedImageColor, "Front", FrontCentroidPoint, 
#                             cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 150, 0), 2)
# =============================================================================
                #finding the relative coordinates of the front contour with
                #respect to the center of the body
                netPositionX = Frontcx - cx
                netPositionY = Frontcy - cy
                netPosition3 = (netPositionX, netPositionY)
                print("net position of robot 3", netPosition3)
                
                angle3 = get_angle(netPositionX, netPositionY)
                print("angle of robot 3 is", angle3)
                if initial3 == False:
                     with open("Initial_Output.txt", "a") as text_file:
                         text_file.write("Centroid of robot 3: x position is %d, y position is %d\n" % (cx, cy))
                         text_file.write("Net position of robot 3: x position is %d, y position is %d\n" % (netPositionX, netPositionY))
                         text_file.write("Angle of robot 3: %d\n" % angle3)
                     initial3 = True
# =============================================================================
#                 cv2.putText(savedImageColor, angle3, FrontCentroidPoint, 
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 150, 150), 2)
# =============================================================================
# =============================================================================
#                 if netPositionX > 0 and netPositionY > 0:
#                     if netPositionX >= netPositionY:
#                         angle3 = math.degrees(math.atan(netPositionY/netPositionX))
#                     elif netPositionX < netPositionY:
#                         angle3 = math.degrees(math.atan(netPositionX/netPositionY))
#                 elif netPositionX < 0 and netPositionY > 0:
#                     if netPositionX >= netPositionY:
#                         angle3 = math.degrees(math.atan(netPositionY/netPositionX)) + 90
#                     elif netPositionX < netPositionY:
#                         angle3 = math.degrees(math.atan(netPositionX/netPositionY)) + 90
#                 elif netPositionX < 0 and netPositionY < 0:
#                     if netPositionX >= netPositionY:
#                         angle3 = math.degrees(math.atan(netPositionY/netPositionX)) + 180
#                     elif netPositionX < netPositionY:
#                         angle3 = math.degrees(math.atan(netPositionX/netPositionY)) + 180
#                 elif netPositionX > 0 and netPositionY < 0:
#                     if netPositionX >= netPositionY:
#                         angle3 = math.degrees(math.atan(netPositionY/netPositionX)) + 270
#                         if angle3 == 360:
#                             angle3 = 0
#                     elif netPositionX < netPositionY:
#                         angle3 = math.degrees(math.atan(netPositionX/netPositionY)) + 270
#                 elif netPositionX == 0:
#                     if netPositionY > 0:
#                         angle3 = 90
#                     elif netPositionY < 0:
#                         angle3 = 270
#                 elif netPositionY == 0:
#                     if netPositionX > 0:
#                         angle3 = 0
#                     elif netPositionX < 0:
#                         angle3 = 180
# =============================================================================
                
# =============================================================================
#                 if initial3 == False:
#                     with open("Initial_Output.txt", "a") as text_file:
#                         text_file.write("Centroid of robot 3: x position is %d, y position is %d\n" % (cx, cy))
#                         text_file.write("Net position of robot 3: x position is %d, y position is %d\n" % (netPositionX, netPositionY))
#                     initial3 = True
#                 
#                 with open("Output.txt", "w") as text_file:
#                     text_file.write("Centroid of robot 3: x position is %d, y position is %d\n" % (cx, cy))
#                     text_file.write("Net position of robot 3: x position is %d, y position is %d\n" % (netPositionX, netPositionY))
# =============================================================================
                    
                
            elif contourTotal == 5:
                #Prints Robot 2 at centroid position of the body
                print("centroid point of robot 4", centroidPoint)
                cv2.putText(savedImageColor, "Robot 4",
        	       (cx-50, cy-50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2)
                #Finds centroid position of the front contour, which will be
                #used to find front of the robot
                FrontM = cv2.moments(imgContours[frontContour])
                Frontcx = int(FrontM['m10']/FrontM['m00'])
                Frontcy = int(FrontM['m01']/FrontM['m00'])
                FrontCentroidPoint = (Frontcx, Frontcy)
# =============================================================================
#                 cv2.putText(savedImageColor, "Front", FrontCentroidPoint, 
#                             cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 150, 0), 2)
# =============================================================================
                #finding the relative coordinates of the front contour with
                #respect to the center of the body
                netPositionX = Frontcx - cx
                netPositionY = Frontcy - cy
                netPosition4 = (netPositionX, netPositionY)
                print("net position of robot 4", netPosition4)
                
                angle4 = get_angle(netPositionX, netPositionY)
                print("angle of robot 4 is", angle4)
                if initial4 == False:
                     with open("Initial_Output.txt", "a") as text_file:
                         text_file.write("Centroid of robot 4: x position is %d, y position is %d\n" % (cx, cy))
                         text_file.write("Net position of robot 4: x position is %d, y position is %d\n" % (netPositionX, netPositionY))
                         text_file.write("Angle of robot 4: %d\n" % angle4)
                     initial4 = True
# =============================================================================
#                 cv2.putText(savedImageColor, angle4, FrontCentroidPoint, 
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 150, 150), 2)
# =============================================================================
# =============================================================================
#                 if netPositionX > 0 and netPositionY > 0:
#                     if netPositionX >= netPositionY:
#                         angle4 = math.degrees(math.atan(netPositionY/netPositionX))
#                     elif netPositionX < netPositionY:
#                         angle4 = math.degrees(math.atan(netPositionX/netPositionY))
#                 elif netPositionX < 0 and netPositionY > 0:
#                     if netPositionX >= netPositionY:
#                         angle4 = math.degrees(math.atan(netPositionY/netPositionX)) + 90
#                     elif netPositionX < netPositionY:
#                         angle4 = math.degrees(math.atan(netPositionX/netPositionY)) + 90
#                 elif netPositionX < 0 and netPositionY < 0:
#                     if netPositionX >= netPositionY:
#                         angle4 = math.degrees(math.atan(netPositionY/netPositionX)) + 180
#                     elif netPositionX < netPositionY:
#                         angle4 = math.degrees(math.atan(netPositionX/netPositionY)) + 180
#                 elif netPositionX > 0 and netPositionY < 0:
#                     if netPositionX >= netPositionY:
#                         angle4 = math.degrees(math.atan(netPositionY/netPositionX)) + 270
#                         if angle4 == 360:
#                             angle4 = 0
#                     elif netPositionX < netPositionY:
#                         angle4 = math.degrees(math.atan(netPositionX/netPositionY)) + 270
#                 elif netPositionX == 0:
#                     if netPositionY > 0:
#                         angle4 = 90
#                     elif netPositionY < 0:
#                         angle4 = 270
#                 elif netPositionY == 0:
#                     if netPositionX > 0:
#                         angle4 = 0
#                     elif netPositionX < 0:
#                         angle4 = 180
# =============================================================================
                
# =============================================================================
#                 if initial4 == False:
#                     with open("Initial_Output.txt", "a") as text_file:
#                         text_file.write("Centroid of robot 4: x position is %d, y position is %d\n" % (cx, cy))
#                         text_file.write("Net position of robot 4: x position is %d, y position is %d\n" % (netPositionX, netPositionY))
#                     initial4 = True
#                 
#                 with open("Output.txt", "w") as text_file:
#                     text_file.write("Centroid of robot 4: x position is %d, y position is %d" % (cx, cy))
#                     text_file.write("Net position of robot 4: x position is %d, y position is %d" % (netPositionX, netPositionY))
# =============================================================================
                    
                
            # Goes to the next parent in the same level (should be another robot body)
            if hierarchy[0][parent][0] > -1:
                parent = hierarchy[0][parent][0]
            elif hierarchy[0][parent][0] == -1:
                break
                
            # Resets the contour total for the next robot body
            contourTotal = 1
       
        
# =============================================================================
#         #Code for size of objects lines 125-209
#         cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#         
#         # sort the contours from left-to-right and initialize the
#         # 'pixels per metric' calibration variable
#         (cnts, _) = contours.sort_contours(cnts)
#         pixelsPerMetric = None
#         
#         # loop over the contours individually
#         for c in cnts:
#             # if the contour is not sufficiently large, ignore it
#             if cv2.contourArea(c) < 100:
#                 continue
#             
#             # compute the rotated bounding box of the contour
#             #orig = transition
#             
#             #black and white image
#             #orig = thresh
#             #color image
#             orig = img
#             
#             box = cv2.minAreaRect(c)
#             box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
#             box = np.array(box, dtype="int")
#             
#             # order the points in the contour such that they appear
#             # in top-left, top-right, bottom-right, and bottom-left
#             # order, then draw the outline of the rotated bounding
#             # box
#             box = perspective.order_points(box)
#             cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
#         
#             # loop over the original points and draw them
#             for (x, y) in box:
#                 cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
#             
#             # unpack the ordered bounding box, then compute the midpoint
#             # between the top-left and top-right coordinates, followed by
#             # the midpoint between bottom-left and bottom-right coordinates
#             (tl, tr, br, bl) = box
#             (tltrX, tltrY) = midpoint(tl, tr)
#             (blbrX, blbrY) = midpoint(bl, br)
#             
#             # compute the midpoint between the top-left and top-right points,
#             # followed by the midpoint between the top-righ and bottom-right
#             (tlblX, tlblY) = midpoint(tl, bl)
#             (trbrX, trbrY) = midpoint(tr, br)
#             
#             # draw the midpoints on the image
#             cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
#             cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
#             cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
#             cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
#             
#             # draw lines between the midpoints
#             cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
#             	(255, 0, 255), 2)
#             cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
#             	(255, 0, 255), 2)
#             
#             # compute the Euclidean distance between the midpoints
#             dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
#             dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
#             
#             # if the pixels per metric has not been initialized, then
#             # compute it as the ratio of pixels to supplied metric
#             # (in this case, inches)
#             if pixelsPerMetric is None:
#                 pixelsPerMetric = dB / 2.25
#             
#             # compute the size of the object
#             dimA = dA / pixelsPerMetric
#             dimB = dB / pixelsPerMetric
#             
#             # draw the object sizes on the image
#             cv2.putText(orig, "{:.1f}in".format(dimA),
#             	(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
#             	0.65, (255, 255, 255), 2)
#             cv2.putText(orig, "{:.1f}in".format(dimB),
#             	(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
#             	0.65, (255, 255, 255), 2)
#             cv2.imshow("Size Image", orig)
# =============================================================================
# =============================================================================
#         if contourTotal == 1:
#             print("1 child contour")
#         elif contourTotal == 2:
#             print("2 child contours")
#         elif contourTotal == 3:
#             print("3 child contours")
#         else:
#             print("More than 3 child contours")
# =============================================================================
                
                
        count += 1
        
    #hierarchy = hierarchy[0] # get the actual inner list of hierarchy descriptions
    

# For each contour, find the bounding rectangle and draw it
# =============================================================================
#     for component in zip(contours, hierarchy):
#         currentContour = component[0]
#         currentHierarchy = component[1]
#         x,y,w,h = cv2.boundingRect(currentContour)
#         if currentHierarchy[2] < 0:
#             # these are the innermost child components
#             cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),3)
#         elif currentHierarchy[3] < 0:
#             # these are the outermost parent components
#             cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),3)
# =============================================================================
    if count == 1:
   #     cv2.imshow('saved image', savedImage)
        cv2.imshow('saved image with color', savedImageColor)

    count = 0

    cv2.imshow('img', img)
    cv2.imshow('test', thresh)
   # cv2.imshow('img2', img2)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
cv2.destroyAllWindows()
cap.release()

# =============================================================================
# 
# img = cv2.imread('opencv-logo2.png')
#  
# imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(imgray,80,255,0)
# img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 
# cv2.drawContours(img, contours, -1, (0,255,255), 3)
# #for i in hierarchy:
#   
# print(contours)  
# print(hierarchy)
# 
# hierarchy = hierarchy[0] # get the actual inner list of hierarchy descriptions
# 
# # For each contour, find the bounding rectangle and draw it
# for component in zip(contours, hierarchy):
#     currentContour = component[0]
#     currentHierarchy = component[1]
#     x,y,w,h = cv2.boundingRect(currentContour)
#     if currentHierarchy[2] < 0:
#         # these are the innermost child components
#         cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),3)
#     elif currentHierarchy[3] < 0:
#         # these are the outermost parent components
#         cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),3)
# 
# #kernel = np.ones((5,5), np.float32)/25
# #dst = cv2.filter2D(img, -1, kernel)
#  
# cv2.imshow('img',img)
# 
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# =============================================================================

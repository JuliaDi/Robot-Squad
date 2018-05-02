# -*- coding: utf-8 -*-
"""
Created on Tue May  1 13:46:49 2018

@author: Alex
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


def revise_centroid(cx, cy):
    
    #Mark the center of the arena
    cv2.circle(img, (400, 300), 3, (255,255,255), -1)
    changeValueX = int(abs(400 - cx)/25)
    changeValueY = int(abs(300 - cy)/25)
    
    if cx >= 400:
        if cy >= 300:
            cv2.circle(img, (cx - changeValueX, cy - changeValueY), 3, (0,0,0), -1)
            newcx = cx - changeValueX
            newcy = cy - changeValueY
        elif cy < 300:
            cv2.circle(img, (cx - changeValueX, cy + changeValueY), 3, (0,0,0), -1)
            newcx = cx - changeValueX
            newcy = cy + changeValueY
    elif cx < 400:
        if cy >= 300:
            cv2.circle(img, (cx + changeValueX, cy - changeValueY), 3, (0,0,0), -1)
            newcx = cx + changeValueX
            newcy = cy - changeValueY
        elif cy < 300:
            cv2.circle(img, (cx + changeValueX, cy + changeValueY), 3, (0,0,0), -1)
            newcx = cx + changeValueX
            newcy = cy + changeValueY
            
    return  newcx, newcy

# =============================================================================
#     if cx > 750 and cy > 250 and cy < 300:
#         cv2.circle(img, (cx - 16, cy), 3, (125,255,125), -1)
# =============================================================================
    
   # return cx, cy

#Not sure if I need this
def get_centroid(centroid):
    
    centroidList.append(centroid)
    
    return centroidList

def get_angle(netPositionX, netPositionY):
    angle1 = 0
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

    
count = 0

initial1 = False
initial2 = False
initial3 = False
initial4 = False

isRobot = False
centroidList = []

while True:
    start = time.time()
    
    ret, img = cap.read()
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,150,255,0)
    thresh = cv2.dilate(thresh, None, iterations=1)
    thresh = cv2.erode(thresh, None, iterations=1)
    img2, imgContours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    largest_areas = sorted(imgContours, key=cv2.contourArea)
    
    if count == 0 and hierarchy is not None:
        savedImage = img2
        savedImageColor = img
        
        # draws a circle at the centroid of each child contour
        for i in range(0,len(imgContours)):
            
            #Moment and centroid stuff
            cnt = imgContours[i] #parameter refers to which contour to use
            if cv2.contourArea(cnt) < 100:
                continue
            
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            centroidPoint = (cx, cy)
            cv2.circle(savedImageColor, centroidPoint, 3, (0,0,255), -1)
            print("outside centroid point", centroidPoint)
    
        maxArea = 0
        

        #print(hierarchy[0])
        #print(hierarchy[0][0])

        parent = 0
        parentRun = 0
        print(hierarchy)
        
# =============================================================================
#                 while hierarchy[0][parentRun][2] > -1:
#             hold = hierarchy[0][parentRun][2]
#             cv2.drawContours(savedImageColor, imgContours, hierarchy[0][hold][3],(0,255,0),3)
#             
#             while hierarchy[0][parentRun][0] > -1:
#                 parentRun = hierarchy[0][parentRun][0]
#                 if hierarchy[0][parentRun][0] > -1 and hierarchy[0][parentRun][2] == -1:
#                     parentRun = hierarchy[0][parentRun[0]
#                     
#                 else:
#                     break
# # =============================================================================
# #                 elif hierarchy[0][parentRun][2] > -1:
# #                     break
# #                 elif hierarchy[0][parentRun][0] == -1:
# #                     break
# # =============================================================================
#             if hierarchy[0][parentRun][0] == -1:
#                 break
# =============================================================================
        
        #Colors the outside of the Robots green
        while hierarchy[0][parentRun][2] > -1:
            hold = hierarchy[0][parentRun][2]
            cv2.drawContours(savedImageColor, imgContours, hierarchy[0][hold][3],(0,255,0),3)
            
            if hierarchy[0][parentRun][0] > -1:
                parentRun = hierarchy[0][parentRun][0]
            elif hierarchy[0][parentRun][0] == -1:
                break
        
        while hierarchy[0][parent][2] == -1:
            cv2.drawContours(savedImageColor, imgContours, hierarchy[0][parent][2],(0,255,0),3) #Only one contour

            if hierarchy[0][parent][0] > -1:
                #This goes to another contour at the same level if there is one
                parent = hierarchy[0][parent][0]
            elif hierarchy[0][parent][0] == -1:
                break
        
        objectRun = 0
        #Detects objects and colors
        while hierarchy[0][objectRun][3] == -1 and (hierarchy[0][objectRun][0] > -1 or hierarchy[0][objectRun][1] > -1):
            if hierarchy[0][objectRun][2] > -1 and hierarchy[0][objectRun][0] > -1:
                objectRun = hierarchy[0][objectRun][0]
                continue
            elif hierarchy[0][objectRun][2] > -1 and hierarchy[0][objectRun][0] == -1:
                break
            
            if hierarchy[0][objectRun][0] > -1:
                hold = hierarchy[0][objectRun][0]
                cv2.drawContours(savedImageColor, imgContours, hierarchy[0][hold][1],(255,0,255),3)
                #get coordinates here
            elif hierarchy[0][objectRun][1] > -1:
                hold = hierarchy[0][objectRun][1]
                cv2.drawContours(savedImageColor, imgContours, hierarchy[0][hold][0],(255,0,255),3)
                #get coordinates here
            
            if hierarchy[0][objectRun][0] > -1:
                objectRun = hierarchy[0][objectRun][0]
            elif hierarchy[0][objectRun][0] == -1:
                break
        
        isObject = True
        
        while hierarchy[0][parent][0] > -1 or hierarchy[0][parent][2] > -1:
            robotNumber = hierarchy[0][0]
            
            #isObject = True

            contourTotal = 1
            childorNext = hierarchy[0][parent][2]
            maxArea = 0
            #This loop draws all the direct children of the parent contour a different color from the parent
            while True:
                isObject = False
                #print(hierarchy[0])
                #Finding the biggest child contour in order to determine which contour to use to locate the front
                #of the robot
                currentArea = cv2.contourArea(imgContours[childorNext])
                holdContour = imgContours[childorNext]
                
                
                #This if statement was just added to potentially skip over too small contours
                if cv2.contourArea(imgContours[hierarchy[0][childorNext][3]]) < 100:
                    childorNext = hierarchy[0][childorNext][0]

                #print("contour Total", contourTotal)
                    if childorNext == -1:
                        break
                    
                    continue
                
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
                        centroidList = get_centroid(centroidPoint)
               # cv2.drawContours(savedImageColor, imgContours, childorNext, (255,0,0), 3)
                
                if contourTotal > 1:
                    cv2.drawContours(savedImageColor, imgContours, hierarchy[0][childorNext][1], (255,0,0), 3)
                    cv2.drawContours(savedImageColor, imgContours, childorNext, (255,0,0), 3)
                    isRobot = True

                childorNext = hierarchy[0][childorNext][0]

                #print("contour Total", contourTotal)
                if childorNext == -1:
                    break
                
                contourTotal += 1
              #  isObject = False
            
            #print("contour Total", contourTotal)
            # Finding info to pass to ros for robot 2
            
            if contourTotal == 2 and isRobot == True:
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

                #finding the relative coordinates of the front contour with
                #respect to the center of the body
                netPositionX = Frontcx - cx
                netPositionY = Frontcy - cy
                netPosition1 = (netPositionX, netPositionY)
                print("net position of robot 1", netPosition1)
                
                angle1 = get_angle(netPositionX, netPositionY)
                print("angle of robot 1 is", angle1)
                strAngle1 = str(angle1)
                
                
                newcx1, newcy1 = revise_centroid(cx, cy)
                print("revised centroid is ", newcx1, newcy1)
                strcx = str(newcx1)
                strcy = str(newcy1)
                cv2.putText(savedImageColor, "Robot 1 at", (0,20), cv2.FONT_HERSHEY_PLAIN, 1, (200,200,200),2)
                cv2.putText(savedImageColor, "(" + strcx + "," + strcy + ")",
        	       (100, 20), cv2.FONT_HERSHEY_PLAIN,
                1, (200, 200, 200), 2)
                
                #infoRobot1 = (cx, cy, angle1)
                infoRobot1 = (newcx1, newcy1, angle1)
            
            elif contourTotal == 3 and isRobot == True:
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

                #finding the relative coordinates of the front contour with
                #respect to the center of the body
                netPositionX = Frontcx - cx
                netPositionY = Frontcy - cy
                netPosition2 = (netPositionX, netPositionY)
                print("net position of robot 2", netPosition2)

                
                
                angle2 = get_angle(netPositionX, netPositionY)
                print("angle of robot 2 is", angle2)
                strAngle2 = str(angle2)
# =============================================================================
#                 cv2.putText(savedImageColor, "Robot 2:", (0,40), cv2.FONT_HERSHEY_PLAIN, 1, (200,200,200),2)
#                 cv2.putText(savedImageColor, "Angle = " + str(strAngle2),
#         	       (80, 40), cv2.FONT_HERSHEY_PLAIN,
#                 1, (0, 0, 255), 2)
# =============================================================================

                newcx2, newcy2 = revise_centroid(cx, cy)
                print("revised centroid is ", newcx2, newcy2)
                
                strcx = str(newcx2)
                strcy = str(newcy2)
                cv2.putText(savedImageColor, "Robot 2 at ", (0,40), cv2.FONT_HERSHEY_PLAIN, 1, (200,200,200),2)
                cv2.putText(savedImageColor, "(" + strcx + "," + strcy + ")",
        	       (100, 40), cv2.FONT_HERSHEY_PLAIN,
                1, (200, 200, 200), 2)
                
                #infoRobot2 = (cx, cy, angle2)
                infoRobot2 = (newcx2, newcy2, angle2)
                    
                #Send centroid point of body and relative direction to ros
            elif contourTotal == 4 and isRobot == True:
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

                #finding the relative coordinates of the front contour with
                #respect to the center of the body
                netPositionX = Frontcx - cx
                netPositionY = Frontcy - cy
                netPosition3 = (netPositionX, netPositionY)
                print("net position of robot 3", netPosition3)
                
                angle3 = get_angle(netPositionX, netPositionY)
                newcx3, newcy3 = revise_centroid(cx, cy)
                print("revised centroid is ", newcx3, newcy3)
                print("angle of robot 3 is", angle3)
                
                strAngle3 = str(angle3)
# =============================================================================
#                 cv2.putText(savedImageColor, "Robot 3:", (0,60), cv2.FONT_HERSHEY_PLAIN, 1, (200,200,200),2)
#                 cv2.putText(savedImageColor, "Angle = " + str(strAngle3),
#         	       (80, 60), cv2.FONT_HERSHEY_PLAIN,
#                 1, (0, 0, 255), 2)
# =============================================================================
                     
                strcx = str(newcx3)
                strcy = str(newcy3)
                cv2.putText(savedImageColor, "Robot 3 at ", (0,60), cv2.FONT_HERSHEY_PLAIN, 1, (200,200,200),2)
                cv2.putText(savedImageColor, "(" + strcx + "," + strcy + ")",
        	       (100, 60), cv2.FONT_HERSHEY_PLAIN,
                1, (200, 200, 200), 2)
                #infoRobot3 = (cx, cy, angle3)
                infoRobot3 = (newcx3, newcy3, angle3)
            
            elif contourTotal == 5 and isRobot == True:
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

                #finding the relative coordinates of the front contour with
                #respect to the center of the body
                netPositionX = Frontcx - cx
                netPositionY = Frontcy - cy
                netPosition4 = (netPositionX, netPositionY)
                print("net position of robot 4", netPosition4)
                
                angle4 = get_angle(netPositionX, netPositionY)
                newcx4, newcy4 = revise_centroid(cx, cy)
                print("revised centroid is ", newcx4, newcy4)
                print("angle of robot 4 is", angle4)
                
                strAngle4 = str(angle4)
# =============================================================================
#                 cv2.putText(savedImageColor, "Robot 4:", (0,80), cv2.FONT_HERSHEY_PLAIN, 1, (200,200,200),2)
#                 cv2.putText(savedImageColor, "Angle = " + str(strAngle4),
#         	       (80, 80), cv2.FONT_HERSHEY_PLAIN,
#                 1, (200, 200, 200), 2)
# =============================================================================
                     
                strcx = str(newcx4)
                strcy = str(newcy4)
                cv2.putText(savedImageColor, "Robot 4 at ", (0,80), cv2.FONT_HERSHEY_PLAIN, 1, (200,200,200),2)
                cv2.putText(savedImageColor,"(" + strcx + "," + strcy + ")",
        	       (100, 80), cv2.FONT_HERSHEY_PLAIN,
                1, (200, 200, 200), 2)
                
                #infoRobot4 = (cx, cy, angle4)
                infoRobot4 = (newcx4, newcy4, angle4)
                
            elif contourTotal == 1 and currentArea > 20 and isObject == True:
                cv2.circle(img, (cx,cy), 10, (150,120,60), -1)
                
                #For some reason it draws on every contour??
                #cv2.drawContours(savedImageColor, imgContours, holdContourLoc,(0,255,255),3) #Only one contour
                
                #get contour coordinates
                print("coordinates of object")
                print(holdContour)         
                
            # Goes to the next parent in the same level (should be another robot body)
            if hierarchy[0][parent][0] > -1:
                parent = hierarchy[0][parent][0]
            elif hierarchy[0][parent][0] == -1:
                break
                
            # Resets the contour total for the next robot body
            contourTotal = 1
            isRobot = False
                
                
        count += 1
        
        

    if count == 1:

        cv2.imshow('saved image with color', savedImageColor)
        

    count = 0
    #This is for me
    holdcentroidList = centroidList
    centroidList = []
    cv2.imshow('img', img)
    cv2.imshow('test', thresh)
    
    end = time.time()
    print(end - start)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
cv2.destroyAllWindows()
cap.release()


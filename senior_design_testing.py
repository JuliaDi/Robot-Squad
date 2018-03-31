# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 18:05:21 2018

@author: Nike
"""
import cv2
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import os
#import imutils

cap = cv2.VideoCapture(1)
count = 0
while True:
    ret, img = cap.read()
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,90,255,0)
    thresh = cv2.dilate(thresh, None, iterations=1)
    thresh = cv2.erode(thresh, None, iterations=1)
    img2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0,255,0), 3)
    
    if count == 0 and (cv2.waitKey(1) & 0xFF == ord('r')):
        savedImage = img2
        savedImageColor = img
        cv2.drawContours(savedImageColor, contours, 0, (0,255,0), 3) #0 argument draws it at outer contour
        
        # draws a circle at the centroid of each child contour
        for i in range(0,len(contours)):
            
            #Moment and centroid stuff
            cnt = contours[i] #parameter refers to which contour to use
            if cv2.contourArea(cnt) < 50:
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
        if hierarchy[0][0][2] == -1:
            cv2.drawContours(savedImageColor, contours, hierarchy[0][0][2],(0,255,0),3) #Only one contour
        elif hierarchy[0][0][2] > -1:
            robotNumber = hierarchy[0][0][2]
            #currentContour = 0   ################ Might not be able to assume initial parent is contour 0!!!
            contourTotal = 1
            childorNext = hierarchy[0][0][2]
            #This loop draws all the direct children of the parent contour a different color from the parent
            while True:
                #hierarchy[0][child]
                if contourTotal == 1:
                    M = cv2.moments(contours[childorNext])
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    centroidPoint = (cx, cy)
                cv2.drawContours(savedImageColor, contours, childorNext, (255,0,0), 3)
                #print("current contour", hierarchy[0][childorNext])
                childorNext = hierarchy[0][childorNext][0]

                print("contour Total", contourTotal)
                if childorNext == -1:
                    break
                
                contourTotal += 1
            
            print("contour Total", contourTotal)
            if contourTotal == 3:
                print("centroid point", centroidPoint)
                cv2.putText(savedImageColor, "Robot 2",
        	       centroidPoint, cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2)
            
            contourTotal = 1
        
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
        cv2.imshow('saved image', savedImage)
        cv2.imshow('saved image with color', savedImageColor)

        

    cv2.imshow('img', img)
    cv2.imshow('test', thresh)
    cv2.imshow('img2', img2)
    

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

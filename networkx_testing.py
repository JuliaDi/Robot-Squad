# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 03:22:54 2018

@author: Alex
"""

import networkx as nx
import numpy as np
import cv2
#import cpickle

graph = nx.grid_2d_graph(5, 5)
array = np.zeros(shape=(5,5))
print(array)

value = array[0,0]
print(value)
array[2,4] = 1
print(array)

print(graph.nodes())
print(graph.edges())
print ("\n")
print(graph[0,1])

imgArray = np.zeros(shape = (600,800))

#Creating the graph
G = nx.grid_2d_graph(600, 800)

img = cv2.imread('SampleView.jpg')
imgr = cv2.resize(img, (800, 600)) #y by x

imgray = cv2.cvtColor(imgr, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,240,255,0)

edged = cv2.erode(thresh, None, iterations=1)
edged = cv2.dilate(edged, None, iterations=1)

# =============================================================================
# Mat source = cv2.imread("chessOrange.png",1);
# imshow("source", source);
# Mat mask;
# cv::Scalar lowerb = cv::Scalar(250, 125, 38);
# cv::Scalar upperb = cv::Scalar(255, 129, 42);
# cv::inRange(source, lowerb, upperb, mask);
# 
# imshow("mask", mask);
# =============================================================================

print(edged[250,250])
print(edged.shape)
yimg = edged.shape[0]
ximg = edged.shape[1]
#rows, columns, channel, ie. y, x, columns
saveALocationTestx = 0
saveALocationTesty = 0
isWhite = False
for i in range(0, 599):
    for j in range(0, 799):
        w1 = edged[i, j]
# =============================================================================
#         w2 = edged[i, j]
#         w3 = edged[i, j]
# =============================================================================
        
        if w1 == 255:
            locWhiteX = i
            locWhiteY = j
            saveALocationTestx = i
            saveALocationTesty = j
            imgArray[i,j] = 1
            
# =============================================================================
# print(imgArray)
# 
# G.edges([0,0],[0,1])
# print(G.edges([0,0],[0,1]))
# #print(G.nodes())
# 
# print(list(G.neighbors((0,1))))
# G.add_edge((0,1),(2,2))
# print(list(G.neighbors((0,1))))
# 
# G[0,1][2,2]['cost'] = 1
# print (G[0,1])
# =============================================================================
print(imgArray.shape)
for i in range(0, 599):
    for j in range(0, 799):
        if imgArray[i,j] == 1:
            
            if i < 599:
                if j == 0:
                    G.add_edge((i,j),(i+1,j+1))
                elif j > 0 and j < 799:
                    G.add_edge((i,j),(i+1,j+1))
                    G.add_edge((i,j),(i+1,j-1))
                elif j == 799:
                    G.add_edge((i,j),(i+1,j-1))
                    
# =============================================================================
#             elif i > 0  and i < 599:
#                 if j == 0:
#                     G.add_edge([i,j],[i+1,j+1])
#                     G.add_edge([i,j],[i-1,j+1])
#                 elif j > 0 and j < 799:
#                     G.add_edge([i,j],[i+1,j+1])
#                     G.add_edge([i,j],[i+1,j-1])
#                     G.add_edge([i,j],[i-1,j+1])
#                     G.add_edge([i,j],[i-1,j-1])
#                 elif j == 799:
#                     G.add_edge([i,j],[i+1,j-1]) 
#                     G.add_edge([i,j],[i-1,j-1])
#                     
#             elif i == 599:
#                 if j == 0:
#                     G.add_edge([i,j],[i-1,j+1]) 
#                 elif j > 0 and j < 799:
#                     G.add_edge([i,j],[i-1,j+1])
#                     G.add_edge([i,j],[i-1,j-1])
#                 elif j == 799:
#                     G.add_edge([i,j],[i-1,j-1])
# =============================================================================
                    
            for x in G.neighbors((i,j)):
                G[(i,j)][x]['cost'] = 100
            
#print (G.neighbors([0,1]))

print(G[saveALocationTestx, saveALocationTesty])

cv2.imshow('output', imgr)
cv2.imshow('thresh', thresh)
cv2.imshow('edged',  edged)

cv2.waitKey(0)
cv2.destroyAllWindows()


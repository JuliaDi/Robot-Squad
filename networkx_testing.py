# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 03:22:54 2018

@author: Alex
"""

import networkx as nx
import numpy as np
import cv2
import _pickle as cPickle
import time


def initializeGraph(runCount):
    
   # if runCount == 0:
        
    G = nx.grid_2d_graph(300, 400)
    
    for i in range(0, 299):
        for j in range(0, 399):
            if i < 299:
                if j == 0:
                     G.add_edge((i,j),(i+1,j+1))
                elif j > 0 and j < 399:
                     G.add_edge((i,j),(i+1,j+1))
                     G.add_edge((i,j),(i+1,j-1))
                elif j == 399:
                     G.add_edge((i,j),(i+1,j-1))
                     
# =============================================================================
#                 labels = []
#                 nx.set_edge_attributes(G, labels, 'cost')
# =============================================================================
            
    return G
                     
   # return G
    
# =============================================================================
# graph = nx.grid_2d_graph(5, 5)
# array = np.zeros(shape=(5,5))
# print(array)
# 
# value = array[0,0]
# print(value)
# array[2,4] = 1
# print(array)
# 
# print(graph.nodes())
# print(graph.edges())
# print ("\n")
# print(graph[0,1])
# =============================================================================
cap = cv2.VideoCapture(1)
cap.set(3,800)

cap.set(4,800)
runCount = 0

while True:
    
    start = time.time()
    
    initializeStart = time.time()
    
    
    imgArray = np.zeros(shape = (300,400))

    #Creating the graph
    # =============================================================================
    # inarraystart = time.time()
    # G = nx.grid_2d_graph(600, 800)
    # inarrayend = time.time()
    # print("array ", inarrayend - inarraystart)
    # =============================================================================
    ret, img = cap.read()
    #img = cv2.imread('SampleView.jpg')
    imgr = cv2.resize(img, (400, 300)) #y by x
    
    imgray = cv2.cvtColor(imgr, cv2.COLOR_BGR2GRAY)
    ret,edged = cv2.threshold(imgray,240,255,0)
    
    
    #This is not needed for lower resolutions
# =============================================================================
#     edged = cv2.erode(thresh, None, iterations=1)
#     edged = cv2.dilate(edged, None, iterations=1)
# =============================================================================
    
    if runCount == 0:
        G = initializeGraph(runCount)
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
    
    # =============================================================================
    # print(edged[250,250])
    # print(edged.shape)
    # yimg = edged.shape[0]
    # ximg = edged.shape[1]
    # =============================================================================
    
    
    #rows, columns, channel, ie. y, x, columns
    saveALocationTestx = 0
    saveALocationTesty = 0
    isWhite = False
    
    initializeEnd = time.time()
    print(initializeEnd - initializeStart)
    
    get1start = time.time()
    for i in range(0, 299):
        for j in range(0, 399):
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
                
    get1end = time.time()
    print("getting 1's", get1end - get1start)
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
    # G.add_edge((0,1),(2,2))
    # print("duplicate")
    # print(list(G.neighbors((0,1))))
    # =============================================================================
    if runCount == 0:
        priorValues = []
        
    elif runCount > 0:
        for a in range(0, len(priorValues)):
            i, j = priorValues[a]
            for x in G.neighbors((i,j)):
                    G[(i,j)][x]['cost'] = 1
            
    priorValues = []
     
    nxstart = time.time()
    #print(imgArray.shape)
    for i in range(0, 299):
        for j in range(0, 399):
    # =============================================================================
    #         if i < 599:
    #             if j == 0:
    #                  G.add_edge((i,j),(i+1,j+1))
    #             elif j > 0 and j < 799:
    #                  G.add_edge((i,j),(i+1,j+1))
    #                  G.add_edge((i,j),(i+1,j-1))
    #             elif j == 799:
    #                  G.add_edge((i,j),(i+1,j-1))
    # # =============================================================================
    # #         if i == 0:
    # #             if j == 0:
    # #                 G.add_edge((i,j),(i+1,j+1))
    # #             elif j > 0 and j < 799:
    # #                 G.add_edge((i,j),(i+1,j+1))
    # #                 G.add_edge((i,j),(i+1,j-1))
    # #             elif j == 799:
    # #                 G.add_edge((i,j),(i+1,j-1))
    # #                 
    # #         elif i > 0  and i < 599:
    # #             if j == 0:
    # #                 G.add_edge((i,j),(i+1,j+1))
    # #                 G.add_edge((i,j),(i-1,j+1))
    # #             elif j > 0 and j < 799:
    # #                 G.add_edge((i,j),(i+1,j+1))
    # #                 G.add_edge((i,j),(i+1,j-1))
    # #                 G.add_edge((i,j),(i-1,j+1))
    # #                 G.add_edge((i,j),(i-1,j-1))
    # #             elif j == 799:
    # #                 G.add_edge((i,j),(i+1,j-1))
    # #                 G.add_edge((i,j),(i-1,j-1))
    # #                 
    # #         elif i == 599:
    # #             if j == 0:
    # #                 G.add_edge((i,j),(i-1,j+1)) 
    # #             elif j > 0 and j < 799:
    # #                 G.add_edge((i,j),(i-1,j+1))
    # #                 G.add_edge((i,j),(i-1,j-1))
    # #             elif j == 799:
    # #                 G.add_edge((i,j),(i-1,j-1))
    # # =============================================================================
    #                 
    # # =============================================================================
    # #         for x in G.neighbors((i,j)):
    # #             G[(i,j)][x]['cost']
    # # =============================================================================
    #             
    #         labels = []
    #         nx.set_edge_attributes(G, labels, 'cost')
    #         
    # =============================================================================
            if imgArray[i,j] == 1:
    # =============================================================================
    #             
    #             if i == 0:
    #                 if j == 0:
    #                     G.add_edge((i,j),(i+1,j+1))
    #                 elif j > 0 and j < 799:
    #                     G.add_edge((i,j),(i+1,j+1))
    #                     G.add_edge((i,j),(i+1,j-1))
    #                 elif j == 799:
    #                     G.add_edge((i,j),(i+1,j-1))
    #                     
    #             elif i > 0  and i < 599:
    #                 if j == 0:
    #                     G.add_edge((i,j),(i+1,j+1))
    #                     G.add_edge((i,j),(i-1,j+1))
    #                 elif j > 0 and j < 799:
    #                     G.add_edge((i,j),(i+1,j+1))
    #                     G.add_edge((i,j),(i+1,j-1))
    #                     G.add_edge((i,j),(i-1,j+1))
    #                     G.add_edge((i,j),(i-1,j-1))
    #                 elif j == 799:
    #                     G.add_edge((i,j),(i+1,j-1))
    #                     G.add_edge((i,j),(i-1,j-1))
    #                     
    #             elif i == 599:
    #                 if j == 0:
    #                     G.add_edge((i,j),(i-1,j+1)) 
    #                 elif j > 0 and j < 799:
    #                     G.add_edge((i,j),(i-1,j+1))
    #                     G.add_edge((i,j),(i-1,j-1))
    #                 elif j == 799:
    #                     G.add_edge((i,j),(i-1,j-1))
    # =============================================================================
                        
                for x in G.neighbors((i,j)):
                    G[(i,j)][x]['cost'] = 100000
                
                priorValues.append((i,j))
                    
    # =============================================================================
    #         elif imgArray[i,j] == 0:
    #             
    # # =============================================================================
    # #             if i < 599:
    # #                 if j == 0:
    # #                     G.add_edge((i,j),(i+1,j+1))
    # #                 elif j > 0 and j < 799:
    # #                     G.add_edge((i,j),(i+1,j+1))
    # #                     G.add_edge((i,j),(i+1,j-1))
    # #                 elif j == 799:
    # #                     G.add_edge((i,j),(i+1,j-1))
    # # =============================================================================
    #                     
    #             for x in G.neighbors((i,j)):
    #                 
    #                 if G[(i,j)][x]['cost'] == 100:
    #                     continue
    #                 
    #                 G[(i,j)][x]['cost'] = 0
    # =============================================================================
    
        
    
    #print(priorValues)
    nxend = time.time()
    print("nx ", nxend - nxstart)
    #print (G.neighbors([0,1]))
    
    print("should be 0", G[0,0])
    print(G[102,89])
    print(G[101,88])
    print(G[saveALocationTestx, saveALocationTesty])
    
    
  #  cv2.imshow('output', imgr)
 #   cv2.imshow('thresh', thresh)
    cv2.imshow('edged',  edged)
    end = time.time()
    
    print(end - start)
    
    runCount += 1
    
    print("test")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("ok")
        break

# =============================================================================
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# =============================================================================
print()

cv2.destroyAllWindows()
cap.release()


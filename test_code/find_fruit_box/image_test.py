from typing import Counter
import cv2
import numpy as np
import ipdb
import queue
import statistics
import matplotlib.pyplot as plt
import os
import traceback  

    
# (hMin = 10 , sMin = 101, vMin = 112), (hMax = 29 , sMax = 182, vMax = 193)

if __name__ == '__main__':
    
    while True:
        
        image=cv2.imread('example242.jpg',cv2.IMREAD_COLOR)
        image_copy=image.copy()
        hsv=cv2.cvtColor(image_copy,cv2.COLOR_BGR2HSV)
        
        lower_mask = np.array([0,194,69]) 
        upper_mask = np.array([26,255,176]) 
        
        mask=cv2.inRange(hsv,lower_mask,upper_mask)
        
        canny=cv2.Canny(mask,100,200)
        minLineLength=50
        maxLineGap=10
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 60, minLineLength=minLineLength, maxLineGap=maxLineGap)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow("line_detect_possible_demo",image_copy)
    
        
        # cv2.imshow('image',image)
        # cv2.imshow('mask',mask)
        # cv2.imshow('canny',canny)

        
        if cv2.waitKey(0):
            break
    
    
    
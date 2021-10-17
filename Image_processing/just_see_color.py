import cv2
import numpy as np
from utilities import *
import matplotlib.pyplot as plt
import ipdb 

mask_window=True
Canny_window=False
Circle_window=True

if mask_window:
    cv2.namedWindow("mask",0)
    cv2.resizeWindow("mask", 960, 480)
    cv2.moveWindow("mask",10,100)

if Canny_window:
    cv2.namedWindow("Canny",0)
    cv2.resizeWindow("Canny", 960, 500)
    cv2.moveWindow("Canny",1300,100)

if Circle_window:
    cv2.namedWindow("Circle",0)
    cv2.resizeWindow("Circle", 960, 500)
    cv2.moveWindow("Circle",1300,100)

cap = cv2.VideoCapture('testdata/tomato_video1.mp4')
# ipdb.set_trace()
if not cap.isOpened():
    print("Cannot open camera")
    exit()

#cv2.namedWindow("live", cv2.WINDOW_AUTOSIZE); # 命名一個視窗，可不寫
while(True):
    # 擷取影像
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    
    hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV) #將BGR轉換為HSV 
    #HSV中的顏色強度參數
    weaker_red = np.array([0,76,157]) 
    strong_red = np.array([179,199,255])
    mask_red = cv2.inRange(hsv,weaker_red,strong_red) #Threshold HSV圖像獲取輸入顏色
    z_array=np.zeros((len(mask_red),len(mask_red[0])))
    mask_red_3d=np.stack((z_array.copy(),z_array.copy(),mask_red.copy()),2)

    weaker_green = np.array([39,55,48]) 
    strong_green = np.array([73,193,179])
    mask_green = cv2.inRange(hsv,weaker_green,strong_green) #Threshold HSV圖像獲取輸入顏色
    z_array=np.zeros((len(mask_green),len(mask_green[0])))
    mask_green_3d=np.stack((z_array.copy(),mask_green.copy(),z_array.copy()),2)

    weaker_black = np.array([4,26,1]) 
    strong_black = np.array([153,139,100])
    mask_black = cv2.inRange(hsv,weaker_black,strong_black) #Threshold HSV圖像獲取輸入顏色
    z_array=np.zeros((len(mask_black),len(mask_black[0])))
    mask_black_3d=np.stack((mask_black.copy(),z_array.copy(),z_array.copy()),2)

    # canny
    if Canny_window:
        canny_origin=canny_picture(frame,display=False)
        canny_mask_red=cv2.Canny(mask_red,30,150)
        canny_mask_green=cv2.Canny(mask_green,30,150)
        canny_mask_black=cv2.Canny(mask_black,30,150)
   

    
    # circle
    if Circle_window:
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame_circles= cv2.HoughCircles(gray.copy(),cv2.HOUGH_GRADIENT,1,100,param1=100,param2=30,minRadius=5,maxRadius=300)
        frame_circles_image=frame.copy()
        try:
            for circle in frame_circles[0]:#根據檢測到圓的資訊，畫出每一個圓
                x=int(circle[0])#座標行列
                y=int(circle[1])
                r=int(circle[2]) #半徑
                frame_circles_image=cv2.circle(frame.copy(),(x,y),r,(0,0,255),-1)#在原圖用指定顏色標記出圓的位置
        except:
            pass


        red_circles= cv2.HoughCircles(mask_red.copy(),cv2.HOUGH_GRADIENT,1,100,param1=100,param2=30,minRadius=5,maxRadius=300)
        red_circles_image=np.stack((mask_red.copy(),mask_red.copy(),mask_red.copy()),2)
        try:
            for circle in red_circles[0]:#根據檢測到圓的資訊，畫出每一個圓
                x=int(circle[0])#座標行列
                y=int(circle[1])
                r=int(circle[2]) #半徑
                red_circles_image=cv2.circle(red_circles_image.copy(),(x,y),r,(0,0,255),-1)#在原圖用指定顏色標記出圓的位置
        except:
            pass

        green_circles= cv2.HoughCircles(mask_green.copy(),cv2.HOUGH_GRADIENT,1,100,param1=100,param2=30,minRadius=5,maxRadius=300)
        green_circles_image=np.stack((mask_green.copy(),mask_green.copy(),mask_green.copy()),2)
        try:
            for circle in green_circles[0]:#根據檢測到圓的資訊，畫出每一個圓
                x=int(circle[0])#座標行列
                y=int(circle[1])
                r=int(circle[2]) #半徑
                green_circles_image=cv2.circle(green_circles_image.copy(),(x,y),r,(0,0,255),-1)#在原圖用指定顏色標記出圓的位置
        except:
            pass


        black_circles= cv2.HoughCircles(mask_black.copy(),cv2.HOUGH_GRADIENT,1,100,param1=100,param2=30,minRadius=5,maxRadius=300)
        black_circles_image=np.stack((mask_black.copy(),mask_black.copy(),mask_black.copy()),2)
        try:
            for circle in black_circles[0]:#根據檢測到圓的資訊，畫出每一個圓
                x=int(circle[0])#座標行列
                y=int(circle[1])
                r=int(circle[2]) #半徑
                black_circles_image=cv2.circle(black_circles_image.copy(),(x,y),r,(0,0,255),-1)#在原圖用指定顏色標記出圓的位置
        except:
            pass

    # ipdb.set_trace()
    #組合圖片
    if mask_window:
        mask_1=np.hstack((frame.copy()/225.,mask_red_3d,mask_green_3d,mask_black_3d))
    if Canny_window:
        canny_mask=np.hstack((canny_picture(frame,display=False),cv2.Canny(mask_red,30,150),cv2.Canny(mask_green,30,150),cv2.Canny(mask_black,30,150)))
    if Circle_window:
        circles_1=np.hstack((frame_circles_image,red_circles_image,green_circles_image,black_circles_image))

    # 顯示圖片
    try:
        if mask_window:
            cv2.imshow('mask', mask_1)

        if Canny_window:
            cv2.imshow('Canny',canny_mask)

        if Circle_window:
            cv2.imshow('Circle',circles_1)
    except:
        pass
    # cv2.imshow('live', mask_1)

    #註這邊可以插其他code


    # 按下 q 鍵離開迴圈
    if cv2.waitKey(1) == ord('q'):
        break

# 釋放該攝影機裝置
cap.release()
cv2.destroyAllWindows()
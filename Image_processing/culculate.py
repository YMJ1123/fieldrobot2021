import cv2
import numpy as np
from utilities import *
import matplotlib.pyplot as plt
import ipdb 

img_path = 'testdata/tomato1.png'
image  = cv2.imread(img_path)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #將BGR轉換為HSV 
#HSV中的顏色強度參數
weaker = np.array([0,76,157]) 
strong = np.array([179,199,255])
mask = cv2.inRange(hsv,weaker,strong) #Threshold HSV圖像獲取輸入顏色

step=5

large_weaker = weaker-np.array([step*10,step*10,step*10])
large_strong =  strong+np.array([step*10,step*10,step*10])

progress=False
if progress:

    for i in range(0,12):
        temp_weaker = large_weaker+np.array([step*i,step*i,step*i])
        temp_strong =  large_strong-np.array([step*i,step*i,step*i])
        mask = cv2.inRange(hsv, temp_weaker, temp_strong) #Threshold HSV圖像獲取輸入顏色
        displayIMG(mask)

        # if #TODO FIND_FRUIT==True:
        #     break

#輪廓識別
gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur=cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 50, 100)
displayIMG(edged,"edged")
dilate= cv2.dilate(edged, None, iterations=1)
# displayIMG(dilate,"dilate")
erode= cv2.erode(dilate, None, iterations=1)
# displayIMG(erode,"erode")
contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
final_contours = []

connect = cv2.morphologyEx(edged,cv2.MORPH_CLOSE,kernel=(3,3),iterations=3)# 使用閉運算連接中斷的圖像前景,迭代運算三次
displayIMG(connect,'connect')


for contour in contours:
    area = cv2.contourArea(contour)
    if area > 2000:
        final_contours.append(contour)
#  final_contours=>>list[numpy.ndarray(376, 1, 2)][numpy.ndarray(1898, 1, 2)]

for i in range(len(final_contours)):
    img_contours = cv2.drawContours(image.copy(), final_contours, i, (50, 250, 50), 2)

displayIMG(img_contours)




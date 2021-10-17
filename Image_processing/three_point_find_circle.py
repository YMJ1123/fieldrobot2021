import numpy as np
import cv2
from utilities import *
import random
import ipdb

image=cv2.imread('testdata/tomato1.png')
edged=canny_picture(image,1,display=False)
# displayIMG(edged)

coord_set=[]

#canny除存成座標
for x in range(len(edged[0])):
    for y in range(len(edged)):
        if edged[y][x]==255:
            coord_set.append((y,x))
    
image_copy=image.copy()
edged_3d=np.stack((edged.copy(),edged.copy(),edged.copy()),2)

for times in range(0,30000):
    #任選三點找外心

    i = random.sample(range(0,len(coord_set)),3)
    # print(i)
    x0,y0,R=getCircle(coord_set[i[0]],coord_set[i[1]],coord_set[i[2]])

    # print(f'x0={x0},y0={y0},R={R}')


    

    # 畫點

    point_size = 1
    point_color =(0,0,255) # BGR
    thickness = 4# 可以為0,4,8
    points_list = [coord_set[i[0]],coord_set[i[1]],coord_set[i[2]]]
    for point in points_list:
        pass
        # print(point)
        # cv2.circle(image_copy,(point[1],point[0]),point_size,point_color,thickness) 
        # cv2.circle(edged_3d,(point[1],point[0]),point_size,point_color,thickness) 

    if x0>0 and y0>0 and x0<len(image[0]) and y0<len(image):
        # ipdb.set_trace()
        cv2.circle(image_copy,(int(x0),int(y0)),point_size,(0,255,0),0)
        cv2.circle(edged_3d,(int(x0),int(y0)),point_size,(0,255,0),0)

    else:
        # print('out of range')
        pass

# edged=canny_picture(image.copy(),display=False)
# edged_3d=np.stack((edged.copy(),edged.copy(),edged.copy()),2)
# output=np.hstack((image_copy,edged_3d))
# print(edged_3d.shape)#(725, 559, 3)

cv2.namedWindow('image')
cv2.namedWindow('canny')
cv2.imshow('image',image_copy)
cv2.imshow('canny',edged_3d)

cv2.waitKey(0)
cv2.destroyAllWindows()

# displayIMG(output)
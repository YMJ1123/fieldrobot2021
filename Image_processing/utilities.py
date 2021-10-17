import cv2
import numpy as np
import sys

from numpy.lib.function_base import disp



def find_range(img):

    def nothing(x):
        pass

    # Create a window
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)

    # create trackbars for color change
    cv2.createTrackbar('HMin','image',0,179,nothing) # Hue is from 0-179 for Opencv
    cv2.createTrackbar('SMin','image',0,255,nothing)
    cv2.createTrackbar('VMin','image',0,255,nothing)
    cv2.createTrackbar('HMax','image',0,179,nothing)
    cv2.createTrackbar('SMax','image',0,255,nothing)
    cv2.createTrackbar('VMax','image',0,255,nothing)

    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos('HMax', 'image', 179)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 255)

    # Initialize to check if HSV min/max value changes
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0

    #input_img = cv2.imread(img)
    output = img
    waitTime = 33

    while(1):

        # get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin','image')
        sMin = cv2.getTrackbarPos('SMin','image')
        vMin = cv2.getTrackbarPos('VMin','image')

        hMax = cv2.getTrackbarPos('HMax','image')
        sMax = cv2.getTrackbarPos('SMax','image')
        vMax = cv2.getTrackbarPos('VMax','image')

        # Set minimum and max HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(img,img, mask= mask)

        # Print if there is a change in HSV value
        if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax

        # Display output image
        cv2.imshow('image',output)
        
        # Wait longer to prevent freeze for videos.
        if cv2.waitKey(waitTime) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def filter_color(frame,color):
    # Image scaling
    scale_percent = 60  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    original = frame.copy()

    # Convert Color range BGR --> RGB --> HSV
    path = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    path = cv2.cvtColor(path, cv2.COLOR_RGB2HSV)

    # Color filtering
    # HSV ranges (0,76,0) to (20,255,255) (use range_finder.py)
    if color == "green":
        lower = np.array([30, 35, 0])
        upper = np.array([53, 255, 255])
    elif color == "white":
        lower = np.array([0,0,241])
        upper = np.array([179,4,255])

    mask = cv2.inRange(path, lower, upper)

    if color == "green":
        # Morphological Closing
        close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        erosion_kernel = np.ones((5,5),np.uint8)
        close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel, iterations=1)
        erosion = cv2.erode(close,erosion_kernel,iterations = 1)
        dilation = cv2.dilate(erosion,erosion_kernel,iterations = 1)
        mask = dilation
    #mask = cv2.fillPoly(dilation, np.array([[(0,0),(0,600),(200,0)]],dtype=np.int32), 0)
    #mask = cv2.fillPoly(mask, np.array([[(1152,0),(952,0),(1152,600)]],dtype=np.int32),0)

    return mask, original

def find_lane(close,frame,X_MID):
    x_delta = 0
    contours, hierarchy = cv2.findContours(close, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if contours:    
        contours = sorted(contours,key=cv2.contourArea,reverse=True)[0]
        hull = cv2.convexHull(contours)
        epsilon = 0.05*cv2.arcLength(hull,True)
        approx = cv2.approxPolyDP(hull,epsilon,True)

        pt_list = approx.tolist()
        pt_list.append(pt_list[0])
        slope_list = []
        
        for i in range(len(pt_list)-1):
            point1 = pt_list[i][0]
            point2 = pt_list[i+1][0]
            if (point1[0]-point2[0]) is not 0:
                slope = (point1[1]-point2[1])/(point1[0]-point2[0])
            else:
                slope = 0
            slope_list.append(slope)
        print(slope_list)
        
        min = np.argmin(np.asarray(slope_list))
        max = np.argmax(np.asarray(slope_list))
        if min == 3:
            min = (3,0)
        else:
            min = (min,min+1)
        if max == 3:
            max = (3,0)
        else:
            max = (max,max+1)
        print(min,max)
        
        if len(approx) == 4:    
            cv2.line(frame,tuple(approx[min[0]][0]),tuple(approx[min[1]][0]),(0,0,255),2)
            cv2.line(frame,tuple(approx[max[0]][0]),tuple(approx[max[1]][0]),(0,0,255),2)
        
            lineA = [approx[min[0]][0],approx[min[1]][0]]
            lineB = [approx[max[0]][0],approx[max[1]][0]]
            if lineA[1][1]>lineA[0][1]:
                temp = lineA[0]
                lineA[0] = lineA[1]
                lineA[1] = temp
            if lineB[1][1]>lineB[0][1]:
                temp = lineB[0]
                lineB[0] = lineB[1]
                lineB[1] = temp
            MID_LINE = [((lineA[0][0]+lineB[0][0])/2,(lineA[0][1]+lineB[0][1])/2),((lineA[1][0]+lineB[1][0])/2,(lineA[1][1]+lineB[1][1])/2)]
            MID_LINE = tuple(tuple(map(int, tup)) for tup in MID_LINE) 
            cv2.line(frame,MID_LINE[0],MID_LINE[1],(0,0,255),2)
            #x_delta = MID_LINE[0][0]-MID_LINE[1][0]
            x_delta = MID_LINE[0][0]- X_MID
             
            cv2.circle(frame,MID_LINE[0], 2, (0,255,0), -1)
            cv2.circle(frame,MID_LINE[1], 2, (0,255,0), -1)
            cv2.putText(frame,str(MID_LINE[0][0])+" , "+str(MID_LINE[0][1]),MID_LINE[0], cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(frame,str(MID_LINE[1][0])+" , "+str(MID_LINE[1][1]),tuple(np.add(MID_LINE[1],(0,50))), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,255,155), 2, cv2.LINE_AA)
    
    return frame, x_delta 

def displayIMG(img, windowName="none"):
    cv2.namedWindow( windowName, cv2.WINDOW_NORMAL )
    cv2.resizeWindow(windowName, 1000, 800)
    cv2.imshow(windowName, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def canny_webcam():
    "Live capture frames from webcam and show the canny edge image of the captured frames."

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()  # ret gets a boolean value. True if reading is successful (I think). frame is an
        # uint8 numpy.ndarray

        frame = cv2.GaussianBlur(frame, (7, 7), 1.41)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        edge = cv2.Canny(frame, 25, 75)

        cv2.imshow('Canny Edge', edge)

        if cv2.waitKey(20) == ord('q'):  # Introduce 20 milisecond delay. press q to exit.
            break

def canny_picture(image,ksize=7,threshold_max=150,threshold_min=60,display=True):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(image, (ksize, ksize), 0)
    if display:
        displayIMG(blurred, "Blurred")
    canny = cv2.Canny(blurred, threshold_min, threshold_max)
    if display:
        displayIMG(canny, "Canny")
    
    return canny

def print_attribute(img):
    print("type {}".format(type(img)))
    print(img.shape)
    print("width: {} pixels".format(img.shape[1]))
    print("height: {} pixels".format(img.shape[0]))
    print("channel: {}".format(img.shape[2]))
    print("size: {}".format(img.size))
    print("datatype: {}".format(img.dtype))

def auto_canny(image, sigma=0.33):
    
    # 灰度化處理
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 進行高斯模糊去噪
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
	# 計算單通道像素強度的中位數
    v = np.median(blurred)

	# 選擇合適的lower和upper值，然後應用它們
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    return edged


# 用滑動條來簡化canny閾值參數調節
def find_canny(image):
    
    cv2.namedWindow("Canny",cv2.WINDOW_NORMAL)#设置窗口
    cv2.namedWindow("blur",cv2.WINDOW_NORMAL)#设置窗口
    cv2.namedWindow("original",cv2.WINDOW_NORMAL)#设置窗口
    


    def nothing(x):#定义回调函数
        pass
    #创建两个滑动条，分别控制threshold1，threshold2
    cv2.createTrackbar("blurr","Canny",0,25,nothing) #200
    cv2.createTrackbar("threshold1","Canny",0,200,nothing) #200
    cv2.createTrackbar("threshold2","Canny",200,1500,nothing)#1000

    cv2.setTrackbarPos("blurr","Canny",1)
    cv2.setTrackbarPos("threshold1","Canny",50)
    cv2.setTrackbarPos("threshold2","Canny",200)

    while(1):
    #返回滑动条所在位置的值
        blurr=cv2.getTrackbarPos("blurr","Canny")
        threshold1=cv2.getTrackbarPos("threshold1","Canny")
        threshold2=cv2.getTrackbarPos("threshold2","Canny")
        #Canny边缘检测
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (blurr*2+1, blurr*2+1), 0)
        img_edges=cv2.Canny(blurred,threshold1,threshold2)
        #显示图片
        cv2.resizeWindow("original", 640, 480)
        cv2.resizeWindow("blur", 640, 480)
        cv2.resizeWindow("Canny", 640, 480)
        cv2.imshow("original",image)
        cv2.imshow("blur",blurred)
        cv2.imshow("Canny",img_edges)
        if cv2.waitKey(1)==ord("q"):
            break

    cv2.destroyAllWindows()
    return

def getCircle(p1,p2,p3,isRound=True):
 

    try:
        x1=p1[1]
        x2=p2[1]
        x3=p3[1]
        y1=p1[0]
        y2=p2[0]
        y3=p3[0]
        if ((x2-x1)*(y3-y2)-(x3-x2)*(y2-y1)==0):
            return(-1,-1,-1)
        x0=((y2-y1)*(y3*y3-y1*y1+x3*x3-x1*x1)-(y3-y1)*(y2*y2-y1*y1+x2*x2-x1*x1))/(2.0*((x3-x1)*(y2-y1)-(x2-x1)*(y3-y1)))
        y0=((x2-x1)*(x3*x3-x1*x1+y3*y3-y1*y1)-(x3-x1)*(x2*x2-x1*x1+y2*y2-y1*y1))/(2.0*((y3-y1)*(x2-x1)-(y2-y1)*(x3-x1)))
        # R=(x1-x0)*(x1-x0+(y1-y0)*(y1-y0))
        R=((x1-x0)**2+(y1-y0)**2)**0.5
        if isRound:
            x0=round(x0,0)
            y0=round(y0,0)
            R=round(R,0)
        return x0,y0,R
    except:
        return(-1,-1,-1)
    

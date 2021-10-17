

import cv2
import os
from os import getcwd
import numpy as np
import ipdb
import random





#使用opencv加載Darknet模型

def readlabel2txt(path=""):
    weightsPath = path+'custom-yolov4-tiny-detector_best.weights'
    configPath = path+'cfg/custom-yolov4-tiny-detector.cfg'
    labelsPath = path+'cfg/obj.names'
    colors=[]
    label2txt = []
    f = open(labelsPath, 'r')
    for line in f.readlines():
        line=line.strip('\n')
        label2txt.append(line)
        if line=="avocado":
            colors.append((11,23,70))
        elif line=="carrot":
            colors.append((199,97,20))
        elif line =="lemon":
            colors.append((34,139,34))
        elif line =="tomato":
            colors.append((0,0,255))
        else:
            colors.append((random.randrange(255),random.randrange(255),random.randrange(255)))
    f.close()
    return label2txt,colors
    

#下麵是通過檢測獲取坐標的函數
def coordinate_get(img):
    
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    
    coordinates_list=[] # 創建坐標列表
    boxes = []
    confidences = []
    classIDs = []
    (H, W) = img.shape[:2]
    # 得到 YOLO需要的輸出層
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # 從輸入圖像構造一個blob，然後通過加載的模型，給我們提供邊界框和相關概率
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)
    # ipdb.set_trace()

    # 在每層輸出上循環
    for output in layerOutputs:
        # 對每個檢測進行循環
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            # 過濾掉那些置信度較小的檢測結果
            if confidence > 0.01:
                # 框後接框的寬度和高度
                box = detection[0:4]  * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                # 邊框的左上角
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                # 更新檢測出來的框
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID) 

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.3)
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            xmin = int(x)
            ymin = int(y)
            xmax = int(x + w)
            ymax = int(y + h)
            coordinates_list.append([[xmin,ymin,xmax,ymax],classIDs[i],confidences[i]])

    return coordinates_list

def draw_boxes(detections, image, colors,label2txt):
    import cv2
    for bbox,label, confidence in detections:
        # left, top, right, bottom = bbox2points(bbox)
        left, top, right, bottom = bbox
        # ipdb.set_trace()
        cv2.rectangle(image, (left, top), (right, bottom), colors[label], 1)
        cv2.putText(image, "{} [{:.2f}]".format(label2txt[label], float(confidence)),
                    (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    colors[label], 2)
    return image



if __name__ == '__main__':
    
    #此處設置相關的文件路徑
    weightsPath = 'custom-yolov4-tiny-detector_best.weights'
    configPath = 'cfg/custom-yolov4-tiny-detector.cfg'
    labelsPath = 'cfg/obj.names'
    
    # label2txt = ["avocado","carrot","lemon","tomato"]
    # avocado carrot lemon tomato
    # colors =[(11,23,70),(199,97,20),(34,139,34),(0,0,255)]
    colors=[]
    label2txt = []
    f = open(labelsPath, 'r')
    for line in f.readlines():
        line=line.strip('\n')
        label2txt.append(line)
        if line=="avocado":
            colors.append((11,23,70))
        elif line=="carrot":
            colors.append((199,97,20))
        elif line =="lemon":
            colors.append((34,139,34))
        elif line =="tomato":
            colors.append((0,0,255))
        else:
            colors.append((random.randrange(255),random.randrange(255),random.randrange(255)))
    f.close()
    
    # ipdb.set_trace()
    
    
     # Video Stream
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
    # Get current frame, quit if no frame 

        ret, frame = cap.read()

        if not ret: break
        
        image=frame
        # image = cv2.resize(frame,(416,416))
        # coordinates_list = [[xmin,ymin,xmax,ymax],classIDs,confidences],[[xmin,ymin,xmax,ymax],classIDs,confidences],[...]...
        #座標可以用在控制，不幸的是，圖片一定要變成416*416才可以用(後來發現好像不用)
        coordinates_list = coordinate_get(image)
        
        frame_draw=image.copy()
        
        # 畫框框
        draw_boxes(coordinates_list, frame_draw, colors,label2txt)
                
        cv2.imshow('live', frame_draw)
        

        # za warudo
        if cv2.waitKey(1) == ord('c'):
            ipdb.set_trace()
            
        # exit
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()
    

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Counter
import cv2
import numpy as np
from tools import *
import ipdb

# img_path = 'testpic.jpg'
# image  = cv2.imread(img_path)
# find_range(image)

if __name__ == '__main__':
    
    cap = cv2.VideoCapture(0)
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

        # 顯示圖片
        cv2.imshow('live', frame)

        #註這邊可以插其他code

        # 按c拍個照嘻嘻
        if cv2.waitKey(1) == ord('c'):
            find_range(frame)
            break

        # 按下 q 鍵離開迴圈
        if cv2.waitKey(1) == ord('q'):
            break

    # 釋放該攝影機裝置
    cap.release()
    cv2.destroyAllWindows()
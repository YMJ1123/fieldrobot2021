
import cv2
import ipdb
from ipdb.__main__ import set_trace
import numpy
import serial  # 引用pySerial模組
import time
import sys
import statistics
import os

from serial.serialwin32 import Serial
from tools import *



# step=1 開始循線
# step=2 看到水果，調車的前後位置
# step=3 調夾爪位置
# step=4 夾爪合起來
# step=5 循線直走
# step=6 看到箱子，調前後
# step=7 夾爪鬆開
# step=8 直走直到檔板


import x64.use_def_return_coord as use_darknet

isconfidence=0.8 #設定看到多少的信心算是有看到

if __name__=='__main__':
    
    step=1
    prefix_path='x64/'
    
    # step1 會用到的變數
    # smooth 變數
    coord_smooth_list=[]
    # mostlikely_smooth=None
    mostlikely_smooth=2
    smooth_num=3
    
    # step2會用到的變數
    nofruit=0

    # 讀取標籤
    label2txt,colors=use_darknet.readlabel2txt(path=prefix_path)
    
    # pyserial 連線
    COM_PORT = 'COM4'    # 指定通訊埠名稱
    BAUD_RATES = 38400    # 設定傳輸速率
    locations=['COM0','COM1','COM2','COM3','COM4','COM5','COM6']
    # location=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3','/dev/ttyS0','/dev/ttyS1','/dev/ttyS2','/dev/ttyS3'] #linux
    ser = serial.Serial(COM_PORT, BAUD_RATES)
    
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
    except:
        print(f"Failed to connect on {COM_PORT}")
        for device in locations:
            try:
                ser=serial.Serial(device,BAUD_RATES)
            except:
                print(f"Failed to connect on {device}")
    
   
    
    # video stream
    cap=cv2.VideoCapture(1)
    
   
    while(cap.isOpened()):
        
        # 讀取frame
        ret, frame = cap.read()
        if not ret: break
        
        w=frame.shape[1]
        h=frame.shape[0]
        frame_draw=frame.copy()
        # 分流開始
        if step==1:
            # 跟arduino說現在是step幾
            try:
                b='0000000'
                success_bytes=ser.write(b.encode(encoding='UTF-8'))
                time.sleep(1)
                print(success_bytes)
            except KeyboardInterrupt:
                ser.close()    # 清除序列通訊物件
                print('Failed to send')
                
            print('in step 1')
            
            # 執行循線code，同時camera偵測(同時分開進行)
            coordinates_list=use_darknet.return_coord(frame,path=prefix_path)
            
        
            
            
            # YOLO 是否偵測到水果
            isfruit=False
            mostlikely=None
            theconfidence=0 #信心
            coord=[0,0,0,0] #儲存的座標 [xmin,ymin,xmax,ymax]
            for coordinate_set in coordinates_list:
                if coordinate_set[2]>isconfidence and coordinate_set[2]>theconfidence:
                    theconfidence=coordinate_set[2]
                    coord=coordinate_set[0]
                    mostlikely=coordinate_set[1]
                    
            #  感覺要smooth數據, e.g.10筆
            if len(coord_smooth_list)==0:
                coord_smooth_list.append(coord)
                mostlikely_smooth=mostlikely
            elif len(coord_smooth_list)==smooth_num:
                isfruit=True #集滿
            elif mostlikely!=mostlikely_smooth:
                coord_smooth_list=[] #砍掉重練
            else:
                coord_smooth_list.append(coord)
            # ipdb.set_trace()    
            if mostlikely!=None:
                use_darknet.draw_boxes([[coord,mostlikely,theconfidence]], frame_draw, colors,label2txt)      
            cv2.imshow('live', frame_draw)
            
            if isfruit:
                # carrot tomato lemon avocado
                if mostlikely==0:
                    # carrot
                    try:
                        b='0000001'
                        success_bytes=ser.write(b.encode(encoding='UTF-8'))
                        time.sleep(1)
                        print(success_bytes)
                        print('carrot')
                    except KeyboardInterrupt:
                        ser.close()    # 清除序列通訊物件
                        print('Failed to send')
                elif mostlikely==1:
                    # tomato 
                    try:
                        b='0000010'
                        success_bytes=ser.write(b.encode(encoding='UTF-8'))
                        time.sleep(1)
                        print(success_bytes)
                        print('tomato')
                    except KeyboardInterrupt:
                        ser.close()    # 清除序列通訊物件
                        print('Failed to send')
                elif mostlikely==2:
                    # lemon
                    try:
                        b='0000011'
                        success_bytes=ser.write(b.encode(encoding='UTF-8'))
                        time.sleep(1)
                        print(success_bytes)
                        print('lemon')
                    except KeyboardInterrupt:
                        ser.close()    # 清除序列通訊物件
                        print('Failed to send')
                    
                elif mostlikely==3:
                    # avocado
                    try:
                        b='0000100'
                        success_bytes=ser.write(b.encode(encoding='UTF-8'))
                        time.sleep(1)
                        print(success_bytes)
                        print('avocado')
                    except KeyboardInterrupt:
                        ser.close()    # 清除序列通訊物件
                        print('Failed to send')
                        
                mean_coord=[0,0,0,0] #[xmin,ymin,xmax,ymax]
                for coords in coord_smooth_list:
                    mean_coord[0]+=coords[0]
                    mean_coord[1]+=coords[1]
                    mean_coord[2]+=coords[2]
                    mean_coord[3]+=coords[3]
                for coord_sum in mean_coord:
                    coord_sum = coord_sum/smooth_num
                   
                # 畫框框
                use_darknet.draw_boxes([[mean_coord,mostlikely,theconfidence]], frame_draw, colors,label2txt)   
                cv2.putText(frame_draw, 'smoothed', (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 1, cv2.LINE_AA)
                print('smoothed')
                cv2.imshow('live', frame_draw)
                
                # ipdb.set_trace()

                step=2
                print('go to step 2')
                #停車
                pass
                
            pass
        
        elif step ==2:
            print('in step 2')
            # 跟arduino說現在是step幾
            try:
                b='0010000'
                success_bytes=ser.write(b.encode(encoding='UTF-8'))
                time.sleep(1)
                print(success_bytes)
            except KeyboardInterrupt:
                ser.close()    # 清除序列通訊物件
                print('Failed to send')
                
            # 檢查圖片，叫車移動
            coordinates_list=use_darknet.return_coord(frame,path=prefix_path) #取得座標
            isfruit=False
            mostlikely=None
            theconfidence=0 #信心
            coord=[0,0,0,0] #儲存的座標 [xmin,ymin,xmax,ymax]
            for coordinate_set in coordinates_list: # 取信心最大
                if coordinate_set[2]>isconfidence and coordinate_set[2]>theconfidence:
                    theconfidence=coordinate_set[2]
                    coord=coordinate_set[0]
                    mostlikely=coordinate_set[1]
            
            use_darknet.draw_boxes([[coord,mostlikely,theconfidence]], frame_draw, colors,label2txt)   
            cv2.putText(frame_draw, 'smoothed', (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 1, cv2.LINE_AA)
            print('smoothed')
            cv2.imshow('live', frame_draw)
            
            if mostlikely==None:#沒偵測到水果
                nofruit+=1
                continue
            elif coord[0]==coord[2] or coord[1]==coord[3]:
                nofruit+=1
                continue
            else:
                nofruit=0
            
            print(coord)
            
            errpix=30 #可容許的對位誤差
            inmiddle=False
            
            if abs((coord[0]+coord[2])/2-w/2)<errpix: #這樣算是有對齊
                inmiddle=True
            elif (coord[0]+coord[2])/2<w/2: #水果在畫面左邊(可以再往前)
                #告訴Arduino要再往前
                print('keep go forward')
                try:
                    b='0010010'
                    success_bytes=ser.write(b.encode(encoding='UTF-8'))
                    time.sleep(1)
                    print(success_bytes)
                except KeyboardInterrupt:
                    ser.close()    # 清除序列通訊物件
                    print('Failed to send')
                    
            elif (coord[0]+coord[2])/2>w/2: #水果在畫面右邊(可以再往後)
                #告訴Arduino要再往後
                print('keep go backward')
                try:
                    b='0010001'
                    success_bytes=ser.write(b.encode(encoding='UTF-8'))
                    time.sleep(1)
                    print(success_bytes)
                except KeyboardInterrupt:
                    ser.close()    # 清除序列通訊物件
                    print('Failed to send')
            
            if  inmiddle: # 畫面中的水果在水平中央
                step=3
                nofruit=0
                try:
                    b='0011111' #代表中間有對齊
                    success_bytes=ser.write(b.encode(encoding='UTF-8'))
                    time.sleep(1)
                    print(success_bytes)
                except KeyboardInterrupt:
                    ser.close()    # 清除序列通訊物件
                    print('Failed to send')
                
                pass
            
            if nofruit==10: #連續10次沒偵測到水果，回到第一步驟
                step=1
                nofruit=0
                coord_smooth_list=[]
            pass
        
        elif step ==3:
            print('in step 3')
            # 跟arduino說現在是step幾
            try:
                b='0100000'
                success_bytes=ser.write(b.encode(encoding='UTF-8'))
                time.sleep(1)
                print(success_bytes)
            except KeyboardInterrupt:
                ser.close()    # 清除序列通訊物件
                print('Failed to send')
                
            #檢查圖片，叫手臂移動
            coordinates_list=use_darknet.return_coord(frame,path=prefix_path) #取得座標
            isfruit=False
            mostlikely=None
            theconfidence=0 #信心
            coord=[0,0,0,0] #儲存的座標 [xmin,ymin,xmax,ymax]
            for coordinate_set in coordinates_list: # 取信心最大
                if coordinate_set[2]>isconfidence and coordinate_set[2]>theconfidence:
                    theconfidence=coordinate_set[2]
                    coord=coordinate_set[0]
                    mostlikely=coordinate_set[1]
            
            use_darknet.draw_boxes([[coord,mostlikely,theconfidence]], frame_draw, colors,label2txt)   
            cv2.imshow('live', frame_draw)
            
            if mostlikely==None:#沒偵測到水果
                nofruit+=1
                continue
            elif coord[0]==coord[2] or coord[1]==coord[3]:
                nofruit+=1
                continue
            else:
                nofruit=0
            
            print(coord)
            
            errpix=10 #可容許的對位誤差
            inmiddle=False
            
            if abs((coord[1]+coord[3])/2-h/2)<errpix: #這樣算是有對齊
                inmiddle=True
            elif (coord[1]+coord[3])/2<h/2: #水果在畫面上邊
                #告訴Arduino手臂要再往上
                print('keep go upward')
                try:
                    b='0100010'
                    success_bytes=ser.write(b.encode(encoding='UTF-8'))
                    time.sleep(1)
                    print(success_bytes)
                except KeyboardInterrupt:
                    ser.close()    # 清除序列通訊物件
                    print('Failed to send')
                    
            elif (coord[1]+coord[3])/2>h/2: #水果在畫面下面
                #告訴Arduino手臂要再往下
                print('keep go downward')
                try:
                    b='0100001'
                    success_bytes=ser.write(b.encode(encoding='UTF-8'))
                    time.sleep(1)
                    print(success_bytes)
                except KeyboardInterrupt:
                    ser.close()    # 清除序列通訊物件
                    print('Failed to send')
            
            if  inmiddle: # 畫面中的水果在水平中央
                step=4
                nofruit=0
                try:
                    b='0101111' #代表中間有對齊
                    success_bytes=ser.write(b.encode(encoding='UTF-8'))
                    time.sleep(1)
                    print(success_bytes)
                except KeyboardInterrupt:
                    ser.close()    # 清除序列通訊物件
                    print('Failed to send')
                
                pass
            
            if nofruit==10: #連續10次沒偵測到水果，回到第一步驟
                step=1
                nofruit=0
                coord_smooth_list=[]

            pass
        
        elif step ==4:
            print('in step 4')
            # 跟arduino說現在是step幾
            
            try:
                b='0110000'
                success_bytes=ser.write(b.encode(encoding='UTF-8'))
                time.sleep(1)
                print(success_bytes)
            except KeyboardInterrupt:
                ser.close()    # 清除序列通訊物件
                print('Failed to send')
            
            # 還是讀一下圖片
            
            coordinates_list=use_darknet.return_coord(frame,path=prefix_path) #取得座標
            isfruit=False
            mostlikely=None
            theconfidence=0 #信心
            coord=[0,0,0,0] #儲存的座標 [xmin,ymin,xmax,ymax]
            for coordinate_set in coordinates_list: # 取信心最大
                if coordinate_set[2]>isconfidence and coordinate_set[2]>theconfidence:
                    theconfidence=coordinate_set[2]
                    coord=coordinate_set[0]
                    mostlikely=coordinate_set[1]
            
            use_darknet.draw_boxes([[coord,mostlikely,theconfidence]], frame_draw, colors,label2txt)   
            cv2.imshow('live', frame_draw)
            
            #TODO Arduio合上夾爪，從Arduino讀值(微動開關碰到發訊息，夾爪完全閉合但微動開關未通電也會發訊息)
            
            
            msg=ser.readline()
            msg=msg.decode('utf-8')
            print(msg)
            try:

                msg=int(msg)
                print(msg)
                if msg==0: #TODO 微動開關通電(代表有夾到[夾到後要升起來一點點]，須從Arduino接收訊息)
                    # 夾到了
                    
                    step=5
                    
                if  msg==2: #TODO 已經到極限角度但還是沒夾到
                    
                    step=3 #退回調整手臂
            except:
                pass
 
            pass
        
        elif step ==5:
            print('in step 5')
            # 跟arduino說現在是step幾
            try:
                b='1000000'
                success_bytes=ser.write(b.encode(encoding='UTF-8'))
                time.sleep(1)
                print(success_bytes)
            except KeyboardInterrupt:
                ser.close()    # 清除序列通訊物件
                print('Failed to send')
            # 執行循線code，同時camera偵測(同時分開進行)
            
            # frame->(480, 640, 3)
            
            #偵測箱子應該是用inRange()
            hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            lower_mask = np.array([0,0,0]) 
            upper_mask = np.array([0,0,0]) 
            
            if mostlikely_smooth==0:
                #TODO 找Range值 carrot 指定mask
                lower_mask = np.array([0,0,0]) 
                upper_mask = np.array([0,0,0]) 
                pass
            elif mostlikely_smooth==1:
                #TODO 找Range值 tomato 指定mask
                lower_mask = np.array([0,175,45]) 
                upper_mask = np.array([20,255,176]) 
                pass
            elif mostlikely_smooth==2:
                #TODO 找Range值 lemon 指定mask
                lower_mask = np.array([43,64,71]) 
                upper_mask = np.array([67,212,175]) 
                pass
            elif mostlikely_smooth==3:
                #TODO 找Range值 avocado 指定mask
                lower_mask = np.array([95,89,84]) 
                upper_mask = np.array([118,209,178]) 
                pass
            else:
                # 沒有東西就開過去
                pass
            
            boxinmiddle=False
            area_threshold=30000
            
            mask = cv2.inRange(hsv, lower_mask, upper_mask) 
            canny=cv2.Canny(mask,100,200)
            area=0
            contours,hierarchy=cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            for cnt in contours:
                area+=cv2.contourArea(cnt)
            print(area)
            cv2.imshow('hsv',mask)
            # 使用inRange，理想情況是先匡出矩形區域，再算面積
            # 但我快死掉了，所以就先只看面積

            
            
            if area>area_threshold:#當箱子面積>閾值
                
                try:
                    b='1000001' #告訴Arduino該慢下來了喔
                    success_bytes=ser.write(b.encode(encoding='UTF-8'))
                    time.sleep(1)
                    print(success_bytes)
                except KeyboardInterrupt:
                    ser.close()    # 清除序列通訊物件
                    print('Failed to send')
                # 開始慢慢開
                
                step=6
                pass
                
            
        
        elif step ==6:
            # 這是一個慢慢開的狀態
            print('in step 6')
            # 跟arduino說現在是step幾
            try:
                b='1010000'
                success_bytes=ser.write(b.encode(encoding='UTF-8'))
                time.sleep(1)
                print(success_bytes)
            except KeyboardInterrupt:
                ser.close()    # 清除序列通訊物件
                print('Failed to send')
            
            boxinmiddle=False
            #TODO 檢查圖片，叫車移動
            if abs((coord[1]+coord[3])/2-h/2)<errpix: # inrange的coord 在箱子正中間
                boxinmiddle=True
                try:
                    b='1010001' #告訴Arduino該停車了喔
                    success_bytes=ser.write(b.encode(encoding='UTF-8'))
                    time.sleep(1)
                    print(success_bytes)
                except KeyboardInterrupt:
                    ser.close()    # 清除序列通訊物件
                    print('Failed to send')
                # 這時應該要停車
            if  boxinmiddle: # 畫面中的箱子在水平中央
                step=7
                pass
            
            pass
        
        elif step ==7:
            print('in step 7')
            # 跟arduino說現在是step幾
            # 應該是停車的狀態
            try:
                b='1100000'
                success_bytes=ser.write(b.encode(encoding='UTF-8'))
                time.sleep(1)
                print(success_bytes)
            except KeyboardInterrupt:
                ser.close()    # 清除序列通訊物件
                print('Failed to send')
            #TODO 夾爪降下來一點，跟Arduino說可以放開夾爪
            
            msg=ser.readline()
            msg=msg.decode('utf-8')
            print(msg)
            try:

                msg=int(msg)
                print(msg)
                if msg==0: #微動開關OFF(代表有已經丟下來了)
                    # 夾到了
                    step=8

                if  msg==2: #已經張到最開             
                    step=8 #退回調整手臂
            except:
                pass
            
        
        elif step ==8:
            print('in step 8')
            # 跟arduino說現在是step幾
            try:
                b='1110000'
                success_bytes=ser.write(b.encode(encoding='UTF-8'))
                time.sleep(1)
                print(success_bytes)
            except KeyboardInterrupt:
                ser.close()    # 清除序列通訊物件
                print('Failed to send')
                
            #TODO 行車直到DMS表示有障礙物在前面
            if '''#TODO 有障礙物在前面''':
                break
            
            pass
        
        # 按下 q 鍵離開迴圈
        if cv2.waitKey(1) == ord('q'):
            break
        
        # # 設定reset鍵
        # if '''#TODO某鍵被按到''':
        #     step=1
        
        # # 設定stop鍵
        # if '''#TODO某鍵被按到''':
        #     break
        

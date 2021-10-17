import cv2
import ipdb
import numpy
import serial  # 引用pySerial模組
import time
import sys
import statistics

import x64.use_def_return_coord as use_darknet


if __name__=='__main__':
    
    
    # pyserial 連線
    COM_PORT = 'COM4'    # 指定通訊埠名稱
    BAUD_RATES = 38400    # 設定傳輸速率
    locations=['COM0','COM1','COM2','COM3','COM4','COM5','COM6']
    # location=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3','/dev/ttyS0','/dev/ttyS1','/dev/ttyS2','/dev/ttyS3'] #linux
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
    except:
        print(f"Failed to connect on {COM_PORT}")
        for device in locations:
            try:
                ser=serial.Serial(device,BAUD_RATES)
            except:
                print(f"Failed to connect on {device}")
    

   
    while True:

        success_bytes=ser.write(str(1000000000000000).encode(encoding='UTF-8'))
        time.sleep(1)
        print(success_bytes)

        
        
        
    
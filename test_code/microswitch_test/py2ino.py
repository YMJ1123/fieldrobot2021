# https://swf.com.tw/?p=1188


import serial  # 引用pySerial模組
import time
 
if __name__ == '__main__':
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
        try:
            # ch=input('input:')
            # ser.write(ch.encode(encoding='UTF-8'))
            # time.sleep(1)
            # print(ser.readline()).
            pass
        
        except KeyboardInterrupt:
            ser.close()    # 清除序列通訊物件
            print('Failed to send')
            
        try:
            buffer = list()
            while ser.in_waiting:
                data_raw = ser.read()
                buffer.append(data_raw)

                if data_raw == b'\n':
                    print('收到的資料：', buffer)
                    buffer.clear()

        except KeyboardInterrupt:
            ser.close()    # 清除序列通訊物件
            print('關閉程式')
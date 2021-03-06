
#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);  // 設定 LCD I2C 位址

Servo servo1;  // 建立SERVO物件
Servo servo2;  // 建立SERVO物件
Servo servo3;  // 建立SERVO物件
char ch;
int pinLED = 13;

int step;
int motion;

int microswitch1 = 6;
int microswitch2 = 7;

const int RGBLED_R=0;
const int RGBLED_G=1;
const int RGBLED_B=2;

const int left_motor=6;
const int right_motor=7;
// 77/80

//手臂的初始角度
int d_servo1 = 45; // 上下
int d_servo2 = 180; //開合
int d_servo3 = 45; // 前後

int s = 2;

boolean manul = true;

const int bufferLength = 7;    // 定义缓存大小为10个字节
char serialBuffer[bufferLength];// 建立字符数组用于缓存

void setup()
{
  pinMode(RGBLED_R, OUTPUT);
  pinMode(RGBLED_G, OUTPUT);
  pinMode(RGBLED_B, OUTPUT);

  Serial.begin(38400);
  Serial.print("Program Initiate\n");
  pinMode(pinLED, OUTPUT); // 設定腳位 13 為輸出模式


  servo1.attach(9);  // 設定要將伺服馬達接到哪一個PIN腳
  servo2.attach(10);  // 設定要將伺服馬達接到哪一個PIN腳
  servo3.attach(11);  // 設定要將伺服馬達接到哪一個PIN腳

  servo1.write(d_servo1);
  servo2.write(d_servo2);
  servo3.write(d_servo3);

  pinMode(microswitch1, INPUT);
  pinMode(microswitch2, INPUT);
  pinMode(pinLED, OUTPUT);

  lcd.begin(16, 2);  

  for(int i = 0; i < 3; i++) {
    lcd.backlight(); // 開啟背光
    delay(250);
    lcd.noBacklight(); // 關閉背光
    delay(250);
  }
  lcd.backlight();

  // 輸出初始化文字
  lcd.setCursor(0, 0); // 設定游標位置在第一行行首
  lcd.print("Hello, world!");
  delay(1000);
}
void loop()
{
  if (manul) {
    // 微動開關
    float v1 = digitalRead(microswitch1);
    float v2 = digitalRead(microswitch2);
    if (v1 > 0.5 || v2 > 0.5) {
      digitalWrite(pinLED, HIGH);
    } else {
      digitalWrite(pinLED, LOW);
    }

    if (Serial.available()) // 檢查電腦端是否有訊息來
    {

      delay(50);

      Serial.readBytes(serialBuffer, bufferLength);
      step=(serialBuffer[0]- '0')*4+(serialBuffer[1]- '0')*2+(serialBuffer[2]- '0')+1; //表示這是step幾
      motion=(serialBuffer[3]- '0')*8+(serialBuffer[4]- '0')*4+(serialBuffer[5]- '0')*2+(serialBuffer[6]- '0');

      //如果有接LCD的話，LCD顯示收到的
      lcd.clear(); //清除
      lcd.setCursor(0, 0); // 設定游標位置在第一行行首
      lcd.print(serialBuffer);


      if (step==1){
        if(motion==0){
          //TODO 循線往前
        }
        else if (motion==1){ //看到紅蘿蔔
          //TODO
          lcd.setCursor(0, 1); // 設定游標位置在第二行行首
          lcd.print('carrot');
          //TODO 停車
        }
        else if (motion==2){ //看到番茄
          //TODO 亮紅燈
          lcd.setCursor(0, 1); // 設定游標位置在第二行行首
          lcd.print('tomato');
          //TODO 停車
        }
        else if(motion==3){ //看到檸檬
          //TODO 亮綠燈
          lcd.setCursor(0, 1); // 設定游標位置在第二行行首
          lcd.print('lemon');
          //TODO 停車

        }else if(motion==4){ //看到酪梨
          //TODO 亮藍燈
          lcd.setCursor(0, 1); // 設定游標位置在第二行行首
          lcd.print('avocado');
          //TODO 停車
        }
      }
      else if(step==2){
        if(motion==1){
          //TODO 車往後走一點
        }else if(motion==2){
          //TODO 車往前走一點
        }else if(motion==15){
          //TODO 代表對齊，好像也不用幹嘛
        }
      }
      else if(step==3){
        if(motion==2){
          // 手臂要再往上
          // 手臂往前
          d_servo1=d_servo1-s;
          servo1.write(d_servo1);

          //手臂往上
          d_servo3=d_servo3+s;
          servo3.write(d_servo3);

        }
        else if(motion==1){
          // 手臂要再往下
          //手臂往後
          d_servo1=d_servo1+s;
          servo1.write(d_servo1);

          //手臂往下
          d_servo3=d_servo3-s;
          servo3.write(d_servo3);
          
        }
        else if(motion==15){
          //TODO 代表對齊，好像也不用幹嘛
        }
        delay(100);
      }
      else if(step==4){
        
        lcd.setCursor(0, 1); // 設定游標位置在第2行行首
        lcd.print('step 4');
        //到定點了
        //TODO 合起夾爪
        d_servo2=d_servo2-s;
        servo2.write(d_servo2);

        
        if(digitalRead(microswitch1)==HIGH || digitalRead(microswitch2)==HIGH){ //碰到微動開關
          //TODO 這裡要傳訊息給python
          Serial.println('0');//夾到東西
          lcd.setCursor(0, 1); // 設定游標位置在第2行行首
          lcd.print('0');
          //夾爪升起來一點
          d_servo3=d_servo3+s;
          servo3.write(d_servo3);

        }else{
          Serial.println('1');//沒有夾到東西
          lcd.setCursor(0, 1); // 設定游標位置在第2行行首
          lcd.print('1');
        }
        int limit_angle=0; //TODO 設定閉最緊的極限角度，要量一下
        if(d_servo2==limit_angle){ //也是沒夾到
          Serial.println('2');
          lcd.setCursor(0, 1); // 設定游標位置在第一行行首
          lcd.print('2');
          //張開夾爪
          d_servo2=180;
          servo2.write(d_servo2);
        }
      }
      else if(step==5){
        if(motion==1){
          //TODO 車要降速
        }
      }
      else if(step==6){
        if(motion==1){
          //TODO 車停下來
          // 先降一下夾爪(剛剛夾到東西時有升一點)
          d_servo3=d_servo3-s;
          servo3.write(d_servo3);
        }
      }
      else if(step==7){
        // TODO 這裡車應該是停止的狀態
        
        //TODO 張開夾爪
        d_servo2=d_servo2+s;// TODO 不確定是不是對的
        servo2.write(d_servo2);

        if(digitalRead(microswitch1)==HIGH || digitalRead(microswitch2)==HIGH){ //碰到微動開關
          //TODO 這裡要傳訊息給python
          Serial.println('1');//還沒掉下來
          lcd.setCursor(0, 1); // 設定游標位置在第2行行首
          lcd.print('1');


        }else{
          Serial.println('0');//沒有夾到東西->已經掉下來了
          lcd.setCursor(0, 1); // 設定游標位置在第2行行首
          lcd.print('0');
        }
        int limit_angle=0; //TODO 設定張最開的極限角度，要量一下
        if(d_servo2==limit_angle){ //已經張最開，代表應該是掉下來了
          Serial.println('2');
          lcd.setCursor(0, 1); // 設定游標位置在第一行行首
          lcd.print('2');
          
        }

      }
      else if(step==8){
        // TODO 直走直到障礙
//        if (/*TODO DMS | 超音波感測到*/):
//          // TODO 停下來，結束程式
      }
      

    }
    delay(100);
  }


}

#include <Servo.h>
#include <SoftwareSerial.h>

Servo servo1;  // 建立SERVO物件
Servo servo2;  // 建立SERVO物件
Servo servo3;  // 建立SERVO物件
char ch;
int pinLED = 13;

int microswitch1=6;
int microswitch2=7;


int d_servo1=45;//0-120 前後
int d_servo2=180; //開合
int d_servo3=0;//90-180 上下

int s=10;

void setup()
{
  Serial.begin(38400);
  Serial.print("Program Initiate\n");
  pinMode(pinLED, OUTPUT); // 設定腳位 13 為輸出模式


  servo1.attach(3);  // 設定要將伺服馬達接到哪一個PIN腳
  servo2.attach(5);  // 設定要將伺服馬達接到哪一個PIN腳
  servo3.attach(9);  // 設定要將伺服馬達接到哪一個PIN腳

  servo1.write(d_servo1);
  servo2.write(d_servo2);
  servo3.write(d_servo3);

  pinMode(microswitch1,INPUT);
  pinMode(microswitch2,INPUT);
  pinMode(pinLED,OUTPUT);
}
void loop()
{
  float v1=digitalRead(microswitch1);
  float v2=digitalRead(microswitch2);
  if (v1>0.5||v2>0.5){
    digitalWrite(pinLED,HIGH);
  }else{
    digitalWrite(pinLED,LOW);
  }
  
  if (Serial.available()) // 檢查電腦端是否有訊息來
  {
    
    delay(50);

    
    ch = Serial.read();  
    if (ch == 'L' ) // 判斷是否為 L 的訊息
    {
      digitalWrite(pinLED, HIGH);
      Serial.println('L');
    }
    else if(ch == 'R'){
      digitalWrite(pinLED, LOW);
      Serial.println('R');
    }
    else if(ch == 'B'){
      d_servo1=d_servo1+s;
      servo1.write(d_servo1);
      delay(10);
      Serial.println('B');
      Serial.println(d_servo1);
    }
    else if(ch == 'F'){
      d_servo1=d_servo1-s;
      servo1.write(d_servo1);
      delay(10);
      Serial.println('F');
      Serial.println(d_servo1);
    }
    else if(ch == 'C'){
      d_servo2=d_servo2-s;
      servo2.write(d_servo2);
      delay(10);
      Serial.println('C');
      Serial.println(d_servo2);
    }
    else if(ch == 'O'){
      d_servo2=d_servo2+s;
      servo2.write(d_servo2);
      delay(10);
      Serial.println('O');
      Serial.println(d_servo2);
    }
    else if(ch == 'U'){
      d_servo3=d_servo3+s;
      servo3.write(d_servo3);
      delay(10);
      Serial.println('U');
      Serial.println(d_servo3);
    }
    else if(ch == 'D'){
      d_servo3=d_servo3-s;
      servo3.write(d_servo3);
      delay(10);
      Serial.println('D');
      Serial.println(d_servo3);
    }

  }
  delay(100);


  
}

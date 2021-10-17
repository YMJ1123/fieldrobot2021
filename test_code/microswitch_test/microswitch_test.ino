#include <Wire.h>  // Arduino IDE 內建
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x3F, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);  // 設定 LCD I2C 位址

int switch1=6;
int switch2=7;
int pinLED=13;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(38400);  
  pinMode(switch1,INPUT);
  pinMode(switch2,INPUT);
  pinMode(pinLED,OUTPUT);

  lcd.begin(16, 2);      // 初始化 LCD，一行 16 的字元，共 2 行，預設開啟背光

  // 閃爍三次
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
  lcd.setCursor(0, 1); // 設定游標位置在第二行行首
  lcd.print("cccccc");
  delay(8000);
  

}

void loop() {
  // put your main code here, to run repeatedly:
  float v1=digitalRead(switch1);
  float v2=digitalRead(switch2);
  if (v1>0.5||v2>0.5){
    lcd.clear();
    lcd.print("catch!!");
    digitalWrite(pinLED,HIGH);
    Serial.println("catch!!");
  }else{
    lcd.clear();
    lcd.print("no~~");
    digitalWrite(pinLED,LOW);
  }
  delay(10);
}

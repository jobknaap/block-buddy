
/*
@purpose This Arduino code that acts as a Slave for the Canbus. The code listens and prints out the canbus data. It also turns on LED based upon specific message.
@author Max Zijlstra
@date 16 oct 2023
*/

#include <SPI.h>
#include <mcp2515.h>

struct can_frame canMsg;
MCP2515 mcp2515(10);

#define LED_PIN 8
#define TARGET_CAN_ID 0x123
byte CAN_DATA_ON[8] = {0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x80};  // example data for "on"
byte CAN_DATA_OFF[8] = {0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x81};  // example data for "off"

void setup() {
  Serial.begin(115200);
  
  mcp2515.reset();
  mcp2515.setBitrate(CAN_125KBPS);
  mcp2515.setNormalMode();
  
  pinMode(LED_PIN, OUTPUT);  // set the LED pin as output
  digitalWrite(LED_PIN, LOW);  // initially set LED off
  
  delay(2000);
  Serial.println("------- CAN Read ----------");
  Serial.println("ID  DLC   DATA");
}

bool compareCANMessage(byte targetData[8]) {
  if(canMsg.can_id != TARGET_CAN_ID) return false;
  if(canMsg.can_dlc != 8) return false;  // 8 bytes of data
  
  for (int i = 0; i < 8; i++) {
    if (canMsg.data[i] != targetData[i]) {
      return false;
    }
  }
  return true;
}

void loop() {
  if (mcp2515.readMessage(&canMsg) == MCP2515::ERROR_OK) {
    Serial.print(canMsg.can_id, HEX); // print ID
    Serial.print(" "); 
    Serial.print(canMsg.can_dlc, HEX); // print DLC
    Serial.print(" ");
    
    for (int i = 0; i < canMsg.can_dlc; i++)  {  // print the data
      Serial.print(canMsg.data[i],HEX);
      Serial.print(" ");
    }

    Serial.println();

    if(compareCANMessage(CAN_DATA_ON)) {
      digitalWrite(LED_PIN, HIGH);  // turn the LED on
    } else if(compareCANMessage(CAN_DATA_OFF)) {
      digitalWrite(LED_PIN, LOW);  // turn the LED off
    }
  }
}

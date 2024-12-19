#include <Stepper.h>

const int forwardPin = 2;
const int backwardPin = 3;

const int stepsPerRevolution = 5;

int lastBackwardState = 0;
int lastForwardState = 0;

Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {
  pinMode(backwardPin, INPUT);
  pinMode(forwardPin, INPUT);
  Serial.begin(9600);
}

void moveBelt(int backwardState, int forwardState) {
  if (backwardState == HIGH && !lastBackwardState) {
    myStepper.setSpeed(2000);
    myStepper.step(stepsPerRevolution);
  } else if (backwardState == HIGH && lastBackwardState) {
    myStepper.setSpeed(2000);
    myStepper.step(stepsPerRevolution);
  }

  else if(forwardState == HIGH && !lastForwardState){
    myStepper.setSpeed(2000);
    myStepper.step(-stepsPerRevolution);
  } else if (forwardState == HIGH && lastForwardState) {
    myStepper.setSpeed(2000);
    myStepper.step(-stepsPerRevolution);
  }

  lastBackwardState = backwardState;
  lastForwardState = forwardState;
}

void loop() {
  int backwardState = digitalRead(backwardPin);
  int forwardState = digitalRead(forwardPin);

  moveBelt(backwardState, forwardState);

  Serial.print("Backwards button is ");
  Serial.println(backwardState == HIGH ? "ON" : "OFF");

  Serial.print("Forwards button is ");
  Serial.println(forwardState == HIGH ? "ON" : "OFF");

  delay(10);
}
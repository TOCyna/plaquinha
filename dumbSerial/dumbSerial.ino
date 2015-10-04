/* Blink without Delay

 Turns on and off a light emitting diode(LED) connected to a digital
 pin, without using the delay() function.  This means that other code
 can run at the same time without being interrupted by the LED code.

 The circuit:
 * LED attached from pin 13 to ground.
 * Note: on most Arduinos, there is already an LED on the board
 that's attached to pin 13, so no hardware is needed for this example.


 created 2005
 by David A. Mellis
 modified 8 Feb 2010
 by Paul Stoffregen

 This example code is in the public domain.


 http://www.arduino.cc/en/Tutorial/BlinkWithoutDelay
 */

// constants won't change. Used here to
// set pin numbers:
const int ledPin =  13;      // the number of the LED pin

// Variables will change:
int ledState = LOW;             // ledState used to set the LED
long previousMillis = 0;        // will store last time LED was updated

// the follow variables is a long because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long interval = 500;           // interval at which to blink (milliseconds)
int n = 0;
int aux = 0;
int com = 0;
bool flag = 0;
String inString = "";

void setup() {
  // set the digital pin as output:
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}

void loop()
{
  unsigned long currentMillis = millis();
  if (Serial.available()) {
    int inChar = Serial.read();
    char a = (char)inChar;
    if (a == 'a') {
      inString = "";
      com = 0;
    }
    if (isDigit(inChar)) {
      // convert the incoming byte to a char
      // and add it to the string:
      inString += (char)inChar;
    }
    // if you get a newline, print the string,
    // then the string's value:
    if (inChar == 'c') {
      com = inString.toInt();
      if (com == 111) {
        flag = 1;
      } else if (com == 101) {
        flag = 0;
      } else if (com == 100) {
        printAngle();
      } else if (com >= 200 && com <= 560) {
        n = com - 200;
        if (ledState == LOW)
          ledState = HIGH;
        else
          ledState = LOW;
        printAngle();
      }
      com = 0;
      // clear the string for new input:
      inString = "";
    }
  }
  if (currentMillis - previousMillis > interval) {
    // save the last time you blinked the LED
    previousMillis = currentMillis;

    // if the LED is off turn it on and vice-versa:


    // set the LED with the ledState of the variable:
    digitalWrite(ledPin, ledState);
    if (flag) {
      printAngle();
    }
  }
}

void printAngle(void) {
  String s = String(n);
  Serial.println('a' + s + 'c');
}


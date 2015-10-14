//alocao dos pinos
const int EN = 10; // pino de enable do L293d
const int IN1 = 11; // pino A1 de direcao do L293D
const int IN2 = 12; // pino A2 de direcao do L293D
const int ENCODER = A0;
const int MSB = 9;
const int B4 = 8;
const int B3 = 7;
const int B2 = 6;
const int LSB = 5;
const int NULL2 = 4;
const int NULL1 = 3;
const int SELECT = 2;
const int LED = 13;

//global consts
const int MIN_ANGLE = 0;
const int MAX_ANGLE = 240;
const int MIN_POWER = 60;
const int MAX_POWER = 255;
const int MIN_ENCODER = 0;
const int MAX_ENCODER = 1022;
float CONST_ENCODER;
const int ERRO = 0;
const long INTERVAL = 200;
const int OFFSET_COM = 200;

//motor consts
const int MOTOR_FREE = 0;
const int MOTOR_STOP = 220;

//variaveis de controle
String inString = "";
bool isHearing = 0;
int input = 0;
int com = 0;
int lastPrintedAngle = 0;

//variaveis do digital input
int selectAngle[5];
int selectMode[3];

void setup() {
  Serial.begin(9600);
  pinMode(EN, OUTPUT); //PWM    PonteH
  pinMode(IN1, OUTPUT); //right gate L293d
  pinMode(IN2, OUTPUT);//left gate L293
  
  pinMode(SELECT, INPUT);//switch
  pinMode(NULL1, INPUT);
  pinMode(NULL2, INPUT);
  
  pinMode(LSB, INPUT);
  pinMode(B2, INPUT);
  pinMode(B3, INPUT);
  pinMode(B4, INPUT);
  pinMode(MSB, INPUT);
  
  pinMode(ENCODER, INPUT); 
  pinMode(LED, OUTPUT);
  CONST_ENCODER = (float)MAX_ANGLE / (float)MAX_ENCODER;
  //debug
}

void loop()
{
  serialRead();
  goToDegree(input);
}

void serialRead() {
  if (Serial.available()) {
    int inChar = Serial.read();
    char a = (char)inChar;
    if (a == 'a') { //Inicio de mensagem
      inString = "";
      com = 0;
    }
    if (isDigit(inChar)) { //Mensagem
      inString += (char)inChar;
    }
    if (inChar == 'c') { //Fim de mensagem
      com = inString.toInt();
      if (com == 111) {
        isHearing = 1; //Habilita o envio Serial (Handshack)
        Serial.println("a111c");
        Serial.flush();
        digitalWrite(LED, HIGH);
      } else if (com == 101) {
        isHearing = 0; //Desabilita o envio Serial (CloseConection)
        digitalWrite(LED, LOW);
      } else if (com == 100) {
        realMeanPosition();
      } else {
        com = com - OFFSET_COM;
        if (com >= MIN_ANGLE && com <= MAX_ANGLE) {
          input = com;
        }
      }
      com = 0; //Limpa para receber proxima mensagem
      inString = ""; //Limpa para receber proxima mensagem
    }
  }
}
//Envia mensagem dentro do protocolo
void printAngle(void) {
  String s = String((realMeanPosition() + OFFSET_COM));
  Serial.println('a' + s + 'c');
}

void printAngle(int angle) {
  if (lastPrintedAngle != angle && isHearing) {
    String s = String(angle + OFFSET_COM);
    Serial.println('a' + s + 'c');
    lastPrintedAngle = angle;
  }
}

void motorStop() { //power 0 to 255
  analogWrite(EN, MOTOR_STOP); 
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, HIGH);
}

void motorFree() { //power 0 to 255
  analogWrite(EN, MOTOR_FREE); 
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}

void goClockWise(int distance) { //power 0 to 255
  int power = motorMap(distance);
  //Serial.println("C: " + String(power));
  analogWrite(EN, power); 
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  //delay(50);
}

void goCClockWise(int distance) { //power 0 to 255
  int power = motorMap(distance);
  //Serial.println("CC: " + String(power));
  analogWrite(EN, power); 
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  //delay(50);
}

int realPosition(){
  int value = analogRead(ENCODER);
  //int degree = map (value,0,1023,0, 360);
  return value;
}

int realMeanPosition(){
  float value = 0;
  int sampleSize = 10;
  for(int i = 0; i < sampleSize; i++){
    value += analogRead(ENCODER);
  }
  int angle = (int)((value/sampleSize) * CONST_ENCODER);
  printAngle(angle);
  return angle; 
}


void goToDegree(int degree) {
      int realPosition, distance, factorOfOcilation;

  if(degree >= MIN_ANGLE && degree <= MAX_ANGLE) {
    realPosition = realMeanPosition();
    
    if((realPosition < (degree - ERRO)) ||
           (realPosition > (degree + ERRO))) {
      distance = realPosition - degree;
      if(distance < 0)
        goClockWise(abs(distance));
      else
        goCClockWise(distance);
      realPosition = realMeanPosition();
    }
  }
  if(realPosition == degree)
    motorStop();
}

int newMap(int x, int in_min, int in_max, int out_min, int out_max) {
  //http://forum.arduino.cc/index.php?topic=38006.0
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

int motorMap(int distance) {
  return map(distance, MIN_ANGLE, MAX_ANGLE, MIN_POWER, MAX_POWER);
}

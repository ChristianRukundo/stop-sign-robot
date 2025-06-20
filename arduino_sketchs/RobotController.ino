#include <Servo.h>

#define SERVO_PIN 9
#define BRAKE_LIGHT_PIN LED_BUILTIN

const int MOVE_POSITION = 0;
const int STOP_POSITION = 90;

Servo motor;

void setup()
{

    Serial.begin(9600);
    pinMode(BRAKE_LIGHT_PIN, OUTPUT);
    motor.attach(SERVO_PIN);

    moveRobot();

    Serial.println("Arduino Initialized. Awaiting commands...");
}

void loop()
{

    if (Serial.available() > 0)
    {

        char command = Serial.read();

        if (command == '1')
        {
            Serial.println("Received: 1 -> Executing STOP");
            stopRobot();
        }
        else if (command == '0')
        {

            Serial.println("Received: 0 -> Executing MOVE");
            moveRobot();
        }
    }
}

void stopRobot()
{

    digitalWrite(BRAKE_LIGHT_PIN, HIGH);
    motor.write(STOP_POSITION);
}

void moveRobot()
{

    digitalWrite(BRAKE_LIGHT_PIN, LOW);

    motor.write(MOVE_POSITION);
}
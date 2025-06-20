# Real-Time Stop Sign Detection and UART Control System

![Status: Production Ready](https://img.shields.io/badge/status-production_ready-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A robust, real-time computer vision system designed to detect stop signs from a live camera feed and send control signals to a microcontroller (e.g., Arduino) via UART serial communication.

> This project is architected for production environments, emphasizing modularity, configuration management, and robust error handling. It serves as a foundational component for autonomous vehicle or robotic navigation systems.


## Key Features

-   **Real-Time Detection:** Utilizes OpenCV and a Haar Cascade classifier for fast, real-time stop sign detection.
-   **Modular Architecture:** The code is separated into distinct modules for Vision, Communication, and State Logic, making it easy to maintain, test, and upgrade.
-   **External Configuration:** All system parameters (camera index, serial port, detection settings) are managed in a `config.ini` file, allowing for easy adjustments without changing the source code.
-   **Formal State Machine:** Manages the robot's behavior (`MOVING`, `STOPPING`) with a clear, predictable state machine that includes timing logic.
-   **Concurrent Processing:** The camera frame-grabbing runs in a separate thread to prevent I/O blocking and ensure the main logic loop remains highly responsive.
-   **Robust Logging:** Implements a professional logging system that outputs status, warnings, and errors to both the console and a log file (`logs/vision_system.log`) for easy debugging.
-   **Hardware Integration:** Provides a ready-to-use Arduino sketch (`RobotController.ino`) for seamless integration and testing with physical hardware (LEDs, servos).

---

## System Architecture

The project is structured into independent, single-responsibility modules:

```
/robot_vision_system/
|
|-- main.py                 # Orchestrator: Initializes modules and runs the main loop.
|-- config.ini              # Central configuration file for all parameters.
|-- vision_module.py        # Handles camera capture and stop sign detection logic.
|-- communication_module.py # Manages serial (UART) communication with the Arduino.
|-- state_machine.py        # Implements the MOVING/STOPPING state logic and timers.
|
|-- arduino_code/
|   |-- RobotController.ino # Arduino sketch for receiving signals and controlling hardware.
|
|-- stop_sign.xml           # Pre-trained Haar Cascade model for detection.
|-- requirements.txt        # List of Python dependencies.
|-- logs/
|   |-- vision_system.log   # Log file for diagnostics.
|
`-- README.md               # This file.
```

---

## Requirements

### Hardware
-   A standard **Webcam** connected via USB.
-   An **Arduino** (e.g., Uno, Nano) connected via USB.
-   (Optional for better demo) A small **Servo Motor** (e.g., SG90) and jumper wires.

### Software
-   **Python 3.8+**
-   **OpenCV** and **PySerial** libraries.
-   **Arduino IDE** to upload the sketch to the board.

---

## Installation and Setup

Follow these steps to get the system running.

### 1. Clone the Repository
```bash
git clone https://github.com/ChristianRukundo/stop-sign-robot.git
cd stop-sign-robot
```

### 2. Set Up Python Environment
It is highly recommended to use a virtual environment.
```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(You will need to create a `requirements.txt` file with `opencv-python` and `pyserial`)*

### 4. Set Up the Arduino
1.  Connect your Arduino to your computer.
2.  Open the `arduino_code/RobotController.ino` sketch in the Arduino IDE.
3.  Go to **Tools > Board** and select your Arduino model.
4.  Go to **Tools > Port** and select the correct serial port for your Arduino. **Make a note of this port name (e.g., `COM3`, `/dev/ttyACM0`).**
5.  Upload the sketch to the Arduino.
6.  (Optional) Connect a servo motor: **Signal** to Pin 9, **Power** to 5V, **Ground** to GND.

---

## Configuration

Before running the application, **you must edit the `config.ini` file**.

```ini
[serial]
# CRITICAL: Change this to the port your Arduino is on.
port = COM3

[camera]
# CRITICAL: Change this to your camera's index.
# Run check_cameras.py if you are not sure.
index = 0
```
Adjust other parameters in `config.ini` as needed for your specific setup.

---

## Running the System

Ensure your virtual environment is activated and you are in the project's root directory.

```bash
python main.py
```
Press `q` in the display window to exit the application gracefully.

---


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
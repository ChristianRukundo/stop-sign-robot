import serial
import logging


class SerialCommunicator:
    """Handles connection and data transmission over UART."""

    def __init__(self, port: str, baud_rate: int):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None

    def connect(self) -> bool:
        """Establishes the serial connection."""
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            logging.info(f"Successfully connected to serial port {self.port}.")
            return True
        except serial.SerialException as e:
            logging.error(f"Failed to connect to serial port {self.port}: {e}")
            return False

    def send_signal(self, signal: bytes):
        """Sends a signal if the connection is active."""
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(signal)
            except serial.SerialException as e:
                logging.warning(f"Failed to write to serial port: {e}")

    def disconnect(self):
        """Closes the serial connection."""
        if self.ser and self.ser.is_open:
            self.send_signal(b"0")
            self.ser.close()
            logging.info("Serial port connection closed.")

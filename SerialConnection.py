"""Utilities for handling serial communication with the module."""

from PyQt6.QtCore import QTimer
from PyQt6.QtSerialPort import QSerialPort

from logger import logger

# Default configuration values
DEFAULT_TIMER_INTERVAL = 100
DEFAULT_BAUD_RATE = 115_200


class SerialConnection:
    """Encapsulate work with a serial port and periodic requests."""

    def __init__(self) -> None:
        self.request_count = 0
        self.response_count = 0
        self.serial = QSerialPort()
        self.timer = QTimer()
        self.flag = False
        self.dcon = ""
        self.response = bytearray()
        self.data = ""

    def open_serial_port(
        self, port: str, baud_rate: int = DEFAULT_BAUD_RATE
    ) -> None:
        """Configure the serial port."""
        self.serial.setPortName(port)
        self.serial.setBaudRate(baud_rate)

    def connect(self) -> None:
        """Open the serial port for read/write communication."""
        self.serial.open(QSerialPort.OpenModeFlag.ReadWrite)

    def stop(self) -> None:
        """Stop communication and release the serial port."""
        try:
            self.timer.stop()
            self.serial.readyRead.disconnect()
            self.serial.close()
        except Exception:
            pass

    def start_automatic_requests(self, request: str) -> None:
        """Begin sending periodic requests."""
        self.timer.start(DEFAULT_TIMER_INTERVAL)
        self.dcon = request

        try:
            self.timer.timeout.disconnect()
        except TypeError:
            pass

        try:
            self.serial.readyRead.disconnect()
        except TypeError:
            pass

        self.timer.timeout.connect(self.write_data)
        self.serial.readyRead.connect(self.read_data)

    def change_request(self, request: str) -> None:
        """Replace the current request."""
        self.dcon = request

    def write_data(self) -> None:
        """Send data to the serial port."""
        self.serial.write(self.dcon.encode())
        if self.flag:
            self.request_count += 1
            logger.info("request %s", self.dcon)
        else:
            self.request_count = 0
            self.response_count = 0

    def read_data(self) -> None:
        """Read data from the serial port."""
        try:
            self.response = self.serial.readAll()
            self.data = self.response.data().decode()
            self.flag = True
            if self.flag:
                self.response_count += 1
                logger.info("%s", self.data)
                logger.info("%s", self.response_count)
        except Exception:
            logger.info("Error")

    def get_data(self) -> str:
        """Return the last received data."""
        return self.data

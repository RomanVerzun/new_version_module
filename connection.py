from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QTimer
from dcon_protocol import Dcon


class SerialConnection():
    def __init__(self, port:str, baud_rate:int):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate

        self.serial = QSerialPort()
        self.initSerialPort()
        self.startAutomaticRequests()

    def initSerialPort(self):
        self.serial.setPortName(self.port)  
        self.serial.setBaudRate(self.baud_rate)
        if not self.serial.open(QSerialPort.OpenModeFlag.ReadWrite):
            print(f"Failed to open port {self.serial.portName()}")
        self.serial.readyRead.connect(self.readData)

    def startAutomaticRequests(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.writeData)
        self.timer.start(200)  # 200 мс

    def writeData(self, character, address, command):
        request = self.request.create_request(character, address, command)
        self.serial.write(request.encode())

    def readData(self):
        if self.serial.canReadLine():
            response = self.serial.readLine()
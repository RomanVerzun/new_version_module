from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QTimer, QByteArray
from logger import logger
from dcon import Dcon

TIMER_INTERVAL = 100

class SerialConnection():
    def __init__(self):
        super().__init__()
        self.serial = QSerialPort()
        self.timer = QTimer()

    def OpenSerialPort(self, port:str, baud_rate:int=115200):
        self.serial.setPortName(port)
        self.serial.setBaudRate(baud_rate)

    def connect(self):
        if not self.serial.open(QSerialPort.OpenModeFlag.ReadWrite):
            raise ConnectionError
    
    def stop(self):
        self.timer.stop()
        self.serial.readyRead.disconnect()
        self.serial.close()

    def startAutomaticRequests(self, request):
        self.timer.start(TIMER_INTERVAL) 
        self.dcon = request

        try:
            self.timer.timeout.disconnect()
        except TypeError:
            pass

        try:
            self.serial.readyRead.disconnect()
        except TypeError:
            pass

        self.timer.timeout.connect(self.writeData)
        self.serial.readyRead.connect(self.readData)
    
    def changeRequest(self, request):
        self.dcon = request

    def writeData(self):
        self.serial.write(self.dcon.encode())

    def readData(self):
        try:
            self.response = self.serial.readAll()
            self.data = self.response.data().decode()
        except:
            ...
    
    def getData(self):
        try:
            return self.data
        except:
            self.data = '>FFFFFFFFFFFA\r'
            return self.data
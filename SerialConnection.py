from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QTimer, QByteArray
from logger import logger
from dcon import Dcon

TIMER_INTERVAL = 200

class SerialConnection():
    def __init__(self):
        super().__init__()
        self.serial = QSerialPort()

    def OpenSerialPort(self, port:str, baud_rate:int=115200):
        self.serial.setPortName(port)
        self.serial.setBaudRate(baud_rate)

    def connect(self):
        if not self.serial.open(QSerialPort.OpenModeFlag.ReadWrite):
            raise ConnectionError
    
    def disconnect(self):
        self.timer.stop()
        self.serial.readyRead.disconnect(self.readData)
        self.timer.timeout.disconnect()
        self.serial.close()

    def startAutomaticRequests(self, request):
        self.timer = QTimer()
        self.timer.start(TIMER_INTERVAL) 
        self.dcon = request

        self.timer.timeout.connect(self.writeData)
        self.serial.readyRead.connect(self.readData)
    
    def changeRequest(self, request):
        self.dcon = request

    def writeData(self):
        self.serial.write(self.dcon.encode())

    def readData(self):
        self.response = self.serial.readAll()
        #print(self.response)
        self.data = self.response.data().decode()
    
    def getData(self):
        try:
            return self.data
        except:
            self.data = '-00AA'
            return self.data
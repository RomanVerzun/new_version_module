from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QTimer, QByteArray
from dcon import Dcon


class SerialConnection():
    def __init__(self):
        super().__init__()
        self.serial = QSerialPort()

    def initSerialPort(self, port:str, baud_rate:int=115200):
        self.serial.setPortName(port)
        self.serial.setBaudRate(baud_rate)

        if not self.serial.open(QSerialPort.OpenModeFlag.ReadWrite):
            print(f"Failed to open port {self.serial.portName()}")
        else:
            print(f"Good")
    
    def disconnect(self):
        self.timer.stop()
        self.serial.readyRead.disconnect(self.readData)
        self.serial.close()

    def startAutomaticRequests(self, request):
        self.timer = QTimer()
        self.timer.start(100) 
        self.request = request

        self.timer.timeout.connect(self.writeData)
        self.serial.readyRead.connect(self.readData)

    def writeData(self):
        self.serial.write(self.request.encode())

    def readData(self):
        self.response = self.serial.readAll()
        print(self.response)
        data = self.response.data().decode()
        data = data.strip('>').rstrip('\r')
        self.binary_data = ''.join(format(int(c, 16), '04b') for c in data)
        global binary_data 
        binary_data = self.binary_data
    
    def getBinaryData(self):
        print(type(self.binary_data))
        return self.binary_data
    
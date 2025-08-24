from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from itertools import chain
from module import Module
from logger import logger
from time import sleep
import time
import sys
import os


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.timer = QTimer(self)
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.find_module)
        self.timer.timeout.connect(self.test_relays)
        self.timer3 = QTimer(self)
        self.timer3.setInterval(200)
        self.timer3.timeout.connect(self.label_update)
        self.timeToDance = QTimer()
        self.timeToDance.setInterval(300)
        self.timeToDance.timeout.connect(self.dance_button)
        self.module = Module()
        self.menu()
        self.main()
        self.initUI()

        self.port_LineEdit.setText('COM4')
        self.address_spinBox.setValue(0)
        self.test_btn.setEnabled(False)

        self.upper_board.currentTextChanged.connect(self.replacement_upper)
        self.down_board.currentTextChanged. connect(self.replacement_down)

        self.connect_btn.setCheckable(True)
        self.connect_btn.clicked.connect(self.connect_module)

        self.test_btn.clicked.connect(self.startStopRepeating)
        self.find_btn.setCheckable(True)
        self.find_btn.clicked.connect(self.start_find_module)

        self.module.aOut_list[1].toggled.connect(self.module.buttonPressed_A2)
        self.module.aOut_list[2].toggled.connect(self.module.buttonPressed_A3)
        self.module.aOut_list[3].toggled.connect(self.module.buttonPressed_A4)
        self.module.aOut_list[4].toggled.connect(self.module.buttonPressed_A5)
        self.module.aOut_list[5].toggled.connect(self.module.buttonPressed_A6)
        self.module.aOut_list[6].toggled.connect(self.module.buttonPressed_A7)
        self.module.aOut_list[7].toggled.connect(self.module.buttonPressed_A8)
        self.module.aOut_list[8].toggled.connect(self.module.buttonPressed_A9)

        self.module.fOut_list[1].toggled.connect(self.module.buttonPressed_F2)
        self.module.fOut_list[2].toggled.connect(self.module.buttonPressed_F3)
        self.module.fOut_list[3].toggled.connect(self.module.buttonPressed_F4)
        self.module.fOut_list[4].toggled.connect(self.module.buttonPressed_F5)
        self.module.fOut_list[5].toggled.connect(self.module.buttonPressed_F6)
        self.module.fOut_list[6].toggled.connect(self.module.buttonPressed_F7)
        self.module.fOut_list[7].toggled.connect(self.module.buttonPressed_F8)
        self.module.fOut_list[8].toggled.connect(self.module.buttonPressed_F9)

        self.module.cOut_list[1].toggled.connect(self.module.buttonPressed_C2)
        self.module.cOut_list[2].toggled.connect(self.module.buttonPressed_C3)
        self.module.cOut_list[3].toggled.connect(self.module.buttonPressed_C4)
        self.module.cOut_list[4].toggled.connect(self.module.buttonPressed_C5)
        self.module.cOut_list[5].toggled.connect(self.module.buttonPressed_C6)
        self.module.cOut_list[6].toggled.connect(self.module.buttonPressed_C7)
        self.module.cOut_list[7].toggled.connect(self.module.buttonPressed_C8)
        self.module.cOut_list[8].toggled.connect(self.module.buttonPressed_C9)

        self.module.dOut_list[1].toggled.connect(self.module.buttonPressed_D2)
        self.module.dOut_list[2].toggled.connect(self.module.buttonPressed_D3)
        self.module.dOut_list[3].toggled.connect(self.module.buttonPressed_D4)
        self.module.dOut_list[4].toggled.connect(self.module.buttonPressed_D5)
        self.module.dOut_list[5].toggled.connect(self.module.buttonPressed_D6)
        self.module.dOut_list[6].toggled.connect(self.module.buttonPressed_D7)
        self.module.dOut_list[7].toggled.connect(self.module.buttonPressed_D8)
        self.module.dOut_list[8].toggled.connect(self.module.buttonPressed_D9)
        self.AF = self.module.aOut_list[1:-1] + self.module.fOut_list[1:-1]
        self.CD = self.module.cOut_list[1:-1] + self.module.dOut_list[1:-1]


        for i in chain(self.module.aOut_list, self.module.cOut_list, self.module.dOut_list, self.module.fOut_list):
            i.setEnabled(False)

    def start_find_module(self):
        self.timer2.setInterval(200)
        self.timer2.start()

    def connect_module(self):
        if self.connect_btn.isChecked():
            self.test_btn.setEnabled(True)
            self.input_status_request = self.module.dcon.create_request(
                character='-', module_address=self.address_spinBox.value(), command=''
            )
            self.module.connection.open_serial_port(
                port=self.port_LineEdit.text(), baud_rate=115200
            )
            self.module.connection.connect()
            self.module.connection.start_automatic_requests(
                request=self.input_status_request
            )
            self.module.connection.serial.readyRead.connect(self.module.show_inputs)
            self.timer3.start()
        else:
            self.test_btn.setEnabled(False)
            self.module.connection.stop()
            self.module.flagCheckedInput = [False] * 42
            self.module.show_inputs()
            self.module.connection.flag = False
            self.timer3.stop()
    

    def label_update(self):
        try:
            self.connection_quality.setText(f'Связь: {self.module.connection.count_response / (self.module.connection.count_request + 1) * 100:.2f}%')
            logger.info(f'request {self.module.connection.count_request}')
            logger.info(f'response {self.module.connection.count_response}')
            logger.info('--------------------------')
        except:
            self.connection_quality.setText(f'Связь: 0')
    
    
    def find_module(self):
        self.address_spinBox.setValue(self.i)
        if self.address_spinBox.value() >= 255:
            self.timer2.stop()
            QMessageBox.information(self, "Информация", 'Модуль не обнаружен')
            self.i = 1
            self.find_btn.setChecked(False)
            self.i = 1
            self.address_spinBox.setValue(1)
        if self.module.connection.flag:
            self.timer2.stop()
            self.module.connection.flag = False
            self.find_btn.setChecked(False)
            self.connect_btn.setChecked(True)
            self.test_btn.setEnabled(True)
            self.address_spinBox.setValue(self.address_spinBox.value() - 1)
            return
        elif self.find_btn.isChecked():
            self.input_status_request = self.module.dcon.create_request(
                character='-', module_address=self.address_spinBox.value(), command=''
            )
            self.module.connection.open_serial_port(
                port=self.port_LineEdit.text(), baud_rate=115200
            )
            self.module.connection.connect()
            self.module.connection.start_automatic_requests(
                request=self.input_status_request
            )
            self.module.connection.serial.readyRead.connect(self.module.show_inputs)
        elif not self.find_btn.isChecked():
            self.timer2.stop()
        else:
            self.module.connection.stop()
        self.i = self.i + 1

    def to_hex_str(self, number):
        hex_str = hex(number)[2:]
        hex_number = hex_str.zfill(4).upper()
        return hex_number
    
    def startStopRepeating(self, state):
        if state == True:
            self.timer.start(200)
            self.timeToDance.start()
        else:
            self.timeToDance.stop()
            for i in chain(self.module.aOut_list, self.module.cOut_list, self.module.dOut_list, self.module.fOut_list):
                i.setChecked(False)
                i.setEnabled(False)
            QTimer.singleShot(500, self.stop_test)
            if (self.count %2) == 0:
                self.outputRelaySet = self.module.dcon.create_request('+', self.address_spinBox.value(), command='FFFF')
            else:
                self.outputRelaySet = self.module.dcon.create_request('=', self.address_spinBox.value(), command='FFFF')
            self.module.connection.change_request(self.outputRelaySet)

    
    def stop_test(self):
        self.connect_btn.setEnabled(True)
        self.timer.stop()
    
    def test_relays(self):
        self.connect_btn.setEnabled(False)
        for i in chain(self.module.aOut_list, self.module.cOut_list, self.module.dOut_list, self.module.fOut_list):
            i.setEnabled(True)
        self.count += 1
        if self.count > 100:
            self.count = 0
        

        self.commandAF = self.to_hex_str(self.module.stateAF)
        self.commandDC = self.to_hex_str(self.module.stateDC)


        if (self.count % 2) == 0:
            self.outputRelaySet = self.module.dcon.create_request('+', self.address_spinBox.value(), command=self.commandAF)
        else:
            self.outputRelaySet = self.module.dcon.create_request('=', self.address_spinBox.value(), command=self.commandDC)
        self.module.connection.change_request(self.outputRelaySet)
    
    def dance_button(self):
        try:
            next(self.step)
        except:
            for i, j in zip(self.AF, self.CD):
                i.setChecked(False)
                j.setChecked(False)
                self.step = self.button()
    
    def button(self):
        for i, j in zip(self.AF, self.CD):
            i.setChecked(True)
            j.setChecked(True)
            yield

    def replacement_upper(self, str):
        if str == 'Outputs':
            self.module.upOut()
        elif str == 'Inputs':
            self.module.upInp()

    def replacement_down(self, str):
        if str == 'Outputs':
            self.module.downOut()
        elif str == 'Inputs':
            self.module.downInp()

    def main(self):
        self.main_layout = QVBoxLayout()
        list_of_buttons = self.module.create_buttons()

        for buttons_list in list_of_buttons:
            horizontal_layout =  self.create_layout_with_buttons(buttons_list)
            self.main_layout.addLayout(horizontal_layout)
        
    def create_layout_with_buttons(self, buttons):
        layout = QHBoxLayout()
        for button in buttons:
            layout.addWidget(button)
        return layout

    def menu(self):
        self.down_board_lb  = QLabel('Нижняя плата')
        self.upper_board_lb   = QLabel('Верхняя плата')
        self.port_lb         = QLabel('Порт')
        self.address_lb      = QLabel('Адрес')
        self.connect_btn     = QPushButton('Соединение')
        self.find_btn        = QPushButton('Найти')
        self.test_btn        = QPushButton('Тестирование')
        self.upper_board     = QComboBox()
        self.down_board      = QComboBox()
        self.port_LineEdit   = QLineEdit('')
        self.address_spinBox = QSpinBox()
        self.connection_quality = QLabel(f'Связь: 0')
        self.address_spinBox.setMinimum(1)
        self.address_spinBox.setMaximum(255)
        self.i = self.address_spinBox.minimum()

        self.upper_board.addItems(['Inputs', 'Outputs'])
        self.down_board.addItems (['Inputs', 'Outputs'])
        self.connect_btn.setCheckable(True)
        self.test_btn.setCheckable(True)

        self.menu_layout = QVBoxLayout()
        self.menu_layout.addWidget(self.down_board_lb)
        self.menu_layout.addWidget(self.upper_board)
        self.menu_layout.addWidget(self.upper_board_lb)
        self.menu_layout.addWidget(self.down_board)
        self.menu_layout.addWidget(self.port_lb)
        self.menu_layout.addWidget(self.port_LineEdit)
        self.menu_layout.addWidget(self.address_lb)
        self.menu_layout.addWidget(self.address_spinBox)
        self.menu_layout.addWidget(self.connect_btn)
        self.menu_layout.addWidget(self.find_btn)
        self.menu_layout.addWidget(self.test_btn)
        self.menu_layout.addWidget(self.connection_quality)

    def initUI(self):
        self.monitor = QHBoxLayout()
        self.monitor.addLayout(self.menu_layout)
        self.monitor.addLayout(self.main_layout)

        self.setLayout(self.monitor)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

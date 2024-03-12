from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from module import Module
from logger import logger
import sys
import os


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.menu()
        self.module = Module()
        self.main()
        self.initUI()

        self.port_LineEdit.setText('COM4')
        self.address_spinBox.setValue(27)
        self.test_btn.setEnabled(False)

        self.upper_board.currentTextChanged.connect(self.replacement_upper)
        self.down_board.currentTextChanged. connect(self.replacement_down)

        self.connect_btn.setCheckable(True)
        self.connect_btn.clicked.connect(self.connect_module)

        self.test_btn.clicked.connect(self.test_relays)
        self.find_btn.clicked.connect(self.find_module_address)

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

        #self.module.cOut_list[1].toggled.connect(self.module.buttonPressed_C2)
        #self.module.cOut_list[2].toggled.connect(self.module.buttonPressed_C3)
        #self.module.cOut_list[3].toggled.connect(self.module.buttonPressed_C4)
        #self.module.cOut_list[4].toggled.connect(self.module.buttonPressed_C5)
        #self.module.cOut_list[5].toggled.connect(self.module.buttonPressed_C6)
        #self.module.cOut_list[6].toggled.connect(self.module.buttonPressed_C7)
        #self.module.cOut_list[7].toggled.connect(self.module.buttonPressed_C8)
        #self.module.cOut_list[8].toggled.connect(self.module.buttonPressed_C9)

        #self.module.dOut_list[1].toggled.connect(self.module.buttonPressed_D2)
        #self.module.dOut_list[2].toggled.connect(self.module.buttonPressed_D3)
        #self.module.dOut_list[3].toggled.connect(self.module.buttonPressed_D4)
        #self.module.dOut_list[4].toggled.connect(self.module.buttonPressed_D5)
        #self.module.dOut_list[5].toggled.connect(self.module.buttonPressed_D6)
        #self.module.dOut_list[6].toggled.connect(self.module.buttonPressed_D7)
        #self.module.dOut_list[7].toggled.connect(self.module.buttonPressed_D8)
        #self.module.dOut_list[8].toggled.connect(self.module.buttonPressed_D9)

    def connect_module(self):
        if self.connect_btn.isChecked():
            self.test_btn.setEnabled(True)
            self.inputStatusRequest = self.module.dcon.create_request(character='-', module_address=self.address_spinBox.value(), command='')
            self.module.connection.OpenSerialPort(port=self.port_LineEdit.text(), baud_rate=115200)
            self.module.connection.connect()
            self.module.connection.startAutomaticRequests(request=self.inputStatusRequest)
            self.module.connection.serial.readyRead.connect(self.module.show_inputs)
        else:
            self.test_btn.setEnabled(False)
            self.module.connection.stop()

    def test_relays(self):
        if self.test_btn.isChecked():
            self.connect_btn.setEnabled(False)
            self.outputRelaySet = self.module.dcon.create_request('+', self.address_spinBox.value(), command=self.module.state)
            self.module.connection.changeRequest(self.outputRelaySet)
        else:
            self.module.connection.changeRequest(self.inputStatusRequest)
            self.connect_btn.setEnabled(True)
            ...
    
    def find_module_address(self):
        print("find_module")

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
        self.upper_board_lb  = QLabel('Верхняя плата')
        self.down_board_lb   = QLabel('Нижняя плата')
        self.port_lb         = QLabel('Порт')
        self.address_lb      = QLabel('Адрес')
        self.connect_btn     = QPushButton('Связь')
        self.find_btn        = QPushButton('Найти')
        self.test_btn        = QPushButton('Тестирование')
        self.upper_board     = QComboBox()
        self.down_board      = QComboBox()
        self.port_LineEdit   = QLineEdit('')
        self.address_spinBox = QSpinBox()
        self.address_spinBox.setMinimum(0)
        self.address_spinBox.setMaximum(255)

        self.upper_board.addItems(['Inputs', 'Outputs'])
        self.down_board.addItems (['Inputs', 'Outputs'])
        self.connect_btn.setCheckable(True)
        self.test_btn.setCheckable(True)

        self.menu_layout = QVBoxLayout()
        self.menu_layout.addWidget(self.upper_board_lb)
        self.menu_layout.addWidget(self.upper_board)
        self.menu_layout.addWidget(self.down_board_lb)
        self.menu_layout.addWidget(self.down_board)
        self.menu_layout.addWidget(self.port_lb)
        self.menu_layout.addWidget(self.port_LineEdit)
        self.menu_layout.addWidget(self.address_lb)
        self.menu_layout.addWidget(self.address_spinBox)
        self.menu_layout.addWidget(self.connect_btn)
        self.menu_layout.addWidget(self.find_btn)
        self.menu_layout.addWidget(self.test_btn)

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

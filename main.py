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

    def connect_module(self):
        if self.connect_btn.isChecked():
            self.test_btn.setEnabled(True)
            self.InputstatusRequest = self.module.dcon.create_request(character='-', module_address=self.address_spinBox.value(), command='')
            self.module.connection.OpenSerialPort(port=self.port_LineEdit.text(), baud_rate=115200)
            self.module.connection.connect()
            self.module.connection.startAutomaticRequests(request=self.InputstatusRequest)

            self.display_input()
        else:
            self.test_btn.setEnabled(False)
            self.module.connection.disconnect()

    def test_relays(self):
        if self.test_btn.isChecked():
            self.connect_btn.setEnabled(False)
            self.outputRelaySet = self.module.request.create_request(character='+', module_address=self.address_spinBox.value(), command='ff00')
            self.module.connection.changeRequest(self.outputRelaySet)
        else:
            self.module.connection.changeRequest(self.InputstatusRequest)
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
        
    def display_input(self):
        response = self.module.connection.getData()
        data, checksum = self.module.dcon.parsedResponse(response)
        print(data, checksum)
        checksumVerificationStatus = self.module.dcon.checksum_verification(response)
        if ~checksumVerificationStatus:
            QMessageBox.information(self, 'Warning', f'Ошибка контрольной суммы')
            raise ValueError


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

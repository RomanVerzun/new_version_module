import sys

from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from module import *


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.menu()
        self.module = MODULE()
        self.main()
        self.initUI()

        self.upper_board.currentTextChanged.connect(self.replacement_upper)
        self.down_board.currentTextChanged. connect(self.replacement_down)

    def replacement_upper(self, str):
        if str == 'outputs':
            self.module.upOut()
        elif str == 'inputs':
            self.module.upInp()

    def replacement_down(self, str):
        if str == 'outputs':
            self.module.downOut()
        elif str == 'inputs':
            self.module.downInp()

    def main(self):
        self.main_layout = QVBoxLayout()

        inputC = QHBoxLayout()
        for button in self.module.iterate_dInp1():
            inputC.addWidget(button)

        inputD = QHBoxLayout()
        for button in self.module.iterate_dInp2():
            inputD.addWidget(button)

        relayC = QHBoxLayout()
        for button in self.module.iterate_dOut1():
            button.hide()
            relayC.addWidget(button)

        relayD = QHBoxLayout()
        for button in self.module.iterate_dOut2():
            button.hide()
            relayD.addWidget(button)

        inputA = QHBoxLayout()
        for button in self.module.iterate_uInp1():
            inputA.addWidget(button)

        inputF = QHBoxLayout()
        for button in self.module.iterate_uInp2():
            inputF.addWidget(button)

        relayA = QHBoxLayout()
        for button in self.module.iterate_uOut1():
            button.hide()
            relayA.addWidget(button)

        relayF = QHBoxLayout()
        for button in self.module.iterate_uOut2():
            relayF.addWidget(button)
            button.hide()

        inputB = QHBoxLayout()
        for button in self.module.iterate_processor_B():
            inputB.addWidget(button)

        inputE = QHBoxLayout()
        for button in self.module.iterate_processor_E():
            inputE.addWidget(button)

        self.main_layout.addLayout(inputF) 
        self.main_layout.addLayout(relayF) 
        self.main_layout.addLayout(inputE)  
        self.main_layout.addLayout(inputD)  
        self.main_layout.addLayout(relayD)  
        self.main_layout.addLayout(inputC)  
        self.main_layout.addLayout(relayC)  
        self.main_layout.addLayout(inputB)  
        self.main_layout.addLayout(inputA)  
        self.main_layout.addLayout(relayA)  

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

        self.upper_board.addItems(['inputs', 'outputs'])
        self.down_board.addItems (['inputs', 'outputs'])
        self.connect_btn.setCheckable(True)

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

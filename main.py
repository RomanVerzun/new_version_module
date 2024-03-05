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
            for button in self.module.iterate_upper_Inp1():
                button.hide()
            for button in self.module.iterate_upper_Inp2():
                button.hide()

            for button in self.module.iterate_upper_Out1():
                button.show()
            for button in self.module.iterate_upper_Out2():
                button.show()
        elif str == 'inputs':
            for button in self.module.iterate_upper_Inp1():
                button.show()
            for button in self.module.iterate_upper_Inp2():
                button.show()

            for button in self.module.iterate_upper_Out1():
                button.hide()
            for button in self.module.iterate_upper_Out2():
                button.hide()

    def replacement_down(self, str):
        if str == 'outputs':
            for button in self.module.iterate_down_Inp1():
                button.hide()
            for button in self.module.iterate_down_Inp2():
                button.hide()

            for button in self.module.iterate_down_Out1():
                button.show()
            for button in self.module.iterate_down_Out2():
                button.show()
        elif str == 'inputs':
            for button in self.module.iterate_down_Inp1():
                button.show()
            for button in self.module.iterate_down_Inp2():
                button.show()

            for button in self.module.iterate_down_Out1():
                button.hide()
            for button in self.module.iterate_down_Out2():
                button.hide()

    def main(self):
        self.main_layout = QVBoxLayout()

        row1 = QHBoxLayout()
        for button in self.module.iterate_down_Inp1():
            row1.addWidget(button)

        row2 = QHBoxLayout()
        for button in self.module.iterate_down_Inp2():
            row2.addWidget(button)

        row3 = QHBoxLayout()
        for button in self.module.iterate_down_Out1():
            button.hide()
            row3.addWidget(button)

        row4 = QHBoxLayout()
        for button in self.module.iterate_down_Out2():
            button.hide()
            row4.addWidget(button)

        row7 = QHBoxLayout()
        for button in self.module.iterate_upper_Inp1():
            row7.addWidget(button)

        row8 = QHBoxLayout()
        for button in self.module.iterate_upper_Inp2():
            row8.addWidget(button)

        row9 = QHBoxLayout()
        for button in self.module.iterate_upper_Out1():
            button.hide()
            row9.addWidget(button)

        row10 = QHBoxLayout()
        for button in self.module.iterate_upper_Out2():
            row10.addWidget(button)
            button.hide()

        # Процессорная плата B
        row5 = QHBoxLayout()
        for button in self.module.iterate_processor_B():
            row5.addWidget(button)

        # Процессорная плата E
        row6 = QHBoxLayout()
        for button in self.module.iterate_processor_E():
            row6.addWidget(button)

        self.main_layout.addLayout(row8)  # Input F 
        self.main_layout.addLayout(row10) # Relay F
        self.main_layout.addLayout(row6)  # Input E процессор
        self.main_layout.addLayout(row2)  # Input D
        self.main_layout.addLayout(row4)  # Relay D
        self.main_layout.addLayout(row1)  # Input C
        self.main_layout.addLayout(row3)  # Relay C
        self.main_layout.addLayout(row5)  # Input B процессор
        self.main_layout.addLayout(row7)  # Input A
        self.main_layout.addLayout(row9)  # Relay A

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

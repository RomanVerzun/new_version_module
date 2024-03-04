import sys

from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from lineIterator import *
from inputs import *
from outputs import *
from processor import *
from module import *


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.menu()
        self.module = MODULE(self.upper_board.currentText(), 'inputs')

        self.main()

        self.initUI()

    def main(self):
        self.main_layout = QVBoxLayout()

        row1 = QHBoxLayout()
        for button in self.module.iterate_upper_line1():
            print(row1)
            row1.addWidget(button)

        row2 = QHBoxLayout()
        for button in self.module.iterate_down_line1():
            row2.addWidget(button)

        row3 = QHBoxLayout()
        for button in self.module.iterate_down_line2():
            row3.addWidget(button)

        row4 = QHBoxLayout()
        for button in self.module.iterate_upper_line2():
            row4.addWidget(button)

        row5 = QHBoxLayout()
        for button in self.module.iterate_processor_B():
            row5.addWidget(button)

        row6 = QHBoxLayout()
        for button in self.module.iterate_processor_E():
            row6.addWidget(button)

        self.main_layout.addLayout(row1)
        self.main_layout.addLayout(row5)
        self.main_layout.addLayout(row2)
        self.main_layout.addLayout(row3)
        self.main_layout.addLayout(row6)
        self.main_layout.addLayout(row4)
    
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

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

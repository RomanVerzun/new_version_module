from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from lineIterator import LineIterator

class OUTPUTS:
    def __init__(self, ch1, ch2):
        self.ch1 = ch1
        self.ch2 = ch2
        self.buttons_line1 = []  # Список для хранения кнопок
        self.buttons_line2 = []  # Список для хранения кнопок
        self.create_outputs()

    def create_outputs(self):
        # Добавляем кнопки для ch1
        for i in range(1, 11):
            self.buttons_line1.append(QPushButton(f'R{self.ch1}{i:02}'))
            if i != 1 and i != 10:
                self.buttons_line1[i-1].setStyleSheet('color: black; background-color: #6666FF')
            else:
                self.buttons_line1[i-1].setStyleSheet('color: black; background-color: yellow')
                self.buttons_line1[i-1].setEnabled(False)

        
        # Добавляем кнопки для ch2
        for i in range(1, 11):
            self.buttons_line2.append(QPushButton(f'R{self.ch2}{i:02}'))
            if i != 1 and i != 10:
                self.buttons_line2[i-1].setStyleSheet('color: black; background-color: #6666FF')
            else:
                self.buttons_line2[i-1].setStyleSheet('color: black; background-color: yellow')
                self.buttons_line2[i-1].setEnabled(False)
    
    def iter_line1(self):
        return LineIterator(self.buttons_line1)
    
    def iter_line2(self):
        return LineIterator(self.buttons_line2)
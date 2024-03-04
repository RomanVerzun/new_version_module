from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from lineIterator import LineIterator

class PROCESSOR:
    def __init__(self):
        self.buttons_lineB =[]
        self.buttons_lineE =[]
        self.create_inputs()
    
    def create_inputs(self):
        for i in range(1, 11):
            self.buttons_lineB.append(QPushButton(f'IB{i:02}'))
            self.buttons_lineB[i-1].setStyleSheet('color: black; background-color: green')
            self.buttons_lineB[i-1].setEnabled(False)

        for i in range(1, 11):
            self.buttons_lineE.append(QPushButton(f'E{i:02}'))
            self.buttons_lineE[i-1].setStyleSheet('color: black; background-color: green')
            self.buttons_lineE[i-1].setEnabled(False)

    def iter_lineB(self):
        return LineIterator(self.buttons_lineB)

    def iter_lineE(self):
        return LineIterator(self.buttons_lineE)
from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from lineIterator import LineIterator

class Board_IO:
    def __init__(self, terminal_block1: str, terminal_block2: str, ioStatus: str):
        self.SIZE = [i for i in range(1, 11)]
        self.terminal_block1 = terminal_block1
        self.terminal_block2 = terminal_block2
        self.ioStatus = ioStatus
        self.terminals1 = self.create_io(terminal_block1)
        self.terminals2 = self.create_io(terminal_block2)

    def create_io(self, terminal_block):
        buttons = [self.create_button(f'{self.ioStatus}{terminal_block}{i:02}', i) for i in self.SIZE]
        return buttons

    def create_button(self, text, index):
        button = QPushButton(text)
        if self.ioStatus == 'R':
            button.setEnabled(True)
            bg = 'blue'
        elif self.ioStatus == 'I':
            button.setEnabled(False)
            bg = 'green'
        color, background = ('black', 'yellow') if index in [self.SIZE[0], self.SIZE[-1]] else ('black', bg)
        button.setStyleSheet(f'color: {color}; background-color: {background}')
        return button

    def iter_terminals1(self):
        return LineIterator(self.terminals1)
    
    def iter_terminals2(self):
        return LineIterator(self.terminals2)
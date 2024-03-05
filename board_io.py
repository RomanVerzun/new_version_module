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
        color, background = ('black', 'yellow') if index in [self.SIZE[0], self.SIZE[-1]] else ('black', self.bg)
        button.setStyleSheet(f'color: {color}; background-color: {background}')
        if background != self.bg or background == 'green':
            button.setEnabled(False)
        return button
    
    def iter_terminals1(self):
        return LineIterator(self.terminals1)
    
    def iter_terminals2(self):
        return LineIterator(self.terminals2)
    

class INPUTS(Board_IO):
    def __init__(self, terminal_block1: str, terminal_block2: str):
        self.bg = 'green'
        super().__init__(terminal_block1, terminal_block2, ioStatus='I')


class OUTPUTS(Board_IO):
    def __init__(self, terminal_block1: str, terminal_block2: str):
        self.bg = '#66ffff'
        super().__init__(terminal_block1, terminal_block2, ioStatus='R')


class PROCESSOR(Board_IO):
    def __init__(self):
        self.bg = 'green'
        super().__init__(terminal_block1='B', terminal_block2='E', ioStatus='I')
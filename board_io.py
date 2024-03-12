from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from iterator import Iterator
from logger import logger
import relays as rel

class Board_IO:
    def __init__(self, terminal_block1: str, terminal_block2: str, ioStatus: str):
        self.SIZE = [i for i in range(1, 11)]
        self.terminal_block1 = terminal_block1
        self.terminal_block2 = terminal_block2
        self.ioStatus = ioStatus
        self.terminals1 = self.create_io(terminal_block1)
        self.terminals2 = self.create_io(terminal_block2)

        #logger.info(f'{self.terminals1}')

        self.all_terminals = list()
        self.all_terminals.extend(self.terminals1)
        self.all_terminals.extend(self.terminals2)

    def get_terminals(self):
        return self.all_terminals

    def create_io(self, terminal_block):
        buttons = [self.create_button(f'{self.ioStatus}{terminal_block}{i:02}', i) for i in self.SIZE]
        return buttons

    def create_button(self, text, index):
        button = QPushButton(text)
        color, background = ('black', 'yellow') if index in [self.SIZE[0], self.SIZE[-1]] else ('black', self.bg)
        button.setStyleSheet(f'color: {color}; background-color: {background}')
        button.setCheckable(True)
        return button
    
    def disable_button(self):
        for btn in self.all_terminals:
            btn.setEnabled(False)
    
    def enable_button(self):
        for btn in self.all_terminals:
            btn.setEnabled(True)
        extreme_buttons = [self.terminals1[0], self.terminals1[-1], self.terminals2[0], self.terminals2[-1]]
        for btn in extreme_buttons:
            btn.setEnabled(False)
    
    def iter_terminals1(self):
        return Iterator(self.terminals1)
    
    def iter_terminals2(self):
        return Iterator(self.terminals2)
    
    def show(self):
        for btn in self.all_terminals:
            btn.show()
    
    def hide(self):
        for btn in self.all_terminals:
            btn.hide()
    

class Inputs(Board_IO):
    def __init__(self, terminal_block1: str, terminal_block2: str):
        self.bg = 'green'
        super().__init__(terminal_block1, terminal_block2, ioStatus='I')
        self.disable_button()
    

class Outputs(Board_IO):
    def __init__(self, terminal_block1: str, terminal_block2: str):
        self.bg = '#66ffff'
        super().__init__(terminal_block1, terminal_block2, ioStatus='R')
        self.enable_button()
        self.state = rel.MASK_R
        self.test_relays()
    
    def getState(self):
        logger.info(f'{self.state}')
    
    def test_relays(self):
        ...
    def relay1_1(self):    
        if self.terminals1[1].isChecked():
            self.state = self.state & rel.RELAY_A01
        else:
            self.state = self.state | (~rel.RELAY_A01 & rel.MASK_R)

    def relay1_2(self):
        if self.terminals1[2].isChecked():
            logger.info("!!!HELLPP")
            self.state = self.state & rel.RELAY_A02
        else:
            self.state = self.state | (~rel.RELAY_A02 & rel.MASK_R)

        if self.terminals1[3].isChecked():
            self.state = self.state & rel.RELAY_A03
        else:
            self.state = self.state | (~rel.RELAY_A03 & rel.MASK_R)

        if self.terminals1[4].isChecked():
            self.state = self.state & rel.RELAY_A04
        else:
            self.state = self.state | (~rel.RELAY_A04 & rel.MASK_R)

        if self.terminals1[5].isChecked():
            self.state = self.state & rel.RELAY_A05
        else:
            self.state = self.state | (~rel.RELAY_A05 & rel.MASK_R)

        if self.terminals1[6].isChecked():
            self.state = self.state & rel.RELAY_A06
        else:
            self.state = self.state | (~rel.RELAY_A06 & rel.MASK_R)

        if self.terminals1[7].isChecked():
            self.state = self.state & rel.RELAY_A07
        else:
            self.state = self.state | (~rel.RELAY_A07 & rel.MASK_R)

        if self.terminals1[8].isChecked():
            self.state = self.state & rel.RELAY_A08
        else:
            self.state = self.state | (~rel.RELAY_A08 & rel.MASK_R)
        


class Processor(Board_IO):
    def __init__(self):
        self.bg = 'green'
        super().__init__(terminal_block1='B', terminal_block2='E', ioStatus='I')
        self.disable_button()
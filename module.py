from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *
    

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


class LineIterator:
    def __init__(self, buttons):
        self.buttons = buttons
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.buttons):
            result = self.buttons[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration


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
            self.buttons_line1[i-1].setStyleSheet('color: black; background-color: #6666FF')
        
        # Добавляем кнопки для ch2
        for i in range(1, 11):
            self.buttons_line2.append(QPushButton(f'R{self.ch2}{i:02}'))
            self.buttons_line2[i-1].setStyleSheet('color: black; background-color: #6666FF')
    
    def iter_line1(self):
        return LineIterator(self.buttons_line1)
    
    def iter_line2(self):
        return LineIterator(self.buttons_line2)


class INPUTS:
    def __init__(self, ch1, ch2):
        self.ch1 = ch1
        self.ch2 = ch2
        self.buttons_line1 = []  # Список для хранения кнопок
        self.buttons_line2 = []  # Список для хранения кнопок
        self.create_inputs()

    def create_inputs(self):
        # Добавляем кнопки для ch1
        for i in range(1, 11):
            self.buttons_line1.append(QPushButton(f'I{self.ch1}{i:02}'))
            self.buttons_line1[i-1].setEnabled(False)
            self.buttons_line1[i-1].setStyleSheet('color: black; background-color: green')
        
        # Добавляем кнопки для ch2
        for i in range(1, 11):
            self.buttons_line2.append(QPushButton(f'I{self.ch2}{i:02}'))
            self.buttons_line2[i-1].setEnabled(False)
            self.buttons_line2[i-1].setStyleSheet('color: black; background-color: green')

    def iter_line1(self):
        return LineIterator(self.buttons_line1)
    
    def iter_line2(self):
        return LineIterator(self.buttons_line2)


class MODULE:
    def __init__(self, t1='inputs', t2='inputs'):
        self.processor = PROCESSOR()

        if t1 == 'inputs':
            self.upper_board = INPUTS ('A', 'F')
        elif t1 == 'outputs':
            self.upper_board = OUTPUTS('A', 'F')

        if t2 == 'inputs':
            self.down_board  = INPUTS ('C', 'D')
        elif t2 == 'outputs':
            self.down_board  = OUTPUTS('C', 'D')
    
    def iterate_upper_line1(self):
        return self.upper_board.iter_line1()
    
    def iterate_upper_line2(self):
        return self.upper_board.iter_line2()
    
    def iterate_down_line1(self):
        return self.down_board.iter_line1()
    
    def iterate_down_line2(self):
        return self.down_board.iter_line2()
    
    def iterate_processor_B(self):
        return self.processor.iter_lineB()
    
    def iterate_processor_E(self):
        return self.processor.iter_lineE()

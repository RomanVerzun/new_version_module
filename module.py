from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from processor import PROCESSOR
from inputs import INPUTS
from outputs import OUTPUTS
    

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

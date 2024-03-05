from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from board_io import PROCESSOR, INPUTS, OUTPUTS
    

class MODULE:
    def __init__(self, t1='inputs', t2='inputs'):
        self.processor = PROCESSOR()

        self.upper_boardInp = INPUTS('A', 'F')
        self.upper_boardOut = OUTPUTS('A', 'F')
        self.down_boardInp  = INPUTS('C', 'D')
        self.down_boardOut  = OUTPUTS('C', 'D')
    
    def iterate_upper_Inp1(self):
        return self.upper_boardInp.iter_terminals1()
    
    def iterate_upper_Inp2(self):
        return self.upper_boardInp.iter_terminals2()
    
    def iterate_down_Inp1(self):
        return self.down_boardInp.iter_terminals1()
    
    def iterate_down_Inp2(self):
        return self.down_boardInp.iter_terminals2()
    
    def iterate_upper_Out1(self):
        return self.upper_boardOut.iter_terminals1()
    
    def iterate_upper_Out2(self):
        return self.upper_boardOut.iter_terminals2()
    
    def iterate_down_Out1(self):
        return self.down_boardOut.iter_terminals1()
    
    def iterate_down_Out2(self):
        return self.down_boardOut.iter_terminals2()
    
    def iterate_processor_B(self):
        return self.processor.iter_terminals1()
    
    def iterate_processor_E(self):
        return self.processor.iter_terminals2()

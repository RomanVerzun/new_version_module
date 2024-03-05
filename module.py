from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from processor import PROCESSOR
from module_io import Board_IO
#from outputs import OUTPUTS
    

class MODULE:
    def __init__(self, t1='inputs', t2='inputs'):
        self.processor = PROCESSOR()

        self.upper_boardInp = Board_IO('A', 'F', 'I')
        self.upper_boardOut = Board_IO('A', 'F', 'R')
        self.down_boardInp  = Board_IO('C', 'D', 'I')
        self.down_boardOut  = Board_IO('C', 'D', 'R')
    
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
        return self.processor.iter_terminalsB()
    
    def iterate_processor_E(self):
        return self.processor.iter_terminalsE()

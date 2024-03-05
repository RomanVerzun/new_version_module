from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from board_io import PROCESSOR, INPUTS, OUTPUTS
    

class MODULE:
    def __init__(self):
        # upper board input
        self.uBoardInp = INPUTS('A', 'F')
        self.uBoardOut = OUTPUTS('A', 'F')

        # down board input
        self.dBoardInp = INPUTS('C', 'D')
        self.dBoardOut = OUTPUTS('C', 'D')

        # processor
        self.processor = PROCESSOR()
    
    def upInp(self):
        """Show upper board input"""
        for btn in self.uBoardInp.get_terminals():
            btn.show()
        for btn in self.uBoardOut.get_terminals():
            btn.hide()

    def upOut(self):
        """Show upper board output"""
        for btn in self.uBoardInp.get_terminals():
            btn.hide()
        for btn in self.uBoardOut.get_terminals():
            btn.show()

    def downInp(self):
        """Show down board input"""
        for btn in self.dBoardInp.get_terminals():
            btn.show()
        for btn in self.dBoardOut.get_terminals():
            btn.hide()

    def downOut(self):
        """Show down board output"""
        for btn in self.dBoardOut.get_terminals():
            btn.show()
        for btn in self.dBoardInp.get_terminals():
            btn.hide()

    def iterate_uInp1(self):
        return self.uBoardInp.iter_terminals1()
    
    def iterate_uInp2(self):
        return self.uBoardInp.iter_terminals2()
    
    def iterate_dInp1(self):
        return self.dBoardInp.iter_terminals1()
    
    def iterate_dInp2(self):
        return self.dBoardInp.iter_terminals2()
    
    def iterate_uOut1(self):
        return self.uBoardOut.iter_terminals1()
    
    def iterate_uOut2(self):
        return self.uBoardOut.iter_terminals2()
    
    def iterate_dOut1(self):
        return self.dBoardOut.iter_terminals1()
    
    def iterate_dOut2(self):
        return self.dBoardOut.iter_terminals2()
    
    def iterate_processor_B(self):
        return self.processor.iter_terminals1()
    
    def iterate_processor_E(self):
        return self.processor.iter_terminals2()

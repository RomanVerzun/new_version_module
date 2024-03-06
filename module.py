from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from board_io       import PROCESSOR, INPUTS, OUTPUTS
from connection     import SerialConnection
from dcon_protocol  import Dcon
    

class MODULE:
    def __init__(self):
        # upper board input
        self.uBoardInp  = INPUTS('A', 'F')
        self.uBoardOut  = OUTPUTS('A', 'F')

        # down board input
        self.dBoardInp  = INPUTS('C', 'D')
        self.dBoardOut  = OUTPUTS('C', 'D')

        # processor
        self.processor  = PROCESSOR()

        self.connection = SerialConnection()
        self.request    = Dcon()
    
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

    def iterate_cInp(self):
        return self.uBoardInp.iter_terminals1()
    
    def iterate_dInp(self):
        return self.uBoardInp.iter_terminals2()
    
    def iterate_aInp(self):
        return self.dBoardInp.iter_terminals1()
    
    def iterate_fInp(self):
        return self.dBoardInp.iter_terminals2()
    
    def iterate_cOut(self):
        return self.uBoardOut.iter_terminals1()
    
    def iterate_dOut(self):
        return self.uBoardOut.iter_terminals2()
    
    def iterate_aOut(self):
        return self.dBoardOut.iter_terminals1()
    
    def iterate_fOut(self):
        return self.dBoardOut.iter_terminals2()
    
    def iterate_processor_B(self):
        return self.processor.iter_terminals1()
    
    def iterate_processor_E(self):
        return self.processor.iter_terminals2()

    def create_buttons(self):

        aInp_list = list()
        for button in self.iterate_aInp():
            aInp_list.append(button)

        cInp_list = list()
        for button in self.iterate_cInp():
            cInp_list.append(button)
        
        dInp_list = list()
        for button in self.iterate_dInp():
            dInp_list.append(button)

        fInp_list = list()
        for button in self.iterate_fInp():
            fInp_list.append(button)

        aOut_list = list()
        for button in self.iterate_aOut():
            button.hide()
            aOut_list.append(button)

        cOut_list = list()
        for button in self.iterate_cOut():
            button.hide()
            cOut_list.append(button)

        dOut_list = list()
        for button in self.iterate_dOut():
            button.hide()
            dOut_list.append(button)

        fOut_list = list()
        for button in self.iterate_fOut():
            button.hide()
            fOut_list.append(button)
        
        b_list = list()
        for button in self.iterate_processor_B():
            b_list.append(button)

        e_list = list()
        for button in self.iterate_processor_E():
            e_list.append(button)
        
        return [
            dInp_list, 
            dOut_list, 
            e_list,
            fInp_list,
            fOut_list,
            aInp_list, 
            aOut_list, 
            b_list, 
            cInp_list, 
            cOut_list, 
        ]
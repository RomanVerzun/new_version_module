from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from board_io           import Processor, Inputs, Outputs
from SerialConnection   import SerialConnection
from dcon               import Dcon
from logger             import logger

class Module:
    def __init__(self):
        # upper board input
        self.uBoardInp  = Inputs('A', 'F')
        self.uBoardOut  = Outputs('A', 'F')

        # down board input
        self.dBoardInp  = Inputs('C', 'D')
        self.dBoardOut  = Outputs('C', 'D')

        # Processor
        self.Processor  = Processor()

        self.dcon       = Dcon()
        self.connection = SerialConnection()

    def connect(self, port:str, character, module_address, command, baud_rate=115200):
        req = self.dcon.create_request(character=self.character, module_address=self.module_address, command=self.command)
        self.connection.OpenSerialPort(port=port, baud_rate=baud_rate)
        self.connection.startAutomaticRequests(req)

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
    
    def iterate_Processor_B(self):
        return self.Processor.iter_terminals1()
    
    def iterate_Processor_E(self):
        return self.Processor.iter_terminals2()

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
        for button in self.iterate_Processor_B():
            b_list.append(button)

        e_list = list()
        for button in self.iterate_Processor_E():
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
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
    
    def show_inputs(self):
        response = self.connection.getData()
        data, checksum = self.dcon.parsedResponse(response)
        checksumVerificationStatus = self.dcon.checksum_verification(response)
        binary_data = ''.join(format(int(c, 16), '04b') for c in data)

        activeInput     = 'red'
        inactiveInput   = 'green'
        #for index, i in enumerate(self.aInp_list, start=16):
        #    color = activeInput if binary_data[2] == '0' else inactiveInput
        #    i.setStyleSheet(f'color: "black; background-color:{color}')

        for i in self.cInp_list:
            ...

        for i in self.dInp_list:
            ...

        for i in self.fInp_list:
            ...


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

    def iterate_aInp(self):
        return self.uBoardInp.iter_terminals1()
    
    def iterate_fInp(self):
        return self.uBoardInp.iter_terminals2()
    
    def iterate_cInp(self):
        return self.dBoardInp.iter_terminals1()
    
    def iterate_dInp(self):
        return self.dBoardInp.iter_terminals2()
    
    def iterate_aOut(self):
        return self.uBoardOut.iter_terminals1()
    
    def iterate_fOut(self):
        return self.uBoardOut.iter_terminals2()
    
    def iterate_cOut(self):
        return self.dBoardOut.iter_terminals1()
    
    def iterate_dOut(self):
        return self.dBoardOut.iter_terminals2()
    
    def iterate_Processor_B(self):
        return self.Processor.iter_terminals1()
    
    def iterate_Processor_E(self):
        return self.Processor.iter_terminals2()

    def create_buttons(self):

        self.aInp_list = list()
        for button in self.iterate_aInp():
            self.aInp_list.append(button)

        self.cInp_list = list()
        for button in self.iterate_cInp():
            self.cInp_list.append(button)
        
        self.dInp_list = list()
        for button in self.iterate_dInp():
            self.dInp_list.append(button)

        self.fInp_list = list()
        for button in self.iterate_fInp():
            self.fInp_list.append(button)

        self.aOut_list = list()
        for button in self.iterate_aOut():
            button.hide()
            self.aOut_list.append(button)

        self.cOut_list = list()
        for button in self.iterate_cOut():
            button.hide()
            self.cOut_list.append(button)

        self.dOut_list = list()
        for button in self.iterate_dOut():
            button.hide()
            self.dOut_list.append(button)

        self.fOut_list = list()
        for button in self.iterate_fOut():
            button.hide()
            self.fOut_list.append(button)
        
        self.b_list = list()
        for button in self.iterate_Processor_B():
            self.b_list.append(button)

        self.e_list = list()
        for button in self.iterate_Processor_E():
            self.e_list.append(button)
        
        return [
            self.fInp_list, 
            self.fOut_list, 
            self.e_list,
            self.dInp_list,
            self.dOut_list,
            self.cInp_list, 
            self.cOut_list, 
            self.b_list, 
            self.aInp_list, 
            self.aOut_list, 
        ]
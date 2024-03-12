from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from SerialConnection   import SerialConnection
from board_io    import Processor, Inputs, Outputs
from dcon        import Dcon
from logger      import logger
from relays      import *

class Module:
    def __init__(self):
        # upper board input
        self.uBoardInp  = Inputs('A', 'F')
        self.uBoardOut  = Outputs('A', 'F')
        self.uBoardOut.terminals1[0].clicked.connect(self.uBoardOut.relay1_1)

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

        activeInput     = f'color: "black"; background-color: red'
        inactiveInput   = f'color: "black"; background-color: green'

        def input_style(binary_index, list_index, inp_list):
            style = activeInput if binary_data[binary_index] == '0' else inactiveInput
            inp_list[list_index].setStyleSheet(style)
        
        for binary_index, list_index in zip(range(23, 15, -1), range(1, 9)):
            input_style(binary_index, list_index, self.aInp_list)
        
        for binary_index, list_index in zip(range(33, 30, -1), range(6, 9)):
            input_style(binary_index, list_index, self.b_list)
        
        for binary_index, list_index in zip(range(39, 31, -1), range(1, 9)):
            input_style(binary_index, list_index, self.cInp_list)
        
        d_indices = [(0, 1), (1, 2), (30, 3), (31, 4), (5, 5), (4, 6), (3, 7), (2, 8)]
        for binary_index, list_index in d_indices:
            input_style(binary_index, list_index, self.dInp_list)
        
        e_indices = [(29, 1), (28, 2), (27, 3), (26, 4), (25, 5), (24, 6), (7, 7), (6, 8)]
        for binary_index, list_index in e_indices:
            input_style(binary_index, list_index, self.e_list)
        
        for binary_index, list_index in zip(range(15, 7, -1), range(1, 9)):
            input_style(binary_index, list_index, self.fInp_list)


       # input_style(33, 6, self.b_list)
       # input_style(32, 7, self.b_list)
       # input_style(31, 8, self.b_list)
       #input_style(39, 1, self.cInp_list)
       #input_style(38, 2, self.cInp_list)
       #input_style(37, 3, self.cInp_list)
       #input_style(36, 4, self.cInp_list)
       #input_style(35, 5, self.cInp_list)
       #input_style(34, 6, self.cInp_list)
       #input_style(33, 7, self.cInp_list)
       #input_style(32, 8, self.cInp_list)
#
        #input_style(0, 1, self.dInp_list)
        #input_style(1, 2, self.dInp_list)
        #input_style(30, 3, self.dInp_list)
        #input_style(31, 4, self.dInp_list)
        #input_style(5, 5, self.dInp_list)
        #input_style(4, 6, self.dInp_list)
        #input_style(3, 7, self.dInp_list)
        #input_style(2, 8, self.dInp_list)
#
        #input_style(29, 1, self.e_list)
        #input_style(28, 2, self.e_list)
        #input_style(27, 3, self.e_list)
        #input_style(26, 4, self.e_list)
        #input_style(25, 5, self.e_list)
        #input_style(24, 6, self.e_list)
        #input_style(7, 7, self.e_list)
        #input_style(6, 8, self.e_list)
#
        #input_style(15, 1, self.fInp_list)
        #input_style(14, 2, self.fInp_list)
        #input_style(13, 3, self.fInp_list)
        #input_style(12, 4, self.fInp_list)
        #input_style(11, 5, self.fInp_list)
        #input_style(10, 6, self.fInp_list)
        #input_style(9, 7, self.fInp_list)
        #input_style(8, 8, self.fInp_list)


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
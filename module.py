from PyQt6.QtWidgets import *
from PyQt6.QtCore    import *
from PyQt6.QtGui     import *

from SerialConnection   import SerialConnection
from board_io    import Processor, Inputs, Outputs
from dcon        import Dcon
from logger      import logger
import relays  as rel

class Module:
    def __init__(self):
        self.stateAF = rel.MASK_R
        self.stateDC = rel.MASK_R
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
        self.flagCheckedInput = [False] * 42

    def connect(self, port:str, character, module_address, command, baud_rate=115200):
        req = self.dcon.create_request(character=self.character, module_address=self.module_address, command=self.command)
        self.connection.OpenSerialPort(port=port, baud_rate=baud_rate)
        self.connection.startAutomaticRequests(req)
    
    def show_inputs(self):
        response = self.connection.getData()
        data, checksum = self.dcon.parsedResponse(response)
        checksumVerificationStatus = self.dcon.checksum_verification(response)
        try:
            binary_data = ''.join(format(int(c, 16), '04b') for c in data)
        except:
            pass

        activeInput     = f'color: "black"; background-color: red'
        inactiveInput   = f'color: "black"; background-color: gray'
        inputchecked    = f'color: "black"; background-color: green'

        def input_style(binary_index, list_index, inp_list):
            try:
                if binary_data[binary_index] == '0':
                    style = activeInput
                    self.flagCheckedInput[binary_index] = True
                elif binary_data[binary_index] == '1' and self.flagCheckedInput[binary_index]:
                    style = inputchecked
                else:
                    style = inactiveInput
                
                inp_list[list_index].setStyleSheet(style)
            except:
                pass
        
        for binary_index, list_index in zip(range(23, 15, -1), range(1, 9)):
            input_style(binary_index, list_index, self.aInp_list)
        
        for binary_index, list_index in zip(range(34, 31, -1), range(6, 9)):
            input_style(binary_index, list_index, self.b_list)
        
        for binary_index, list_index in zip(range(39, 34, -1), range(1, 6)):
            input_style(binary_index, list_index, self.cInp_list)
        
        d_indices = [(0, 1), (1, 2), (30, 3), (31, 4), (5, 5), (4, 6), (3, 7), (2, 8)]
        for binary_index, list_index in d_indices:
            input_style(binary_index, list_index, self.dInp_list)
        
        e_indices = [(29, 1), (28, 2), (27, 3), (26, 4), (25, 5), (24, 6), (7, 7), (6, 8)]
        for binary_index, list_index in e_indices:
            input_style(binary_index, list_index, self.e_list)
        
        for binary_index, list_index in zip(range(15, 7, -1), range(1, 9)):
            input_style(binary_index, list_index, self.fInp_list)
    
    
    def updateStateAF(self, relay, state):
        if state:
            self.stateAF = self.stateAF | relay
        else:
            self.stateAF = self.stateAF & (~relay & rel.MASK_R)
        return self.stateAF

    def buttonPressed_A2(self, state):
        self.updateStateAF(rel.RELAY_A02, state)
        
    def buttonPressed_A3(self, state):
        self.updateStateAF(rel.RELAY_A03, state)
    
    def buttonPressed_A4(self, state):
        self.updateStateAF(rel.RELAY_A04, state)
    
    def buttonPressed_A5(self, state):
        self.updateStateAF(rel.RELAY_A05, state)
    
    def buttonPressed_A6(self, state):
        self.updateStateAF(rel.RELAY_A06, state)
    
    def buttonPressed_A7(self, state):
        self.updateStateAF(rel.RELAY_A07, state)
    
    def buttonPressed_A8(self, state):
        self.updateStateAF(rel.RELAY_A08, state)
    
    def buttonPressed_A9(self, state):
        self.updateStateAF(rel.RELAY_A09, state)


    def buttonPressed_F2(self, state):
        self.updateStateAF(rel.RELAY_F02, state)
        
    def buttonPressed_F3(self, state):
        self.updateStateAF(rel.RELAY_F03, state)
    
    def buttonPressed_F4(self, state):
        self.updateStateAF(rel.RELAY_F04, state)
    
    def buttonPressed_F5(self, state):
        self.updateStateAF(rel.RELAY_F05, state)
    
    def buttonPressed_F6(self, state):
        self.updateStateAF(rel.RELAY_F06, state)
    
    def buttonPressed_F7(self, state):
        self.updateStateAF(rel.RELAY_F07, state)
    
    def buttonPressed_F8(self, state):
        self.updateStateAF(rel.RELAY_F08, state)
    
    def buttonPressed_F9(self, state):
        self.updateStateAF(rel.RELAY_F09, state)

    def updateStateDC(self, relay, state):
        if state:
            self.stateDC = self.stateDC | relay
        else:
            self.stateDC = self.stateDC & (~relay & rel.MASK_R)
        return self.stateDC

    def buttonPressed_C2(self, state):
        self.updateStateDC(rel.RELAY_C02, state)
        
    def buttonPressed_C3(self, state):
        self.updateStateDC(rel.RELAY_C03, state)
    
    def buttonPressed_C4(self, state):
        self.updateStateDC(rel.RELAY_C04, state)
    
    def buttonPressed_C5(self, state):
        self.updateStateDC(rel.RELAY_C05, state)
    
    def buttonPressed_C6(self, state):
        self.updateStateDC(rel.RELAY_C06, state)
    
    def buttonPressed_C7(self, state):
        self.updateStateDC(rel.RELAY_C07, state)
    
    def buttonPressed_C8(self, state):
        self.updateStateDC(rel.RELAY_C08, state)
    
    def buttonPressed_C9(self, state):
        self.updateStateDC(rel.RELAY_C09, state)

    def buttonPressed_D2(self, state):
        self.updateStateDC(rel.RELAY_D02, state)
        
    def buttonPressed_D3(self, state):
        self.updateStateDC(rel.RELAY_D03, state)
    
    def buttonPressed_D4(self, state):
        self.updateStateDC(rel.RELAY_D04, state)
    
    def buttonPressed_D5(self, state):
        self.updateStateDC(rel.RELAY_D05, state)
    
    def buttonPressed_D6(self, state):
        self.updateStateDC(rel.RELAY_D06, state)
    
    def buttonPressed_D7(self, state):
        self.updateStateDC(rel.RELAY_D07, state)
    
    def buttonPressed_D8(self, state):
        self.updateStateDC(rel.RELAY_D08, state)
    
    def buttonPressed_D9(self, state):
        self.updateStateDC(rel.RELAY_D09, state)
    
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
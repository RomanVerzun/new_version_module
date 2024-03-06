import serial
from dcon_protocol import Dcon

class Connection():
    def __init__(self, port='COM4', address=0, baud_rate=115200) -> None:
        self.port       = port
        self.address    = address
        self.baud_rate  = baud_rate
        self.read_inputs = '-'
        self.write_outputs = ''
    
    def connect(self):
        try:
            with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
                if ser.is_open:
                    ...
        except Exception as e:
            print(e)
    
    def request(self, command, address):
        req = Dcon()
        req.create_request('-', 27, '')
        return req

if __name__ == '__main__':
    con = Connection(port='COM4', address='', baud_rate=115200)
    con.request('+', 27)
from logger import logger

class Dcon():
    def __init__(self):
        ...

    def create_request(self, character, module_address, command):
        if module_address is None:
            raise ValueError("Module address can't be None")
        address = str(hex(module_address))[2:].upper().zfill(2)
        request_string = f"{character}{address}{command}"
        checksum = self.create_checksum(request_string)
        return (request_string + checksum + '\r')

    def create_checksum(self, request_string):
        sum_ascii = sum(ord(char) for char in request_string)
        checksum_hex = hex(sum_ascii)[-2:].upper()
        return checksum_hex
    
    def checksum_verification(self, response):
        #print(response)
        data     = response[:-2]
        x = sum(ord(char) for char in data)
    
    def parsedResponse(self, response):
        data     = response[:-2]
        checksum = response[-2:]
        return data, checksum
"""Improved serial connection with better error handling and configuration."""

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QTimer, QByteArray
from logger import setup_logger
from dcon import Dcon
from util import safe_operation, retry
from config import config

logger = setup_logger(__name__)


class SerialConnectionError(Exception):
    """Custom exception for serial connection errors."""
    pass


class SerialConnection:
    """Improved serial connection class with better error handling."""
    
    def __init__(self):
        super().__init__()
        self.count_request = 0
        self.count_response = 0
        self.serial = QSerialPort()
        self.timer = QTimer()
        self.flag = False
        self.data = ""
        self.is_connected = False
        
        # Get timer interval from config
        self.timer_interval = config.get('serial.timer_interval', 100)
    
    def OpenSerialPort(self, port: str, baud_rate: int = None):
        """Configure serial port with validation."""
        if not port:
            raise SerialConnectionError("Port name cannot be empty")
        
        if baud_rate is None:
            baud_rate = config.get('serial.default_baud_rate', 115200)
        
        with safe_operation(f"Configuring serial port {port}"):
            self.serial.setPortName(port)
            self.serial.setBaudRate(baud_rate)
            logger.info(f"Serial port configured: {port} @ {baud_rate}")
    
    @retry(max_attempts=3, delay=0.5)
    def connect(self):
        """Connect to serial port with retry logic."""
        if self.is_connected:
            logger.warning("Already connected to serial port")
            return
        
        try:
            if not self.serial.open(QSerialPort.OpenModeFlag.ReadWrite):
                raise SerialConnectionError(
                    f"Failed to open serial port: {self.serial.errorString()}"
                )
            self.is_connected = True
            logger.info("Serial connection established")
        except Exception as e:
            logger.error(f"Failed to connect to serial port: {e}")
            raise SerialConnectionError(f"Connection failed: {e}")
    
    def disconnect(self):
        """Safely disconnect from serial port."""
        try:
            self.stop()
            if self.serial.isOpen():
                self.serial.close()
            self.is_connected = False
            logger.info("Serial connection closed")
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
    
    def stop(self):
        """Stop communication and clean up resources."""
        try:
            if self.timer.isActive():
                self.timer.stop()
            
            # Safely disconnect signals
            try:
                self.serial.readyRead.disconnect()
            except TypeError:
                pass  # No connections to disconnect
            
            logger.info("Communication stopped")
        except Exception as e:
            logger.error(f"Error stopping communication: {e}")
    
    def startAutomaticRequests(self, request):
        """Start automatic request sending with improved error handling."""
        if not self.is_connected:
            raise SerialConnectionError("Not connected to serial port")
        
        self.timer.start(self.timer_interval)
        self.dcon = request
        
        # Safely disconnect existing connections
        try:
            self.timer.timeout.disconnect()
        except TypeError:
            pass
        
        try:
            self.serial.readyRead.disconnect()
        except TypeError:
            pass
        
        # Connect new signals
        self.timer.timeout.connect(self.writeData)
        self.serial.readyRead.connect(self.readData)
        
        logger.info("Automatic requests started")
    
    def changeRequest(self, request):
        """Change the current request being sent."""
        self.dcon = request
        logger.debug(f"Request changed to: {request}")
    
    def writeData(self):
        """Write data to serial port with error handling."""
        try:
            if not self.is_connected or not hasattr(self, 'dcon'):
                return
            
            data_to_send = self.dcon.encode()
            bytes_written = self.serial.write(data_to_send)
            
            if bytes_written == -1:
                logger.error(f"Failed to write data: {self.serial.errorString()}")
                return
            
            if self.flag:
                self.count_request += 1
                logger.debug(f'Request sent: {self.dcon}')
            else:
                self.count_request = 0
                self.count_response = 0
                
        except Exception as e:
            logger.error(f"Error writing data: {e}")
    
    def readData(self):
        """Read data from serial port with improved error handling."""
        try:
            if not self.is_connected:
                return
            
            response = self.serial.readAll()
            if response.isEmpty():
                logger.debug("Received empty response")
                return
            
            try:
                self.data = response.data().decode('utf-8')
                self.flag = True
                
                if self.flag:
                    self.count_response += 1
                    logger.debug(f'Response received: {self.data}')
                    
            except UnicodeDecodeError as e:
                logger.error(f"Failed to decode response: {e}")
                
        except Exception as e:
            logger.error(f'Error reading data: {e}')
    
    def getData(self):
        """Get the last received data with proper error handling."""
        if not hasattr(self, 'data'):
            logger.warning("No data available")
            return ""
        return self.data
    
    def get_connection_quality(self) -> float:
        """Calculate connection quality as percentage."""
        if self.count_request == 0:
            return 0.0
        return (self.count_response / self.count_request) * 100
    
    def is_port_available(self, port_name: str) -> bool:
        """Check if a serial port is available."""
        available_ports = [port.portName() for port in QSerialPortInfo.availablePorts()]
        return port_name in available_ports
    
    @staticmethod
    def get_available_ports() -> list:
        """Get list of available serial ports."""
        return [port.portName() for port in QSerialPortInfo.availablePorts()]
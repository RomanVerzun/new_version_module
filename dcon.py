"""Improved DCON protocol handler with better validation and error handling."""

from logger import setup_logger
from util import validate_address
from typing import Tuple, Optional

logger = setup_logger(__name__)


class DconError(Exception):
    """Custom exception for DCON protocol errors."""
    pass


class Dcon:
    """Improved DCON protocol handler."""
    
    def __init__(self):
        """Initialize DCON protocol handler."""
        pass
    
    def create_request(self, character: str, module_address: int, command: str) -> str:
        """Create a DCON request with validation.
        
        Args:
            character: Command character
            module_address: Module address (1-255)
            command: Command string
            
        Returns:
            Complete DCON request string
            
        Raises:
            DconError: If parameters are invalid
        """
        # Validate inputs
        if not character or not isinstance(character, str):
            raise DconError("Character must be a non-empty string")
        
        if not validate_address(module_address):
            raise DconError(f"Invalid module address: {module_address}")
        
        if not isinstance(command, str):
            raise DconError("Command must be a string")
        
        try:
            # Convert address to hex format
            address = str(hex(module_address))[2:].upper().zfill(2)
            request_string = f"{character}{address}{command}"
            checksum = self.create_checksum(request_string)
            complete_request = request_string + checksum + '\r'
            
            logger.debug(f"Created DCON request: {complete_request.strip()}")
            return complete_request
            
        except Exception as e:
            logger.error(f"Failed to create DCON request: {e}")
            raise DconError(f"Request creation failed: {e}")
    
    def create_checksum(self, request_string: str) -> str:
        """Create checksum for DCON request.
        
        Args:
            request_string: The request string to create checksum for
            
        Returns:
            2-character uppercase hex checksum
        """
        if not isinstance(request_string, str):
            raise DconError("Request string must be a string")
        
        try:
            sum_ascii = sum(ord(char) for char in request_string)
            checksum_hex = hex(sum_ascii)[-2:].upper().zfill(2)
            logger.debug(f"Created checksum {checksum_hex} for '{request_string}'")
            return checksum_hex
        except Exception as e:
            logger.error(f"Failed to create checksum: {e}")
            raise DconError(f"Checksum creation failed: {e}")
    
    def checksum_verification(self, response: str) -> bool:
        """Verify checksum of DCON response.
        
        Args:
            response: Complete DCON response string
            
        Returns:
            True if checksum is valid, False otherwise
        """
        try:
            if not response or len(response) < 4:
                logger.warning(f"Response too short for verification: '{response}'")
                return False
            
            data = response[1:-3]
            received_checksum = response[-3:-1]
            
            calculated_sum = sum(ord(char) for char in data)
            calculated_checksum = hex(calculated_sum)[-2:].upper().zfill(2)
            
            is_valid = received_checksum.upper() == calculated_checksum
            
            if not is_valid:
                logger.warning(
                    f"Checksum mismatch: received={received_checksum}, "
                    f"calculated={calculated_checksum}"
                )
            else:
                logger.debug(f"Checksum verified for response: {response.strip()}")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Checksum verification failed: {e}")
            return False
    
    def parsedResponse(self, response: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse DCON response into data and checksum components.
        
        Args:
            response: Complete DCON response string
            
        Returns:
            Tuple of (data, checksum) or (None, None) if parsing fails
        """
        try:
            if not response or len(response) < 5:  # Minimum: >XYnn\r
                logger.warning(f"Invalid response format: '{response}'")
                return None, None
            
            # Validate basic structure - should start with '>' and end with '\r'
            if not response.startswith('>') or not response.endswith('\r'):
                logger.warning(f"Invalid response structure: '{response}'")
                return None, None
            
            # Expected format: >DATA12\r where DATA is actual data and 12 is checksum
            data = response[1:-3]
            checksum = response[-3:-1]
            
            logger.debug(f"Parsed response - data: '{data}', checksum: '{checksum}'")
            return data, checksum
            
        except Exception as e:
            logger.error(f"Failed to parse response '{response}': {e}")
            return None, None
    
    def validate_response_format(self, response: str) -> bool:
        """Validate basic DCON response format.
        
        Args:
            response: Response string to validate
            
        Returns:
            True if format is valid, False otherwise
        """
        if not response:
            return False
        
        # Basic format checks
        if len(response) < 4:
            return False
        
        if not response.endswith('\r'):
            return False
        
        # Check if response has proper structure
        data, checksum = self.parsedResponse(response)
        if data is None or checksum is None:
            return False
        
        return True
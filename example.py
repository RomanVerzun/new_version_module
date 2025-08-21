#!/usr/bin/env python3
"""Example script demonstrating the improved components."""

import sys
import time
from config import config
from logger import setup_logger
from dcon import Dcon
from relay_manager import AFRelayManager, DCRelayManager
from util import validate_address, format_binary_data, safe_operation


def main():
    """Demonstrate the improved components."""
    
    # Setup logging
    logger = setup_logger("example", level="INFO")
    logger.info("Starting example demonstration")
    
    # Demonstrate configuration system
    logger.info("=== Configuration System ===")
    logger.info(f"Default port: {config.get('serial.default_port')}")
    logger.info(f"Default baud rate: {config.get('serial.default_baud_rate')}")
    
    # Save custom configuration
    config.set('example.test_value', 'Hello World')
    config.save_config()
    logger.info("Configuration saved")
    
    # Demonstrate DCON protocol
    logger.info("\n=== DCON Protocol ===")
    dcon = Dcon()
    
    try:
        request = dcon.create_request('-', 10, '')
        logger.info(f"Created DCON request: {request.strip()}")
        
        # Simulate response parsing
        mock_response = ">ABCD12\r"
        data, checksum = dcon.parsedResponse(mock_response)
        logger.info(f"Parsed response - Data: {data}, Checksum: {checksum}")
        
        # Verify checksum
        is_valid = dcon.checksum_verification(mock_response)
        logger.info(f"Checksum valid: {is_valid}")
        
    except Exception as e:
        logger.error(f"DCON demonstration failed: {e}")
    
    # Demonstrate relay managers
    logger.info("\n=== Relay Managers ===")
    
    af_manager = AFRelayManager()
    dc_manager = DCRelayManager()
    
    # Test AF relay
    handler = af_manager.get_button_handler('buttonPressed_A02')
    if handler:
        logger.info("Testing AF relay A02")
        handler(True)  # Activate
        logger.info(f"AF State after activation: {bin(af_manager.state)}")
        handler(False)  # Deactivate
        logger.info(f"AF State after deactivation: {bin(af_manager.state)}")
    
    # Test DC relay
    handler = dc_manager.get_button_handler('buttonPressed_C02')
    if handler:
        logger.info("Testing DC relay C02")
        handler(True)  # Activate
        logger.info(f"DC State after activation: {bin(dc_manager.state)}")
        
    # Demonstrate utility functions
    logger.info("\n=== Utility Functions ===")
    
    # Address validation
    test_addresses = [0, 1, 128, 255, 256]
    for addr in test_addresses:
        is_valid = validate_address(addr)
        logger.info(f"Address {addr} is valid: {is_valid}")
    
    # Binary data formatting
    hex_data = "A1B2"
    binary_data = format_binary_data(hex_data)
    if binary_data:
        logger.info(f"Hex {hex_data} -> Binary {binary_data}")
    
    # Safe operation context manager
    with safe_operation("test operation"):
        logger.info("Performing safe operation")
        time.sleep(0.1)
    
    logger.info("\n=== Example completed successfully ===")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExample interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Example failed: {e}")
        sys.exit(1)
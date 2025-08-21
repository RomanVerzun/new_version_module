"""Basic tests for the module testing application."""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from util import validate_address, format_binary_data, RetryError, retry
from dcon import Dcon, DconError
from relay_manager import AFRelayManager, DCRelayManager


class TestConfig(unittest.TestCase):
    """Test configuration management."""
    
    def test_config_initialization(self):
        """Test config initialization with defaults."""
        config = Config()
        self.assertEqual(config.get('serial.default_port'), 'COM4')
        self.assertEqual(config.get('serial.default_baud_rate'), 115200)
    
    def test_config_get_with_default(self):
        """Test getting config value with default."""
        config = Config()
        self.assertEqual(config.get('nonexistent.key', 'default'), 'default')
    
    def test_config_set_and_get(self):
        """Test setting and getting config values."""
        config = Config()
        config.set('test.key', 'test_value')
        self.assertEqual(config.get('test.key'), 'test_value')


class TestUtil(unittest.TestCase):
    """Test utility functions."""
    
    def test_validate_address_valid(self):
        """Test address validation with valid addresses."""
        self.assertTrue(validate_address(1))
        self.assertTrue(validate_address(128))
        self.assertTrue(validate_address(255))
    
    def test_validate_address_invalid(self):
        """Test address validation with invalid addresses."""
        self.assertFalse(validate_address(0))
        self.assertFalse(validate_address(256))
        self.assertFalse(validate_address(-1))
        self.assertFalse(validate_address('string'))
    
    def test_format_binary_data_valid(self):
        """Test binary data formatting with valid input."""
        result = format_binary_data('A1')
        self.assertEqual(result, '10100001')
    
    def test_format_binary_data_invalid(self):
        """Test binary data formatting with invalid input."""
        self.assertIsNone(format_binary_data('ZZ'))
        self.assertIsNone(format_binary_data(None))
    
    def test_retry_decorator_success(self):
        """Test retry decorator with successful function."""
        @retry(max_attempts=3)
        def success_func():
            return "success"
        
        result = success_func()
        self.assertEqual(result, "success")
    
    def test_retry_decorator_failure(self):
        """Test retry decorator with failing function."""
        call_count = 0
        
        @retry(max_attempts=3, delay=0.01)
        def fail_func():
            nonlocal call_count
            call_count += 1
            raise ValueError("Test error")
        
        with self.assertRaises(RetryError):
            fail_func()
        
        self.assertEqual(call_count, 3)


class TestDcon(unittest.TestCase):
    """Test DCON protocol handler."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.dcon = Dcon()
    
    def test_create_request_valid(self):
        """Test creating valid DCON request."""
        request = self.dcon.create_request('-', 1, '')
        self.assertTrue(request.endswith('\r'))
        self.assertIn('01', request)  # Address should be 01
    
    def test_create_request_invalid_address(self):
        """Test creating request with invalid address."""
        with self.assertRaises(DconError):
            self.dcon.create_request('-', 0, '')
        
        with self.assertRaises(DconError):
            self.dcon.create_request('-', 256, '')
    
    def test_create_checksum(self):
        """Test checksum creation."""
        checksum = self.dcon.create_checksum('-01')
        self.assertEqual(len(checksum), 2)
        self.assertTrue(checksum.isupper())
    
    def test_parse_response_valid(self):
        """Test parsing valid response."""
        # Create a mock response with proper format
        response = ">ABCD12\r"
        data, checksum = self.dcon.parsedResponse(response)
        self.assertEqual(data, "ABCD")
        self.assertEqual(checksum, "12")
    
    def test_parse_response_invalid(self):
        """Test parsing invalid response."""
        data, checksum = self.dcon.parsedResponse("short")
        self.assertIsNone(data)
        self.assertIsNone(checksum)


class TestRelayManager(unittest.TestCase):
    """Test relay manager classes."""
    
    def test_af_relay_manager_initialization(self):
        """Test AF relay manager initialization."""
        manager = AFRelayManager()
        self.assertEqual(manager.state, 0)  # MASK_R is 0
        self.assertIsInstance(manager.button_handlers, dict)
    
    def test_dc_relay_manager_initialization(self):
        """Test DC relay manager initialization."""
        manager = DCRelayManager()
        self.assertEqual(manager.state, 0)
        self.assertIsInstance(manager.button_handlers, dict)
    
    def test_update_state_activate(self):
        """Test updating relay state to activate."""
        manager = AFRelayManager()
        new_state = manager.update_state(1, True)  # Activate relay 1
        self.assertEqual(new_state, 1)
    
    def test_update_state_deactivate(self):
        """Test updating relay state to deactivate."""
        manager = AFRelayManager()
        manager.state = 1  # Set initial state
        new_state = manager.update_state(1, False)  # Deactivate relay 1
        self.assertEqual(new_state, 0)
    
    def test_get_button_handler(self):
        """Test getting button handler."""
        manager = AFRelayManager()
        handler = manager.get_button_handler('buttonPressed_A02')
        self.assertIsNotNone(handler)
        self.assertTrue(callable(handler))


if __name__ == '__main__':
    unittest.main()
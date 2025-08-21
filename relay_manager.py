"""Base classes for relay management to reduce code duplication."""

from abc import ABC, abstractmethod
from typing import Dict, Callable, List
import relays as rel
from logger import setup_logger

logger = setup_logger(__name__)


class RelayManagerBase(ABC):
    """Base class for managing relay states and button handlers."""
    
    def __init__(self):
        self.state = rel.MASK_R
        self.button_handlers = self._create_button_handlers()
    
    @abstractmethod
    def _get_relay_mapping(self) -> Dict[str, int]:
        """Return mapping of relay names to relay constants."""
        pass
    
    def _create_button_handlers(self) -> Dict[str, Callable]:
        """Create button handler functions dynamically."""
        handlers = {}
        relay_mapping = self._get_relay_mapping()
        
        for relay_name, relay_constant in relay_mapping.items():
            # Create closure to capture relay_constant
            def create_handler(relay_const):
                return lambda state: self.update_state(relay_const, state)
            
            handlers[f"buttonPressed_{relay_name}"] = create_handler(relay_constant)
        
        return handlers
    
    def update_state(self, relay: int, state: bool) -> int:
        """Update relay state with proper bit manipulation.
        
        Args:
            relay: Relay constant value
            state: True to activate, False to deactivate
            
        Returns:
            Updated state value
        """
        if state:
            self.state = self.state | relay
        else:
            self.state = self.state & (~relay & rel.MASK_R)
        
        logger.debug(f"Updated relay state: {bin(self.state)}")
        return self.state
    
    def get_button_handler(self, handler_name: str) -> Callable:
        """Get button handler by name."""
        return self.button_handlers.get(handler_name)
    
    def get_all_handlers(self) -> Dict[str, Callable]:
        """Get all button handlers."""
        return self.button_handlers.copy()


class AFRelayManager(RelayManagerBase):
    """Relay manager for AF (A and F) relays."""
    
    def _get_relay_mapping(self) -> Dict[str, int]:
        return {
            'A02': rel.RELAY_A02,
            'A03': rel.RELAY_A03,
            'A04': rel.RELAY_A04,
            'A05': rel.RELAY_A05,
            'A06': rel.RELAY_A06,
            'A07': rel.RELAY_A07,
            'A08': rel.RELAY_A08,
            'A09': rel.RELAY_A09,
            'F02': rel.RELAY_F02,
            'F03': rel.RELAY_F03,
            'F04': rel.RELAY_F04,
            'F05': rel.RELAY_F05,
            'F06': rel.RELAY_F06,
            'F07': rel.RELAY_F07,
            'F08': rel.RELAY_F08,
            'F09': rel.RELAY_F09,
        }


class DCRelayManager(RelayManagerBase):
    """Relay manager for DC (C and D) relays."""
    
    def _get_relay_mapping(self) -> Dict[str, int]:
        return {
            'C02': rel.RELAY_C02,
            'C03': rel.RELAY_C03,
            'C04': rel.RELAY_C04,
            'C05': rel.RELAY_C05,
            'C06': rel.RELAY_C06,
            'C07': rel.RELAY_C07,
            'C08': rel.RELAY_C08,
            'C09': rel.RELAY_C09,
            'D02': rel.RELAY_D02,
            'D03': rel.RELAY_D03,
            'D04': rel.RELAY_D04,
            'D05': rel.RELAY_D05,
            'D06': rel.RELAY_D06,
            'D07': rel.RELAY_D07,
            'D08': rel.RELAY_D08,
            'D09': rel.RELAY_D09,
        }


class InputStyleManager:
    """Manager for input styling operations."""
    
    ACTIVE_INPUT = 'color: "black"; background-color: red'
    INACTIVE_INPUT = 'color: "black"; background-color: gray'
    CHECKED_INPUT = 'color: "black"; background-color: green'
    
    @staticmethod
    def apply_input_style(binary_index: int, list_index: int, 
                         inp_list: List, binary_data: str, flag_list: List):
        """Apply styling to input based on state.
        
        Args:
            binary_index: Index in binary data
            list_index: Index in input list
            inp_list: List of input elements
            binary_data: Binary representation of data
            flag_list: List of checked flags
        """
        try:
            if not binary_data or binary_index >= len(binary_data):
                return
            
            if list_index >= len(inp_list) or list_index >= len(flag_list):
                return
            
            element = inp_list[list_index]
            
            if binary_data[binary_index] == '0':
                if flag_list[list_index]:
                    element.setStyleSheet(InputStyleManager.CHECKED_INPUT)
                else:
                    element.setStyleSheet(InputStyleManager.INACTIVE_INPUT)
            else:
                element.setStyleSheet(InputStyleManager.ACTIVE_INPUT)
                flag_list[list_index] = True
                
        except (IndexError, AttributeError) as e:
            logger.error(f"Error applying input style: {e}")
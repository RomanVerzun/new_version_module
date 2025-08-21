"""Configuration management for the module testing application."""

import json
import logging
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration manager for application settings."""
    
    DEFAULT_CONFIG = {
        "serial": {
            "default_port": "COM4",
            "default_baud_rate": 115200,
            "timeout": 1.0,
            "timer_interval": 100
        },
        "ui": {
            "window_title": "Module Tester",
            "timer_intervals": {
                "test_relays": 300,
                "label_update": 200,
                "find_module": 100
            }
        },
        "module": {
            "default_address": 0,
            "max_address": 255,
            "min_address": 1
        },
        "logging": {
            "level": "INFO",
            "format": "%(levelname)s %(filename)s: line %(lineno)d: message: %(message)s"
        }
    }
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration with optional config file."""
        self.config_file = Path(config_file)
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file if it exists."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self._merge_config(self.config, file_config)
                logging.info(f"Configuration loaded from {self.config_file}")
            except (json.JSONDecodeError, IOError) as e:
                logging.warning(f"Failed to load config file: {e}")
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logging.info(f"Configuration saved to {self.config_file}")
        except IOError as e:
            logging.error(f"Failed to save config file: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key path."""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> None:
        """Set configuration value by dot-separated key path."""
        keys = key_path.split('.')
        config_dict = self.config
        
        for key in keys[:-1]:
            if key not in config_dict or not isinstance(config_dict[key], dict):
                config_dict[key] = {}
            config_dict = config_dict[key]
        
        config_dict[keys[-1]] = value
    
    def _merge_config(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """Recursively merge configuration dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value


# Global configuration instance
config = Config()
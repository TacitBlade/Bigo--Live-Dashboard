"""
Application settings and configuration.
Contains default values and configuration options for the Bigo Live Dashboard.
"""

import os
from typing import Dict, Any
import streamlit as st
import json

# App Settings
APP_TITLE = "Bigo Live Dashboard"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Analytics and management dashboard for Bigo Live agencies"

# Google Sheets Settings
GOOGLE_CREDENTIALS_FILE = "google_credentials.json"
SHEET_REFRESH_INTERVAL = 300  # seconds (5 minutes)

# Default Google Sheets URLs (can be overridden)
DEFAULT_SHEET_URLS = {
    "Sheet 1": "https://docs.google.com/spreadsheets/d/1T2Za-VeqUe4hN-00X-Qa5T3FAgXMExz2B1Brhspbr7w/edit?gid=920344037",
    "Sheet 2": "https://docs.google.com/spreadsheets/d/1DD7I5sMu55wRVwGjPEv43iygq2b8oudfMspGlOY1zck/edit?gid=1990132269",
    "Sheet 3": "https://docs.google.com/spreadsheets/d/1iS9acwW9DrjZQh_d51_Pv4DcN9_X4alzK3wC2KIWXYw/edit?gid=1234468340",
}

# Payment Settings
PAYMENT_CONFIG = {
    "base_rate": 0.4,
    "bonus_threshold": 10000,
    "bonus_rate": 0.1,
    "pk_win_bonus": 500,
    "attendance_bonus": 1000,
    "beans_to_diamonds_rate": 210,
    "diamond_to_usd_rate": 0.005,
}

# UI Settings
UI_CONFIG = {
    "page_title": "Bigo Dashboard",
    "layout": "wide",
    "sidebar_state": "expanded",
    "theme": "light",
}

# Security Settings
SECURITY_CONFIG = {
    "enable_auth": False,  # Set to True to enable authentication
    "session_timeout": 3600,  # seconds (1 hour)
    "max_login_attempts": 3,
}

# File Paths
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"
CONFIG_DIR = "config"
UTILS_DIR = "utils"

def get_setting(key: str, default: Any = None) -> Any:
    """Get a setting value from environment variables or default."""
    return os.getenv(key, default)

def get_google_credentials_path() -> str:
    """Get path to Google credentials file."""
    return os.path.join(os.getcwd(), GOOGLE_CREDENTIALS_FILE)

def get_sheet_urls() -> Dict[str, str]:
    """Get configured sheet URLs."""
    # In production, these could come from environment variables
    return DEFAULT_SHEET_URLS.copy()

def is_auth_enabled() -> bool:
    """Check if authentication is enabled."""
    return get_setting("ENABLE_AUTH", SECURITY_CONFIG["enable_auth"])

def get_payment_config() -> Dict[str, float]:
    """Get payment configuration."""
    return PAYMENT_CONFIG.copy()

# Environment-specific settings
def is_development() -> bool:
    """Check if running in development mode."""
    return get_setting("ENVIRONMENT", "development").lower() == "development"

def is_production() -> bool:
    """Check if running in production mode."""
    return get_setting("ENVIRONMENT", "development").lower() == "production"

class AppConfig:
    def __init__(self):
        self.config_file = os.path.join('config', 'app_config.json')
        self.ensure_config_directory()
        self.load_config()
    
    def ensure_config_directory(self):
        """Ensure the config directory exists."""
        config_dir = os.path.dirname(self.config_file)
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir, exist_ok=True)
            except OSError as e:
                print(f"Warning: Could not create config directory: {e}")
    
    def load_config(self):
        """Load configuration from file or create default."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = self.default_config()
                self.save_config()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config file, using defaults: {e}")
            self.config = self.default_config()
    
    def default_config(self):
        """Return default configuration."""
        return {
            'theme': 'light',
            'currency': 'USD',
            'decimal_places': 2,
            'auto_refresh': False,
            'refresh_interval': 300,
            'export_formats': ['xlsx', 'csv', 'json'],
            'user_roles': ['Host', 'Agency', 'Admin']
        }
    
    def save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save config file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value and save."""
        self.config[key] = value
        self.save_config()

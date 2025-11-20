"""
Configuration module for Project Management Dashboard
"""

import os
from typing import Optional


class Config:
    """Configuration class for the dashboard application."""
    
    # Google Sheets configuration
    CREDENTIALS_FILE = os.getenv("CREDENTIALS", "credentials.json")
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
    
    # Application settings
    UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "10"))  # in seconds
    MANAGEMENT_SHEET_NAME = os.getenv("MANAGEMENT_SHEET_NAME", "Quản Lý")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration is present."""
        if not cls.GOOGLE_SHEET_ID:
            raise ValueError("GOOGLE_SHEET_ID environment variable must be set")
        
        if not os.path.exists(cls.CREDENTIALS_FILE):
            raise FileNotFoundError(f"Credentials file {cls.CREDENTIALS_FILE} not found")
        
        return True
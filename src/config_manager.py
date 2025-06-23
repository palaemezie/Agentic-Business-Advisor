"""
Loading default values from config.py when needed
Reading user configurations from storage
Saving user configurations back to storage
Providing functions to reset to factory defaults
"""
import os
import sys
import json
import copy
from datetime import datetime
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import (DEFAULT_FINANCIAL_DATA, DEFAULT_PRODUCT_DATA, 
                   DEFAULT_WEBSITE_URL, DEFAULT_RESEARCH_TOPIC, OUTPUT_DIR)

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Path for user configuration
USER_CONFIG_PATH = os.path.join(OUTPUT_DIR, "user_config.json")

def load_user_config():
    """Load user configuration if it exists, otherwise return the defaults."""
    if os.path.exists(USER_CONFIG_PATH):
        try:
            with open(USER_CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            st.warning("Failed to load user configuration. Using default values.")
            
    # Return a copy of default config
    return {
        "financial_data": copy.deepcopy(DEFAULT_FINANCIAL_DATA),
        "product_data": copy.deepcopy(DEFAULT_PRODUCT_DATA),
        "website_url": DEFAULT_WEBSITE_URL,
        "research_topic": DEFAULT_RESEARCH_TOPIC
    }

def save_user_config(config_data):
    """Save user configuration."""
    try:
        with open(USER_CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
        return True, "Configuration saved successfully!"
    except IOError:
        return False, "Failed to save configuration."

def reset_to_defaults():
    """Reset configuration to default values."""
    if os.path.exists(USER_CONFIG_PATH):
        try:
            os.remove(USER_CONFIG_PATH)
            return True, "Reset to default values successfully!"
        except IOError:
            return False, "Failed to reset configuration."
    return True, "Already using default configuration."

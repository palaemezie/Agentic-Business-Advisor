"""
Configuration settings for the Business Advisor Suite.
"""

# Default values for the financial advisor module
DEFAULT_FINANCIAL_DATA = {
    "income": 5000,
    "expenses": {
        "rent": 1500,
        "utilities": 300,
        "groceries": 400,
        "transportation": 200,
        "entertainment": 150,
        "other": 450
    },
    "debts": {
        "credit_card": {
            "balance": 2000,
            "interest_rate": 0.18
        },
        "student_loan": {
            "balance": 15000,
            "interest_rate": 0.045
        }
    },
    "savings_goal": 500
}

# Default values for the product launch module
DEFAULT_PRODUCT_DATA = {
    'product_name': "New Product",
    'product_description': "A description of your new product.",
    'launch_date': "2025-12-31",
    'target_market': "General consumers",
    'budget': 50000
}

# Default values for the web researcher module
DEFAULT_WEBSITE_URL = "https://en.wikipedia.org/wiki/Alan_Turing"
DEFAULT_RESEARCH_TOPIC = "Artificial intelligence"

# File paths
OUTPUT_DIR = "outputs"

"""
Set up necessary environment variables and Azure configurations.
"""

import os
import streamlit as st

def setup_environment_variables():
    """Set up necessary environment variables if not already set."""
    # Check if keys are already in environment variables
    required_vars = ["AZURE_API_KEY", "AZURE_API_BASE", "AZURE_OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if os.environ.get(var) is None]
    
    if missing_vars:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            # Check again after loading .env
            missing_vars = [var for var in required_vars if os.environ.get(var) is None]
            if missing_vars:
                return False, f"Missing environment variables: {', '.join(missing_vars)}"
        except ImportError:
            return False, "python-dotenv not installed and environment variables missing"
    
    # Ensure OPENAI_API_KEY is set for compatibility
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = os.environ.get("AZURE_OPENAI_API_KEY")
    
    return True, "Environment variables set successfully"

# CRITICAL OPTIMIZATION: Import heavy libraries only when function is called
@st.cache_resource(show_spinner=False)
def get_azure_llm(temperature=0.7):
    """Initialize and return the Azure LLM instance."""
    success, message = setup_environment_variables()
    if not success:
        raise ValueError(message)
    
    # Import only when needed - not at module level
    from langchain_openai import AzureChatOpenAI
    
    return AzureChatOpenAI(
        openai_api_version="2025-01-01-preview",
        azure_deployment="azure/gpt-4o",
        api_key=os.environ.get("AZURE_API_KEY"),
        azure_endpoint=os.environ.get("AZURE_API_BASE"),
        temperature=temperature
    )

@st.cache_resource(show_spinner=False)
def get_azure_config():
    """Return Azure configuration for tools requiring it."""
    success, message = setup_environment_variables()
    if not success:
        raise ValueError(message)
    
    return dict(
        llm=dict(
            provider="azure_openai",
            config=dict(
                model="gpt-4o",
                deployment_name="gpt-4o",
                api_key=os.environ["AZURE_API_KEY"],
                base_url=os.environ["AZURE_API_BASE"],
                api_version="2025-01-01-preview",
                temperature=0.2,
            ),
        ),
        embedder=dict(
            provider="azure_openai",
            config=dict(
                model="text-embedding-ada-002",
                deployment_name="text-embedding-ada-002",
                api_key=os.environ["AZURE_API_KEY"],
                api_base=os.environ["AZURE_API_BASE"],
            )
        )
    )

@st.cache_resource(show_spinner=False)
def pre_cache_essentials():
    """Pre-load critical resources in background"""
    get_azure_llm()
    get_azure_config()

# """Set up environment variables and Azure configurations.""" 
# import os
# import streamlit as st
# from functools import lru_cache

# # Cached environment check
# @st.cache_resource(show_spinner=False)
# def _cached_env_check():
#     """Cached environment validation"""
#     required_vars = ["AZURE_API_KEY", "AZURE_API_BASE", "AZURE_OPENAI_API_KEY"]
#     missing_vars = [var for var in required_vars if os.environ.get(var) is None]
    
#     if missing_vars:
#         try:
#             from dotenv import load_dotenv
#             load_dotenv()
#             missing_vars = [var for var in required_vars if os.environ.get(var) is None]
#             return (False, f"Missing variables: {', '.join(missing_vars)}") if missing_vars else (True, "Environment ready")
#         except ImportError:
#             return False, "python-dotenv required for .env loading"
#     return True, "Environment ready"

# @st.cache_resource(show_spinner=False)
# def get_azure_llm(temperature=0.7):
#     """Azure LLM instance with pre-checked environment"""
#     success, message = _cached_env_check()
#     if not success:
#         raise RuntimeError(message)
    
#     from langchain_openai import AzureChatOpenAI
#     return AzureChatOpenAI(
#         openai_api_version="2025-01-01-preview",
#         azure_deployment="gpt-4o",
#         api_key=os.environ["AZURE_API_KEY"],
#         azure_endpoint=os.environ["AZURE_API_BASE"],
#         temperature=temperature
#     )

# @st.cache_resource(show_spinner=False)
# def get_azure_config():
#     """Shared Azure configuration for tools"""
#     return {
#         'llm': {
#             'provider': "azure_openai",
#             'config': {
#                 'model': "gpt-4o",
#                 'api_key': os.environ["AZURE_API_KEY"],
#                 'base_url': os.environ["AZURE_API_BASE"],
#                 'api_version': "2025-01-01-preview"
#             }
#         }
#     }

# @st.cache_resource(show_spinner=False)
# def pre_cache_essentials():
#     """Pre-load critical resources in background"""
#     get_azure_llm()
#     get_azure_config()

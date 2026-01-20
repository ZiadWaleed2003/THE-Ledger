import os
from dotenv import load_dotenv
from typing import Dict

def load_environment() -> Dict[str, str]:
    """Load and validate all required environment variables"""
    load_dotenv()  
    
    required_vars = {
        'CEREBRAS_API_KEY' : 'Cerebas Api key',
        'LANGSMITH_TRACING': 'LangSmith tracing flag',
        'LANGSMITH_API_KEY': 'LangSmith API key',
        'LANGSMITH_PROJECT': 'LangSmith Project'
    }

    config = {}
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            raise ValueError(f"Missing required environment variable: {var} ({description})")
        config[var] = value
    
    # Set LangSmith environment variables for proper initialization
    os.environ['LANGSMITH_TRACING'] = config['LANGSMITH_TRACING']
    os.environ['LANGSMITH_API_KEY'] = config['LANGSMITH_API_KEY']
    os.environ['LANGSMITH_PROJECT'] = config['LANGSMITH_PROJECT']
    
    return config

# Initialize and export all configs
try:
    CONFIG = load_environment()
except ValueError as e:
    print(f"Configuration error: {str(e)}")
    raise
from langchain_core.tools import tool 

from backend.src.agents.db_manager import DBManager
from backend.src.utils.logger import get_session_logger

# tool used by the asset manager
@tool
def ask_db_manager(query:str):
    """
        Use this tool to ask the Database Manager questions about assets.
        Pass the user's natural language query directly to this tool.
        Example: "Find my most expensive laptop" or "Total value of assets".
    """
    logger = get_session_logger()
    db_manager = DBManager()

    logger.info("calling db agent to get db info")
    result = db_manager.run_query(query)

    if result is None:
        logger.error("Oops somthing happened while calling db agent")
        return "tool failed to retrieve anything"
    
    return result
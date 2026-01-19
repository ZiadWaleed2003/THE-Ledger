from langchain_core.tools import tool 
from langsmith import traceable

from backend.src.agents.db_manager import DBManager
from backend.src.utils.logger import get_session_logger


"""
    so first of all I get the conusion that u might have right now while reading the nonsense code below
    however I've implemented it this way just to enable monitoring as u can't but 2 decorators over each other in python
"""



# tool used by the asset manager
@tool
def ask_db_manager(query:str):
    """
        Use this tool to ask the Database Manager questions about assets.
        Pass the user's natural language query directly to this tool.
        Example: "Find my most expensive laptop" or "Total value of assets".
    """
    logger = get_session_logger()
    
    result = run_query(query)

    logger.info("calling db agent to get db info")
    

    if result is None:
        logger.error("Oops somthing happened while calling db agent")
        return "tool failed to retrieve anything"
    
    return result

@traceable
def run_query(query):
    db_manager = DBManager()
    result = db_manager.run_query(query)
    return result
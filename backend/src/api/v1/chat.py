from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.src.agents.asset_manager import AssetManager
from backend.src.utils.logger import get_session_logger


router = APIRouter()


class ChatQuery(BaseModel):
    question: str

@router.post("/query")
def query_agent(query: ChatQuery):
    try:
        logger = get_session_logger()
        asset_manager = AssetManager()
        logger.info(f"running user query : {query.question}")
        response = asset_manager.run_query(query.question)

        logger.info(f"replying with {response[:10]}")
        return response
      
            
    except Exception as e:
        logger.error("Opps something bad happended at the chat route")
        raise HTTPException(status_code=500, detail=str(e))
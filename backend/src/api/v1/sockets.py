from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.src.agents.asset_manager import AssetManager
from backend.src.utils.logger import get_session_logger
import json

router = APIRouter()


"""
    this endpoint here is an extra one from me but anyway I though it seems really convinient to add it
    so basically we are spinning up a WebSocket connection between the client and the server 
    and once we get the client req we give it to the agent and then respond back with the agent answer
"""

@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    
    await websocket.accept()
    
    try:
        while True:
            
            
            user_text = await websocket.receive_text()
            
            asset_manager = AssetManager()
            logger = get_session_logger()

            agent_response_str = asset_manager.run_query(user_text)
            
            
            response_data = {
                    "answer": agent_response_str,
                    "sources": []
                }
            
            logger.info("replying to the client through the socket connection")
            await websocket.send_json(response_data)
            
    except WebSocketDisconnect:
        logger.warning("Socket Client disconnected")
    except Exception as e:
        logger.error(f"smth really bad happended at the socket connection error : {e}")
        await websocket.send_json({"answer": f"Error: {str(e)}", "sources": []})
        await websocket.close()
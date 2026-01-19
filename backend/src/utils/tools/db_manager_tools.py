from langchain_core.tools import tool
from typing import Literal


from backend.src.core.database import get_db
from backend.src.services.assets_service import AssetService
from backend.src.utils.logger import get_session_logger
from backend.src.schemas.asset import AssetResponse


db = next(get_db())

# tools used by the DB manager

@tool
def search_assets_by_name_or_category(query:str):
    "" """
    An AI Tool to help the agent search the DB 
    for partial matches in name or category
    Example:
    search_assets(
        query="macbook"
    )
    """""
    
    logger = get_session_logger()
    asset_service = AssetService(db,logger)

    logger.info("The agent used search_assets tool")

    result , error = asset_service.search_asset(query)

    if error is None and len(result) == 0:
        return "No Assets found"
    
    elif result is None:
        return "error with the DB, couldn't retrieve any data"
    else:
        asset = [AssetResponse.model_validate(asset).model_dump(mode='json') for asset in result]
        logger.info(f"tool about to return {asset}") 
        return asset
    

@tool
def get_all_assets():
    "a tool to help the agent get all the assets from the db"

    logger = get_session_logger()
    asset_service = AssetService(db,logger)

    logger.info("Agent used the get all assets tool")

    result , error = asset_service.get_all_assets()

    if error:
        logger.error("get all assets tools failed to retrieve anyting")
        return "No assets found in the DB"
    
    logger.info(f"tool call succeeded and got {result}")
    return [AssetResponse.model_validate(asset).model_dump(mode='json') for asset in result]



@tool
def get_asset_value_statistics(metric: Literal["max", "min", "mean"]):
    """
    Get statistics over asset values.

    metric:
    - "max"  -> most valuable asset
    - "min"  -> least valuable asset
    - "mean" -> average asset value
    """

    logger = get_session_logger()
    asset_service = AssetService(db, logger)

    logger.info(f"Agent requested asset value statistics: metric={metric}")

    metric = metric.lower()

    if metric == "max":
        result, error = asset_service.get_max_value()

    elif metric == "min":
        result, error = asset_service.get_min_value()

    elif metric == "mean":
        result, error = asset_service.get_asset_values_mean()

    else:
        # damn we recieved invalid input (hallucinations from the llm)
        logger.error(f"Invalid metric received: {metric}")
        return {
            "error": "Invalid metric. Allowed values are: max, min, mean."
        }

    if error:
        logger.error("Database error while computing asset statistics")
        return {
            "error": "Database error while retrieving asset statistics."
        }

    if result is None:
        logger.info("No asset records found in database")
        return {
            "error": "No asset records found."
        }

    logger.info("Asset statistics retrieved successfully")

    # If the result is a DB model (max/min), serialize it. If it's a number (mean), keep it as is.
    serialized_result = result
    if metric in ["max", "min"]:
         serialized_result = AssetResponse.model_validate(result).model_dump(mode='json')

    return {
        "metric": metric,
        "result": serialized_result
    }

    




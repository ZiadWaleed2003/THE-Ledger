from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.orm import Session
from typing import List


from backend.src.core.database import get_db
from backend.src.schemas.asset import AssetCreate, AssetUpdate, AssetResponse
from backend.src.services.assets_service import AssetService
from backend.src.utils.logger import get_session_logger

router = APIRouter()


# creating a new asset enpoint
@router.post("/", response_model= AssetResponse , status_code=status.HTTP_201_CREATED)
def create_asset(asset : AssetCreate , db : Session = Depends(get_db)):
    logger  = get_session_logger()
    
    asset_service = AssetService(db , logger)

    result =  asset_service.create_asset(asset)

    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create asset")
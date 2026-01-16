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

    new_asset, error = asset_service.create_asset(asset)

    if error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create asset: {error}")
    
    return new_asset


# get all the assets
@router.get("/", response_model=List[AssetResponse])
def get_all_assets(skip : int = 0 , limit : int = 100 , db: Session = Depends(get_db)):

    logger = get_session_logger()

    asset_service = AssetService(db,logger)

    assets, error = asset_service.get_all_assets(skip , limit)

    if error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=f"Failed to get assets: {error}")
    
    return assets
    


# get an asset by UUID
@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id: str , db : Session = Depends(get_db)):

    logger = get_session_logger()
    asset_service = AssetService(db,logger)

    asset, error = asset_service.get_asset_by_id(asset_id)

    if error:
        if "not found" in error.lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Asset with ID {asset_id} not found")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=f"Error retrieving asset: {error}")

    return asset


#delete an asset
@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(asset_id : str , db : Session = Depends(get_db)):
    logger = get_session_logger()
    asset_service = AssetService(db,logger)

    _, error = asset_service.delete_asset(asset_id)

    if error:
        if "not found" in error.lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Asset not found")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=f"Error deleting asset: {error}")
        
    return None


# update an asset
@router.put("/{asset_id}" , response_model= AssetResponse)
def update_asset(asset_id : str , asset_update : AssetUpdate , db : Session = Depends(get_db)):

    logger = get_session_logger()
    asset_service = AssetService(db,logger)

    updated_asset, error = asset_service.update_asset(asset_update , asset_id)

    if error:
        if "not found" in error.lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Asset not found")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=f"Error updating asset: {error}")
    
    return updated_asset


    
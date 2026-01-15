from sqlalchemy.orm import Session
import uuid
from datetime import datetime , timezone

from backend.src.models.asset import Asset
from backend.src.schemas.asset import AssetCreate, AssetUpdate


class AssetService:
    
    def __init__(self, db: Session, logger):
        self.db = db
        self.logger = logger

    def create_asset(self, asset: AssetCreate)-> bool:

        """
            basically a func to create an asset and try to log it into the db
            if we couldn't for some reason then rollback on the db
        """

        try: 
            
            asset = Asset(
                id = str(uuid.uuid4()),
                name = asset.name,
                category=asset.category,
                value=asset.value,
                quantity=asset.quantity,
                status=asset.status,
                purchase_date=asset.purchase_date,
                created_at=datetime.now(timezone.utc)
            )

            self.db.add(asset)
            self.db.commit()
            self.db.refresh(asset)
            self.logger.info("Logged an asset record to the DB")
            return True
        
        except Exception as e:
            self.logger.error("couldn't log the asset to the DB ... error happened while inserting the asset to the DB")
            self.db.rollback()
            return False


    def get_asset_by_id(self, asset_id):
        "retrieving an a single asset from the DB"
        try:
            asset = self.db.query(Asset).filter(Asset.id == asset_id).first()

            if asset is None:
                self.logger.warning(f"Asset with ID {asset_id} not found")
                return None
            
            self.logger.info("retrieving an Asset record from the DB")
            return asset
        except Exception as e:
            self.logger.error(f"DB Error: {e}")
            return None
        

    def get_all_assets(self, skip = 0, limit = 100):

        "retrieving all the assets in the DB"
        try:
            assets = self.db.query(Asset).offset(skip).limit(limit).all()

            if not assets:
                self.logger.warning("No Assets found in the DB")
                return []

            self.logger.info("retrieving Assets from the DB")
            return assets
        
        except Exception as e:
            self.logger.error(f"DB Error: {e}")
            return None
        

    def update_asset(self, asset_update : AssetUpdate ,asset_id)-> bool:

        # get the the asset to update
        db_asset = self.get_asset_by_id(asset_id)

        # check if we actually got somehting
        if db_asset is None:
            self.logger.error("couldn't find any asset to update")
            return False
        
        # now let's update it
        try:

            update_data = asset_update.model_dump(exclude_unset=True)

            for key , value in update_data.items():
                setattr(db_asset , key , value)

            # commit if we did it but rollback if we didn't gang
            self.db.commit()
            self.db.refresh(db_asset)
            return True
        except Exception as e:
            self.logger.error(f"DB Error while updating the DB {e}")
            self.db.rollback()
            return False


    def delete_asset(self, asset_id)-> bool:

        # 1st let's get the asset record

        asset = self.get_asset_by_id(asset_id)

        if asset is None:
            self.logger.error("couldn't find any asset to delete")
            return False
        
        # since we found it so let's delete it
        try:
            self.db.delete(asset)
            self.db.commit()
            return True
        

        except Exception as e:
            self.logger.error(f"DB Error while deleting asset with id {asset_id}")
            self.db.rollback()
            return False

